---
name: kp-amboss-validate
description: Autonomously validate KP Mainz review decks against the stored verbatim AMBOSS captures (sources/amboss/) — correct only clear factual contradictions with minimal edits, never add, expand or delete content. Use for "validate against AMBOSS", "AMBOSS check", R5 step 2, or any deck fact-check.
---

# kp-amboss-validate

Checks the facts on the KP website (repo `drkamal85/kp-mainz-drills`) against the verbatim
AMBOSS captures in `sources/amboss/`. It **protects existing content**: it fixes clear errors
and nothing else. Runs fully autonomously — never asks Mohamed anything mid-run.

## Inputs
- A slug, a list of slugs, `all KERN`, `all STANDARD`, or `all` (tiers from `data/lernliste.csv`).
- Default when no input is given: `all KERN`.

## Sources (the only allowed reference)
- `sources/amboss/<slug>.md` plus any `sources/amboss/<slug>--*.md` (multi-article topics).
- `sources/amboss/INDEX.md` for mappings and known capture gaps.
- Never memory, never the web, never another deck. No capture → skip the deck, log `keine Erfassung`.

## Scope per deck (`reviews/*/<slug>.html`)
- Checked: panels `grundlagen`, `klinik`, `diagnostik`, `therapie`, `perlen` (incl. Rapid-Fire),
  and the answers (`.ans`) in `protokoll` (tab 6).
- Never touched: tab-6 questions (`.pq-frage`, source = KP-Intel), `.pk-akte` case vignettes,
  headings, layout, CSS, JS, badges, Eselsbrücken/mnemonics, didactic framing.
- Helper: `python3 tools/_amboss-deck-text.py <slug>` prints the checkable text per panel.

## Verdict per claim
Check every number, threshold, unit, time window, drug, dose, classification/stage,
eponym, score item and diagnostic/therapeutic criterion:
- **✓** matches AMBOSS (same value, or deck is a faithful simplification).
- **✗** clear contradiction: wrong number/threshold/unit, wrong drug or dose, wrong
  classification/stage, reversed meaning, wrong first-line choice. Must quote the AMBOSS line.
- **?** not in the capture, in a known capture gap, or ambiguous (AMBOSS gives a range or
  alternatives, deck value lies inside it; guideline nuance; rounding; different but
  compatible wording; protocol-derived exam phrasing). **When in doubt → ?, never ✗.**

## Edit rules (hard)
1. Change only ✗. Minimal edit: replace the wrong value/word/phrase with the AMBOSS one,
   inside the existing sentence. Keep sentence structure, style, length and markup.
2. Never add facts, bullets, cards, sentences, qualifiers or explanations — even when AMBOSS
   has more or the deck "misses" something.
3. Never delete a claim. `?` claims are logged only.
4. **Diagnostik panel: never edited.** Its ✗ go to `reports/amboss-diagnostik-queue.md`
   (deck text → AMBOSS quote → proposed minimal fix) for Mohamed's approval (standing rule).
5. Tab-6 answers: fix ✗ values only; keep the 3-Zug structure and word counts (rules in
   `tools/TAB6-ANTWORTFORMAT.md`).
6. `python3 tools/_check-amboss-edits.py <deck>` must PASS (no line added/removed, no
   large rewrites, Diagnostik and questions untouched). FAIL → `git checkout -- <deck>`, log it.

## Run order
1. Repo sync: `cd /home/claude/repo && git fetch -q origin main && git reset -q --hard origin/main`
   (clone `https://github.com/drkamal85/kp-mainz-drills.git` if missing).
2. Per deck: extract text → compare against the capture → write
   `reports/amboss/<slug>.json` → apply ✗ fixes (non-Diagnostik) → run the edit guard.
   Decks are independent; fan out to parallel sub-agents in batches when validating many.
3. Aggregate: `reports/amboss-validation.md` (one row per deck: ✓/✗/? counts, fixes applied,
   queued Diagnostik fixes, skipped/reverted) and `reports/amboss-diagnostik-queue.md`.
4. Validators and full build chain, in order: `_check-fragen.py`, `_build-master.py`,
   `_build-content.py`, `_build-kernprinzip.py`, `_check-feeds.py` (must PASS).
5. Commit: one commit per changed deck (`AMBOSS-Validierung: <slug> — n Korrekturen` with the
   ✗ list in the body), then one commit for reports + derived files. Pull/rebase, push, verify.
   PAT is session-only — if missing, ask once at the very end, never mid-run.
6. Final message: 3 lines (decks checked, fixes applied, Diagnostik items queued).

## Per-deck report format (`reports/amboss/<slug>.json`)
```json
{"slug": "...", "deck": "reviews/.../<slug>.html", "capture": ["sources/amboss/<slug>.md"],
 "counts": {"ok": 0, "fix": 0, "unclear": 0},
 "fixes": [{"panel": "therapie", "deck_text": "...", "new_text": "...", "amboss_quote": "..."}],
 "diagnostik_queue": [{"deck_text": "...", "proposed": "...", "amboss_quote": "..."}],
 "unclear": [{"panel": "...", "deck_text": "...", "reason": "..."}],
 "status": "done | skipped: <reason> | reverted: <reason>"}
```
