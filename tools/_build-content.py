# -*- coding: utf-8 -*-
"""Build content/topics.json — the native-content feed for the mobile app.
Mirrors the index (one entry per shown review), id = review slug (matches the progress API).
Stations -> flat blocks (text|table|callout); plus perlen and fragen."""
import re, glob, json, io, html
from collections import OrderedDict

GROUPS = {
 'kardiologie':('Kardiologie',25),'pneumologie':('Pneumologie',210),'viszeralchirurgie':('Viszeralchirurgie',180),
 'chirurgie':('Viszeralchirurgie',180),'gastroenterologie':('Gastroenterologie',150),'unfallchirurgie':('Unfallchirurgie',50),
 'drittes-fach':('Drittes Fach',18),'notfallmedizin':('Notfallmedizin',255),'gefaesschirurgie':('Gefäßchirurgie',10),
 'neurologie':('Neurologie',300),'endokrinologie':('Endokrinologie',330),'haematologie':('Hämatologie',350),
}
STATION_KEYS = ['grundlagen','klinik','diagnostik','therapie']
VARIANT = {'critical':'cave','warning':'cave','fact':'fakt','pearl':'merksatz'}

def md(s):
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</li>\s*', '\n', s); s = re.sub(r'<li[^>]*>', '- ', s)
    s = re.sub(r'</(ul|ol)>', '\n', s); s = re.sub(r'<(ul|ol)[^>]*>', '', s)
    s = re.sub(r'<(strong|b)>', '**', s); s = re.sub(r'</(strong|b)>', '**', s)
    s = re.sub(r'<(em|i)>', '*', s); s = re.sub(r'</(em|i)>', '*', s)
    s = re.sub(r'<[^>]+>', '', s); s = html.unescape(s)
    lines = [re.sub(r'[ \t]+',' ',ln).strip() for ln in s.split('\n')]
    return '\n'.join([ln for ln in lines if ln]).strip()

def parse_table(tbl):
    rows = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', tbl, re.S):
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', tr, re.S)
        if cells: rows.append([md(c) for c in cells])
    return rows

def card_to_blocks(title, body_html):
    callouts = re.findall(r'<div class="callout (\w+)"><span class="(?:lab|callout-label)">(.*?)</span>(.*?)</div>', body_html, re.S)
    tables = re.findall(r'<table[^>]*>(.*?)</table>', body_html, re.S)
    prose_html = re.sub(r'<div class="callout \w+">.*?</div>', '', body_html, flags=re.S)
    prose_html = re.sub(r'<table[^>]*>.*?</table>', '', prose_html, flags=re.S)
    prose = md(prose_html)
    blocks = []
    if title or prose: blocks.append({'type':'text','title':title,'body':prose})
    for variant, lab, txt in callouts:
        blocks.append({'type':'callout','variant':VARIANT.get(variant,'fakt'),'title':md(lab),'body':md(txt)})
    for tbl in tables:
        rows = parse_table(tbl)
        if rows: blocks.append({'type':'table','title':title,'rows':rows})
    return blocks

def parse_stations(h):
    stations = {k: [] for k in STATION_KEYS}
    if 'data-panel=' in h:  # proto (R2/R3)
        for key in STATION_KEYS:
            pm = re.search(r'<section class="panel[^"]*" data-panel="'+key+r'">(.*?)</section>', h, re.S)
            if not pm: continue
            panel = pm.group(1)
            intro = re.search(r'<p class="panel-intro">(.*?)</p>', panel, re.S)
            if intro:
                t = md(intro.group(1))
                if t: stations[key].append({'type':'text','title':'','body':t})
            for cm in re.finditer(r'<details class="card[^"]*"[^>]*>(.*?)</details>', panel, re.S):
                inner = cm.group(1)
                tm = re.search(r'<span class="ctitle">(.*?)</span>', inner, re.S)
                bm = re.search(r'<div class="body">(.*)</div>\s*$', inner, re.S)
                stations[key].extend(card_to_blocks(md(tm.group(1)) if tm else '', bm.group(1) if bm else ''))
    else:  # v1 (R1) — sections in order
        secs = re.findall(r'<section class="station[^"]*"[^>]*>(.*?)</section>', h, re.S)
        for idx, sec in enumerate(secs[:4]):
            key = STATION_KEYS[idx]
            for ch in re.split(r'(?=<div class="card[ "])', sec):
                tm = re.search(r'<div class="card-title">(.*?)</div>', ch, re.S)
                if not tm: continue
                bm = re.search(r'<div class="card-body-inner">(.*)', ch, re.S)
                stations[key].extend(card_to_blocks(md(tm.group(1)), bm.group(1) if bm else ''))
    return stations

def parse_perlen(h):
    out = []
    for m in re.finditer(r'<div class="pearl"><div class="ph">⭐ Perle \d+ · (.*?)</div><div class="pt">(.*?)</div>(?:<div class="mn">(.*?)</div>)?</div>', h, re.S):
        p = {'stichwort': md(m.group(1)), 'prinzip': md(m.group(2))}
        mn = md(m.group(3)) if m.group(3) else ''
        mn = re.sub(r'^\**Merke:?\**\s*','',mn)
        if mn: p['merke'] = mn
        out.append(p)
    return out

def parse_fragen(h, spec_name):
    out = []
    pm = re.search(r'<section class="panel[^"]*" data-panel="protokoll">(.*?)</section>', h, re.S)
    if not pm: return out
    tag = 'MAINZ · ' + spec_name.upper()
    for chunk in re.split(r'(?=<div class="pk">)', pm.group(1)):
        if 'pk-akte' not in chunk: continue
        akte = re.search(r'<div class="pk-akte"><span class="lab">Fall</span>(.*?)</div>', chunk, re.S)
        fall = md(akte.group(1)) if akte else ''
        for q in re.finditer(r'<div class="pq"><div class="pq-frage">(.*?)</div><details class="reveal"><summary>Antwort</summary><div class="ans">(.*?)</div></details></div>', chunk, re.S):
            item = {'frage': md(q.group(1)), 'antwort': md(q.group(2)), 'tag': tag}
            if fall: item['fall'] = fall
            out.append(item)
    return out

# --- build from the index card list (so the feed == the library) ---
idx = io.open('index.html', encoding='utf-8').read()
cards = re.findall(r'<a class="card" href="(reviews/([a-z-]+)/([a-z0-9-]+-r(\d))\.html)" data-id="', idx)
specs = OrderedDict()
topics = []
for path, folder, slug, lvl in cards:
    h = io.open(path, encoding='utf-8').read()
    name, hue = GROUPS.get(folder, (folder.title(), 200))
    if folder not in specs: specs[folder] = {'id': folder, 'name': name, 'hue': hue}
    title = md(re.search(r'<h1>(.*?)</h1>', h, re.S).group(1))
    mm = re.search(r'(\d+)\s*Min', h)
    words = len(re.findall(r'\w+', re.sub(r'<[^>]+>',' ',h)))
    minutes = int(mm.group(1)) if mm else max(3, round(words/180))
    _st = parse_stations(h)
    _present = [k for k in ('grundlagen','klinik','diagnostik','therapie') if _st.get(k)]
    topics.append({
        'id': slug, 'title': title, 'specialty': folder, 'level': 'R'+lvl, 'minutes': minutes,
        'complete': len(_present) == 4, 'stationsPresent': _present,
        'stations': _st,
        'perlen': parse_perlen(h),
        'fragen': parse_fragen(h, name),
    })

feed = {'version': 1, 'updatedAt': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'specialties': list(specs.values()), 'topics': topics}
out = json.dumps(feed, ensure_ascii=False, separators=(',',':'))
io.open('content/topics.json','w',encoding='utf-8').write(out)
io.open('api/topics.json','w',encoding='utf-8').write(out)  # bundled into the kp-progress Worker (served at /api/content)

# report
print('topics:', len(topics), '| specialties:', len(specs), '| bytes:', len(out.encode()), '(', round(len(out.encode())/1024), 'KB )')
withf = sum(1 for t in topics if t['fragen']); withp = sum(1 for t in topics if t['perlen'])
print('with fragen:', withf, '| with perlen:', withp)
import collections
blk = collections.Counter(b['type'] for t in topics for k in t['stations'] for b in t['stations'][k])
print('station blocks:', dict(blk))
s = topics[[i for i,t in enumerate(topics) if t['id']=='synkope-r3'][0]]
print('--- sample synkope-r3 ---')
print('  grundlagen[0]:', json.dumps(s['stations']['grundlagen'][0], ensure_ascii=False)[:160])
print('  grundlagen[1]:', json.dumps(s['stations']['grundlagen'][1], ensure_ascii=False)[:160])
print('  perle[0]:', json.dumps(s['perlen'][0], ensure_ascii=False)[:140])
print('  frage[0]:', json.dumps(s['fragen'][0], ensure_ascii=False)[:200] if s['fragen'] else 'none')
