# -*- coding: utf-8 -*-
# Master-Themenliste builder. RUN FROM REPO ROOT:  python3 tools/_build-master.py
# Re-globs reviews/ for live R-levels and regenerates tools/master-themenliste.html.
# Topic universe + frequencies mirror KP-Master-Themenliste.md (project knowledge, 88 topics);
# the Review column + analytics are read LIVE from the repo, so re-running after any publish refreshes them.
import io, glob, re

repo={}
for f in sorted(glob.glob('reviews/**/*-r[0-9].html',recursive=True)):
    m=re.search(r'(reviews/[a-z-]+/([a-z0-9-]+)-r(\d)\.html)$',f)
    if not m: continue
    path,slug,lvl=m.group(1),m.group(2),int(m.group(3))
    if slug not in repo or lvl>repo[slug][0]: repo[slug]=(lvl,path)

def esc(s): return s.replace('&','&amp;')
def trow(fach, thema, slug, cnt, note="", drill=False):
    info=repo.get(slug); badges=""; done=""; topic=esc(thema)
    if info:
        lvl,path=info; topic=f'<a href="../{path}">{esc(thema)}</a>'; badges+=f'<span class="have">✓ R{lvl}</span>'; done=" done"
    if drill: badges+='<span class="have drill">Drill</span>'
    notehtml=f'<div class="note">{esc(note)}</div>' if note else ""
    return (f'<tr class="{done.strip()}" data-topic="{esc(thema)}"><td class="chk"><span class="box"></span></td>'
            f'<td class="topic">{topic}{badges}{notehtml}</td><td class="fach">{esc(fach)}</td><td class="cnt">{cnt}</td></tr>')
def freq(t,p,w): return f'<span class="n">{t}</span><span class="src">{p}·PB {w}·WA</span>'
def c06(n): return f'<span class="n">{n}</span><span class="src">·06/26</span>'
def amb(c,pr): return f'<span class="n">{pr}</span><span class="src">{c}·Chat</span>'
def built(): return '<span class="src">gebaut</span>'

T1=[(42,2,40,"Viszeralchirurgie","Ileus (inkl. Sigmavolvulus-DD)","ileus"),(35,3,32,"Viszeralchirurgie","Appendizitis","appendizitis"),(35,2,33,"Viszeralchirurgie","Cholezystitis / Cholelithiasis","cholezystitis"),(32,2,30,"Viszeralchirurgie","Divertikulitis / Divertikulose",None),(31,1,30,"Viszeralchirurgie","Kolonkarzinom",None),(25,2,23,"Angiologie","Lungenembolie","lungenembolie"),(23,6,17,"Kardiologie","Herzinsuffizienz","herzinsuffizienz"),(22,1,21,"Viszeralchirurgie","Pankreatitis ↑",None),(21,0,21,"Endokrinologie","Schilddrüse (allg.)",None)]
T2=[(18,0,18,"Pneumologie","Pneumothorax","pneumothorax"),(17,2,15,"Pneumologie","Pneumonie","pneumonie"),(16,2,14,"Pneumologie","COPD","copd"),(14,0,14,"Unfallchirurgie","Allg. Frakturlehre","allgemeine-frakturlehre"),(14,1,13,"Endokrinologie","Schilddrüsenkarzinom",None),(13,3,10,"Hämatologie","ALL / Leukämie","akute-leukaemien"),(13,1,12,"Endokrinologie","Hyperthyreose","hyperthyreose"),(12,2,10,"Kardiologie","AV-Block","av-block"),(12,1,11,"Unfallchirurgie","Distale Radiusfraktur","distale-radiusfraktur"),(12,1,11,"Unfallchirurgie","Sprunggelenkfraktur (OSG)","sprunggelenksfraktur"),(12,0,12,"Kardiologie","Vorhofflimmern","vorhofflimmern")]
T3=[(9,1,8,"Kardiologie","KHK / Angina pectoris","khk"),(9,3,6,"Viszeralchirurgie","Rektumkarzinom",None),(8,1,7,"Endokrinologie","Hypothyreose",None),(8,2,6,"Viszeralchirurgie","Magenkarzinom",None),(6,1,5,"Kardiologie","Aortenklappenstenose (Herzklappen)","herzklappenerkrankungen"),(6,3,3,"Hämatologie","Eisenmangelanämie (Thalassämie-DD, B12)","eisenmangelanaemie"),(6,1,5,"Viszeralchirurgie","Pankreaskarzinom",None),(5,0,5,"Unfallchirurgie","Femurfraktur","proximale-femurfraktur"),(5,5,0,"Viszeralchirurgie","GI-Blutung (OGIB + UGIB) ↑","gi-blutung"),(5,2,3,"Unfallchirurgie","Hüft-/Knie-TEP",None),(5,1,4,"Unfallchirurgie","Schenkelhalsfraktur","proximale-femurfraktur"),(5,0,5,"Unfallchirurgie","Wirbelsäulenfraktur",None)]
T4=[(4,0,4,"Unfallchirurgie","Beckenfraktur","beckenringfrakturen"),(4,2,2,"Unfallchirurgie","Humerusfraktur",None),(4,0,4,"Kardiologie","Myokardinfarkt / ACS","acs-myokardinfarkt"),(3,1,2,"Kardiologie","Endokarditis","infektioese-endokarditis"),(3,1,2,"Gastroenterologie","Lebermetastasen / Lebertumor",None),(3,2,1,"Gastroenterologie","Leberzirrhose / portale Hypertonie",None),(3,0,3,"Kardiologie","Mitralklappenvitium (Herzklappen)","herzklappenerkrankungen"),(3,2,1,"Hämatologie","Morbus Hodgkin",None),(3,1,2,"Notfallmedizin","Sepsis","sepsis"),(3,0,3,"Endokrinologie","Struma",None),(3,1,2,"Kardiologie","Synkope","synkope"),(2,0,2,"Pneumologie","Asthma bronchiale","asthma-bronchiale"),(2,1,1,"Pneumologie","Bronchialkarzinom",None),(2,0,2,"Endokrinologie","Cushing-Syndrom","cushing-syndrom"),(2,1,1,"Notfallmedizin","Delir",None),(2,2,0,"Gastroenterologie","Hepatitis",None),(2,1,1,"Gastroenterologie","Ikterus / Cholestase",None),(2,0,2,"Neurologie","Schlaganfall ↑ (+ Para-/Tetraplegie)","schlaganfall"),(2,2,0,"Unfallchirurgie","Sturz / Polytrauma (inkl. Thoraxtrauma)",None),(1,1,0,"Angiologie","Aortenaneurysma (AAA)",None),(1,1,0,"Kardiologie","Arterielle Hypertonie","arterielle-hypertonie"),(1,1,0,"Querschnitt","Check-up / Prävention",None),(1,1,0,"Endokrinologie","Diabetes mellitus (inkl. DKA)","diabetes-mellitus"),(1,1,0,"Viszeralchirurgie","Diarrhoe / Gastroenteritis",None),(1,1,0,"Viszeralchirurgie","Gastroduodenales Ulkus",None),(1,0,1,"Hämatologie","Lymphom","non-hodgkin-lymphome"),(1,1,0,"Viszeralchirurgie","Morbus Crohn","morbus-crohn"),(1,0,1,"Notfallmedizin","Schock","schock"),(1,0,1,"Angiologie","TVT / Phlebothrombose",None),(1,1,0,"Angiologie","pAVK",None)]
NEU=[(2,"Viszeralchirurgie","Leistenhernie / Hernien","leistenhernie","bereits gebaut",False),(1,"Viszeralchirurgie","Hämorrhoiden",None,"neu",False),(1,"Kardiologie","Paroxysmale SVT / AVNRT–AVRT",None,"distinkt von AV-Block & VHF",False),(1,"Unfallchirurgie","Claviculafraktur (+ Plexus-Läsion)",None,"neu",False),(1,"Angiologie","Aortendissektion (+ Stanford)","aortendissektion","Liste hatte nur AAA",False),(2,"Gastroenterologie","Gastritis (Typ A/B/C, H. pylori)",None,"Liste hatte nur Ulkus",False),(1,"Nephrologie","Akutes Nierenversagen",None,"bisher keine Nephro-Zeile",False),(2,"Drittes Fach","Rechtsmedizin / Leichenschau","rechtsmedizin","+ Drill",True),(1,"Drittes Fach","Strahlenschutz (ALARA, 5 A)","strahlenschutz","",False),(1,"Drittes Fach","Bluttransfusion (Kreuzprobe, Bedside)",None,"Einwilligung betont",False),(2,"Drittes Fach","Schmerztherapie / WHO-Stufenschema",None,"tlw. in Notfallpharma-R2",False),(1,"Drittes Fach","Evidenzbasierte Medizin (EBM)",None,"neu",False),(1,"Drittes Fach","KI in der Medizin",None,"aufkommend",False),(2,"Drittes Fach","Aufklärung / Einwilligung / Betreuung","aufklaerung-einwilligung-betreuung","bereits gebaut",False),(1,"Drittes Fach","Impfungen / STIKO","impfungen-stiko","bereits gebaut",False),(1,"Drittes Fach","Sozialrecht / Hygiene (BG, D-Arzt)","sozialrecht-hygiene","bereits gebaut",False)]
AMB=[(30,62,"Notfallmedizin","Akuttoxikologie / Intoxikation",None),(27,54,"Unfallchirurgie","Schädel-Hirn-Trauma","schaedel-hirn-trauma"),(22,59,"Pneumologie","Tuberkulose",None),(22,52,"Unfallchirurgie","Kompartmentsyndrom",None),(21,71,"Kardiologie","Ventrikuläre Tachykardie / Kammerflimmern",None),(19,35,"Notfallmedizin","Verbrennung (Neuner-Regel, VKOF)",None),(17,70,"Endokrinologie","Osteoporose",None),(12,55,"Nephrologie","Harnwegsinfekt / Pyelonephritis",None),(11,48,"Gastroenterologie","GERD / Refluxkrankheit",None),(5,47,"Gastroenterologie","Colitis ulcerosa",None)]
EXTRA=[("Notfallmedizin","Pleuraerguss","pleuraerguss"),("Kardiologie","Hypertrophe Kardiomyopathie","hypertrophe-kardiomyopathie"),("Notfallmedizin","Notfallpharmakologie","notfallpharmakologie"),("Hämatologie","CML","cml")]

# ── analytics (computed live) ──
md_rows=[(t,f,th,s) for t,p,w,f,th,s in T1+T2+T3+T4]+[(0,f,th,s) for n,f,th,s,no,d in NEU]+[(0,f,th,s) for c,pr,f,th,s in AMB]
n_md=len(md_rows)
covered=lambda s: bool(s) and s in repo
md_cov=sum(1 for _,_,_,s in md_rows if covered(s))
cov_pct=round(md_cov/n_md*100)
nr={3:0,2:0,1:0}
for lvl,_ in repo.values(): nr[lvl]=nr.get(lvl,0)+1
def tiercov(T): tot=len(T); c=sum(1 for *_,s in [(r[3],r[4],r[5]) for r in T] if covered(s)); return c,tot
def tc(T): return sum(1 for r in T if covered(r[5])), len(T)
t1c,t1n=tc(T1); t2c,t2n=tc(T2); t3c,t3n=tc(T3); t4c,t4n=tc(T4)
gaps=sorted([(t,th,f) for t,p,w,f,th,s in T1+T2+T3+T4 if not covered(s)], key=lambda x:-x[0])[:6]
fab={"Viszeralchirurgie":"Viszeralchir.","Unfallchirurgie":"Unfallchir.","Endokrinologie":"Endokrin.","Kardiologie":"Kardio.","Gastroenterologie":"Gastro.","Angiologie":"Angio.","Notfallmedizin":"Notfall","Pneumologie":"Pneumo.","Hämatologie":"Häm.","Nephrologie":"Nephro.","Neurologie":"Neuro.","Drittes Fach":"Drittes Fach","Querschnitt":"Querschnitt"}

def section(tc_,title,desc,count,rows):
    return (f'<section class="tier" style="--tc:{tc_}"><div class="tier-head"><div><div class="tier-title">{title}</div>'
            f'<div class="tier-desc">{desc}</div></div><div class="tier-count">{count}</div></div><table><tbody>{rows}</tbody></table></section>')
s1=section("#C0392B","Tier 1 · Kernthemen","≥ 20 Nennungen — mit Sicherheit prüfungsrelevant",f"{t1n} Themen","".join(trow(f,t,s,freq(to,p,w)) for to,p,w,f,t,s in T1))
s2=section("#D97706","Tier 2 · Hochfrequent","10–19 Nennungen — sehr wahrscheinlich",f"{t2n} Themen","".join(trow(f,t,s,freq(to,p,w)) for to,p,w,f,t,s in T2))
s3=section("#0E7C7B","Tier 3 · Mittelfrequent","5–9 Nennungen — solide vorbereiten",f"{t3n} Themen","".join(trow(f,t,s,freq(to,p,w)) for to,p,w,f,t,s in T3))
s4=section("#64748B","Tier 4 · Niedrigfrequent / Drittes Fach","1–4 Nennungen — Überblick genügt",f"{t4n} Themen","".join(trow(f,t,s,freq(to,p,w)) for to,p,w,f,t,s in T4))
sN=section("#5B53B0","Neu · Protokolle 03–06/2026","Themen aus den fünf neuen Protokollen — historische Frequenz noch nicht codiert",f"{len(NEU)} Themen","".join(trow(f,t,s,c06(n),note,drill) for n,f,t,s,note,drill in NEU))
sA=section("#0F766E","Neu · Amboss-152-Validierung","Bestätigte Lücken aus dem statistischen Korpus-Abgleich",f"{len(AMB)} Themen","".join(trow(f,t,s,amb(c,pr)) for c,pr,f,t,s in AMB))
sE=section("#2D7A3E","Weitere gebaute Reviews","In der Library vorhanden, aber noch nicht in der Frequenzliste codiert",f"{len(EXTRA)} Themen","".join(trow(f,t,s,built()) for f,t,s in EXTRA))

def bar(label,c,n,col):
    pct=round(c/n*100) if n else 0
    return f'<div class="ana-tier" style="--tcc:{col}"><span class="ana-tl">{label}</span><div class="bar"><div class="fill" style="width:{pct}%"></div></div><span class="ana-tc">{c} / {n}</span></div>'
gaps_html="".join(f'<div class="gap"><span class="gap-n">{t}</span><span class="gap-t">{esc(th)}</span><span class="gap-f">{fab.get(f,f)}</span></div>' for t,th,f in gaps)
analytics=f'''<section class="analytics">
  <div class="ana-grid">
    <div class="ana-card"><div class="ana-n">{n_md}</div><div class="ana-l">Themen · Frequenzliste</div></div>
    <div class="ana-card"><div class="ana-n">{len(repo)}</div><div class="ana-l">Reviews live</div></div>
    <div class="ana-card"><div class="ana-n">{cov_pct}<span style="font-size:18px"> %</span></div><div class="ana-l">Liste abgedeckt</div></div>
    <div class="ana-card"><div class="ana-n">{t1c}<span style="font-size:18px"> / {t1n}</span></div><div class="ana-l">Tier 1 abgedeckt</div></div>
  </div>
  <div class="ana-strip">Review-Reife · <b>{nr[3]}</b>×R3 · <b>{nr[2]}</b>×R2 · <b>{nr[1]}</b>×R1 · +{len(EXTRA)} außerhalb der Liste &nbsp;·&nbsp; <span id="prog">0 abgehakt</span></div>
  <div class="ana-sub">
    <div class="ana-box"><div class="ana-box-h">Abdeckung nach Tier</div>
      {bar("Tier 1",t1c,t1n,"#C0392B")}{bar("Tier 2",t2c,t2n,"#D97706")}{bar("Tier 3",t3c,t3n,"#0E7C7B")}{bar("Tier 4",t4c,t4n,"#64748B")}
    </div>
    <div class="ana-box"><div class="ana-box-h">Größte Lücken — höchste Frequenz, kein Review</div>{gaps_html}</div>
  </div>
</section>'''

html=f'''<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KP Mainz · Master-Themenliste</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,500;0,600;1,400&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FBFAF7;--ink:#1A1A1A;--muted:#6B6B6B;--soft:#9A9A9A;--rule:#E6E2D9;--paper:#fff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:Manrope,sans-serif;font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}}
.container{{max-width:780px;margin:0 auto;padding:56px 22px 90px}}
.back{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#9A9A9A;text-decoration:none;margin-bottom:22px}}
.kicker{{font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--soft);margin-bottom:16px}}
h1{{font-family:Fraunces,serif;font-weight:500;font-size:clamp(32px,6vw,46px);line-height:1.02;letter-spacing:-.02em;margin-bottom:14px}}
.lede{{font-family:Fraunces,serif;font-size:17px;color:var(--muted);max-width:560px;margin-bottom:8px}}
.analytics{{margin-top:26px}}
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
.gap-n{{font-family:'JetBrains Mono',monospace;font-weight:600;color:#C0392B;min-width:22px;font-size:13px}}
.gap-t{{font-family:Fraunces,serif;font-weight:500;flex:1;font-size:14px}}
.gap-f{{font-size:10.5px;color:var(--soft);white-space:nowrap}}
.tier{{margin-top:40px}}
.tier-head{{display:flex;justify-content:space-between;align-items:flex-end;border-left:3px solid var(--tc);padding-left:13px;margin-bottom:10px}}
.tier-title{{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--tc)}}
.tier-desc{{font-family:Fraunces,serif;font-style:italic;font-size:13.5px;color:var(--muted);margin-top:3px;max-width:500px}}
.tier-count{{font-size:11.5px;color:var(--soft);white-space:nowrap}}
table{{width:100%;border-collapse:collapse}}
td{{padding:11px 8px;border-bottom:1px solid var(--rule);vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:rgba(0,0,0,.014)}}
.chk{{width:26px}}
.box{{display:inline-block;width:16px;height:16px;border:1.5px solid var(--soft);border-radius:4px;vertical-align:middle;cursor:pointer;transition:.15s}}
.box.checked{{background:var(--ink);border-color:var(--ink);position:relative}}
.box.checked::after{{content:"✓";color:#fff;font-size:12px;font-weight:700;position:absolute;top:-1px;left:2px}}
.topic{{font-family:Fraunces,serif;font-size:16px;font-weight:500}}
.topic a{{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}}
.topic a:hover{{border-bottom-color:var(--ink)}}
tr.done .topic a,tr.done .topic{{color:var(--soft)}}
.note{{font-family:Manrope;font-size:11px;font-style:normal;color:var(--soft);margin-top:2px}}
.have{{display:inline-block;font-family:Manrope;font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#2D7A3E;background:#E3F1E6;padding:2px 6px;border-radius:3px;margin-left:8px;vertical-align:middle}}
.have.drill{{color:#5B53B0;background:#ECEAF8}}
.fach{{font-size:12.5px;color:var(--muted);white-space:nowrap}}
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
<p class="lede">88 konsolidierte Prüfungsthemen aus 82 Protokoll-Fällen + 176 WhatsApp-Berichten, nach Häufigkeit in Tiers. Review-Status + Statistik live aus der Library; gebaute Themen sind verlinkt.</p>
{analytics}
{s1}{s2}{s3}{s4}{sN}{sA}{sE}
<div class="legend">
<b>Häufigkeit</b> = wie oft das Thema als Prüfungsfall auftauchte (PB = Protokolle bearbeitet, WA = WhatsApp; neue Abschnitte: 06/26 = Treffer in den fünf neuesten Protokollen, Chat/Prot = Korpus-Treffer).
<b>Review</b>-Badge zeigt das gebaute Level (✓ R1 → R3) und verlinkt direkt; die Statistik oben wird bei jedem Build live aus dem Repo neu berechnet. <b>↑</b> = zuletzt steigende Häufigkeit. Häkchen werden lokal im Browser gespeichert.
</div>
<div class="foot">KP Mainz · Master-Themenliste · {n_md} Themen · {len(repo)} Reviews live · Statistik direkt aus dem Repo · Stand 06/2026</div>
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
# validate
h=html
print("topic rows:",h.count('<tr '),"(88 Liste + 4 extra = 92) | review badges:",h.count('class="have"'),"| live reviews:",len(repo))
links=re.findall(r'href="\.\./(reviews/[^"]+)"',h); print("links:",len(links),"| broken:",[p for p in links if not glob.glob(p)] or "none")
print(f"analytics: {n_md} Themen · {len(repo)} live · {cov_pct}% · Tier1 {t1c}/{t1n} · R3/R2/R1 {nr[3]}/{nr[2]}/{nr[1]} · gaps {[g[1] for g in gaps]}")
print("tier counts:",f"T1 {t1n} T2 {t2n} T3 {t3n} T4 {t4n} NEU {len(NEU)} AMB {len(AMB)} EXTRA {len(EXTRA)}")
for t in ["section","table","tr","td","div"]:
    o=h.count("<"+t+" ")+h.count("<"+t+">"); c=h.count("</"+t+">"); print(f"  {t}:{o}/{c}{'' if o==c else ' ***'}")
print("bytes:",len(h.encode()))
