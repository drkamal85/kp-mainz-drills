#!/usr/bin/env python3
"""Guard for kp-amboss-validate: an AMBOSS fix may only REPLACE a value/word.

Compares each changed deck against the git HEAD version and fails if:
  - the number of lines changed (content added or removed),
  - any changed line grew by more than MAX_GROWTH characters,
  - any single line changed by more than MAX_CHANGED characters,
  - any tab-6 question (.pq-frage) changed.
Usage: python3 tools/_check-amboss-edits.py [deck paths...]   (default: all modified reviews)
Exit 1 on any violation, listing the offending deck(s).
"""
import difflib, re, subprocess, sys

MAX_GROWTH = 40
MAX_CHANGED = 80


def head(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def panel(src, name):
    m = re.search(rf'<section class="panel[^"]*" data-panel="{name}".*?</section>', src, re.S)
    return m.group(0) if m else ""


paths = sys.argv[1:] or [
    l[3:] for l in subprocess.run(["git", "status", "--porcelain", "reviews"],
                                  capture_output=True, text=True).stdout.splitlines()
    if l[:2].strip() == "M"
]
bad = []
for p in paths:
    old, new = head(p), open(p, encoding="utf-8").read()
    if old is None:
        continue
    o, n = old.splitlines(), new.splitlines()
    why = []
    if len(o) != len(n):
        why.append(f"line count {len(o)}→{len(n)}")
    if re.findall(r'<div class="pq-frage".*?</div>', old, re.S) != re.findall(r'<div class="pq-frage".*?</div>', new, re.S):
        why.append("tab-6 question changed")
    for a, b in zip(o, n):
        if a == b:
            continue
        sm = difflib.SequenceMatcher(None, a, b)
        changed = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal")
        if len(b) - len(a) > MAX_GROWTH or changed > MAX_CHANGED:
            why.append(f"line edit too large (+{len(b)-len(a)} chars, {changed} changed)")
            break
    if why:
        bad.append((p, why))
for p, why in bad:
    print(f"FAIL {p}: {'; '.join(why)}")
print("RESULT:", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)
