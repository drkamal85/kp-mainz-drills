---
name: "kp-amboss-validate"
description: "Autonomously validate KP Mainz review decks against the stored verbatim AMBOSS captures (sources/amboss/) — fix only clear contradictions in every panel incl. Diagnostik, never add, expand or delete; flag every validated deck. Use for AMBOSS check or R5 step 2."
---

# kp-amboss-validate

Checks the facts on the KP website (repo `drkamal85/kp-mainz-drills`) against the verbatim AMBOSS captures in `sources/amboss/`. It protects existing content: it fixes clear errors and nothing else. Runs only when Mohamed asks for it, then fully autonomously — never asks anything mid-run, never queues anything for his approval.

Repo copy of the skill `kp-amboss-validate` (the skill wins where the two differ).

## Standing rule (09.10.2026)
All 88 decks were validated in one pass on 09.10.2026. **From now on every newly built or changed deck — new deck, R-promotion, new tab 6, new Perlen — runs through this validation before publishing and carries the flag.** Content added after the flag date is unvalidated until the deck is re-run.

## Inputs
- A slug, a list of slugs, `all KERN`, `all STANDARD` or `all` (tiers from `data/lernliste.csv`).

## Reference (the only allowed source)
- `sources/amboss/<slug>.md` plus any `sources/amboss/<slug>--*.md` (multi-article topics).
- `sources/amboss/INDEX.md` for slug mappings and known capture gaps.
- Never memory, never the web, never another deck. No capture -> skip the deck, log `keine Erfassung`.

## Scope per deck (`reviews/*/<slug>.html`)
- Checked and corrected, all under the same rules: panels `grundlagen`, `klinik`, `diagnostik`, `therapie`, `perlen` (incl. Rapid-Fire) and the answers (`.ans`) in `protokoll` (tab 6).
- Never touched: tab-6 questions (`.pq-frage`, source = KP-Intel), `.pk-akte` vignettes, headings, layout, CSS, JS, badges (except the AMBOSS flag this skill sets), mnemonics, didactic framing.
- Helper: `python3 tools/_amboss-deck-text.py <slug>` prints the checkable text per panel.

## Verdict per claim
Check every number, threshold, unit, time window, drug, dose, classification/stage, eponym, score item and criterion:
- ✓ matches AMBOSS (same value, or a faithful simplification).
- ✗ clear contradiction: wrong value/unit, wrong drug or dose, wrong stage, reversed meaning, wrong first-line choice, wrong first-line test, wrong lab threshold. Must quote the AMBOSS line.
- ? not in the capture, in a known gap, or ambiguous (range, alternatives, guideline nuance, protocol-derived exam phrasing). When in doubt -> ?, never ✗.

## Edit rules (hard)
1. Change only ✗ — in every checked panel, Diagnostik included. Minimal edit: replace the wrong value/word inside the existing sentence. Keep structure, style, length, markup.
2. Never add facts, bullets, cards, sentences, qualifiers or explanations — even when AMBOSS has more.
3. Never delete a claim. ? is logged only.
4. Tab-6 answers: fix ✗ values only; keep the 3-Zug structure and word counts (`tools/TAB6-ANTWORTFORMAT.md`).
5. `python3 tools/_check-amboss-edits.py <deck>` must PASS. FAIL -> `git checkout -- <deck>`, log it, continue.

## AMBOSS flag (mandatory for every validated deck)

Every deck that finishes with status `done` gets the flag — including decks with 0 fixes. Decks that are `skipped` or `reverted` never get it.

1. **When:** only AFTER the edit guard has passed for that deck. Never before — the guard compares against HEAD and would fail on the added markup.
2. **Where:** on the `<h1>` line of the deck header, directly after `</h1>` and after an existing `r4pill`/`r5pill` if there is one. Same line, no new line.
3. **Markup (exact):**
   `<span class="amboss-pill" data-amboss-validated="YYYY-MM-DD" style="display:inline-block;margin-left:8px;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;background:#e6f4ea;color:#1e6b34;vertical-align:middle">AMBOSS-validiert · DD.MM.YYYY</span>`
   with the run date in both places.
4. **Re-validation:** if the deck already carries an `amboss-pill`, update its date in both places. Never add a second pill.
5. **Record:** add `"validated": "YYYY-MM-DD"` to `reports/amboss/<slug>.json`, and list every flagged deck in `reports/amboss-validation.md` under a heading `AMBOSS-validiert`.
6. The flag is the only markup this skill may add. It changes no content.

## Run order
1. **Repo sync and rule sync.** `cd /home/claude/repo && git fetch -q origin main && git reset -q --hard origin/main` (clone `https://github.com/drkamal85/kp-mainz-drills.git` if missing). Then, if still needed (idempotent):
   - In `tools/_check-amboss-edits.py` remove the Diagnostik block so the guard allows Diagnostik fixes:
     ```
     python3 - <<'PY'
     import io
     p='tools/_check-amboss-edits.py'; s=io.open(p,encoding='utf-8').read()
     s=s.replace('    if panel(old, "diagnostik") != panel(new, "diagnostik"):\n        why.append("Diagnostik panel changed")\n','')
     s=s.replace('the Diagnostik panel or any tab-6 question','any tab-6 question')
     io.open(p,'w',encoding='utf-8').write(s)
     PY
     grep -q 'Diagnostik panel changed' tools/_check-amboss-edits.py && echo "GUARD NOT PATCHED"
     ```
   - Rewrite `tools/AMBOSS-VALIDATE.md` so its Scope, Edit rules, AMBOSS flag, Run order and report format match this skill (Diagnostik corrected like every panel, no Diagnostik queue, flag section, no PAT request). Keep its other sections.
   - Commit both as `AMBOSS-Regeln: Diagnostik wird wie alle Panels korrigiert, Flag AMBOSS-validiert` before touching any deck.
2. Per deck: extract text -> compare with the capture -> write `reports/amboss/<slug>.json` -> apply ✗ fixes in all checked panels -> run the edit guard -> on PASS set the AMBOSS flag. Decks are independent; fan out to parallel sub-agents in batches of ~7 when validating many, each editing only its own decks and never running git or builds.
3. Aggregate `reports/amboss-validation.md` (per deck: ✓/✗/? counts, fixes per panel, skipped/reverted, flag date).
4. Validators and full build chain in order: `_check-fragen.py`, `_build-master.py`, `_build-content.py`, `_build-kernprinzip.py`, `_check-feeds.py` (must PASS).
5. One commit per changed deck (`AMBOSS-Validierung: <slug> — n Korrekturen, AMBOSS-validiert`, ✗ list in the body), then one commit for reports + derived files. Pull/rebase, then publish: git push if the session can; otherwise the kp-outbox route (`git format-patch` into `autoflow/kp-outbox`, confirm via `autoflow/kp-autopublish.log`). Never ask for a PAT.
6. Final message: 3 lines (decks checked, fixes applied incl. how many in Diagnostik, decks flagged AMBOSS-validiert).

## Per-deck report (`reports/amboss/<slug>.json`)
```json
{"slug": "...", "deck": "reviews/.../<slug>.html", "capture": ["sources/amboss/<slug>.md"],
 "counts": {"ok": 0, "fix": 0, "unclear": 0},
 "fixes": [{"panel": "diagnostik", "deck_text": "...", "new_text": "...", "amboss_quote": "..."}],
 "unclear": [{"panel": "...", "deck_text": "...", "reason": "..."}],
 "status": "done | skipped: <reason> | reverted: <reason>",
 "validated": "YYYY-MM-DD (only when status is done)"}
```