#!/usr/bin/env python3
"""Prueft, ob die Haken in KP-Themenliste-flach.md mit api/themen.json uebereinstimmen.

Die Themenliste wird von Hand gepflegt, themen.json aus index.html generiert —
sie koennen auseinanderlaufen. Nach jedem neuen Review laufen lassen.
"""
import json, re, sys

th = json.load(open('api/themen.json', encoding='utf-8'))
core = {x['thema'] for x in th['topics'] if x.get('covered')}
md = open('sources/KP-Themenliste-flach.md', encoding='utf-8').read()
haken = {m.group(1).strip() for m in
         re.finditer(r'\|\s*\d+\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|\s*\u2713 R', md)}
stated = re.search(r'Aktuell \*\*(\d+) von 97\*\*', md)
stated = int(stated.group(1)) if stated else -1

miss = sorted(core - haken)
extra = sorted(haken - core)
print('themen.json covered : %d' % len(core))
print('Themenliste-Haken   : %d' % len(haken))
print('Kopfzeile sagt      : %d' % stated)
print('  Review da, Haken fehlt : %s' % (miss or 'keine'))
print('  Haken da, Review fehlt : %s' % (extra or 'keine'))
ok = not miss and not extra and stated == len(core)
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
