#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validiert den Fragen-Index gegen den Protokollkorpus.  RUN FROM REPO ROOT.

    python3 tools/_check-mining.py

Das ist die Pruefung, die aus dem Index eine *belastbare* Quelle macht:
keine Frage ohne Beleg, kein Beleg ins Leere, keine stille Veralterung.

PASS heisst: jede Frage im Index steht so in mindestens einem Protokoll,
jede zitierte Protokoll-ID existiert, der Index passt zum aktuellen Korpus,
und jede Frage in sources/mining/*.md ist im Index wiederzufinden.
"""
import json, io, re, sys, os, glob, hashlib, collections

def norm(q):  return re.sub(r'\s+', ' ', (q or '').strip())
def key(q):   return re.sub(r'[^a-zäöüß0-9]', '', (q or '').lower())[:110]

fail = []
warn = []

# ---------------------------------------------------------------- laden
for p in ('data/protokoll-korpus.json', 'data/fragen-index.json'):
    if not os.path.exists(p):
        print(f'FEHLT: {p}'); sys.exit(1)

K = json.load(io.open('data/protokoll-korpus.json', encoding='utf-8'))
IDX = json.load(io.open('data/fragen-index.json', encoding='utf-8'))
PROT = {p['protokoll_id']: p for p in K['protokolle']}
FRAGEN = IDX['fragen']

# ---------------------------------------------------------------- 1 Frische
sha = hashlib.sha256(io.open('data/protokoll-korpus.json', 'rb').read()).hexdigest()[:16]
if IDX.get('korpus_sha256_16') != sha:
    fail.append(f"Index ist veraltet: korpus_sha256_16={IDX.get('korpus_sha256_16')} "
                f"aber Korpus hat {sha}. tools/_build-fragen.py neu laufen lassen.")

# ---------------------------------------------------------------- 2 Belege
# Alle im Korpus tatsaechlich vorkommenden Fragen, nach Schluessel
korpus_keys = collections.defaultdict(set)
for pid, p in PROT.items():
    for fach, items in (p.get('fragen') or {}).items():
        for raw in items or []:
            q = norm(raw)
            if len(q) >= 6:
                korpus_keys[(fach, key(q))].add(pid)

ohne_beleg = tote_id = falsche_zuordnung = zahl_falsch = 0
for f in FRAGEN:
    pids = f.get('protokolle') or []
    if not pids:
        ohne_beleg += 1
        if ohne_beleg <= 3: fail.append(f"{f['id']} hat keine Protokoll-ID: {f['frage'][:60]}")
        continue
    for pid in pids:
        if pid not in PROT:
            tote_id += 1
            if tote_id <= 3: fail.append(f"{f['id']} zitiert unbekanntes Protokoll {pid}")
    if f.get('anzahl_protokolle') != len(set(pids)):
        zahl_falsch += 1
        if zahl_falsch <= 3: fail.append(f"{f['id']}: anzahl_protokolle passt nicht zur ID-Liste")
    # steht die Frage wirklich in diesen Protokollen?
    echte = korpus_keys.get((f['fach'], key(f['frage'])), set())
    if not echte:
        falsche_zuordnung += 1
        if falsche_zuordnung <= 3:
            fail.append(f"{f['id']} steht so in keinem Protokoll: {f['frage'][:60]}")
    elif not set(pids) <= echte:
        falsche_zuordnung += 1
        if falsche_zuordnung <= 3:
            fail.append(f"{f['id']} nennt Protokolle, in denen die Frage nicht steht")

# ---------------------------------------------------------------- 3 Duplikate
seen = {}
dupes = 0
for f in FRAGEN:
    k = (f['fach'], key(f['frage']))
    if k in seen:
        dupes += 1
        if dupes <= 3: fail.append(f"Doppelt im Index: {f['id']} und {seen[k]}")
    seen[k] = f['id']

# ---------------------------------------------------------------- 4 Themen
if os.path.exists('data/themen-muster.json'):
    muster = json.load(io.open('data/themen-muster.json', encoding='utf-8'))['muster']
    unbekannt = {s for f in FRAGEN for s in f.get('themen', [])} - set(muster)
    if unbekannt:
        fail.append(f"Index nennt Themen ohne Muster: {sorted(unbekannt)[:5]}")
    import csv as _csv
    slugs = {r['slug'] for r in _csv.DictReader(io.open('data/lernliste.csv', encoding='utf-8')) if r['rank']}
    verwaist = set(muster) - slugs
    if verwaist:
        warn.append(f"Muster ohne Thema in der Lernliste: {sorted(verwaist)}")

# ---------------------------------------------------------------- 5 Mining-Dateien
idx_ids = {f['id'] for f in FRAGEN}
mining_bad = 0
for path in sorted(glob.glob('sources/mining/*.md')):
    txt = io.open(path, encoding='utf-8').read()
    for fid in re.findall(r'·\s+(F\d{5})', txt):
        if fid not in idx_ids:
            mining_bad += 1
            if mining_bad <= 3: fail.append(f"{os.path.basename(path)} zitiert unbekannte Frage {fid}")

# ---------------------------------------------------------------- Bericht
print(f"Korpus            : {len(PROT)} Protokolle")
print(f"Index             : {len(FRAGEN)} Fragen, {IDX.get('anzahl_nennungen')} Nennungen")
print(f"  ohne Beleg      : {ohne_beleg}")
print(f"  tote Protokoll-ID: {tote_id}")
print(f"  falsch zugeordnet: {falsche_zuordnung}")
print(f"  Zahl != IDs     : {zahl_falsch}")
print(f"  Duplikate       : {dupes}")
print(f"Mining-Dateien    : {len(glob.glob('sources/mining/*.md'))} | unbekannte IDs: {mining_bad}")
for w in warn:
    print('WARN:', w)
for f_ in fail[:12]:
    print('FAIL:', f_)
ok = not fail
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
