/*
 * KP progress sync API — standalone Cloudflare Worker.
 * Deploy as its OWN Worker (does not touch the static site). The static pages call it cross-origin.
 *
 * Required binding:
 *   PROGRESS         KV namespace — per user: progress "u:<userId>", full deck state "c:<userId>"
 * Optional env vars / secrets:
 *   AUTH_SALT        secret — salts the token->userId hash (SET THIS; default is insecure)
 *   API_TOKENS       comma-separated allowlist of accepted tokens (omit = any token >=8 chars)
 *   ALLOWED_ORIGINS  comma-separated CORS origins (omit or "*" = any; Bearer auth makes * safe)
 *
 * The reusable handler is `handleApi(request, env, url)` — to host the API on your EXISTING
 * Worker instead, route `/api/*` to it and serve everything else via env.ASSETS.fetch(request).
 */

import topicsFeed from './topics.json';
const TOPICS_JSON = JSON.stringify(topicsFeed);
import themenFeed from './themen.json';
const THEMEN_JSON = JSON.stringify(themenFeed);
import deckFeed from './deck.json';
const DECK_JSON = JSON.stringify(deckFeed);
import commsContract from './comms-contract.json';

const STATUS = ['new', 'learning', 'mastered'];
const DEFAULTS = () => ({
  streak: 0,
  examDate: null,
  reviews: {},
  cards: { doneToday: 0, goal: 5, mastered: 0, total: 0, dueTomorrow: 0, remainingCycle: 0 },
  dueToday: []
});

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    return handleApi(request, env, url);
  }
};

export async function handleApi(request, env, url) {
  const origin = request.headers.get('Origin') || '';
  const ch = corsHeaders(origin, env);

  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: ch });
  if (!url.pathname.startsWith('/api/')) return jsonRes({ error: 'not_found' }, 404, ch);

  // ---- public: native content feed (no auth) — bundled into the Worker, CORS + cache ----
  if (url.pathname === '/api/content') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    return new Response(TOPICS_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache', ...ch } });
  }

  // ---- public: master curriculum list (no auth) — bundled, CORS + cache ----
  if (url.pathname === '/api/themen') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    return new Response(THEMEN_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache', ...ch } });
  }

  // ---- public: Kernprinzip flashcard deck (no auth) — bundled, CORS + cache ----
  if (url.pathname === '/api/deck') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    return new Response(DECK_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache', ...ch } });
  }

  // ---- shared backend<->frontend comms: contract (bundled) + message log (KV) ----
  if (url.pathname === '/api/comms') {
    const key = 'comms:log';
    if (request.method === 'GET') {
      const log = (await readJson(env.PROGRESS, key)) || [];
      return jsonRes({ contract: commsContract, log }, 200, { 'Cache-Control': 'no-store', ...ch });
    }
    if (request.method === 'POST') {
      const tok = bearer(request) || url.searchParams.get('token') || '';
      if (!tokenAllowed(tok, env)) return jsonRes({ error: 'invalid_token' }, 401, ch);
      let body; try { body = await request.json(); } catch { return jsonRes({ error: 'bad_json' }, 400, ch); }
      const from = (body && (body.from === 'frontend' || body.from === 'backend')) ? body.from : 'unknown';
      const msg = body && typeof body.msg === 'string' ? body.msg.trim().slice(0, 4000) : '';
      if (!msg) return jsonRes({ error: 'bad_body', hint: '{ from: "frontend" | "backend", msg }' }, 400, ch);
      const log = (await readJson(env.PROGRESS, key)) || [];
      log.push({ from, ts: new Date().toISOString(), msg });
      while (log.length > 200) log.shift();
      await env.PROGRESS.put(key, JSON.stringify(log));
      return jsonRes({ ok: true, count: log.length }, 200, ch);
    }
    return jsonRes({ error: 'method_not_allowed' }, 405, ch);
  }

  // ---- auth: Bearer token (or ?token= for quick testing) -> stable userId ----
  const token = bearer(request) || url.searchParams.get('token') || '';
  if (!token) return jsonRes({ error: 'missing_token' }, 401, ch);
  if (!tokenAllowed(token, env)) return jsonRes({ error: 'invalid_token' }, 401, ch);
  const userId = await deriveUserId(token, env);

  if (url.pathname === '/api/whoami') return jsonRes({ userId }, 200, ch);

  if (url.pathname === '/api/progress') {
    const key = 'u:' + userId;
    if (request.method === 'GET') {
      const stored = await readJson(env.PROGRESS, key);
      return jsonRes(withMeta(mergeProgress(DEFAULTS(), stored || {}), userId), 200, ch);
    }
    if (request.method === 'POST') {
      let body;
      try { body = await request.json(); } catch { return jsonRes({ error: 'bad_json' }, 400, ch); }
      const current = (await readJson(env.PROGRESS, key)) || DEFAULTS();
      const merged = mergeProgress(current, sanitize(body));
      merged.updatedAt = new Date().toISOString();
      await env.PROGRESS.put(key, JSON.stringify(merged));
      return jsonRes(withMeta(merged, userId), 200, ch);
    }
    return jsonRes({ error: 'method_not_allowed' }, 405, ch);
  }

  // ---- full flashcard deck state (authed) — opaque blob, last-write-wins by updatedAt ----
  if (url.pathname === '/api/cards') {
    const key = 'c:' + userId;
    if (request.method === 'GET') {
      const stored = await readJson(env.PROGRESS, key);
      return jsonRes(stored || { empty: true }, 200, ch);
    }
    if (request.method === 'POST') {
      let body;
      try { body = await request.json(); } catch { return jsonRes({ error: 'bad_json' }, 400, ch); }
      if (!body || typeof body !== 'object' || Array.isArray(body)) return jsonRes({ error: 'bad_body' }, 400, ch);
      // merge instead of blind overwrite — card-level last-write-wins by box (higher = more learned)
      const existing = normalizeState(await readJson(env.PROGRESS, key));
      const incoming = normalizeState(body);
      // merge cards: keep whichever entry has the higher box (more progress)
      const mergedCards = { ...existing.cards };
      for (const id in incoming.cards) {
        const e = existing.cards[id], ic = incoming.cards[id];
        mergedCards[id] = (!e || ic.box >= e.box) ? ic : e;
      }
      // merge day: keep the one with the higher count on the same date; if different dates keep most recent
      let mergedDay;
      if (existing.day.date === incoming.day.date) {
        mergedDay = incoming.day.count >= existing.day.count ? incoming.day : existing.day;
      } else {
        mergedDay = incoming.day.date > existing.day.date ? incoming.day : existing.day;
      }
      const merged = {
        v: 2,
        cards: mergedCards,
        day: mergedDay,
        streak: Math.max(existing.streak || 0, incoming.streak || 0),
        lastDone: incoming.lastDone > existing.lastDone ? incoming.lastDone : existing.lastDone,
        totalKnown: Math.max(existing.totalKnown || 0, incoming.totalKnown || 0),
        updatedAt: new Date().toISOString(),
      };
      await env.PROGRESS.put(key, JSON.stringify(merged));
      return jsonRes(merged, 200, ch);
    }
    return jsonRes({ error: 'method_not_allowed' }, 405, ch);
  }

  // ---- computed daily session: due+fresh queue + live stats (authed) ----
  if (url.pathname === '/api/session') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    const t = dayParam(url.searchParams.get('today'));
    const goal = clampGoal(url.searchParams.get('goal'));
    const S = normalizeState(await readJson(env.PROGRESS, 'c:' + userId));
    const cards = buildQueue(deckFeed.cards, S, t, goal).map(toClientCard);
    return jsonRes({ today: t, stats: computeStats(deckFeed.cards, S, t, goal), cards }, 200, ch);
  }

  // ---- grade one card server-side (Leitner) -> returns updated stats (authed) ----
  if (url.pathname === '/api/review') {
    if (request.method !== 'POST') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    let body; try { body = await request.json(); } catch { return jsonRes({ error: 'bad_json' }, 400, ch); }
    const id = body && typeof body.id === 'string' ? body.id : '';
    const result = body && (body.result === 'known' || body.result === 'again') ? body.result : '';
    if (!id || !result) return jsonRes({ error: 'bad_body', hint: 'send { id, result: "known" | "again", today, goal }' }, 400, ch);
    if (!deckFeed.cards.some(c => c.id === id)) return jsonRes({ error: 'unknown_card', id }, 400, ch);
    const t = dayParam(body.today);
    const goal = clampGoal(body.goal);
    const key = 'c:' + userId;
    const S = normalizeState(await readJson(env.PROGRESS, key));
    gradeCard(S, id, result, t, goal);
    S.updatedAt = new Date().toISOString();
    await env.PROGRESS.put(key, JSON.stringify(S));
    const stats = computeStats(deckFeed.cards, S, t, goal);
    try { // mirror lightweight summary into the progress feed for other consumers (best-effort)
      const pkey = 'u:' + userId;
      const merged = mergeProgress((await readJson(env.PROGRESS, pkey)) || DEFAULTS(), { streak: stats.streak, cards: { doneToday: stats.doneToday, goal: stats.goal, mastered: stats.mastered, total: stats.total, dueTomorrow: stats.dueTomorrow, remainingCycle: stats.remainingCycle } });
      merged.updatedAt = new Date().toISOString();
      await env.PROGRESS.put(pkey, JSON.stringify(merged));
    } catch (e) { /* non-fatal */ }
    return jsonRes({ ok: true, stats }, 200, ch);
  }

  return jsonRes({ error: 'not_found' }, 404, ch);
}

function bearer(req) { const h = req.headers.get('Authorization') || ''; const m = h.match(/^Bearer\s+(.+)$/i); return m ? m[1].trim() : ''; }
function tokenAllowed(token, env) { const list = (env.API_TOKENS || '').split(',').map(s => s.trim()).filter(Boolean); return list.length ? list.includes(token) : token.length >= 8; }
async function deriveUserId(token, env) {
  const salt = env.AUTH_SALT || 'kpm-default-salt-change-me';
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(token + ':' + salt));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 24);
}
async function readJson(kv, key) { const v = await kv.get(key); if (!v) return null; try { return JSON.parse(v); } catch { return null; } }

// ---- spaced-repetition engine (server-authoritative; mirrors the client byte-for-byte) ----
// Zyklus statt Langzeitparken: Das Deck laeuft rund, jede Karte kommt wieder.
// Gegen [1,3,7,16,35] simuliert (72 Karten, Ziel 5, 20 % Fehlerquote, 140 Tage):
// gleicher Rhythmus von rund 15 Tagen je Deckdurchgang, aber 56 statt 26 Karten
// erreichen die hoechste Box. Falsch beantwortet heisst Box 0 und in 2 Tagen wieder.
const INTERVALS = [3, 6, 10, 16, 24];
const WRONG_DAYS = 2;
const GOAL_DEFAULT = 5;
function todayUTC() { return new Date().toISOString().slice(0, 10); }
function dayParam(v) { return (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) ? v : todayUTC(); }
function clampGoal(v) { const n = parseInt(v, 10); return Number.isFinite(n) ? Math.min(100, Math.max(1, n)) : GOAL_DEFAULT; }
function addDays(s, n) { const d = new Date(s + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function defaultState() { return { v: 2, cards: {}, day: { date: '', count: 0, seen: [] }, streak: 0, lastDone: '', totalKnown: 0 }; }
function normalizeState(s) {
  if (!s || typeof s !== 'object' || s.empty) return defaultState();
  const day = (s.day && typeof s.day === 'object') ? s.day : {};
  return {
    v: 2,
    cards: (s.cards && typeof s.cards === 'object' && !Array.isArray(s.cards)) ? s.cards : {},
    day: { date: day.date || '', count: day.count || 0, seen: Array.isArray(day.seen) ? day.seen : [] },
    streak: s.streak || 0, lastDone: s.lastDone || '', totalKnown: s.totalKnown || 0,
    updatedAt: s.updatedAt
  };
}
function specAccent(hue) { return (hue === null || hue === undefined) ? '#64748B' : `oklch(56% 0.16 ${hue})`; }
function toClientCard(c) { return { id: c.id, front: c.front, back: c.back || {}, topic: c.topic || '', fach: c.fach || '', hue: c.hue, accent: specAccent(c.hue), acute: !!c.acute, draft: !!c.draft }; }
function buildQueue(deckCards, S, t, goal) {
  const seen = new Set((S.day && S.day.seen) || []);
  const due = [], fresh = [];
  for (const c of deckCards) {
    if (seen.has(c.id)) continue;
    const st = S.cards[c.id];
    if (st) { if (st.due <= t) due.push(c); } else fresh.push(c);
  }
  shuffle(due); shuffle(fresh);
  // Faellige Karten: laengst ueberfaellige zuerst, bei gleichem Datum die
  // schwaechere Karte. Reine Box-Sortierung waere falsch — dann fuellen die
  // schwachen Karten dauerhaft alle Plaetze und keine Karte festigt sich
  // (in der Simulation erreichte so keine einzige Karte die hoechste Box).
  due.sort((a, b) => {
    const A = S.cards[a.id] || {}, B = S.cards[b.id] || {};
    return (A.due || '').localeCompare(B.due || '') || ((A.box || 0) - (B.box || 0));
  });
  // Neue Karten zuerst: erst wenn jede Karte des Decks einmal dran war,
  // beginnen die Wiederholungen. Vorher stand due vor fresh — weil jede
  // beantwortete Karte am naechsten Tag wieder faellig war, fuellten die immer
  // gleichen Karten die Sitzung und der Rest kam nie dran.
  return fresh.concat(due).slice(0, Math.max(1, goal));
}
function computeStats(deckCards, S, t, goal) {
  const tm = addDays(t, 1);
  let mastered = 0, dueTomorrow = 0;
  for (const id in S.cards) { const st = S.cards[id]; if (st.box >= 5) mastered++; if (st.due === tm) dueTomorrow++; }
  const doneToday = (S.day && S.day.date === t) ? (S.day.count || 0) : 0;
  // Wie viele Karten des Decks waren in dieser Runde noch nie dran.
  // buildQueue setzt fresh vor due, die erste Runde geht also einmal durch
  // das ganze Deck; erst danach beginnen die Wiederholungen.
  let remainingCycle = 0;
  for (const c of deckCards) if (!S.cards[c.id]) remainingCycle++;
  return { doneToday, goal, streak: S.streak || 0, total: deckCards.length, mastered, dueTomorrow, remainingCycle };
}
function gradeCard(S, id, result, t, goal) {
  if (!S.day || S.day.date !== t) S.day = { date: t, count: 0, seen: [] };
  const st = S.cards[id] || { box: 0, due: t, kn: 0, unk: 0 };
  if (result === 'known') {
    st.box = Math.min(st.box + 1, 5);
    st.due = addDays(t, INTERVALS[st.box - 1]);
    st.kn = (st.kn || 0) + 1;
    S.day.count = (S.day.count || 0) + 1;
    S.totalKnown = (S.totalKnown || 0) + 1;
  } else {
    st.box = 0;
    st.due = addDays(t, WRONG_DAYS);
    st.unk = (st.unk || 0) + 1;
  }
  st.seen = t;
  S.cards[id] = st;
  if (!S.day.seen.includes(id)) S.day.seen.push(id);
  if (result === 'known' && S.day.count === goal && S.lastDone !== t) {
    S.streak = (S.lastDone === addDays(t, -1)) ? ((S.streak || 0) + 1) : 1;
    S.lastDone = t;
  }
}

function sanitize(b) {
  const out = {};
  if (typeof b.streak === 'number') out.streak = b.streak;
  if (b.examDate === null || typeof b.examDate === 'string') out.examDate = b.examDate;
  if (b.reviews && typeof b.reviews === 'object') {
    const r = {};
    for (const [k, v] of Object.entries(b.reviews)) if (STATUS.includes(v)) r[k] = v;
    out.reviews = r;
  }
  if (b.cards && typeof b.cards === 'object') {
    const c = {};
    for (const f of ['doneToday', 'goal', 'mastered', 'total', 'dueTomorrow']) if (typeof b.cards[f] === 'number') c[f] = b.cards[f];
    out.cards = c;
  }
  if (Array.isArray(b.dueToday)) out.dueToday = b.dueToday.filter(x => typeof x === 'string');
  return out;
}
function mergeProgress(cur, inc) {
  const out = { ...DEFAULTS(), ...cur };
  if ('streak' in inc) out.streak = inc.streak;
  if ('examDate' in inc) out.examDate = inc.examDate;
  out.reviews = { ...(cur.reviews || {}), ...(inc.reviews || {}) };          // last-write-wins per reviewId
  out.cards = { ...DEFAULTS().cards, ...(cur.cards || {}), ...(inc.cards || {}), goal: DEFAULTS().cards.goal };
  out.dueToday = ('dueToday' in inc) ? inc.dueToday : (cur.dueToday || []);  // replace when provided
  return out;
}
function withMeta(o, userId) { return { userId, ...o }; }

function corsHeaders(origin, env) {
  const allow = env.ALLOWED_ORIGINS || '*';
  let ao = '*';
  if (allow !== '*') { const list = allow.split(',').map(s => s.trim()).filter(Boolean); ao = list.includes(origin) ? origin : (list[0] || '*'); }
  return {
    'Access-Control-Allow-Origin': ao,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin'
  };
}
function jsonRes(obj, status, ch) { return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', ...ch } }); }
