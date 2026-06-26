# -*- coding: utf-8 -*-
"""Regenerate the flashcard deck (DECK region in flashcards.html) from all R3 Rapid-Fire Q&A."""
import re,glob,json,hashlib,io,html
GROUPS={  # folder -> (label, oklch hue)
 'kardiologie':('Kardiologie',25),'pneumologie':('Pneumologie',210),'viszeralchirurgie':('Viszeralchirurgie',180),
 'gastroenterologie':('Gastroenterologie',150),'chirurgie':('Viszeralchirurgie',180),'unfallchirurgie':('Unfallchirurgie',50),'drittes-fach':('Drittes Fach',18),
 'notfallmedizin':('Notfallmedizin',255),'gefaesschirurgie':('Gefäßchirurgie',10),'neurologie':('Neurologie',300),
 'endokrinologie':('Endokrinologie',330),'haematologie':('Hämatologie',350),
}
def clean(s):
    s=re.sub(r'<[^>]+>','',s); s=html.unescape(s); return re.sub(r'\s+',' ',s).strip()
deck=[]
for f in sorted(glob.glob('reviews/**/*-r3.html',recursive=True)):
    h=io.open(f,encoding='utf-8').read()
    folder=re.search(r'reviews/([a-z-]+)/',f).group(1)
    label,hue=GROUPS.get(folder,(folder.title(),200))
    topic=clean(re.search(r'<h1>(.*?)</h1>',h,re.S).group(1))
    for m in re.finditer(r'<details class="sf"><summary>(.*?)</summary><div class="sfa">(.*?)</div></details>',h,re.S):
        q,a=clean(m.group(1)),clean(m.group(2))
        if len(q)<3 or len(a)<1: continue
        cid=hashlib.md5((topic+'|'+q).encode()).hexdigest()[:10]
        deck.append({'id':cid,'t':topic,'g':label,'h':hue,'q':q,'a':a})
# stats
from collections import Counter
bygrp=Counter(c['g'] for c in deck); bytop=Counter(c['t'] for c in deck)
print("total cards:",len(deck),"| topics:",len(bytop),"| groups:",len(bygrp))
print("per group:",dict(bygrp))
print("sample card:",json.dumps(deck[0],ensure_ascii=False))
print("dup ids:",len(deck)-len(set(c['id'] for c in deck)))
# write deck into flashcards.html if it exists (between markers), else dump json
blob='/*DECK_START*/const DECK='+json.dumps(deck,ensure_ascii=False,separators=(',',':'))+';/*DECK_END*/'
import os
if os.path.exists('flashcards.html'):
    page=io.open('flashcards.html',encoding='utf-8').read()
    page=re.sub(r'/\*DECK_START\*/.*?/\*DECK_END\*/',blob.replace('\\','\\\\'),page,flags=re.S)
    io.open('flashcards.html','w',encoding='utf-8').write(page)
    print("flashcards.html DECK updated:",len(deck),"cards")
else:
    io.open('/tmp/deck.json','w',encoding='utf-8').write(json.dumps(deck,ensure_ascii=False))
    print("(flashcards.html not yet created — deck dumped to /tmp/deck.json)")
