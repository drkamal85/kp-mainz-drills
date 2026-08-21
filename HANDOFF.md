# KP-Mainz Drills — Project Handoff & Instructions

**Purpose:** Resume building Mohamed's KP Mainz medical-exam prep website in a new chat with full continuity. Upload this file (or paste it) at the start of a new chat.

---

## 1. PROJECT BASICS

- **What it is:** A personal study website — a library of interactive HTML *drills*, spaced-repetition *reviews*, and 1-page *summaries* for the Kenntnisprüfung (KP) Mainz oral exam. Target exam: March 2027.
- **GitHub repo:** `github.com/drkamal85/kp-mainz-drills`
- **Live URL:** `https://kp-mainz-drills.autoflow-med.workers.dev` (Cloudflare Worker, static assets)
- **Local clone path (per session):** `/home/claude/repo`
- **Chat language:** English (content is German)

---

## 2. DEPLOYMENT WORKFLOW (do this every change)

```
cd /home/claude/repo
git pull origin main                 # always pull first
# ...make edits...
# ...update index.html if adding/removing a card...
git add -A
git commit -m "message"
git push origin main 2>&1 | sed 's/ghp_[A-Za-z0-9]*/REDACTED/g' | tail -1
```

**CRITICAL rules:**
- **ALWAYS pipe `git push` through `sed 's/ghp_[A-Za-z0-9]*/REDACTED/g'`** so the GitHub token never prints.
- **GitHub PAT is session-only.** A NEW chat has NO token. At the start of a new session, **ask Mohamed for a fresh GitHub Personal Access Token (PAT)**, then set the remote:
  `git clone https://<PAT>@github.com/drkamal85/kp-mainz-drills.git /home/claude/repo`
  (or update the existing remote). Never persist the PAT anywhere.
- **Cloudflare auto-deploys ~25s after push.** `web_fetch` caches aggressively; Mohamed verifies in a real browser with hard-refresh (Cmd/Ctrl+Shift+R) or by appending `?v=N` to the URL.
- **Known issue:** the live Worker has at times served a *stale* build even after push + cache-buster. If "changes not reflected" persists, the repo is correct — it's a Cloudflare deploy lag / cache, OR check the Cloudflare dashboard (Workers & Pages → project → Deployments) for the commit's build status. An empty commit (`git commit --allow-empty -m "redeploy"`) can re-trigger.
- **The `ask_user_input_v0` tool's button selections DO NOT return the user's choice** (only echo the question). DO NOT use it. Ask directly with numbered options in plain text.

---

## 3. REPO STRUCTURE (current state)

```
drills/
  bga-komplett.html        (BGA — 2 week-tabs)
  echo-komplett.html       (Echo — 2 week-tabs)
  eeg-komplett.html        (EEG — 1 chapter)
  sono-komplett.html       (Sono — 2 chapter-tabs, GROWING)
reviews/
  chirurgie/      appendizitis-r2, cholezystitis-r2, ileus-r2, leistenhernie-r1, leistenhernie-r2
  gefaesschirurgie/  aortendissektion-r1
  notfallmedizin/    schaedel-hirn-trauma-r1
  pneumologie/    asthma-bronchiale-r1, copd-r1, copd-r2, lungenembolie-r2,
                  pleuraerguss-r1, pleuraerguss-r2, pneumonie-r1, pneumothorax-r1, pneumothorax-r2
  unfallchirurgie/   distale-radiusfraktur-r2
summaries/
  kardiologie/synkope.html
  neurologie/meningitis-enzephalitis.html
tools/
  master-themenliste.html
index.html
```

**Current homepage counts:** Alle 20 · Drills 4 · Reviews 13 · Summaries 2 · Tools 1.
Specialty groups (review section): Allgemein-/Viszeralchirurgie 4 · Pneumologie 6 · Unfallchirurgie/Orthopädie 1 · Notfall-&-Gefäßchirurgie 2.

**Last commit:** `ea75ee4` (Fix Pneumothorax R2 title leftovers).

---

## 4. STANDING RULES (apply to ALL future work)

### 4a. DRILLS — "simplistic" standard
- Single growing page per modality (e.g. `sono-komplett.html`), **tab-based** chapters/weeks.
- Pill-tab bar (`.tabs` + `.tab`) switching ONE section at a time; expandable cards within.
- **1–2 core cards per chapter.** Tables + Merksätze + visual schematics over prose. Plain language.
- v1 design system (see §5). Back-link to `../index.html`.
- **Sono:** NO Self-Check tab; inline KP-style Q&A allowed. New organs = NEW TAB in `sono-komplett.html`, not new files.
- **Tab-switching JS:** newer files use `data-k` / `tab.dataset.k` + `getElementById`; older used `data-station`. Both fine. The WORKING template uses `.chapter`/`.chapter.active` with plain `display:none`/`display:block` (NO `animation` on the section — a fadeIn animation once caused panels to stay at opacity:0 on tab switch).

### 4b. REVIEWS — levels (superset model)
- **R1** = 4 core stations only (Grundlagen · Klinik · Diagnostik · Therapie), v1-kurz, 4 pill-tabs.
- **R2** = same 4 core stations + **KP-Fragen** + **KP-Perlen** = 6 tabs.
- **R3** = R2 + **Protokolle** station (real documented Mainz cases). Protokolle is R3-only.
- **Superset rule:** lower levels stay *wortgleich*; higher levels APPEND. (In practice, when building a fresh R2 now, build the core in the new anchor-first format — see 4c.)

### 4c. REVIEWS — anchor-first memorization format (NEWEST RULE — applies to all reviews going forward)
Each core-station card:
1. Opens with a **bold ★ Merksatz / mnemonic line** (a `.callout.fact` with `<span class="callout-label">★ Merksatz</span>`).
2. Followed by a **comparison table**.
3. Minimal prose. Drop secondary detail.

### 4d. AUTOPUBLISH (trigger phrase: "Review: [topic] R[N]")
Build the review AND publish in one go:
1. Build in v1 review format at `reviews/[fachgebiet]/[topic]-r[n].html`.
2. Add/Update the card on `index.html` under the correct specialty group.
3. Bump all counts (see §6).
4. Commit + push.
If the topic already has an R1 card, **replace the card's href + badge to point to the new R2** (R2 supersets R1). Keep the R1 file in the repo.

### 4e. Build method for R2 (efficient)
Copy an existing anchor-first R2 as the structural shell (e.g. `leistenhernie-r2.html` or `pneumothorax-r2.html` — both have the proven 6-tab layout + KP-Fragen/Perlen CSS), then replace: `<title>`, eyebrow, `<h1>`, subtitle, footer, the 4 core stations, the KP-Fragen station, the KP-Perlen station. **WATCH OUT:** after copying a template, the title/h1/subtitle/footer carry the OLD topic name — replace ALL of them (this bug hit Pneumothorax R2).

---

## 5. v1 REVIEW DESIGN SYSTEM (reference)

- Fonts: **Fraunces** serif (body) + **Manrope** sans (UI). Background `#F7F4EE`, paper cards `#FFFFFF`.
- Max-width 860px. Pill-tab nav. Expandable cards (toggle `+` rotates 45° to ×).
- **Station colors** (each with a soft-tint variant): Grundlagen `#C0392B` · Klinik `#D97706` · Diagnostik `#1E5F9E` · Therapie `#2D7A3E` · KP-Fragen `#7B3F9E` · KP-Perlen `#B8860B`.
- **Callouts:** `.critical` (red), `.warning` (orange), `.fact` (blue), `.pearl` (gold) — 3px left border + tinted bg.
- **Q&A cards (R2):** `.qa` with `.qa-q` (question), `.qa-a` (answer), `.qa-meta` (e.g. "Mainz · Dr. X · Protokoll").
- **Pearl cards:** `.pearl-card` with `.pearl-label` ("⭐ Perle N · Thema"), `.pearl-content`, `.pearl-mnemonic`.
- **Tab JS (R2):** 6 buttons `data-s="1..6"`, JS via `tab.dataset.s` + `getElementById('s'+target)`.
- **Highlight inline:** `<em class="h">…</em>` = colored highlight.

**Homepage card markup (review):**
```html
<a class="card" href="reviews/[fach]/[topic]-rN.html" data-id="[topic]-rN">
  <div class="c-top">
    <div class="c-tags">
      <span class="pill" style="background:oklch(...);color:oklch(...);border-color:oklch(...)">Specialty</span>
    </div>
    <span class="lvl r2">R2</span>   <!-- or r1 -->
  </div>
  <div class="c-title">Topic Name</div>
  <div class="c-foot"><span class="c-arrow">→</span></div>
</a>
```
Specialty pill oklch hues: Pneumologie 200 · Chirurgie/Viszeralchir 35 · Unfallchir 50 · Notfall/Gefäß 18.
**Cards intentionally show ONLY: specialty pill + level badge + title → arrow.** Redundant `.c-desc`, `.c-meta`, `p-type` pill, "Komplett" pill were all removed. Do not re-add them.

---

## 6. UPDATING HOMEPAGE COUNTS (when adding/removing)

Every time a card is added/removed, update ALL of these in `index.html`:
- Filter-tab counts: `Alle <span class="tab-ct">N</span>`, `Reviews <span class="tab-ct">N</span>`, `Drills <span class="tab-ct">N</span>`, etc.
- Section label: `Themen-Reviews — N` / `Drills — N`.
- Per-group count: `<span class="spe-ct">N Themen</span>` for the relevant specialty.
- (The hero stat-row was REMOVED — only the filter tabs carry counts now. Do not re-add a stat-row.)

When **replacing** R1→R2 (same topic): counts DON'T change (replace, not add).

---

## 7. SOURCE MATERIAL (in project knowledge — use `project_knowledge_search`)

- **Amboss KP Lernplan** — authoritative topic source.
- **Stex Lernkarten (Elsevier)** — German content reference.
- **Mainz Protokolle 2023–2026** — real exam cases + examiner names (Dr. Dahm, Dr. Lakmann, Dr. Linke, Dr. Voßeler, Dr. Schniep Mendelssohn, Dr. Fischer, Dr. Werner, Dr. Hock, Dr. Kirdorf, Dr. Gervais, Dr. Morgenthaler, etc.) — pull KP-Fragen/Perlen from these (cite examiner + date in `.qa-meta`).
- **radiologische Zeichen** PDF — imaging signs.

Always `project_knowledge_search` for a topic's content + its documented Mainz protocol questions BEFORE building a review.

---

## 8. DRILLS — current content (for "grow further" requests)

- **sono-komplett.html** (GROWING, 2 tabs): K1 Grundlagen (Schallkopf, Orientierung, echofrei/arm/reich/iso, 2 Artefakte) + K2 Systematik (nüchtern/Inspiration/Schallfenster, scan order Leber→Galle→Pankreas→Milz→Nieren→Aorta→Blase→freie Flüssigkeit, "Größe-Form-Echo-Herd?"). **Roadmap (new TABS, one at a time on request "Sono Kapitel N"):** K3 Leber (normal+Steatosis), K4 Galle (+Stein), K5 Niere (+Stau), K6 Milz+freie Flüssigkeit, K7 Pankreas (+Pankreatitis), K8 Aorta (+AAA), K9 FAST, K10 Mainz-Bildbefunde.
- **bga-komplett.html** (2 week-tabs): Wk1 Grundlagen (Normalwerte, zwei Achsen, 4-Schritt, Mini-Cases) + Wk2 Respiratorisch (Kernlogik, Azidose, Alkalose, Kompensation). Kompensation card has a driver/compensator SCHEMA (red TREIBER "passt zum pH" → "→ pH →" → blue KOMPENSATOR "zieht dagegen") + a fully-compensated pH-HALF bar (7,36–7,40 Azidose-Hälfte | 7,40 | 7,40–7,44 Alkalose-Hälfte; "Kompensation überschreitet nie 7,40").
- **echo-komplett.html** (2 week-tabs): Wk1 Grundlagen (Sektorsonde, 4 Fenster, PLAX/PSAX/A4C) + Wk2 Herzinsuffizienz (EF/Simpson, HFrEF<40/HFmrEF 40-49/HFpEF≥50, diastolische Dysfunktion E/A E/e', Wandbewegung regional=KHK vs global=Muskel, 4-Säulen ACE/ARNI+BB+MRA+SGLT2, ICD≤35%/CRT).
- **eeg-komplett.html** (1 chapter): 4 Wellen (B-A-T-D), Alpha-Grundrhythmus+Berger-Effekt, pathologische Muster (Spike-Wave, 3-Hz, Delta-im-Wachen, Status→Diazepam), 4-Frage-Befund.

---

## 9. WHAT'S DONE vs. WHAT'S NEXT

**Reviews completed:**
- Chirurgie: cholezystitis-r2, appendizitis-r2, ileus-r2, leistenhernie-r2 (R1 also exists)
- Pneumologie: copd-r2, lungenembolie-r2, pleuraerguss-r2, pneumothorax-r2 (R1s exist), asthma-bronchiale-r1, pneumonie-r1
- Unfallchirurgie: distale-radiusfraktur-r2
- Gefäßchirurgie: aortendissektion-r1
- Notfallmedizin: schaedel-hirn-trauma-r1

**R1s still needing R2 upgrade (anchor-first):** asthma-bronchiale, pneumonie, aortendissektion, schaedel-hirn-trauma, distale-radiusfraktur (already R2).

**Tier-1 topics with NO review yet (high-yield gaps):** Divertikulitis, Kolonkarzinom, Herzinsuffizienz (full review — currently only an Echo drill chapter), Pankreatitis, Vorhofflimmern, Gastroenterologie topics.

**No R3 reviews exist yet** — R3 adds a Protokolle station with real documented Mainz cases.

---

## 10b. RANG AUF DEN THEMENSEITEN

Jede Themenseite trägt ihren Korpus-Rang als erste Angabe der Meta-Zeile:

```html
<span class="rk hi">Rang 32 von 96</span>
```

**Woher der Rang kommt:** `tools/_build-master.py` führt in `FLAT` je Thema die Zahl der
Erwähnungen im WhatsApp-Chat und in den Protokoll-Dateien. Sortiert wird absteigend nach dieser
Summe (`FLAT.sort(key=lambda r:-r[0])`), der Rang ist schlicht die Position — Cholezystitis mit
381 Erwähnungen steht auf 1, Gicht mit 6 auf 96. Die Trefferzahl selbst steht **nicht** mehr auf
der Seite: sie ist mechanisch gezählt, erfasst auch beiläufige Nennungen und täuscht deshalb
(Delir hat nur 37 Erwähnungen, war aber zweimal der Prüfungsfall).

**Farbstufe nach Rangdrittel**, damit der Rang ohne Zahlenvergleich spricht:
`hi` rot (Rang 1–32) · `mid` bernstein (33–64) · `lo` grau (65–96).

Gesetzt von **`tools/_stamp-rank.py`**, Quelle ist `api/themen.json` — also dieselbe Rangliste
wie Themenliste und Startseite. Der Lauf ist idempotent (vorhandener Span wird ersetzt) und
überspringt Seiten ohne Rangeintrag: Drills sowie die Extras Pleuraerguss und
Notfallpharmakologie. Stand: **80 von 82 Themenseiten**.

**Nach jeder Rangänderung erneut laufen lassen**, direkt nach `_build-master.py`:

```
python3 tools/_build-master.py && python3 tools/_stamp-rank.py
```

Der Stil steht als `.meta .rk` in jeder Seite und in `print.css`, erscheint also auch im PDF.

---

## 10c. META-ZEILE

Unter dem Untertitel stehen nur noch **zwei** Angaben:

```html
<span class="rk lo">Rang 71 von 97</span>
<span>R1 von 5</span>
```

Gesetzt von **`tools/_clean-meta.py`**. Entfernt wurden Lesezeit (geschätzt, nach Kürzungen nie
nachgezogen), Baudatum und die auf jeder Seite identische Quellenangabe.

**Massgeblich für die Stufe ist `data-lvl` in `index.html`**, nicht die Meta-Zeile. Bei
R4-Beförderungen wurde bisher nur der Index nachgezogen — **47 Seiten trugen eine veraltete
Stufe im Kopf**, etwa Cholezystitis mit R3 statt R4. Ausserdem war die Angabe über 19 Varianten
zersplittert ("R3 von 5 · Superset von R2", "R3 · 6 Tabs · …", blosses "R3"); jetzt einheitlich
`RN von 5`.

**Nach jeder Level-Änderung erneut laufen lassen**, zusammen mit der Rangpille:

```
python3 tools/_build-master.py && python3 tools/_stamp-rank.py && python3 tools/_clean-meta.py
```

---

## 11. DRUCK / PDF (Standard-Layout — Aug 2026)

Ein einziges Layout für alle Themenseiten. Nie pro Thema anpassen.

- **`/print.css`** — kanonische Quelle. Zwei Konsumenten: `<link media="print">` auf jeder
  Themenseite (Ctrl+P im Browser) und Inline-Injektion durch den PDF-Builder.
- **`/print.js`** — klappt vor dem Druck alle Stationen/Karten auf, zieht die Stationsbänder ein,
  stellt danach den Bildschirmzustand wieder her. Beide Tags sitzen im `<head>` jeder Themenseite —
  **bei neuen Themenseiten mitkopieren**:
  ```html
  <link rel="stylesheet" media="print" href="/print.css">
  <script src="/print.js" defer></script>
  ```
- **`tools/_build-pdf.py`** — WeasyPrint-Renderer (`pip install weasyprint --break-system-packages`).
  ```
  python3 tools/_build-pdf.py reviews/chirurgie/cholezystitis.html
  python3 tools/_build-pdf.py --all
  python3 tools/_build-pdf.py reviews/kardiologie/*.html --merge kardiologie.pdf
  python3 tools/_build-pdf.py --all --mode quiz     # Antworten verdeckt (Selbsttest)
  python3 tools/_build-pdf.py --all --flow          # fortlaufend statt Seite je Station
  ```
  Default-Ausgabe: `/mnt/user-data/outputs/pdf/`. PDFs werden **nicht** ins Repo committet.

**Layout-Regeln:** A4, 17/15/16/15 mm · Kopf: Thema links, Station rechts (ab Seite 2) ·
Fuß: Quelle links, `Seite / Gesamt` rechts · alle Karten offen, `break-inside: avoid` ·
PDF-Lesezeichen: Station = Ebene 1, Kartentitel = Ebene 2 · Bildschirm-Chrome (Tabs, Back-Link,
Footer, Toggles, Timer) entfällt.

**Seitenaufteilung (Soll):**

| Tab | Seiten |
|---|---|
| 1–4 Grundlagen · Klinik · Diagnostik · Therapie | **je genau 1** |
| 5 KP-Perlen | **genau 2** — Seite 1 Perlen, Seite 2 Rapid-Fire |
| 6 Fragen & Protokolle | mehr als 1, so wenige wie möglich |

Erzwungen wird das durch `.sf-wrap { break-before: page }` (Rapid-Fire startet immer neu) und
durch **vier Fit-Stufen** `body.fit-1` … `body.fit-4` in `print.css`, die progressiv enger setzen
(8,4pt bis 7,2pt Grundschrift, dazu Karten-, Callout- und Listenabstände).

`_build-pdf.py` probiert die Stufen **automatisch** aufsteigend durch und nimmt die lockerste,
bei der keine Station umbricht — sichtbar als `· fit-N` in der Ausgabe. Stand Aug 2026 passen
**70 von 72 Decks exakt**; Verteilung fit-0 47 · fit-1 8 · fit-2 10 · fit-3 5 · fit-4 2.
`sozialrecht-hygiene` und `diabetes-mellitus` brauchen für die Rapid-Fire bzw. Therapie eine
zweite Seite — das ist ein Inhaltslimit, kein Layoutfehler.

**Schriften beim Rendern:** Fraunces + Manrope müssen systemweit liegen
(`~/.fonts` + `fc-cache -f`, Quelle `raw.githubusercontent.com/google/fonts`), sonst Fallback auf Serif/Sans.

**Druckseite `print-pdf.html`:** Die Action **`.github/workflows/build-pdfs.yml`** rendert bei
jeder Änderung an `reviews/**`, `print.css` oder dem Builder alle Themen mit WeasyPrint und legt
sie unter `pdf/` ab — Vollversion, `pdf/quiz/` mit verdeckten Antworten und `pdf/fach/` als
Sammel-PDF je Fachgruppe. `tools/_build-pdf-index.py` baut daraus `print-pdf.html`, verlinkt von
der Startseite. Die Action committet das Ergebnis mit `[skip ci]` zurück.

Weil `wrangler.jsonc` das Repo-Root als `assets.directory` hat, wird `pdf/` automatisch
mit ausgeliefert. In `.gitignore` steht `*.pdf`, aber `!pdf/**/*.pdf` nimmt den Ausgabeordner aus.

**Warum nicht im Browser erzeugen:** WeasyPrint ist Python mit nativen Abhängigkeiten (Cairo,
Pango) — läuft weder im Browser noch auf Cloudflare Workers. Die JS-Bibliotheken für
PDF-Erzeugung beherrschen weder `@page`-Margin-Boxen noch Lesezeichen. Ein Knopf auf der Seite
würde also ein anderes, schlechteres Layout liefern als das vereinbarte.

**Browserdruck (Safari auf dem iPad, Chrome):** Die Fit-Stufe steckt **fest im `<body>`** jeder
Themenseite als `class="fit-N"` — sonst säht der Browser immer fit-0 und die 34 engeren Decks
liefen über. Geschrieben wird sie mit:

```
python3 tools/_build-pdf.py --all --write-fit
```

**Nach jedem Inhaltszuwachs erneut laufen lassen** — sonst stimmt die Stufe nicht mehr.
Die Klasse wirkt nur im Druck, weil `print.css` mit `media="print"` eingebunden ist; auf dem
Bildschirm ändert sie nichts. Ermittelt wird sie gegen ein um **12 mm verkürztes Blatt**
(`SAFETY_MM`), weil Safari und Chrome großzügiger setzen als WeasyPrint. Zusätzlich stehen zu
allen `break-*`-Regeln die alten `page-break-*`-Aliase, die WebKit teils noch braucht.

**Bekannte Grenze:** Chrome ignoriert `@page`-Margin-Boxen — im Browser-Ausdruck fehlen laufender
Kopf und Seitenzahl. Layout, Umbrüche und Farben stimmen. Für die volle Fassung `_build-pdf.py` nutzen.

---

## 10. OTHER NOTES & PREFERENCES

- Discovery-based, information-rich review formats preferred over Socratic quizzing during prep.
- Mohamed has an orthopedic surgical background — orthopedic topics need no written summaries.
- Spaced-repetition schedule (managed separately in Motion): R1 → R2 at day +7 → R3 at day +21.
- Pearl/Q&A content should cite the real examiner + date when drawn from a Mainz protocol.
- Mohamed verifies in-browser; if he says "not reflected," suspect cache/deploy, not the code (the repo is the source of truth — verify with `git log` / `grep`).
- He often asks to "simplify" right after a build — expect a follow-up pass converting prose → tables/Merksätze.
