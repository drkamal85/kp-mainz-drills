# -*- coding: utf-8 -*-
"""Regenerate the flashcard deck (DECK in flashcards.html) from the KP-Perlen of every R3.
Perlen = curated high-yield principles (each with a Merke), NOT the full Rapid-Fire recall set.
Card: q=Perle-Stichwort, a=Prinzip (explanation), m=Merke."""
import re,glob,json,hashlib,io,html
GROUPS={
 'kardiologie':('Kardiologie',25),'pneumologie':('Pneumologie',210),'viszeralchirurgie':('Viszeralchirurgie',180),
 'chirurgie':('Viszeralchirurgie',180),'gastroenterologie':('Gastroenterologie',150),'unfallchirurgie':('Unfallchirurgie',50),
 'drittes-fach':('Drittes Fach',18),'notfallmedizin':('Notfallmedizin',255),'gefaesschirurgie':('Gefäßchirurgie',10),
 'neurologie':('Neurologie',300),'endokrinologie':('Endokrinologie',330),'haematologie':('Hämatologie',350),
}
def clean(s):
    s=re.sub(r'<br\s*/?>',' · ',s)            # keep <br> separations readable
    s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
    s=re.sub(r'\s*·\s*',' · ',s)              # normalise bullet spacing
    return re.sub(r'\s+',' ',s).strip(' ·')
deck=[]
for f in sorted(glob.glob('reviews/**/*.html',recursive=True)):
    h=io.open(f,encoding='utf-8').read()
    folder=re.search(r'reviews/([a-z-]+)/',f).group(1)
    label,hue=GROUPS.get(folder,(folder.title(),200))
    topic=clean(re.search(r'<h1>(.*?)</h1>',h,re.S).group(1))
    for m in re.finditer(r'<div class="pearl"><div class="ph">⭐ Perle \d+ · (.*?)</div><div class="pt">(.*?)</div><div class="mn">(.*?)</div></div>',h,re.S):
        title,expl,mn=clean(m.group(1)),clean(m.group(2)),clean(m.group(3))
        mn=re.sub(r'^Merke:\s*','',mn)
        if len(title)<2 or len(expl)<3: continue
        cid=hashlib.md5((topic+'|'+title).encode()).hexdigest()[:10]
        deck.append({'id':cid,'t':topic,'g':label,'h':hue,'q':title,'a':expl,'m':mn})
from collections import Counter
bytop=Counter(c['t'] for c in deck)
print("PERLEN cards:",len(deck),"| topics:",len(bytop),"| avg/topic:",round(len(deck)/max(len(bytop),1),1),"| range",min(bytop.values()),"-",max(bytop.values()))
print("dup ids:",len(deck)-len(set(c['id'] for c in deck)))
for c in deck[:3]: print("   Q:",repr(c['q']),"| A:",repr(c['a'][:60]),"| M:",repr(c['m'][:45]))
blob='/*DECK_START*/const DECK='+json.dumps(deck,ensure_ascii=False,separators=(',',':'))+';/*DECK_END*/'
import os
if os.path.exists('flashcards.html'):
    page=io.open('flashcards.html',encoding='utf-8').read()
    page=re.sub(r'/\*DECK_START\*/.*?/\*DECK_END\*/',lambda m:blob,page,flags=re.S)
    io.open('flashcards.html','w',encoding='utf-8').write(page)
    print("flashcards.html DECK updated:",len(deck),"cards")
