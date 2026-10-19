#!/usr/bin/env python3
"""Ein Kern-Thema auf R5 setzen, nachdem die R5-Sitzung bestanden ist.

Aufruf aus dem Repo-Root:  python3 tools/_mark-r5.py <slug> [<slug> ...]

Macht pro Slug, idempotent:
  1. Slug in R5_TOPICS in tools/_build-master.py eintragen
  2. Indexkarte: data-lvl="5" und Badge <span class="lvl r5">R5</span>
  3. Deckseite: Stufe in der Meta-Zeile auf R5
Danach die Build-Kette vollstaendig laufen lassen:
  _build-master -> _build-fragen -> _build-content -> _build-kernprinzip
  -> _check-feeds -> _check-themenliste -> _check-fragen -> _check-mining
"""
import os
import csv, io, re, sys

if len(sys.argv) < 2:
    sys.exit("Aufruf: python3 tools/_mark-r5.py <slug> [<slug> ...]")

kern = {r['slug'] for r in csv.DictReader(io.open('data/lernliste.csv', encoding='utf-8'))
        if r['stufe'] == 'KERN'}
bm = 'tools/_build-master.py'
src = io.open(bm, encoding='utf-8').read()
m = re.search(r'^R5_TOPICS=(set\(\)|\{[^}]*\})$', src, re.M)
if not m:
    sys.exit("R5_TOPICS nicht gefunden in tools/_build-master.py")
cur = set() if m.group(1) == 'set()' else set(re.findall(r'"([^"]+)"', m.group(1)))

idx = io.open('index.html', encoding='utf-8').read()
for slug in sys.argv[1:]:
    if slug not in kern:
        sys.exit(f"{slug}: kein KERN-Thema laut data/lernliste.csv — R5 gilt nur fuer Kern.")
    card = re.search(r'<a class="card"[^>]*data-id="%s"[^>]*>.*?</a>' % re.escape(slug), idx, re.S)
    if not card:
        sys.exit(f"{slug}: keine Karte in index.html")
    c = card.group(0)
    c2 = re.sub(r'data-lvl="\d"', 'data-lvl="5"', c, count=1)
    c2 = re.sub(r'<span class="lvl r\d">R\d</span>', '<span class="lvl r5">R5</span>', c2, count=1)
    if '<span class="lvl r5">R5</span>' not in c2:
        sys.exit(f"{slug}: Badge auf der Karte nicht gefunden")
    idx = idx.replace(c, c2)
    # Deckseite: Stufenangabe in der Meta-Zeile (<span>R4</span>) auf R5
    href = re.search(r'href="([^"]+)"', c).group(1)
    if os.path.exists(href):
        deck = io.open(href, encoding='utf-8').read()
        meta = re.search(r'<div class="meta">.*?</div>', deck, re.S)
        if meta:
            m2 = re.sub(r'<span>R\d</span>', '<span>R5</span>', meta.group(0), count=1)
            if m2 != meta.group(0):
                io.open(href, 'w', encoding='utf-8').write(deck.replace(meta.group(0), m2))
                print(f"{slug}: Deckseite {href} auf R5")
    cur.add(slug)
    print(f"{slug}: R5 gesetzt")

new = '{' + ', '.join(f'"{s}"' for s in sorted(cur)) + '}'
src = src[:m.start(1)] + new + src[m.end(1):]
io.open(bm, 'w', encoding='utf-8').write(src)
io.open('index.html', 'w', encoding='utf-8').write(idx)
print(f"R5_TOPICS: {len(cur)} Themen. Jetzt die Build-Kette laufen lassen.")
