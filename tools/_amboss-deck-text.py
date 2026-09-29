#!/usr/bin/env python3
"""Dump the checkable text of a review deck, panel by panel, for AMBOSS validation.

Usage: python3 tools/_amboss-deck-text.py <slug>
Prints: panel name, then numbered text lines (L<n>) from the deck's source HTML.
Scope: grundlagen, klinik, diagnostik, therapie, perlen (incl. Rapid-Fire) and the
answers (.ans) of the protokoll panel. Questions (.pq-frage) are skipped.
"""
import glob, html, re, sys

slug = sys.argv[1]
paths = glob.glob(f"reviews/*/{slug}.html")
if not paths:
    sys.exit(f"NO DECK: {slug}")
src = open(paths[0], encoding="utf-8").read()
print(f"# DECK {paths[0]}")

panels = re.split(r'(?=<section class="panel[^"]*" data-panel=")', src)
for p in panels:
    m = re.match(r'<section class="panel[^"]*" data-panel="([^"]+)"', p)
    if not m:
        continue
    name = m.group(1)
    body = p
    if name == "protokoll":
        body = "\n".join(re.findall(r'<div class="ans"[^>]*>(.*?)</div>', p, re.S))
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<br\s*/?>|</(p|li|tr|div|h\d|summary|td|th)>", "\n", body)
    body = re.sub(r"<[^>]+>", " ", body)
    lines = [re.sub(r"\s+", " ", html.unescape(l)).strip() for l in body.split("\n")]
    lines = [l for l in lines if l]
    print(f"\n## PANEL {name}")
    for i, l in enumerate(lines, 1):
        print(f"L{i}: {l}")
