# -*- coding: utf-8 -*-
"""Baut den Fragen-Index aus dem Protokollkorpus.  RUN FROM REPO ROOT.

    python3 tools/_build-fragen.py

Liest   data/protokoll-korpus.json, data/lernliste.csv, data/themen-muster.json
Schreibt data/fragen-index.json   — vollstaendig, mit allen Protokoll-IDs
         api/fragen.json          — kompakt fuer den Worker (/api/fragen)
         sources/mining/<slug>.md — menschenlesbare Sicht je Thema

Der Index ist abgeleitet, nie von Hand pflegen. Aendert sich der Korpus oder
ein Suchmuster, dieses Skript neu laufen lassen und _check-mining.py gruen sehen.
"""
import json, io, re, csv, os, collections, datetime, hashlib

ROOT = os.getcwd()
K = json.load(io.open('data/protokoll-korpus.json', encoding='utf-8'))
PROT = K['protokolle']
LL = [r for r in csv.DictReader(io.open('data/lernliste.csv', encoding='utf-8')) if r['rank']]
MUSTER = json.load(io.open('data/themen-muster.json', encoding='utf-8'))['muster']
PAT = {slug: re.compile(rx, re.I) for slug, rx in MUSTER.items()}
THEMA = {r['slug']: r['thema'] for r in LL}

FACH_ORDER = ['Innere', 'Chirurgie', 'Notfall/Anästhesie', 'Radiologie', 'EKG',
              'Pharmakologie', 'Rechtsmedizin', 'Strahlenschutz', 'Sonstiges']

def norm(q):  return re.sub(r'\s+', ' ', (q or '').strip())
def key(q):   return re.sub(r'[^a-zäöüß0-9]', '', q.lower())[:110]

# ---------------------------------------------------------------- aggregieren
agg = {}
for p in PROT:
    pid = p['protokoll_id']; d = p.get('pruefungsdatum')
    for fach, items in (p.get('fragen') or {}).items():
        for raw in items or []:
            q = norm(raw)
            if len(q) < 6:
                continue
            k = (fach, key(q))
            e = agg.setdefault(k, {'frage': q, 'fach': fach, 'protokolle': [],
                                   'daten': [], 'varianten': set(), 'themen': set()})
            if len(q) > len(e['frage']):
                e['frage'] = q                      # laengste Fassung fuehrt
            e['protokolle'].append(pid)
            e['varianten'].add(q)
            if d:
                e['daten'].append(d)
            for slug, rx in PAT.items():
                if rx.search(q):
                    e['themen'].add(slug)

fragen = []
for i, (_k, e) in enumerate(sorted(agg.items(), key=lambda kv: -len(set(kv[1]['protokolle']))), 1):
    pids = sorted(set(e['protokolle'])); ds = sorted(e['daten'])
    fragen.append({
        'id': f'F{i:05d}', 'frage': e['frage'], 'fach': e['fach'],
        'themen': sorted(e['themen']),
        'anzahl_protokolle': len(pids), 'protokolle': pids,
        'erstmals': ds[0] if ds else None, 'zuletzt': ds[-1] if ds else None,
        'varianten': sorted(e['varianten'])[:5] if len(e['varianten']) > 1 else [],
    })

korpus_sha = hashlib.sha256(io.open('data/protokoll-korpus.json', 'rb').read()).hexdigest()[:16]
full = {'schema': 'kp-fragen-index/1',
        'quelle': 'abgeleitet aus data/protokoll-korpus.json',
        'korpus_sha256_16': korpus_sha,
        'stand': str(datetime.date.today()),
        'anzahl_fragen': len(fragen),
        'anzahl_nennungen': sum(f['anzahl_protokolle'] for f in fragen),
        'hinweise': ('Jede Frage traegt die Protokoll-IDs, in denen sie dokumentiert ist. '
                     'Nie Fragen erfinden oder Formulierungen hinzufuegen, die hier nicht stehen. '
                     'Themenzuordnung ueber data/themen-muster.json, eine Frage kann mehreren Themen gehoeren.'),
        'fragen': fragen}
io.open('data/fragen-index.json', 'w', encoding='utf-8').write(
    json.dumps(full, ensure_ascii=False, separators=(',', ':')))

# ---------------------------------------------------------------- Worker-Feed
kompakt = {'schema': 'kp-fragen-kompakt/1', 'stand': full['stand'],
           'korpus_sha256_16': korpus_sha,
           'hinweis': ('Nur themenzugeordnete Fragen, Protokoll-IDs auf 6 gekuerzt. '
                       'Vollstaendig: data/fragen-index.json im Repo.'),
           'anzahl_fragen': sum(1 for f in fragen if f['themen']),
           'fragen': [{'id': f['id'], 'q': f['frage'], 'fach': f['fach'], 't': f['themen'],
                       'n': f['anzahl_protokolle'], 'p': f['protokolle'][:6],
                       'zuletzt': f['zuletzt']}
                      for f in fragen if f['themen']]}
io.open('api/fragen.json', 'w', encoding='utf-8').write(
    json.dumps(kompakt, ensure_ascii=False, separators=(',', ':')))

# ---------------------------------------------------------------- Mining-Sicht
os.makedirs('sources/mining', exist_ok=True)
by_topic = collections.defaultdict(list)
for f in fragen:
    for s in f['themen']:
        by_topic[s].append(f)

faelle = collections.defaultdict(collections.Counter)
bilder = collections.defaultdict(collections.Counter)
pruefer = collections.defaultdict(collections.Counter)
for p in PROT:
    txt_f = ' '.join((x.get('diagnose') or '') + ' ' + (x.get('leitsymptom') or '')
                     for x in p.get('faelle') or [])
    for slug, rx in PAT.items():
        if txt_f and rx.search(txt_f):
            for x in p.get('faelle') or []:
                if x.get('diagnose'):
                    faelle[slug][norm(x['diagnose'])[:110]] += 1
        for b in p.get('bildmaterial') or []:
            if rx.search(b):
                bilder[slug][norm(b)[:90]] += 1
    alle_fragen = []
    for v in (p.get('fragen') or {}).values():
        alle_fragen += (v or [])
    txt_q = ' '.join(alle_fragen)
    hit = {s for s, rx in PAT.items() if txt_q and rx.search(txt_q)}
    for s in hit:
        for k in p.get('kommission') or []:
            pruefer[s][k['name'].replace(' [unsicher]', '')] += 1

written = 0
for slug, fs in sorted(by_topic.items()):
    L = [f'# Mining-Input: {slug}', '',
         f'Thema: {THEMA.get(slug, slug)}', '',
         f'Erzeugt aus data/fragen-index.json ({len(PROT)} Protokolle, Stand {full["stand"]}).',
         '**Nicht von Hand pflegen** — `python3 tools/_build-fragen.py` schreibt diese Datei neu.',
         'Jede Zeile ist dokumentiert; die Zahl in Klammern ist die Anzahl Protokolle,',
         'danach die Protokoll-IDs als Beleg. Fuer Tab 6 die oberen 12-18 nehmen und nach Spec gewichten.', '']
    if faelle.get(slug):
        L += ['## Dokumentierte Faelle', ''] + [f'- {d}  ({n})' for d, n in faelle[slug].most_common(12)] + ['']
    if bilder.get(slug):
        L += ['## Gezeigtes Bildmaterial', ''] + [f'- {b}  ({n})' for b, n in bilder[slug].most_common(8)] + ['']
    L += ['## Dokumentierte Fragen', '']
    per_fach = collections.defaultdict(list)
    for f in fs:
        per_fach[f['fach']].append(f)
    for fach in FACH_ORDER:
        rows = sorted(per_fach.get(fach, []), key=lambda f: -f['anzahl_protokolle'])[:40]
        if not rows:
            continue
        L += [f'### {fach}', '']
        for f in rows:
            L.append(f"- ({f['anzahl_protokolle']}) {f['frage']}  \n  `{', '.join(f['protokolle'][:4])}`  ·  {f['id']}")
        L.append('')
    if pruefer.get(slug):
        L += ['## Haeufigste Pruefer zu diesem Thema', '',
              ', '.join(f'{k} ({v})' for k, v in pruefer[slug].most_common(6)), '']
    io.open(f'sources/mining/{slug}.md', 'w', encoding='utf-8').write('\n'.join(L))
    written += 1

print(f"fragen-index.json : {len(fragen)} Fragen, {full['anzahl_nennungen']} Nennungen")
print(f"api/fragen.json   : {kompakt['anzahl_fragen']} themenzugeordnete Fragen")
print(f"sources/mining/   : {written} Themen geschrieben")
