#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Kernprinzip flashcard deck.

ONE card per topic = a merge of "core skeleton" (Model 1) + "clinical reflex" (Model 3):
  front  = a recognition cue (acute) or a concept question (chronic/Drittes Fach)
  back   = Wesen -> Erstes Vorgehen -> Kernfakt -> Nie vergessen

Authored cards live in tools/kernprinzip.json (hand-written = the value). Every topic in the
content feed (api/topics.json) is covered: a topic WITHOUT an authored card is auto-DRAFTED from
its stations and flagged draft:true — so any NEW review (incl. new R3) shows up automatically and
just needs the 4 lines refined later.

Emits:
  - flashcards.html   DECK blob  (trainer schema {id,t,g,h,acute,q,a,m}; a = back as HTML)
  - api/deck.json     canonical content feed for the app  ({version,updatedAt,total,authored,drafts,cards:[...]})
Run AFTER tools/_build-content.py (it reads api/topics.json). The api/deck.json change needs a
Worker redeploy (cd api && npx wrangler deploy) to go live at /api/deck.
"""
import json, re, io, html, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = {  # specialty -> (display label, hue)  — mirrors the library groups
 'kardiologie':('Kardiologie',25), 'pneumologie':('Pneumologie',210),
 'chirurgie':('Allgemein- und Viszeralchirurgie',180), 'viszeralchirurgie':('Allgemein- und Viszeralchirurgie',180),
 'gastroenterologie':('Gastroenterologie',150), 'unfallchirurgie':('Unfallchirurgie',50),
 'drittes-fach':('Drittes Fach',18), 'notfallmedizin':('Notfallmedizin',255),
 'gefaesschirurgie':('Gefäßchirurgie',10), 'neurologie':('Neurologie',300),
 'endokrinologie':('Endokrinologie',330), 'haematologie':('Hämatologie',350),
}
def esc(s): return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def txt(b):
    b=re.sub(r'<[^>]+>',' ', b or ''); b=html.unescape(b); return re.sub(r'\s+',' ',b).strip()

# ---- 1. authored cards ----
authored = {c['slug']: c for c in json.load(io.open(os.path.join(ROOT,'tools/kernprinzip.json'),encoding='utf-8'))}

# ---- 2. every topic in the content feed (highest level per slug) ----
feed = json.load(io.open(os.path.join(ROOT,'api/topics.json'),encoding='utf-8'))
bytopic = {}
for t in feed['topics']:
    slug = re.sub(r'-r[0-9]+$','', t['id'])
    lvl  = int(re.sub(r'[^0-9]','', t['level']) or 0)
    if slug not in bytopic or lvl > bytopic[slug][0]:
        bytopic[slug] = (lvl, t)

def draft_from(t):
    """Auto-draft a card from a topic's stations (for topics without an authored card)."""
    st = t['stations']
    def body(x): return txt(x.get('body','') or '')
    g  = st.get('grundlagen',[]); th = st.get('therapie',[])
    allb = g + st.get('klinik',[]) + st.get('diagnostik',[]) + th
    w = next((body(x) for x in g if x.get('variant')=='fakt' and body(x)), '') or next((body(x) for x in g if body(x)),'')
    v = next((body(x) for x in th if body(x)), '')
    n = next((body(x) for x in allb if x.get('variant') in ('cave','warnung','critical') and body(x)), '')
    return {'slug':re.sub(r'-r[0-9]+$','',t['id']), 'title':t['title'], 'spec':t['specialty'], 'acute':False,
            'q': t['title'] + ' — Kernprinzip?', 'w':w[:240], 'v':v[:200], 'k':'', 'n':n[:200], 'draft':True}

cards_src = []
for slug,(lvl,t) in sorted(bytopic.items()):
    cards_src.append(authored[slug] if slug in authored else draft_from(t))

# authored cards whose topic isn't in the feed (shouldn't happen) — keep + warn
orphans = [s for s in authored if s not in bytopic]
for s in orphans: cards_src.append(authored[s])

# ---- 3. assemble trainer DECK + feed cards ----
def back_html(c):
    rows = [('Wesen', c['w']), ('Erstes Vorgehen', c['v'])]
    if c.get('k'): rows.append(('Kernfakt', c['k']))
    rows.append(('Nie vergessen', c['n']))
    out = '<div class="kp">'
    for i,(lbl,val) in enumerate(rows):
        cls = 'kpl kpn' if lbl=='Nie vergessen' else 'kpl'
        out += '<div class="%s"><span class="kpk">%s</span> %s</div>' % (cls, lbl, esc(val))
    return out + '</div>'

deck_trainer, deck_feed = [], []
for c in cards_src:
    label,hue = SPEC.get(c['spec'], (c['spec'].title(),200))
    cid = 'kp-' + c['slug']
    deck_trainer.append({'id':cid,'t':c['title'],'g':label,'h':hue,'acute':bool(c.get('acute')),
                         'q':c['q'],'a':back_html(c),'m':''})
    deck_feed.append({'id':cid,'slug':c['slug'],'topic':c['title'],'fach':label,'hue':hue,
                      'acute':bool(c.get('acute')),'draft':bool(c.get('draft')),
                      'front':c['q'],'back':{'wesen':c['w'],'vorgehen':c['v'],'kernfakt':c.get('k',''),'nieVergessen':c['n']}})

drafts = [c['slug'] for c in cards_src if c.get('draft')]
now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# ---- 4. patch flashcards.html DECK ----
fp = os.path.join(ROOT,'flashcards.html')
page = io.open(fp,encoding='utf-8').read()
blob = '/*DECK_START*/const DECK='+json.dumps(deck_trainer,ensure_ascii=False,separators=(',',':'))+';/*DECK_END*/'
page = re.sub(r'/\*DECK_START\*/.*?/\*DECK_END\*/', lambda m: blob, page, flags=re.S)
io.open(fp,'w',encoding='utf-8').write(page)

# ---- 5. write api/deck.json (the /api/deck feed) ----
feedobj = {'version':1,'updatedAt':now,'total':len(deck_feed),
           'authored':len(deck_feed)-len(drafts),'drafts':len(drafts),'cards':deck_feed}
io.open(os.path.join(ROOT,'api/deck.json'),'w',encoding='utf-8').write(json.dumps(feedobj,ensure_ascii=False,separators=(',',':')))

print('Kernprinzip deck: %d cards (%d authored, %d auto-draft)' % (len(deck_feed), len(deck_feed)-len(drafts), len(drafts)))
if drafts: print('  DRAFTS to refine later:', ', '.join(drafts))
if orphans: print('  WARNING authored-but-no-review:', ', '.join(orphans))
print('  -> flashcards.html DECK patched + api/deck.json written')
