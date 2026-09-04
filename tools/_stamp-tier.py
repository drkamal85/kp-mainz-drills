# -*- coding: utf-8 -*-
"""Setzt auf jeder Themenseite eine Tier-Marke in die Meta-Zeile.
KERN ab 100 Protokoll-Treffern (Ziel R5), STANDARD 50-99 (R4), RAND darunter (R2).
Zeigt zusaetzlich den Zielabstand. Idempotent - mehrfaches Laufen aendert nichts."""
import re,io,glob
k=io.open('tools/_build-master.py',encoding='utf-8').read()
PROT={m.group(6):int(m.group(3)) for m in re.finditer(r'\((\d+),(\d+),(\d+),"([^"]*)","([^"]*)",\s*"([a-z0-9-]+)"\)',k)}
def tier(p):
    if p>=100: return ('KERN','kern',5)
    if p>=50:  return ('STANDARD','std',4)
    return ('RAND','rand',2)
CSS='''
  /* Tier-Marke zusaetzlich in der Reiterleiste: der Kopfbereich scrollt weg,
     die Leiste bleibt haften - so ist das Ziel beim Lernen immer sichtbar. */
  .tier-sticky{margin-left:auto;align-self:center;display:inline-flex;align-items:center;gap:4px;
    font:700 9px/1 'Manrope',sans-serif;letter-spacing:.09em;text-transform:uppercase;
    padding:5px 8px;border-radius:5px;white-space:nowrap}
  .tier-sticky.kern{background:#FBE9E7;color:#B3261E}
  .tier-sticky.std{background:#FDF2E2;color:#B07214}
  .tier-sticky.rand{background:#EFEDE8;color:#7A736A}
  .tier-sticky .zt{font-weight:600;letter-spacing:.02em;text-transform:none;opacity:.85}
  @media(max-width:640px){
    /* kein margin-left auto - sonst landet die Marke allein in einer
       umgebrochenen Zeile und wird abgeschnitten. So fliesst sie als
       weitere Pille hinter den Reitern mit. */
    .tier-sticky{margin-left:0;font-size:8.5px;padding:5px 7px;order:99}
    .tier-sticky .zt{display:none}
  }
  .tier{display:inline-flex;align-items:center;gap:5px;font:700 9.5px/1 'Manrope',sans-serif;
    letter-spacing:.1em;text-transform:uppercase;padding:5px 9px;border-radius:4px}
  .tier.kern{background:#FBE9E7;color:#B3261E}
  .tier.std{background:#FDF2E2;color:#B07214}
  .tier.rand{background:#EFEDE8;color:#7A736A}
  .tier .zt{font-weight:600;letter-spacing:.02em;text-transform:none;opacity:.8}
'''
n=0; skip=0
for f in sorted(glob.glob('reviews/*/*.html')):
    slug=f.split('/')[-1][:-5]
    if slug not in PROT: skip+=1; continue
    t=io.open(f,encoding='utf-8').read()
    m=re.search(r'<div class="meta">(.*?)</div>',t,re.S)
    if not m: skip+=1; continue
    lv=re.search(r'<span>R(\d)</span>',m.group(1))
    lvl=int(lv.group(1)) if lv else 0
    name,cls,tgt=tier(PROT[slug])
    zt='Ziel erreicht' if lvl>=tgt else f'Ziel R{tgt}'
    # Marke NICHT mehr im Kopfbereich - der scrollt weg und sie stuende doppelt.
    body=re.sub(r'\s*<span class="tier [^"]*">.*?</span>\s*</span>','',m.group(1),flags=re.S)
    t=t[:m.start(1)]+body.rstrip()+'\n    '+t[m.end(1):]
    # zweite Marke in die haftende Reiterleiste
    t=re.sub(r'\s*<span class="tier-sticky [^"]*">.*?</span>\s*</span>','',t,flags=re.S)
    sticky=f'\n    <span class="tier-sticky {cls}">{name}<span class="zt">{zt}</span></span>'
    mt=re.search(r'(<div class="tabs">)(.*?)(\n\s*</div>)',t,re.S)
    if mt: t=t[:mt.end(2)]+sticky+t[mt.end(2):]
    # CSS immer erneuern, sonst bleiben alte Fassungen stehen
    t=re.sub(r'\n\s*/\* Tier-Marke zusaetzlich in der Reiterleiste.*?(?=</style>)','',t,flags=re.S)
    t=t.replace('</style>',CSS+'</style>',1)
    io.open(f,'w',encoding='utf-8').write(t); n+=1
print(f'  Tier-Marke: {n} Seiten gesetzt \u00b7 {skip} ohne Rangeintrag')
