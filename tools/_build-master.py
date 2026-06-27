# -*- coding: utf-8 -*-
# Master-Themenliste builder — FLAT single ranking by Korpus-Treffer (chat+prot mentions).
# RUN FROM REPO ROOT:  python3 tools/_build-master.py
# Re-globs reviews/ for live R-levels; review column + analytics read LIVE from the repo.
# Topic universe/frequencies mirror KP-Master-Themenliste.md (88 topics, project knowledge).
import io, glob, re

repo={}
for f in sorted(glob.glob('reviews/**/*-r[0-9].html',recursive=True)):
    m=re.search(r'(reviews/[a-z-]+/([a-z0-9-]+)-r(\d)\.html)$',f)
    if not m: continue
    path,slug,lvl=m.group(1),m.group(2),int(m.group(3))
    if slug not in repo or lvl>repo[slug][0]: repo[slug]=(lvl,path)

DRILL={"Rechtsmedizin / Leichenschau"}
def esc(s): return s.replace('&','&amp;')
def trow(rank, treffer, chat, prot, fach, thema, slug):
    info=repo.get(slug); badges=""; done=""; topic=esc(thema)
    if info:
        lvl,path=info; topic=f'<a href="../{path}">{esc(thema)}</a>'; badges+=f'<span class="have">✓ R{lvl}</span>'; done=" done"
    if thema in DRILL: badges+='<span class="have drill">Drill</span>'
    rk=f'<td class="rk">{rank}</td>' if rank else '<td class="rk">·</td>'
    cnt=f'<span class="n">{treffer}</span><span class="src">{chat}·{prot}</span>' if treffer else '<span class="src">gebaut</span>'
    return (f'<tr class="{done.strip()}" data-topic="{esc(thema)}"><td class="chk"><span class="box"></span></td>'
            f'{rk}<td class="topic">{topic}{badges}</td><td class="fach">{esc(fach)}</td><td class="cnt">{cnt}</td></tr>')

# FLAT ranking (treffer, chat, prot, fach, thema, slug) — rank = position
FLAT=[
(381,122,259,"Viszeralchirurgie","Cholezystitis / Cholelithiasis","cholezystitis"),
(353,130,223,"Kardiologie","Vorhofflimmern","vorhofflimmern"),
(327,66,261,"Kardiologie","Herzinsuffizienz","herzinsuffizienz"),
(304,72,232,"Notfallmedizin","Schock","schock"),
(298,88,210,"Viszeralchirurgie","Ileus","ileus"),
(296,56,240,"Notfallmedizin","Sepsis","sepsis"),
(282,103,179,"Drittes Fach","Bluttransfusion",None),
(278,74,204,"Endokrinologie","Diabetes mellitus","diabetes-mellitus"),
(264,98,166,"Drittes Fach","Impfungen / STIKO","impfungen-stiko"),
(255,84,171,"Pneumologie","Pneumothorax","pneumothorax"),
(244,78,166,"Neurologie","Schlaganfall","schlaganfall"),
(243,44,199,"Gastroenterologie","Ikterus / Cholestase","ikterus-cholestase"),
(241,43,198,"Nephrologie","Nierenversagen (akut / akut-auf-chron.)",None),
(236,79,157,"Viszeralchirurgie","GI-Blutung","gi-blutung"),
(234,61,173,"Pneumologie","Pneumonie","pneumonie"),
(232,58,174,"Kardiologie","Myokardinfarkt / ACS","acs-myokardinfarkt"),
(226,78,148,"Viszeralchirurgie","Leistenhernie / Hernien","leistenhernie"),
(224,118,106,"Drittes Fach","Rechtsmedizin / Leichenschau","rechtsmedizin"),
(220,76,144,"Angiologie","Lungenembolie","lungenembolie"),
(218,88,130,"Viszeralchirurgie","Gastroduodenales Ulkus",None),
(203,74,129,"Viszeralchirurgie","Pankreatitis",None),
(203,68,135,"Viszeralchirurgie","Divertikulitis",None),
(202,55,147,"Endokrinologie","Schilddrüse (allg.)",None),
(171,46,125,"Gastroenterologie","Leberzirrhose","leberzirrhose"),
(169,69,100,"Unfallchirurgie","Schenkelhalsfraktur","proximale-femurfraktur"),
(169,54,115,"Viszeralchirurgie","Appendizitis","appendizitis"),
(155,42,113,"Kardiologie","AV-Block","av-block"),
(151,61,90,"Hämatologie","Eisenmangelanämie","eisenmangelanaemie"),
(151,18,133,"Gastroenterologie","Hepatitis",None),
(143,42,101,"Viszeralchirurgie","Kolonkarzinom",None),
(142,16,126,"Kardiologie","KHK / Angina pectoris","khk"),
(132,39,93,"Gastroenterologie","Lebermetastasen / Lebertumor",None),
(131,82,49,"Drittes Fach","Strahlenschutz","strahlenschutz"),
(130,31,99,"Pneumologie","COPD","copd"),
(127,44,83,"Unfallchirurgie","Sprunggelenkfraktur (OSG)","sprunggelenksfraktur"),
(122,39,83,"Endokrinologie","Hyperthyreose","hyperthyreose"),
(120,40,80,"Unfallchirurgie","Hüft- / Knie-TEP",None),
(120,36,84,"Gastroenterologie","Gastritis (Typ A/B/C)",None),
(119,31,88,"Drittes Fach","Sozialrecht / Hygiene","sozialrecht-hygiene"),
(117,24,93,"Angiologie","pAVK",None),
(111,37,74,"Angiologie","TVT / Phlebothrombose",None),
(108,35,73,"Kardiologie","Arterielle Hypertonie","arterielle-hypertonie"),
(102,15,87,"Pneumologie","Asthma","asthma-bronchiale"),
(100,35,65,"Pneumologie","Bronchialkarzinom",None),
(95,18,77,"Kardiologie","Synkope","synkope"),
(93,40,53,"Unfallchirurgie","Distale Radiusfraktur","distale-radiusfraktur"),
(93,30,63,"Drittes Fach","Schmerztherapie / WHO-Schema",None),
(92,30,62,"Notfallmedizin","Akuttoxikologie / Intoxikation",None),
(92,21,71,"Kardiologie","Ventr. Tachykardie / Kammerflimmern",None),
(91,15,76,"Hämatologie","ALL / Leukämie","akute-leukaemien"),
(89,37,52,"Drittes Fach","Aufklärung / Einwilligung / Betreuung","aufklaerung-einwilligung-betreuung"),
(87,17,70,"Endokrinologie","Osteoporose",None),
(87,6,81,"Hämatologie","Lymphom (NHL)","non-hodgkin-lymphome"),
(84,16,68,"Gastroenterologie","Morbus Crohn","morbus-crohn"),
(82,16,66,"Endokrinologie","Hypothyreose","hypothyreose"),
(81,27,54,"Unfallchirurgie","Schädel-Hirn-Trauma","schaedel-hirn-trauma"),
(81,22,59,"Pneumologie","Tuberkulose",None),
(81,16,65,"Unfallchirurgie","Sturz / Polytrauma",None),
(74,22,52,"Unfallchirurgie","Kompartmentsyndrom",None),
(73,11,62,"Angiologie","Aortendissektion","aortendissektion"),
(68,12,56,"Unfallchirurgie","Allg. Frakturlehre","allgemeine-frakturlehre"),
(67,12,55,"Nephrologie","Harnwegsinfekt / Pyelonephritis",None),
(65,22,43,"Endokrinologie","Schilddrüsenkarzinom",None),
(62,15,47,"Viszeralchirurgie","Rektumkarzinom",None),
(60,15,45,"Unfallchirurgie","Humerusfraktur",None),
(59,11,48,"Gastroenterologie","GERD / Refluxkrankheit",None),
(59,7,52,"Kardiologie","Endokarditis","infektioese-endokarditis"),
(57,17,40,"Viszeralchirurgie","Diarrhoe / Gastroenteritis",None),
(56,15,41,"Viszeralchirurgie","Pankreaskarzinom",None),
(56,11,45,"Viszeralchirurgie","Hämorrhoiden",None),
(55,11,44,"Viszeralchirurgie","Magenkarzinom",None),
(55,9,46,"Hämatologie","Morbus Hodgkin",None),
(54,19,35,"Notfallmedizin","Verbrennung",None),
(52,5,47,"Gastroenterologie","Colitis ulcerosa",None),
(49,10,39,"Unfallchirurgie","Claviculafraktur",None),
(47,8,39,"Endokrinologie","Struma",None),
(43,19,24,"Kardiologie","Paroxysmale SVT / AVNRT-AVRT",None),
(43,14,29,"Kardiologie","Aortenklappenstenose","herzklappenerkrankungen"),
(43,13,30,"Querschnitt","Check-up / Prävention",None),
(43,10,33,"Unfallchirurgie","Femurfraktur","proximale-femurfraktur"),
(40,12,28,"Kardiologie","Mitralklappenvitium","herzklappenerkrankungen"),
(40,10,30,"Angiologie","Aortenaneurysma (AAA)",None),
(40,7,33,"Unfallchirurgie","Beckenfraktur","beckenringfrakturen"),
(37,12,25,"Notfallmedizin","Delir",None),
(32,5,27,"Endokrinologie","Cushing-Syndrom","cushing-syndrom"),
(23,3,20,"Unfallchirurgie","Wirbelsäulenverletzungen","wirbelsaeulenverletzungen"),
(13,8,5,"Drittes Fach","KI in der Medizin",None),
(12,10,2,"Drittes Fach","EBM",None),
]
EXTRA=[("Notfallmedizin","Pleuraerguss","pleuraerguss"),("Kardiologie","Hypertrophe Kardiomyopathie","hypertrophe-kardiomyopathie"),("Notfallmedizin","Notfallpharmakologie","notfallpharmakologie"),("Hämatologie","CML","cml")]

# rank + tier split
ranked=[(i+1,)+row for i,row in enumerate(FLAT)]
def tier(lo,hi): return [r for r in ranked if lo<=r[1]<hi]   # r[1]=treffer
T1=[r for r in ranked if r[1]>=200]; T2=[r for r in ranked if 120<=r[1]<200]; T3=[r for r in ranked if 60<=r[1]<120]; T4=[r for r in ranked if r[1]<60]
covered=lambda s: bool(s) and s in repo
def tc(T): return sum(1 for r in T if covered(r[6])), len(T)  # r[6]=slug
t1c,t1n=tc(T1); t2c,t2n=tc(T2); t3c,t3n=tc(T3); t4c,t4n=tc(T4)
n_md=len(FLAT); md_cov=sum(1 for r in ranked if covered(r[6])); cov_pct=round(md_cov/n_md*100)
nr={3:0,2:0,1:0}
for lvl,_ in repo.values(): nr[lvl]=nr.get(lvl,0)+1
gaps=[(t,th,f) for rk,t,c,p,f,th,s in ranked if not covered(s)][:6]
fab={"Viszeralchirurgie":"Viszeralchir.","Unfallchirurgie":"Unfallchir.","Endokrinologie":"Endokrin.","Kardiologie":"Kardio.","Gastroenterologie":"Gastro.","Angiologie":"Angio.","Notfallmedizin":"Notfall","Pneumologie":"Pneumo.","Hämatologie":"Häm.","Nephrologie":"Nephro.","Neurologie":"Neuro.","Drittes Fach":"Drittes Fach","Querschnitt":"Querschnitt"}

def section(tc_,title,desc,count,rows):
    return (f'<section class="tier" style="--tc:{tc_}"><div class="tier-head"><div><div class="tier-title">{title}</div>'
            f'<div class="tier-desc">{desc}</div></div><div class="tier-count">{count}</div></div>'
            f'<table><tbody>{rows}</tbody></table></section>')
def rowsfor(T): return "".join(trow(rk,t,c,p,f,th,s) for rk,t,c,p,f,th,s in T)
s1=section("#C0392B","Tier 1 · höchste Präsenz","≥ 200 Korpus-Treffer",f"{t1n} Themen",rowsfor(T1))
s2=section("#D97706","Tier 2 · hohe Präsenz","120–199 Treffer",f"{t2n} Themen",rowsfor(T2))
s3=section("#0E7C7B","Tier 3 · mittlere Präsenz","60–119 Treffer",f"{t3n} Themen",rowsfor(T3))
s4=section("#64748B","Tier 4 · niedrige Präsenz","< 60 Treffer",f"{t4n} Themen",rowsfor(T4))
sE=section("#2D7A3E","Weitere gebaute Reviews","In der Library vorhanden, aber nicht in der Korpus-Rangliste",f"{len(EXTRA)} Themen","".join(trow(None,0,0,0,f,th,s) for f,th,s in EXTRA))

def bar(label,c,n,col):
    pct=round(c/n*100) if n else 0
    return f'<div class="ana-tier" style="--tcc:{col}"><span class="ana-tl">{label}</span><div class="bar"><div class="fill" style="width:{pct}%"></div></div><span class="ana-tc">{c} / {n}</span></div>'
gaps_html="".join(f'<div class="gap"><span class="gap-n">{t}</span><span class="gap-t">{esc(th)}</span><span class="gap-f">{fab.get(f,f)}</span></div>' for t,th,f in gaps)
analytics=f'''<section class="analytics">
  <div class="ana-grid">
    <div class="ana-card"><div class="ana-n">{n_md}</div><div class="ana-l">Themen · Inventar</div></div>
    <div class="ana-card"><div class="ana-n">{len(repo)}</div><div class="ana-l">Reviews live</div></div>
    <div class="ana-card"><div class="ana-n">{cov_pct}<span style="font-size:18px"> %</span></div><div class="ana-l">abgedeckt</div></div>
    <div class="ana-card"><div class="ana-n">{t1c}<span style="font-size:18px"> / {t1n}</span></div><div class="ana-l">Tier 1 (≥200) erledigt</div></div>
  </div>
  <div class="ana-strip">Review-Reife · <b>{nr[3]}</b>×R3 · <b>{nr[2]}</b>×R2 · <b>{nr[1]}</b>×R1 · +{len(EXTRA)} außerhalb der Liste &nbsp;·&nbsp; <span id="prog">0 abgehakt</span></div>
  <div class="ana-sub">
    <div class="ana-box"><div class="ana-box-h">Abdeckung nach Präsenz-Tier</div>
      {bar("Tier 1",t1c,t1n,"#C0392B")}{bar("Tier 2",t2c,t2n,"#D97706")}{bar("Tier 3",t3c,t3n,"#0E7C7B")}{bar("Tier 4",t4c,t4n,"#64748B")}
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
</style></head><body><div class="container">
<a href="../index.html" class="back">← Zurück zur Library</a>
<div class="kicker">KP Mainz · Studienplanung</div>
<h1>Master-Themenliste</h1>
<p class="lede">Alle {n_md} Themen in einer Rangliste, sortiert nach Korpus-Präsenz — Wortvorkommen im WhatsApp-Chat + in den Protokoll-Dateien. Review-Status + Statistik live aus der Library; gebaute Themen sind verlinkt.</p>
{caveat}
{analytics}
{s1}{s2}{s3}{s4}{sE}
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
_themen=[{
  'rank':rk,'treffer':t,'fach':f,'thema':th,
  'slug':s,'covered':bool(s) and s in repo,
  'level':(repo[s][0] if (s and s in repo) else None),
  'reviewId':(f'{s}-r{repo[s][0]}' if (s and s in repo) else None)
} for rk,t,c,p,f,th,s in ranked]
_out={'version':1,'updatedAt':_dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
      'total':len(ranked),'covered':sum(1 for x in _themen if x['covered']),'coveragePct':cov_pct,
      'topics':_themen}
io.open("api/themen.json","w",encoding="utf-8").write(_json.dumps(_out,ensure_ascii=False,separators=(',',':')))
print("api/themen.json:",len(_themen),"rows |",_out['covered'],"covered")
print("FLAT rows:",len(FLAT),"| tiers:",f"T1 {t1n} T2 {t2n} T3 {t3n} T4 {t4n} (sum {t1n+t2n+t3n+t4n}) + EXTRA {len(EXTRA)}")
print("topic rows total:",h.count('<tr '),"| review badges:",h.count('class=\"have\"'),"| live reviews:",len(repo))
links=re.findall(r'href="\.\./(reviews/[^"]+)"',h); print("links:",len(links),"| broken:",[p for p in links if not glob.glob(p)] or "none")
print(f"analytics: {n_md} Themen · {len(repo)} live · {cov_pct}% · offen {n_md-md_cov} · R3/R2/R1 {nr[3]}/{nr[2]}/{nr[1]}")
print("tier cov:",f"T1 {t1c}/{t1n} T2 {t2c}/{t2n} T3 {t3c}/{t3n} T4 {t4c}/{t4n}")
print("gaps:",[f'{t} {th}' for t,th,f in gaps])
print("caveat present:", 'Erwähnungs-Häufigkeit' in h, "| rank col:", h.count('class="rk"'))
for t in ["section","table","tr","td","div"]:
    o=h.count("<"+t+" ")+h.count("<"+t+">"); c=h.count("</"+t+">"); print(f"  {t}:{o}/{c}{'' if o==c else ' ***'}")
print("bytes:",len(h.encode()))
