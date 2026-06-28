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

const STATUS = ['new', 'learning', 'mastered'];
const DEFAULTS = () => ({
  streak: 0,
  examDate: null,
  reviews: {},
  cards: { doneToday: 0, goal: 10, mastered: 0, total: 0, dueTomorrow: 0 },
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
    return new Response(TOPICS_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=300', ...ch } });
  }

  // ---- public: master curriculum list (no auth) — bundled, CORS + cache ----
  if (url.pathname === '/api/themen') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    return new Response(THEMEN_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=300', ...ch } });
  }

  // ---- public: Kernprinzip flashcard deck (no auth) — bundled, CORS + cache ----
  if (url.pathname === '/api/deck') {
    if (request.method !== 'GET') return jsonRes({ error: 'method_not_allowed' }, 405, ch);
    return new Response(DECK_JSON, { status: 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=300', ...ch } });
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
      body.updatedAt = new Date().toISOString();
      await env.PROGRESS.put(key, JSON.stringify(body));
      return jsonRes(body, 200, ch);
    }
    return jsonRes({ error: 'method_not_allowed' }, 405, ch);
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
  out.cards = { ...DEFAULTS().cards, ...(cur.cards || {}), ...(inc.cards || {}) };
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
