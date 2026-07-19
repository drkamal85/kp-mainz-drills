#!/usr/bin/env python3
"""
Build drills/hoffart-bildatlas.html from the 149 extracted Hoffart exam images.

- One reveal-card per image (see image -> click to reveal Befund), matching the
  Proto house style used across the drill library.
- Befunde live in the EXPL dict below, keyed by image number (1..149). Images
  without an entry render a muted "Befund folgt" state, so the atlas is fully
  browsable from day one and explanations drop in batch by batch.
- Each Befund is Claude's Erstlesung and is marked as "zu bestaetigen" until
  Mohamed (the expert) confirms it. Move confirmed reads out of that state by
  setting "ok": True on the entry.

Run:  python3 tools/_build-hoffart-atlas.py
"""
import html
import os
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "drills" / "hoffart"
OUT = REPO / "drills" / "hoffart-bildatlas.html"

N = len(sorted(IMG_DIR.glob("p*.jpg")))

# ---------------------------------------------------------------------------
# EXPL[num] = {
#   "mod":  short modality/region tag shown on the card  (e.g. "Sono Abdomen")
#   "dx":   the one-line Befund / diagnosis (the reveal headline)
#   "look": what to point at in the image (bullet list, optional)
#   "kp":   the exam hook / typical Mainz follow-up (optional)
#   "ok":   True once Mohamed has confirmed the read (drops the "zu bestaetigen" flag)
# }
# Only images with a genuinely identifiable archetype are seeded here; the rest
# stay "folgt" until read at full resolution in a verified batch.
# ---------------------------------------------------------------------------
EXPL = {
    # --- Sono batch 1: images whose Diagnose is captioned/annotated on the
    #     image itself (reliable). Un-captioned US series (Niere 117-122,
    #     Leber 125-128, Galle 135, p147) follow next pass, read at full res.
    #     All entries are Claude-Erstlesung until Mohamed confirms (ok=True).
    117: {
        "mod": "Sono · Niere",
        "dx": "Harnstauungsniere (Hydronephrose) — erweitertes, echofreies Nierenbeckenkelchsystem.",
        "look": [
            "Zentral im Nierensinus echofreie, miteinander kommunizierende Räume — das aufgestaute Hohlsystem",
            "Je nach Ausmaß nur das Nierenbecken oder auch die Kelche ballonartig erweitert",
        ],
        "kp": "Immer die Ursache suchen — prä-, intra- oder postrenal. Beim postrenalen Aufstau ist der häufigste Grund ein Konkrement, bei älteren Männern die Prostata.",
    },
    118: {
        "mod": "Sono · Niere",
        "dx": "Gradeinteilung der Harnstauung nach dem sonografischen Ausmaß der Dilatation.",
        "look": [
            "Grad I: nur das Nierenbecken erweitert",
            "Grad II: zusätzlich die Kelche, Fornices noch spitz",
            "Grad III: plumpe, kolbige Kelche, Parenchym noch erhalten",
            "Grad IV: hochgradige Erweiterung mit Parenchymverschmälerung",
        ],
        "kp": "Bei kompletter Obstruktion mit Fieber und Sepsis ist die Entlastung ein Notfall (infizierter Aufstau).",
    },
    119: {
        "mod": "Sono · Niere",
        "dx": "Höhergradige Harnstauung — kolbig aufgetriebene Kelche.",
        "look": [
            "Die Kelche sind plump und rund, nicht mehr spitz",
            "Bei chronischem Aufstau wird der Parenchymsaum zunehmend schmaler",
        ],
        "kp": "Chronische Obstruktion führt zur Druckatrophie — irreversibler Parenchymverlust, daher zeitnahe Entlastung.",
    },
    120: {
        "mod": "Sono · Niere",
        "dx": "Fortgeschrittene Hydronephrose mit Parenchymverschmälerung (Grad IV).",
        "look": [
            "Nur noch ein schmaler Parenchymsaum um das massiv erweiterte Hohlsystem",
            "„Wasserballon-Niere“ beim terminalen Aufstau",
        ],
        "kp": "Einseitig kompensiert die Gegenseite; beidseitiger Aufstau droht ins postrenale Nierenversagen mit Urämie zu kippen.",
    },
    121: {
        "mod": "Sono · Niere",
        "src": "caption",
        "dx": "Nephrolithiasis — Nierenstein am oberen Pol: echoreiche Raumforderung mit dorsalem Schallschatten, ohne Harnstau.",
        "look": [
            "Echoreicher Fokus im Nierenparenchym mit dorsalem Schallschatten (transhepatischer Längsschnitt rechts)",
            "Die zentralen Nierenanteile sind nicht dilatiert → keine Obstruktion",
        ],
        "kp": "Bei Beschwerdefreiheit ohne Stau abwartend. Symptomatischer oder obstruierender Stein: je nach Größe/Lage ESWL, URS oder Doppel-J.",
    },
    122: {
        "mod": "Sono · Niere",
        "src": "caption",
        "dx": "Nierentumor — solide Raumforderung der Niere, malignitätsverdächtig bis zum Beweis des Gegenteils.",
        "look": [
            "Solide, oft echoarm-inhomogene Raumforderung, die die Nierenkontur vorwölbt",
            "Abgrenzung zur Zyste: solide statt echofrei, keine dorsale Schallverstärkung",
        ],
        "kp": "Häufigster maligner Nierentumor ist das Nierenzellkarzinom. Weiter mit KM-CT/MRT; Therapie meist (partielle) Nephrektomie.",
    },
    123: {
        "mod": "Sono · Niere",
        "src": "caption",
        "dx": "Nierenzyste — echofreie, glatt begrenzte Raumforderung mit dorsaler Schallverstärkung; ein zartes Septum bleibt noch benigne.",
        "look": [
            "Echofrei (schwarz), scharf begrenzt, mit dünner oder kaum sichtbarer Wand",
            "Dorsale Schallverstärkung hinter der Zyste — beweist die Flüssigkeit",
            "Ein einzelnes zartes Septum entspricht Bosniak II: kontrollbedürftig, nicht operationspflichtig",
        ],
        "kp": "Nierenzyste vs. Nierenkarzinom ist die klassische Diskriminierung — echofrei + Schallverstärkung + glatt = benigne; echoarm-solide mit Binnenechos = karzinomverdächtig, dann CT/MRT.",
    },
    124: {
        "mod": "Sono · Pleura",
        "src": "caption",
        "dx": "Pleuraerguss — echofreie Flüssigkeitssichel über dem Zwerchfell im Recessus costodiaphragmaticus.",
        "look": [
            "Echofreier (schwarzer) Saum zwischen Lunge und Zwerchfell im Recessus costodiaphragmaticus",
            "Darüber die Pleuralinie; die belüftete Lunge wirft darunter Schallartefakte",
            "Bei größerem Erguss flottiert die kollabierte Lunge im Erguss — das „Quallenzeichen“",
        ],
        "kp": "Sono erkennt schon ~50 ml und ist damit sensitiver als das Röntgen. Transsudat vs. Exsudat klärt die Punktion über die Light-Kriterien.",
    },
    125: {
        "mod": "Sono · Leber",
        "src": "caption",
        "dx": "Leberzyste — große echofreie Raumforderung am kaudalen Leberrand mit dorsaler Schallverstärkung.",
        "look": [
            "Echofrei, glatt begrenzt, dorsale Schallverstärkung → benigne Zyste (schräger Oberbauchschnitt rechts)",
            "Darmgas-Schallauslöschung kann den kaudalen Zystenrand verdecken",
        ],
        "kp": "Einfache Zyste = Zufallsbefund ohne Konsequenz. Septen, Wandknoten oder Binnenechos machen sie abklärungsbedürftig (Echinokokkus, zystischer Tumor).",
    },
    126: {
        "mod": "Sono · Leber",
        "src": "caption",
        "dx": "Lebermetastase — echoreiche Raumforderung mit echoarmem Randsaum („Halo“) nahe der Bauchwand.",
        "look": [
            "Der echoarme Halo spricht für Malignität",
            "Bei Metastasenverdacht: sonografisch gesteuerte Punktion (Stichkanal einplanen)",
        ],
        "kp": "Immer den Primarius suchen. Die Feinnadelpunktion sichert die Histologie; posteriore Schallverstärkung nicht mit einer Zyste verwechseln.",
    },
    127: {
        "mod": "Sono · Leber",
        "src": "caption",
        "dx": "Lebermetastase eines klarzelligen Nierenzellkarzinoms — massive, inhomogene, infiltrierend wachsende Raumforderung.",
        "look": [
            "Große Raumforderung mit echoreichen und echoarmen Arealen (inhomogen)",
            "Infiltratives Wachstum in das Leberparenchym",
        ],
        "kp": "Das klarzellige Nierenzellkarzinom metastasiert häufig hämatogen (Leber, Lunge, Knochen). Staging mit CT Thorax/Abdomen.",
    },
    128: {
        "mod": "Sono · Leber",
        "src": "caption",
        "dx": "Multiple Lebermetastasen — mehrere Rundherde unterschiedlicher Echogenität, normales Parenchym kaum noch abgrenzbar.",
        "look": [
            "Disseminierte Herde verschiedener Größe und Echogenität (Längsschnitt)",
            "Bei Konfluenz ist normales Leberparenchym nicht mehr abzugrenzen",
        ],
        "kp": "Multiple Herde bedeuten fortgeschrittene Metastasierung. Primariussuche (Kolon, Magen, Pankreas, Mamma, Lunge) und Tumormarker.",
    },
    129: {
        "mod": "Sono · FAST",
        "src": "caption",
        "dx": "Positiver FAST — freie Flüssigkeit im Morison-Pouch, dem hepatorenalen Recessus zwischen Leber und rechter Niere.",
        "look": [
            "Echofreier Streifen genau an der Grenze zwischen Leberunterrand und Nierenkapsel",
            "Der Morison-Pouch ist beim liegenden Patienten der tiefste Punkt des rechten Oberbauchs — hier sammelt sich Blut zuerst",
        ],
        "kp": "Die vier FAST-Fenster: Morison-Pouch, Koller-Pouch (perisplenisch), Douglas-Raum und Perikard. Positiver FAST plus instabiler Patient bedeutet sofortige Laparotomie.",
    },
    130: {
        "mod": "Sono · FAST",
        "dx": "Rechtes Oberbauch-Fenster — Leber und rechte Niere mit dem hepatorenalen Recessus (Morison-Pouch) dazwischen.",
        "look": [
            "Die Leber ist echoreicher als das Nierenparenchym — das ist der normale Kontrast",
            "Der Pfeil markiert die hepatorenale Grenzfläche; genau hier auf einen echofreien Saum als Zeichen freier Flüssigkeit achten",
        ],
        "kp": "Das erste und wichtigste FAST-Fenster. Schallkopf in die rechte mittlere Axillarlinie, subkostal bis interkostal geführt.",
    },
    131: {
        "mod": "Sono · Milz",
        "dx": "Sonographische Darstellung der Milz — homogenes, echoarmes Parenchym unter dem linken Zwerchfell.",
        "look": [
            "Normale Milz: glatt begrenzt, homogen, Poldistanz bis etwa 11 cm",
            "Splenomegalie ab etwa 12–13 cm; die Pole runden sich und wölben sich über die Nierenlinie vor",
        ],
        "kp": "Im linken Oberbauch-Fenster (Koller-Pouch) sammelt sich freie Flüssigkeit perisplenisch. Die Milzruptur ist die häufigste Organverletzung beim stumpfen Bauchtrauma.",
    },
    132: {
        "mod": "Sono · Pankreas",
        "src": "caption",
        "dx": "Normales Pankreas — quer angeschnitten vor der V. lienalis und der Aorta, homogen und glatt begrenzt.",
        "look": [
            "Leitstruktur: die V. lienalis läuft dorsal am Pankreaskorpus entlang und führt einen zum Organ",
            "Homogenes Parenchym, isoechogen bis leicht echoreicher als die Leber; der Ductus pancreaticus ist zart (< 2 mm)",
        ],
        "kp": "Der Pankreasschwanz ist wegen Luftüberlagerung oft schwer einsehbar. Bei V.a. Pankreatitis oder Tumor ergänzt das CT.",
    },
    133: {
        "mod": "Sono · Pankreas",
        "dx": "Pankreas-Sonographie — systematische Beurteilung von Größe, Echogenität und Gang.",
        "look": [
            "Leitgefäß V. lienalis dorsal am Korpus; Kopf rechts, Schwanz nach links",
            "Beurteilen: homogenes Parenchym? Ductus < 2 mm? umschriebene Raumforderung? peripankreatische Flüssigkeit?",
        ],
        "kp": "Akute Pankreatitis: vergrößert, echoarm, peripankreatische Flüssigkeit. Pankreaskarzinom: echoarme Raumforderung mit Gangabbruch (double-duct sign).",
    },
    134: {
        "mod": "Sono · Pankreas",
        "src": "caption",
        "dx": "Autoimmunpankreatitis — diffus vergrößertes, echoarmes „wurstförmiges“ Pankreas ohne umschriebene Raumforderung.",
        "look": [
            "Plump geschwollenes, homogen echoarmes Organ (sausage-shaped) mit glattem Rand",
            "Oft ein schmaler echoarmer Randsaum (Kapsel-Halo); der Gang ist eng, nicht dilatiert",
        ],
        "kp": "IgG4-assoziiert und steroidsensibel. Wichtige DD zum Pankreaskarzinom — dort umschriebene echoarme Raumforderung mit Gangabbruch (double-duct sign).",
    },
    135: {
        "mod": "Sono · Galle",
        "src": "caption",
        "dx": "Cholezystolithiasis — Konkrement in der Gallenblase: echoreicher Reflex mit komplettem dorsalem Schallschatten.",
        "look": [
            "Echoreiches (helles) Areal im Gallenblasenlumen mit glattem Reflex",
            "Dahinter vollständige dorsale Schallauslöschung — das Beweiszeichen des Steins",
            "Lageabhängig: der Stein rollt beim Umlagern nach — so grenzt man ihn vom wandständigen Polypen ab, der haftet und keinen Schatten wirft",
        ],
        "kp": "DAS Top-Sono in Mainz. Kette weiter: symptomatische Steine → OP-Indikation → Cholezystektomie. Eine zusätzlich verdickte Gallenblasenwand (> 3 mm) spricht für eine Cholezystitis.",
    },
}

# ---------------------------------------------------------------------------
CSS = """
  :root{
    --bg:#F7F4EE; --paper:#FFFFFF; --ink:#1A1A1A;
    --ink-muted:#5C5C5C; --ink-soft:#8A8A8A; --rule:#E8E2D6;
    --accent:#1E5F9E; --accent-soft:#E5EEF7;
    --key:#2D7A3E; --key-soft:#E3F1E6;
    --warn:#D97706; --warn-soft:#FDF2E2;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--ink);font-family:'Fraunces',Georgia,serif;font-size:16.5px;line-height:1.6;-webkit-font-smoothing:antialiased}
  .container{max-width:820px;margin:0 auto;padding:40px 24px 90px}
  .back{display:inline-block;font-family:'Manrope',sans-serif;font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-muted);text-decoration:none;margin-bottom:22px}
  .back:hover{color:var(--ink)}
  .eyebrow{font-family:'Manrope',sans-serif;font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-muted);margin-bottom:12px}
  .eyebrow::before{content:"— "}
  h1{font-family:'Fraunces',serif;font-weight:600;font-size:clamp(30px,5vw,44px);line-height:1.05;letter-spacing:-.02em;margin-bottom:12px}
  h1 .accent{font-style:italic;color:var(--accent)}
  .subtitle{font-family:'Fraunces',serif;font-style:italic;font-size:17px;color:var(--ink-muted);margin-bottom:18px;max-width:640px}
  .meta{font-family:'Manrope',sans-serif;font-size:12.5px;color:var(--ink-soft);display:flex;flex-wrap:wrap;align-items:center;margin-bottom:24px}
  .meta span+span::before{content:"•";margin:0 12px}
  .howto{border-left:3px solid var(--accent);background:var(--accent-soft);padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:14px;font-family:'Fraunces',serif;font-size:14.5px;line-height:1.55}
  .howto .lab{font-family:'Manrope',sans-serif;font-style:normal;font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:6px}
  .howto b{font-weight:600}
  .disc{border-left:3px solid var(--warn);background:var(--warn-soft);padding:12px 16px;border-radius:0 8px 8px 0;margin-bottom:30px;font-family:'Manrope',sans-serif;font-size:13px;line-height:1.5;color:#7a4a08}
  .disc .lab{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:10px;color:var(--warn);display:block;margin-bottom:5px}
  .progress{font-family:'Manrope',sans-serif;font-size:12px;color:var(--ink-soft);margin:0 0 26px;padding:10px 14px;background:var(--paper);border:1px solid var(--rule);border-radius:8px}
  .progress b{color:var(--key);font-weight:700}

  .card{background:var(--paper);border:1px solid var(--rule);border-radius:14px;margin-bottom:22px;overflow:hidden}
  .card-top{display:flex;justify-content:space-between;align-items:center;padding:12px 16px 10px;gap:10px}
  .num{font-family:'Manrope',sans-serif;font-size:11px;font-weight:800;letter-spacing:.1em;color:#fff;background:var(--ink);padding:3px 9px;border-radius:5px}
  .modtag{font-family:'Manrope',sans-serif;font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:3px 9px;border-radius:4px;background:var(--accent-soft);color:var(--accent)}
  .modtag.todo{background:#F0EBE0;color:var(--ink-soft)}
  .imgwrap{background:#0d0d0d;text-align:center;line-height:0}
  .imgwrap a{display:block}
  .imgwrap img{max-width:100%;max-height:560px;height:auto;object-fit:contain}
  .bf-open{border-top:1px solid var(--rule);padding:14px 18px 18px}
  .dx{font-family:'Fraunces',serif;font-weight:600;font-size:18px;line-height:1.3;color:var(--ink);margin-bottom:4px}
  .flag{display:inline-block;font-family:'Manrope',sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--warn);background:var(--warn-soft);border:1px solid #f2d9b3;padding:2px 7px;border-radius:4px;margin-bottom:10px}
  .flag.done{color:var(--key);background:var(--key-soft);border-color:#bfe0c6}
  .flag.cap{color:var(--accent);background:var(--accent-soft);border-color:#b9d4ec}
  h4{font-family:'Manrope',sans-serif;font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-muted);margin:12px 0 6px}
  ul{list-style:none;padding-left:2px;margin-bottom:4px}
  li{position:relative;padding-left:18px;margin-bottom:5px;line-height:1.5;font-size:15px;font-family:'Manrope',sans-serif}
  li::before{content:"";position:absolute;left:4px;top:8px;width:6px;height:6px;border-radius:50%;background:var(--accent)}
  .kp{margin-top:10px;background:var(--key-soft);border-left:3px solid var(--key);border-radius:0 6px 6px 0;padding:9px 13px;font-family:'Manrope',sans-serif;font-size:13.5px;line-height:1.45}
  .kp .lab{font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--key);display:block;margin-bottom:3px}
  .folgt{font-family:'Manrope',sans-serif;font-size:14px;color:var(--ink-soft);font-style:italic}
  strong{font-weight:600}
  .tabs{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 6px;background:var(--paper);padding:5px;border-radius:50px;border:1px solid var(--rule);position:sticky;top:8px;z-index:20}
  .tab{flex:1;min-width:150px;padding:12px 10px;font-family:'Manrope',sans-serif;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-muted);background:transparent;border:none;border-radius:50px;cursor:pointer;text-align:center;transition:all .2s ease}
  .tab:hover{color:var(--ink)}
  .tab.active{color:#fff;background:var(--accent)}
  .tab .c{opacity:.6;font-weight:800;margin-left:5px}
  .panel{display:none}
  .panel.active{display:block;animation:fadeIn .25s ease}
  @keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
  .panel-note{font-family:'Manrope',sans-serif;font-size:12.5px;color:var(--ink-soft);margin:16px 0 18px;padding-left:2px;line-height:1.5}
  .panel-note b{color:var(--key);font-weight:700}
  footer{margin-top:46px;padding-top:20px;border-top:1px solid var(--rule);font-family:'Manrope',sans-serif;font-size:11.5px;color:var(--ink-soft);text-align:center}
  @media(max-width:600px){.container{padding:28px 16px 60px}.imgwrap img{max-height:70vh}}
"""

# Sono block = pages 117-135 (contiguous ultrasound run) + 147.
SONO_PAGES = set(range(117, 136)) | {147}

# Non-Sono images placed into category tabs (OCR captions + contact-sheet survey).
_G = {
 "roentgen": [1,3,4,5,8,10,13,14,15,16,17,18,19,27,28,29,31,32,33,34,35,36,37,38,39,40,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,76,77,78,79,80,85,86,87,88,89,90,92,93,94,95,103,104,105,106,107,108],
 "ct":       [2,7,9,11,12,20,21,22,23,24,25,26,30,81,82,83,84,91,97,98,99,100,101,102],
 "mrt":      [75,96,116],
 "haut":     [6,41,42,59,60,61,68,69,70,71,72,73,74,136,137,138,139,140,141,142,143,144,145,146],
 "auge":     [62,63,64,65,66,67],
 "blut":     [109,110,111,112,113,114,115],
 "schema":   [148,149],
}
GROUPS = [
 ("sono","Sonografie","Alle Ultraschallbilder — Niere · Galle · Leber · Pankreas · Milz · FAST · Pleura.", sorted(SONO_PAGES)),
 ("roentgen","Röntgen","Projektionsaufnahmen — Thorax, Schädel/NNH, Skelett und Gelenke.", _G["roentgen"]),
 ("ct","CT","Computertomografie — Schädel, NNH, Thorax, Gefäße.", _G["ct"]),
 ("mrt","MRT","Magnetresonanztomografie — v. a. Schädel.", _G["mrt"]),
 ("haut","Haut / Klinik","Klinische Fotos — Exantheme, Gesicht, Nägel/Hände, Weichteile.", _G["haut"]),
 ("auge","Auge","Fundoskopie — Netzhaut- und Papillenbefunde.", _G["auge"]),
 ("blut","Blut / Labor","Blutausstriche und Zellschemata — Hämatologie.", _G["blut"]),
 ("schema","Schemata","Diagramme und Kurven.", _G["schema"]),
]
# safety net: any page not placed lands in a 'Sonstiges' tab
_placed = set(SONO_PAGES)
for _k,_l,_n,_ps in GROUPS: _placed.update(_ps)
_missing = [i for i in range(1,150) if i not in _placed]
if _missing:
    GROUPS.append(("sonstiges","Sonstiges","Noch nicht zugeordnet.", _missing))


def render_bf(num):
    e = EXPL.get(num)
    if not e:
        return ('<span class="modtag todo">Befund folgt</span>',
                '<div class="bf-open"><p class="folgt">Befund folgt.</p></div>')
    modtag = f'<span class="modtag">{html.escape(e["mod"])}</span>'
    if e.get("ok"):
        flag = '<span class="flag done">bestätigt</span>'
    elif e.get("src") == "caption":
        flag = '<span class="flag cap">aus Bildlegende (OCR)</span>'
    else:
        flag = '<span class="flag">Erstlesung · bitte bestätigen</span>'
    parts = [f'<div class="dx">{html.escape(e["dx"])}</div>', flag]
    if e.get("look"):
        parts.append('<h4>Worauf achten</h4><ul>'
                     + ''.join(f'<li>{x}</li>' for x in e["look"]) + '</ul>')
    if e.get("kp"):
        parts.append(f'<div class="kp"><span class="lab">KP-Anschluss</span>{e["kp"]}</div>')
    inner = ''.join(parts)
    return (modtag, f'<div class="bf-open">{inner}</div>')

def build_card(i):
    img = f"hoffart/p{i:03d}.jpg"
    modtag, bf = render_bf(i)
    return (
        f'<div class="card" id="bild-{i}">'
        f'<div class="card-top"><span class="num">Bild {i}</span>{modtag}</div>'
        f'<div class="imgwrap"><a href="{img}" target="_blank" rel="noopener">'
        f'<img src="{img}" loading="lazy" alt="Prüfungsbild {i}"></a></div>'
        f'{bf}</div>'
    )


def main():
    done = sum(1 for i in range(1, N + 1) if i in EXPL)
    tabs_list, panels_list = [], []
    for gi, (key, label, note, pages) in enumerate(GROUPS):
        pages = [p for p in pages if 1 <= p <= N]
        act = " active" if gi == 0 else ""
        gdone = sum(1 for p in pages if p in EXPL)
        tabs_list.append(f'<button class="tab{act}" data-t="{key}">{label}<span class="c">{len(pages)}</span></button>')
        cards = "\n".join(build_card(p) for p in pages)
        bfnote = f' Befunde: <b>{gdone}/{len(pages)}</b>.' if gdone else ' Befunde folgen.'
        panels_list.append(f'<section class="panel{act}" data-p="{key}">\n    <p class="panel-note">{note} ({len(pages)} Bilder).{bfnote}</p>\n{cards}\n  </section>')
    tabs_block = "\n    ".join(tabs_list)
    panels_block = "\n\n  ".join(panels_list)
    doc = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hoffart Bildatlas · {N} Prüfungsbilder</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="container">
  <a href="../index.html" class="back">← Zurück zur Library</a>
  <header>
    <div class="eyebrow">Hoffart · Bildatlas</div>
    <h1>Prüfungs<span class="accent">bilder</span></h1>
    <p class="subtitle">Die {N} Bilder aus der Sammlung von Dr. Hoffart — genau die Sono-, CT- und Röntgenbilder, die in Mainz gezeigt werden. Bild ansehen, Befund laut formulieren, dann aufdecken.</p>
    <div class="meta"><span>{N} Bilder</span><span>nach Kategorie</span><span>Befunde wachsen laufend</span></div>
  </header>

  <div class="howto"><span class="lab">So nutzen</span>
  Bild anschauen, in einem Satz den Befund und die Verdachtsdiagnose formulieren (<i>„Ich sehe … das spricht für …"</i>), dann mit dem Befund direkt darunter vergleichen. Zum Vergrößern aufs Bild tippen.</div>

  <div class="disc"><span class="lab">Wichtig</span>
  Die aufgedeckten Befunde sind Claudes <b>Erstlesung</b> und tragen bis zu deiner fachlichen Bestätigung den Hinweis „bitte bestätigen". Bilder ohne Befund zeigen „Befund folgt".</div>

  <div class="tabs">
    {tabs_block}
  </div>

  {panels_block}

  <footer>Hoffart-Bildatlas · {N} Prüfungsbilder · Quelle: Bilder Dr. Hoffart (WhatsApp-Gruppe) · Befunde: Claude-Erstlesung, fachlich zu bestätigen</footer>
</div>
<script>
  const tabs=[...document.querySelectorAll('.tab')];
  const panels=[...document.querySelectorAll('.panel')];
  tabs.forEach(t=>t.addEventListener('click',()=>{{
    tabs.forEach(x=>x.classList.toggle('active',x===t));
    panels.forEach(p=>p.classList.toggle('active',p.dataset.p===t.dataset.t));
    window.scrollTo({{top:0,behavior:'smooth'}});
  }}));
</script>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}  (" + " | ".join(f"{l} {len([p for p in ps if 1<=p<=N])}" for _,l,_,ps in GROUPS) + ")")

if __name__ == "__main__":
    main()
