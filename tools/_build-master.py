# -*- coding: utf-8 -*-
# Master-Themenliste builder — FLAT single ranking by Korpus-Treffer (chat+prot mentions).
# RUN FROM REPO ROOT:  python3 tools/_build-master.py
# Re-globs reviews/ for live R-levels; review column + analytics read LIVE from the repo.
# Topic universe/frequencies mirror KP-Master-Themenliste.md (88 topics, project knowledge).
import io
import os as _os, glob, re

repo={}
_idx=io.open('index.html',encoding='utf-8').read()
for path,_fl,slug,lvl in re.findall(r'<a class="card" href="(reviews/([a-z-]+)/([a-z0-9-]+)\.html)" data-id="[a-z0-9-]+" data-lvl="(\d)"', _idx):
    repo[slug]=(int(lvl),path)

# Topics that completed the R4 audio drill (activity-only tier — no separate file by design,
# so this can't be glob-detected like R1-R3). Badge/level display ONLY: repo[slug][1] (the real
# file path) and reviewId always still resolve to the actual highest file (r3), never a fake r4.
R4_TOPICS={"distale-radiusfraktur","schock","copd","lungenembolie","cholezystitis","appendizitis","ileus","wirbelsaeulenverletzungen","allgemeine-frakturlehre","polytrauma-abcde","leistenhernie","pleuraerguss","asthma-bronchiale","tvt","hypothyreose","hyperthyreose","ikterus-cholestase","proximale-femurfraktur","leberzirrhose","beckenringfrakturen","sprunggelenksfraktur","pneumothorax","pneumonie","aortendissektion","schaedel-hirn-trauma","cushing-syndrom","schilddruesenkarzinom","sepsis","schlaganfall","impfungen-stiko","eisenmangelanaemie","synkope","infektioese-endokarditis","arterielle-hypertonie","herzklappenerkrankungen","notfallpharmakologie","acs-myokardinfarkt","khk","herzinsuffizienz","morbus-crohn","cml","diabetes-mellitus","akute-leukaemien","aufklaerung-einwilligung-betreuung","strahlenschutz","av-block","vorhofflimmern","rechtsmedizin","humerusfraktur", "gi-blutung", "non-hodgkin-lymphome"}
def _badge_lvl(slug,filelvl): return 4 if slug in R4_TOPICS else filelvl

# --- Ziel-Stufen nach Protokollpraesenz (prot = 3. Wert der FLAT-Zeile) -------------
# prot >= 100 -> KERN     Ziel R5
# prot 50-99  -> STANDARD Ziel R4
# prot < 100  -> RAND     Ziel R2
def ziel_tier(prot):
    if prot >= 100: return ("KERN", 5, "kern")
    if prot >= 50:  return ("STANDARD", 4, "std")
    return ("RAND", 2, "rand")

# Hat die Seite einen Tab 6 (Fragen & Protokolle)?
_hasq={}
for _f in glob.glob('reviews/*/*.html'):
    _s=_f.split('/')[-1][:-5]
    try: _hasq[_s] = 'Fragen &amp; Protokolle' in io.open(_f,encoding='utf-8').read()
    except: _hasq[_s]=False

# Eingefaltete Themen: kein eigenes Deck, Inhalt lebt im Zieldeck
FOLDED={
 "allgemeine-frakturlehre": ["Kompartmentsyndrom"],
 "reanimation-cpr":         ["Ventr. Tachykardie / Kammerflimmern"],
 "vorhofflimmern":          ["Paroxysmale SVT / AVNRT-AVRT"],
 "schaedel-hirn-trauma":    ["Hirnblutungen (EDH/SDH/SAB/ICB)"],
}

DRILL={"Rechtsmedizin / Leichenschau"}
def esc(s): return s.replace('&','&amp;')
def trow(rank, treffer, chat, prot, fach, thema, slug, force_tier=False):
    info=repo.get(slug); badges=""; done=""; topic=esc(thema)
    tname,tgt,tcls = ziel_tier(prot)
    lvl = _badge_lvl(slug, info[0]) if info else 0
    if info:
        _l,path=info; topic=f'<a href="../{path}">{esc(thema)}</a>'
        badges+=f'<span class="have">\u2713 R{lvl}</span>'; done=" done"
    if thema in DRILL: badges+='<span class="have drill">Drill</span>'
    for _f in FOLDED.get(slug,[]):
        badges+=f'<span class="fold" title="eingefaltet, kein eigenes Deck">+ {esc(_f)}</span>'
    # Zielspalte
    if not treffer and not force_tier:
        zi='<span class="zi-none">\u00b7</span>'
    elif lvl>tgt:
        zi=f'<span class="zi-over">R{lvl} \u00b7 \u00fcber Ziel</span>'
    elif lvl==tgt:
        zi='<span class="zi-ok">Ziel erreicht</span>'
    else:
        zi=f'<span class="zi-gap">R{lvl if lvl else 0} \u2192 R{tgt}</span>'
    if tgt>=4 and info and not _hasq.get(slug,False):
        zi+='<span class="zi-deck" title="Kern/Standard ohne Tab 6">DECK</span>'
    tb=f'<span class="tier-b {tcls}">{tname}</span>' if (treffer or force_tier) else ''
    rk=f'<td class="rk">{rank}</td>' if rank else '<td class="rk">\u00b7</td>'
    cnt=f'<span class="n">{treffer}</span><span class="src">{chat}\u00b7{prot}</span>' if treffer else '<span class="src">gebaut</span>'
    return (f'<tr class="{done.strip()}" data-topic="{esc(thema)}" data-tier="{tcls}"><td class="chk"><span class="box"></span></td>'
            f'{rk}<td class="topic">{topic}{badges}</td><td class="fach">{esc(fach)}{tb}</td>'
            f'<td class="ziel">{zi}</td><td class="cnt">{cnt}</td></tr>')

# FLAT ranking (treffer, chat, prot, fach, thema, slug) — rank = position
FLAT=[
(381,122,259,"Allgemein- und Viszeralchirurgie","Cholezystitis / Cholelithiasis","cholezystitis"),
(396,130,223,"Kardiologie","Vorhofflimmern","vorhofflimmern"),
(327,66,261,"Kardiologie","Herzinsuffizienz","herzinsuffizienz"),
(304,72,232,"Notfallmedizin","Schock","schock"),
(298,88,210,"Allgemein- und Viszeralchirurgie","Ileus","ileus"),
(296,56,240,"Notfallmedizin","Sepsis & septischer Schock","sepsis"),
(282,103,179,"Drittes Fach","Bluttransfusion","bluttransfusion"),
(279,90,189,"Drittes Fach","Anästhesie & Atemwegssicherung","anaesthesie-atemweg"),
(278,74,204,"Endokrinologie","Diabetes mellitus","diabetes-mellitus"),
(264,98,166,"Drittes Fach","Impfungen / STIKO","impfungen-stiko"),
(255,84,171,"Pneumologie","Pneumothorax","pneumothorax"),
(244,78,166,"Neurologie","Schlaganfall / Apoplex","schlaganfall"),
(243,44,199,"Gastroenterologie","Ikterus & Cholestase","ikterus-cholestase"),
(241,43,198,"Nephrologie","Nierenversagen (akut / akut-auf-chron.)","nierenversagen"),
(236,79,157,"Allgemein- und Viszeralchirurgie","GI-Blutung","gi-blutung"),
(234,61,173,"Pneumologie","Pneumonie","pneumonie"),
(232,58,174,"Kardiologie","ACS / Myokardinfarkt","acs-myokardinfarkt"),
(226,78,148,"Allgemein- und Viszeralchirurgie","Leistenhernie / Hernien","leistenhernie"),
(224,118,106,"Drittes Fach","Rechtsmedizin / Leichenschau","rechtsmedizin"),
(220,76,144,"Angiologie","Lungenembolie","lungenembolie"),
(218,88,130,"Allgemein- und Viszeralchirurgie","Gastroduodenales Ulkus","gastroduodenales-ulkus"),
(212,79,133,"Unfallchirurgie","Proximale Femurfraktur","proximale-femurfraktur"),
(203,74,129,"Allgemein- und Viszeralchirurgie","Pankreatitis","pankreatitis"),
(203,68,135,"Allgemein- und Viszeralchirurgie","Divertikulitis","divertikulitis"),
(171,46,125,"Gastroenterologie","Leberzirrhose","leberzirrhose"),
(169,54,115,"Allgemein- und Viszeralchirurgie","Appendizitis","appendizitis"),
(155,42,113,"Kardiologie","AV-Block","av-block"),
(151,61,90,"Hämatologie","Eisenmangelanämie","eisenmangelanaemie"),
(151,18,133,"Gastroenterologie","Hepatitis","hepatitis"),
(143,42,101,"Allgemein- und Viszeralchirurgie","Kolonkarzinom","kolonkarzinom"),
(142,16,126,"Kardiologie","KHK / Koronarsyndrom","khk"),
(132,39,93,"Gastroenterologie","Lebermetastasen / Lebertumor","lebertumoren"),
(131,82,49,"Drittes Fach","Strahlenschutz","strahlenschutz"),
(130,31,99,"Pneumologie","COPD","copd"),
(127,44,83,"Unfallchirurgie","Sprunggelenksfraktur (OSG)","sprunggelenksfraktur"),
(122,39,83,"Endokrinologie","Hyperthyreose","hyperthyreose"),
(120,40,80,"Unfallchirurgie","Hüft- / Knie-TEP","hueft-knie-tep"),
(120,36,84,"Gastroenterologie","Gastritis (Typ A/B/C)","gastritis"),
(119,31,88,"Drittes Fach","Sozialrecht & Hygiene","sozialrecht-hygiene"),
(117,24,93,"Angiologie","pAVK","pavk"),
(111,37,74,"Angiologie","Tiefe Beinvenenthrombose (TVT)","tvt"),
(108,35,73,"Kardiologie","Arterielle Hypertonie","arterielle-hypertonie"),
(102,15,87,"Pneumologie","Asthma bronchiale","asthma-bronchiale"),
(100,35,65,"Pneumologie","Bronchialkarzinom","bronchialkarzinom"),
(95,18,77,"Kardiologie","Synkope","synkope"),
(93,40,53,"Unfallchirurgie","Distale Radiusfraktur","distale-radiusfraktur"),
(93,30,63,"Drittes Fach","Schmerztherapie / WHO-Schema","schmerztherapie"),
(92,30,62,"Notfallmedizin","Akuttoxikologie / Intoxikation","akuttoxikologie"),
(91,15,76,"Hämatologie","Akute Leukämien (ALL)","akute-leukaemien"),
(89,37,52,"Drittes Fach","Aufklärung, Einwilligung & Betreuung","aufklaerung-einwilligung-betreuung"),
(87,17,70,"Endokrinologie","Osteoporose","osteoporose"),
(87,6,81,"Hämatologie","Non-Hodgkin-Lymphom (NHL)","non-hodgkin-lymphome"),
(136,21,115,"Gastroenterologie","Morbus Crohn & Colitis ulcerosa","morbus-crohn"),
(83,26,57,"Kardiologie","Herzklappenerkrankungen","herzklappenerkrankungen"),
(82,16,66,"Endokrinologie","Hypothyreose","hypothyreose"),
(139,27,54,"Unfallchirurgie","Schädel-Hirn-Trauma","schaedel-hirn-trauma"),
(81,22,59,"Pneumologie","Tuberkulose","tuberkulose"),
(81,16,65,"Unfallchirurgie","Polytrauma / ABCDE (Sturz)","polytrauma-abcde"),
(81,24,57,"Allgemein- und Viszeralchirurgie","Milzruptur / Splenektomie","milzruptur-splenektomie"),
(77,37,40,"Drittes Fach","Borreliose / FSME / Zeckenbiss","borreliose-fsme"),
(168,29,47,"Notfallmedizin","Reanimation / CPR","reanimation-cpr"),
(73,11,62,"Angiologie","Aortendissektion","aortendissektion"),
(142,12,56,"Unfallchirurgie","Allgemeine Frakturlehre","allgemeine-frakturlehre"),
(67,12,55,"Nephrologie","Harnwegsinfekt / Pyelonephritis","harnwegsinfekt"),
(65,22,43,"Endokrinologie","Schilddrüsenkarzinom","schilddruesenkarzinom"),
(64,29,35,"Allgemein- und Viszeralchirurgie","Akutes Abdomen","akutes-abdomen"),
(63,25,38,"Notfallmedizin","Anaphylaxie","anaphylaxie"),
(62,15,47,"Allgemein- und Viszeralchirurgie","Rektumkarzinom","rektumkarzinom"),
(60,15,45,"Unfallchirurgie","Humerusfraktur","humerusfraktur"),
(59,11,48,"Gastroenterologie","GERD / Refluxkrankheit","gerd"),
(59,7,52,"Kardiologie","Infektiöse Endokarditis","infektioese-endokarditis"),
(57,17,40,"Gastroenterologie","Diarrhoe / Gastroenteritis","diarrhoe"),
(56,15,41,"Allgemein- und Viszeralchirurgie","Pankreaskarzinom","pankreaskarzinom"),
(56,11,45,"Allgemein- und Viszeralchirurgie","Hämorrhoiden","haemorrhoiden"),
(55,11,44,"Allgemein- und Viszeralchirurgie","Magenkarzinom","magenkarzinom"),
(55,9,46,"Hämatologie","Morbus Hodgkin","morbus-hodgkin"),
(54,19,35,"Notfallmedizin","Verbrennung","verbrennung"),
(49,10,39,"Unfallchirurgie","Claviculafraktur","claviculafraktur"),
(47,8,39,"Endokrinologie","Struma","struma"),
(43,13,30,"Querschnitt","Check-up / Prävention","praevention"),
(40,10,30,"Angiologie","Aortenaneurysma (AAA)","aortenaneurysma"),
(40,7,33,"Unfallchirurgie","Beckenringfrakturen","beckenringfrakturen"),
(37,12,25,"Notfallmedizin","Delir","delir"),
(32,5,27,"Endokrinologie","Cushing-Syndrom","cushing-syndrom"),
(32,9,23,"Nephrologie","Hyponatriämie / SIADH","hyponatriaemie-siadh"),
(30,0,30,"Unfallchirurgie","Kreuzbandruptur","kreuzbandruptur"),
(23,3,20,"Unfallchirurgie","Wirbelsäulenverletzungen","wirbelsaeulenverletzungen"),
(62,22,40,"Neurologie","Meningitis / Enzephalitis","meningitis"),
]
EXTRA=[("Notfallmedizin","Pleuraerguss","pleuraerguss"),("Notfallmedizin","Notfallpharmakologie","notfallpharmakologie")]

# rank + tier split
FLAT.sort(key=lambda r:-r[0])  # keep ranking correct after additions
ranked=[(i+1,)+row for i,row in enumerate(FLAT)]
def tier(lo,hi): return [r for r in ranked if lo<=r[1]<hi]   # r[1]=treffer
# Gruppierung nach Ziel-Tier (prot = r[4])
TK=[r for r in ranked if r[3]>=100]; TS=[r for r in ranked if 50<=r[3]<100]; TR=[r for r in ranked if r[3]<50]
covered=lambda s: bool(s) and s in repo
def tc(T): return sum(1 for r in T if covered(r[6])), len(T)  # r[6]=slug
tkc,tkn=tc(TK); tsc,tsn=tc(TS); trc,trn=tc(TR)
n_md=len(FLAT); md_cov=sum(1 for r in ranked if covered(r[6])); cov_pct=round(md_cov/n_md*100)
nr={3:0,2:0,1:0}
for lvl,_ in repo.values(): nr[lvl]=nr.get(lvl,0)+1
gaps=[(t,th,f) for rk,t,c,p,f,th,s in ranked if not covered(s)][:6]
fab={"Allgemein- und Viszeralchirurgie":"Viszeralchir.","Unfallchirurgie":"Unfallchir.","Endokrinologie":"Endokrin.","Kardiologie":"Kardio.","Gastroenterologie":"Gastro.","Angiologie":"Angio.","Notfallmedizin":"Notfall","Pneumologie":"Pneumo.","Hämatologie":"Häm.","Nephrologie":"Nephro.","Neurologie":"Neuro.","Drittes Fach":"Drittes Fach","Querschnitt":"Querschnitt"}

def section(tc_,title,desc,count,rows):
    return (f'<section class="tier" style="--tc:{tc_}"><div class="tier-head"><div><div class="tier-title">{title}</div>'
            f'<div class="tier-desc">{desc}</div></div><div class="tier-count">{count}</div></div>'
            f'<table><tbody>{rows}</tbody></table></section>')
def rowsfor(T): return "".join(trow(rk,t,c,p,f,th,s) for rk,t,c,p,f,th,s in T)
sK=section("#B3261E","KERN \u00b7 Ziel R5","ab 100 Protokoll-Treffer \u2014 muss bis zur Pr\u00fcfung sitzen",f"{tkn} Themen",rowsfor(TK))
sS=section("#B07214","STANDARD \u00b7 Ziel R4","50 bis 99 Protokoll-Treffer \u2014 sicher beherrschen",f"{tsn} Themen",rowsfor(TS))
sR=section("#7A736A","RAND \u00b7 Ziel R2","unter 50 Protokoll-Treffer \u2014 kennen, nicht vertiefen",f"{trn} Themen",rowsfor(TR))
sE=section("#2D7A3E","Weitere gebaute Reviews","In der Library vorhanden, aber nicht in der Korpus-Rangliste",f"{len(EXTRA)} Themen","".join(trow(None,0,0,0,f,th,s,force_tier=True) for f,th,s in EXTRA))

# --- Ziel-Erreichung je Tier (KERN/STANDARD/RAND) ------------------------------
def _lvl_of(slug):
    inf=repo.get(slug)
    return _badge_lvl(slug,inf[0]) if inf else 0
_ZT={"kern":[0,0,0],"std":[0,0,0],"rand":[0,0,0]}   # [am Ziel, offen, ueber Ziel]
for _rk,_t,_c,_p,_f,_th,_s in ranked:
    _n,_tg,_cl=ziel_tier(_p)
    _l=_lvl_of(_s); _ZT[_cl][2 if _l>_tg else (0 if _l==_tg else 1)]+=1
for _f,_th,_s in EXTRA:                        # EXTRA zaehlt als RAND, Ziel R2
    _l=_lvl_of(_s); _ZT["rand"][2 if _l>2 else (0 if _l==2 else 1)]+=1
_ZTOT=[sum(v[i] for v in _ZT.values()) for i in (0,1,2)]
def _zrow(lbl,cls,tgt,v):
    ges=sum(v); pct=round((v[0]+v[2])/ges*100) if ges else 0
    return (f'<tr><td><span class="tier-b {cls}">{lbl}</span></td><td class="zt-t">Ziel R{tgt}</td>'
            f'<td class="zt-n">{ges}</td><td class="zt-n zt-ok">{v[0]}</td><td class="zt-n zt-ov">{v[2]}</td><td class="zt-n zt-of">{v[1]}</td>'
            f'<td class="zt-bar"><div class="zb"><div class="zf" style="width:{pct}%"></div></div><span class="zp">{pct}\u00a0%</span></td></tr>')
zieltab=('<section class="zieltab"><div class="zt-h">Ziel-Stufen \u00b7 Stand</div>'
    '<table><thead><tr><th>Tier</th><th>Ziel</th><th>Themen</th><th>am Ziel</th><th>\u00fcber Ziel</th><th>offen</th><th></th></tr></thead><tbody>'
    +_zrow("KERN","kern",5,_ZT["kern"])+_zrow("STANDARD","std",4,_ZT["std"])+_zrow("RAND","rand",2,_ZT["rand"])
    +f'<tr class="zt-sum"><td colspan="2">Gesamt</td><td class="zt-n">{sum(_ZTOT)}</td>'
     f'<td class="zt-n zt-ok">{_ZTOT[0]}</td><td class="zt-n zt-ov">{_ZTOT[2]}</td><td class="zt-n zt-of">{_ZTOT[1]}</td><td></td></tr>' 
    +'</tbody></table></section>')


def bar(label,c,n,col):
    pct=round(c/n*100) if n else 0
    return f'<div class="ana-tier" style="--tcc:{col}"><span class="ana-tl">{label}</span><div class="bar"><div class="fill" style="width:{pct}%"></div></div><span class="ana-tc">{c} / {n}</span></div>'
gaps_html="".join(f'<div class="gap"><span class="gap-n">{t}</span><span class="gap-t">{esc(th)}</span><span class="gap-f">{fab.get(f,f)}</span></div>' for t,th,f in gaps)
analytics=f'''<section class="analytics">
  <div class="ana-grid">
    <div class="ana-card"><div class="ana-n">{n_md}</div><div class="ana-l">Themen · Inventar</div></div>
    <div class="ana-card"><div class="ana-n">{len(repo)}</div><div class="ana-l">Reviews live</div></div>
    <div class="ana-card"><div class="ana-n">{cov_pct}<span style="font-size:18px"> %</span></div><div class="ana-l">abgedeckt</div></div>
    <div class="ana-card"><div class="ana-n">{tkc}<span style="font-size:18px"> / {tkn}</span></div><div class="ana-l">Kern-Themen abgedeckt</div></div>
  </div>
  <div class="ana-strip">Review-Reife · <b>{nr[3]}</b>×R3 · <b>{nr[2]}</b>×R2 · <b>{nr[1]}</b>×R1 · +{len(EXTRA)} außerhalb der Liste &nbsp;·&nbsp; <span id="prog">0 abgehakt</span></div>
  <div class="ana-sub">
    <div class="ana-box"><div class="ana-box-h">Abdeckung nach Ziel-Tier</div>
      {bar("Kern",tkc,tkn,"#B3261E")}{bar("Standard",tsc,tsn,"#B07214")}{bar("Rand",trc,trn,"#7A736A")}
    </div>
    <div class="ana-box"><div class="ana-box-h">Größte Lücken · höchste Korpus-Präsenz, kein Review <span style="font-weight:400;text-transform:none;letter-spacing:0">(s. Hinweis)</span></div>{gaps_html}</div>
  </div>
</section>'''

caveat='''<div class="caveat"><b>Hinweis zur Kennzahl.</b> Dies ist <b>Erwähnungs-Häufigkeit</b> (Korpus-Treffer), nicht Fall-Häufigkeit. Begriffe, die als Befund oder Therapie innerhalb vieler Fälle vorkommen, ranken höher als ihre Eigenständigkeit — v. a. Bluttransfusion, Ikterus/Cholestase, Gastroduodenales Ulkus, Rechtsmedizin, Hepatitis, Lymphom. Umgekehrt ranken klassische Einzelfälle wie Distale Radiusfraktur oder Cushing niedriger, als sie geprüft werden. Für reine <b>Lern-Priorität</b> bleibt die fallzahl-basierte Sicht die bessere Quelle; diese flache Liste ist v. a. ein einziges, scannbares Gesamt-Inventar.</div>'''

html=f'''<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KP Mainz · Master-Themenliste</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,500;0,600;1,400&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FBFAF7;--ink:#1A1A1A;--muted:#6B6B6B;--soft:#9A9A9A;--rule:#E6E2D9;--paper:#fff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:Manrope,sans-serif;font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}}
.container{{max-width:790px;margin:0 auto;padding:56px 22px 90px}}
.back{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#9A9A9A;text-decoration:none;margin-bottom:22px}}
.kicker{{font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--soft);margin-bottom:16px}}
h1{{font-family:Fraunces,serif;font-weight:500;font-size:clamp(32px,6vw,46px);line-height:1.02;letter-spacing:-.02em;margin-bottom:14px}}
.lede{{font-family:Fraunces,serif;font-size:17px;color:var(--muted);max-width:570px;margin-bottom:16px}}
.caveat{{font-size:12.5px;line-height:1.55;color:var(--muted);background:#FDF8EF;border:1px solid #EAD9BC;border-left:3px solid #D97706;border-radius:9px;padding:13px 15px;margin-bottom:24px}}
.caveat b{{color:var(--ink)}}
.analytics{{margin-top:8px}}
.ana-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px}}
.ana-card{{background:var(--paper);border:1px solid var(--rule);border-radius:12px;padding:17px 14px;text-align:center}}
.ana-n{{font-family:Fraunces,serif;font-weight:600;font-size:31px;line-height:1;color:var(--ink)}}
.ana-l{{font-size:10px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--soft);margin-top:8px}}
.ana-strip{{font-size:12px;color:var(--muted);background:var(--paper);border:1px solid var(--rule);border-radius:9px;padding:9px 14px;margin-bottom:18px}}
.ana-strip b{{color:var(--ink);font-family:'JetBrains Mono',monospace}}
.ana-sub{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.ana-box{{background:var(--paper);border:1px solid var(--rule);border-radius:12px;padding:16px 18px}}
.ana-box-h{{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:13px}}
.ana-tier{{display:flex;align-items:center;gap:10px;margin-bottom:10px;font-size:12.5px}}
.ana-tier:last-child{{margin-bottom:0}}
.ana-tl{{width:46px;color:var(--ink);font-weight:600}}
.bar{{flex:1;height:7px;background:var(--rule);border-radius:4px;overflow:hidden}}
.bar .fill{{height:100%;border-radius:4px;background:var(--tcc)}}
.ana-tc{{width:44px;text-align:right;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted)}}
.gap{{display:flex;align-items:baseline;gap:10px;padding:7px 0;border-bottom:1px solid var(--rule)}}
.gap:last-child{{border-bottom:none;padding-bottom:0}}
.gap-n{{font-family:'JetBrains Mono',monospace;font-weight:600;color:#C0392B;min-width:30px;font-size:13px}}
.gap-t{{font-family:Fraunces,serif;font-weight:500;flex:1;font-size:14px}}
.gap-f{{font-size:10.5px;color:var(--soft);white-space:nowrap}}
.tier{{margin-top:40px}}
.tier-head{{display:flex;justify-content:space-between;align-items:flex-end;border-left:3px solid var(--tc);padding-left:13px;margin-bottom:10px}}
.tier-title{{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--tc)}}
.tier-desc{{font-family:Fraunces,serif;font-style:italic;font-size:13.5px;color:var(--muted);margin-top:3px}}
.tier-count{{font-size:11.5px;color:var(--soft);white-space:nowrap}}
table{{width:100%;border-collapse:collapse}}
td{{padding:10px 8px;border-bottom:1px solid var(--rule);vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:rgba(0,0,0,.014)}}
.chk{{width:24px}}
.rk{{width:30px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--soft);text-align:right}}
.box{{display:inline-block;width:16px;height:16px;border:1.5px solid var(--soft);border-radius:4px;vertical-align:middle;cursor:pointer;transition:.15s}}
.box.checked{{background:var(--ink);border-color:var(--ink);position:relative}}
.box.checked::after{{content:"✓";color:#fff;font-size:12px;font-weight:700;position:absolute;top:-1px;left:2px}}
.topic{{font-family:Fraunces,serif;font-size:15.5px;font-weight:500}}
.topic a{{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}}
.topic a:hover{{border-bottom-color:var(--ink)}}
tr.done .topic a,tr.done .topic{{color:var(--soft)}}
.have{{display:inline-block;font-family:Manrope;font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#2D7A3E;background:#E3F1E6;padding:2px 6px;border-radius:3px;margin-left:8px;vertical-align:middle}}
.have.drill{{color:#5B53B0;background:#ECEAF8}}
.fach{{font-size:12px;color:var(--muted);white-space:nowrap}}
.cnt{{text-align:right;white-space:nowrap}}
.cnt .n{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:14px;color:var(--tc)}}
.cnt .src{{display:block;font-size:10px;color:var(--soft);font-family:'JetBrains Mono',monospace}}
.legend{{margin-top:38px;padding:16px;background:var(--paper);border:1px solid var(--rule);border-radius:10px;font-size:13px;color:var(--muted)}}
.legend b{{color:var(--ink)}}
.foot{{margin-top:48px;padding-top:18px;border-top:1px solid var(--rule);font-size:11.5px;color:var(--soft);text-align:center}}
@media(max-width:560px){{.container{{padding:36px 15px}}.fach{{display:none}}.ana-grid{{grid-template-columns:1fr 1fr}}.ana-sub{{grid-template-columns:1fr}}}}

.tier-b{{display:inline-block;margin-left:7px;font:700 8.5px/1 Manrope,sans-serif;letter-spacing:.09em;
  padding:3px 6px;border-radius:3px;vertical-align:middle;text-transform:uppercase}}
.tier-b.kern{{background:#FBE9E7;color:#B3261E}}
.tier-b.std{{background:#FDF2E2;color:#B07214}}
.tier-b.rand{{background:#EFEDE8;color:#7A736A}}
td.ziel{{white-space:nowrap;text-align:right;padding-right:12px}}
.zi-ok{{font:600 11px/1 Manrope,sans-serif;color:#2D7A3E}}
.zi-gap{{font:600 11px/1 'JetBrains Mono',monospace;color:#B07214}}
.zi-none{{color:#C9C3B8}}
.zi-deck{{display:inline-block;margin-left:6px;font:700 8.5px/1 Manrope,sans-serif;letter-spacing:.08em;
  padding:3px 5px;border-radius:3px;background:#B3261E;color:#fff}}
.fold{{display:inline-block;margin-left:6px;font:600 9.5px/1 Manrope,sans-serif;color:#5C5C5C;
  background:#EFEDE8;border-radius:3px;padding:3px 6px}}

.zieltab{{margin:26px 0 30px}}
.zt-h{{font:700 10px/1 Manrope,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8A8375;margin-bottom:10px}}
.zieltab table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E8E2D6;border-radius:6px;overflow:hidden}}
.zieltab th{{font:700 9.5px/1 Manrope,sans-serif;letter-spacing:.09em;text-transform:uppercase;color:#8A8375;
  text-align:right;padding:9px 12px;border-bottom:1px solid #E8E2D6;background:#FBF9F5}}
.zieltab th:first-child,.zieltab th:nth-child(2){{text-align:left}}
.zieltab td{{padding:9px 12px;border-bottom:1px solid #F1EDE4;font:500 13px/1 Manrope,sans-serif}}
.zieltab tr:last-child td{{border-bottom:none}}
.zt-t{{color:#8A8375;font-size:11.5px}}
.zt-n{{text-align:right;font-family:'JetBrains Mono',monospace}}
.zt-ok{{color:#2D7A3E;font-weight:600}}
.zt-of{{color:#B07214;font-weight:600}}
.zi-over{{font:600 11px/1 Manrope,sans-serif;color:#1E5F9E}}
.zt-ov{{color:#1E5F9E;font-weight:600}}
.zt-sum td{{background:#FBF9F5;font-weight:700}}
.zt-bar{{width:150px}}
.zb{{display:inline-block;width:100px;height:6px;background:#EFEBE1;border-radius:3px;overflow:hidden;vertical-align:middle}}
.zf{{display:block;height:100%;background:#2D7A3E}}
.zp{{margin-left:8px;font:600 11px/1 'JetBrains Mono',monospace;color:#5C5C5C}}
</style></head><body><div class="container">
<a href="../index.html" class="back">← Zurück zur Library</a>
<div class="kicker">KP Mainz · Studienplanung</div>
<h1>Master-Themenliste</h1>
<p class="lede">Alle {n_md} Themen in einer Rangliste, sortiert nach Korpus-Präsenz — Wortvorkommen im WhatsApp-Chat + in den Protokoll-Dateien. Review-Status + Statistik live aus der Library; gebaute Themen sind verlinkt.</p>
{caveat}
{analytics}
{zieltab}
{sK}{sS}{sR}{sE}
<div class="legend">
<b>Treffer</b> = Korpus-Erwähnungen gesamt; <b>{'{chat}·{prot}'}</b> darunter = Chat- bzw. Protokoll-Treffer. <b>#</b> = Rang in der Gesamtliste.
<b>Review</b>-Badge zeigt das gebaute Level (✓ R1 → R3) und verlinkt direkt; die Statistik oben wird bei jedem Build live aus dem Repo berechnet. Häkchen werden lokal im Browser gespeichert.
</div>
<div class="foot">KP Mainz · Master-Themenliste · {n_md} Themen · flache Rangliste nach Korpus-Präsenz · {len(repo)} Reviews live · Stand 06/2026</div>
</div>
<script>
const boxes=document.querySelectorAll('.box');
function load(){{try{{return JSON.parse(localStorage.getItem('kp_master')||'{{}}')}}catch(e){{return {{}}}}}}
function save(s){{localStorage.setItem('kp_master',JSON.stringify(s))}}
let st=load();
boxes.forEach((b)=>{{const row=b.closest('tr'); const key=row.dataset.topic; if(st[key]) b.classList.add('checked');
  b.addEventListener('click',()=>{{b.classList.toggle('checked');st[key]=b.classList.contains('checked');save(st);prog();}});}});
function prog(){{const n=document.querySelectorAll('.box.checked').length;document.getElementById('prog').innerHTML='<b>'+n+'</b> abgehakt';}}
prog();
</script>
</body></html>'''
io.open("tools/master-themenliste.html","w",encoding="utf-8").write(html)
h=html
# --- JSON feed for the app (bundled into the kp-progress Worker at /api/themen) ---
import json as _json, datetime as _dt
def _cov(s): return bool(s) and s in repo
def _rid(s): return (f'{s}-r{repo[s][0]}' if _cov(s) else None)
def _lvl(s): return (_badge_lvl(s,repo[s][0]) if _cov(s) else None)
_themen=[{
  'tier':'core','rank':rk,'treffer':t,'fach':f,'thema':th,
  'slug':s,'covered':_cov(s),'level':_lvl(s),'reviewId':_rid(s)
} for rk,t,c,p,f,th,s in ranked]
_extras=[{
  'tier':'extra','fach':f,'thema':th,
  'slug':s,'covered':_cov(s),'level':_lvl(s),'reviewId':_rid(s)
} for f,th,s in EXTRA]

# Drills und Atlanten erscheinen in der App unter den Extras — sie sind keine
# der 97 Pruefungsthemen, muessen aber in themen.json stehen, weil die App ihre
# Bibliotheksliste aus diesem Feed baut und topics.json nur als Inhaltsspeicher nutzt.
DRILLS = [
  ('Drills & Atlanten','EKG Komplett','ekg-komplett'),
  ('Drills & Atlanten','BGA Komplett','bga-komplett'),
  ('Drills & Atlanten','Sono Komplett','sono-komplett'),
  ('Drills & Atlanten','Echo Komplett','echo-komplett'),
  ('Drills & Atlanten','EEG Komplett','eeg-komplett'),
  ('Drills & Atlanten','Rechtsmedizin Komplett','rechtsmedizin-komplett'),
  ('Drills & Atlanten','Hoffart-Bildatlas','hoffart-bildatlas'),
]
_extras += [{'tier':'drill','fach':f,'thema':th,'slug':s2,
             'covered':_os.path.exists('drills/%s.html' % s2),'level':None,'reviewId':s2}
            for f,th,s2 in DRILLS]

_out={'version':2,'updatedAt':_dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
      'total':len(ranked),'covered':sum(1 for x in _themen if x['covered']),'coveragePct':cov_pct,
      'extrasTotal':len(_extras),'extrasCovered':sum(1 for x in _extras if x['covered']),
      'topics':_themen,'extras':_extras}
io.open("api/themen.json","w",encoding="utf-8").write(_json.dumps(_out,ensure_ascii=False,separators=(',',':')))
print("api/themen.json:",len(_themen),"rows |",_out['covered'],"covered")
print("FLAT rows:",len(FLAT),"| tiers:",f"KERN {tkn} STANDARD {tsn} RAND {trn} (sum {tkn+tsn+trn}) + EXTRA {len(EXTRA)}")
print("topic rows total:",h.count('<tr '),"| review badges:",h.count('class=\"have\"'),"| live reviews:",len(repo))
links=re.findall(r'href="\.\./(reviews/[^"]+)"',h); print("links:",len(links),"| broken:",[p for p in links if not glob.glob(p)] or "none")
print(f"analytics: {n_md} Themen · {len(repo)} live · {cov_pct}% · offen {n_md-md_cov} · R3/R2/R1 {nr[3]}/{nr[2]}/{nr[1]}")
print("tier cov:",f"KERN {tkc}/{tkn} STANDARD {tsc}/{tsn} RAND {trc}/{trn}")
print("gaps:",[f'{t} {th}' for t,th,f in gaps])
print("caveat present:", 'Erwähnungs-Häufigkeit' in h, "| rank col:", h.count('class="rk"'))
for t in ["section","table","tr","td","div"]:
    o=h.count("<"+t+" ")+h.count("<"+t+">"); c=h.count("</"+t+">"); print(f"  {t}:{o}/{c}{'' if o==c else ' ***'}")
print("bytes:",len(h.encode()))
