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
    124: {
        "mod": "Sono · Pleura",
        "dx": "Pleuraerguss — echofreie Flüssigkeitssichel über dem Zwerchfell im Recessus costodiaphragmaticus.",
        "look": [
            "Echofreier (schwarzer) Saum zwischen Lunge und Zwerchfell im Recessus costodiaphragmaticus",
            "Darüber die Pleuralinie; die belüftete Lunge wirft darunter Schallartefakte",
            "Bei größerem Erguss flottiert die kollabierte Lunge im Erguss — das „Quallenzeichen“",
        ],
        "kp": "Sono erkennt schon ~50 ml und ist damit sensitiver als das Röntgen. Transsudat vs. Exsudat klärt die Punktion über die Light-Kriterien.",
    },
    129: {
        "mod": "Sono · FAST",
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
        "dx": "Normales Pankreas — quer angeschnitten vor der V. lienalis und der Aorta, homogen und glatt begrenzt.",
        "look": [
            "Leitstruktur: die V. lienalis läuft dorsal am Pankreaskorpus entlang und führt einen zum Organ",
            "Homogenes Parenchym, isoechogen bis leicht echoreicher als die Leber; der Ductus pancreaticus ist zart (< 2 mm)",
        ],
        "kp": "Der Pankreasschwanz ist wegen Luftüberlagerung oft schwer einsehbar. Bei V.a. Pankreatitis oder Tumor ergänzt das CT.",
    },
    134: {
        "mod": "Sono · Pankreas",
        "dx": "Autoimmunpankreatitis — diffus vergrößertes, echoarmes „wurstförmiges“ Pankreas ohne umschriebene Raumforderung.",
        "look": [
            "Plump geschwollenes, homogen echoarmes Organ (sausage-shaped) mit glattem Rand",
            "Oft ein schmaler echoarmer Randsaum (Kapsel-Halo); der Gang ist eng, nicht dilatiert",
        ],
        "kp": "IgG4-assoziiert und steroidsensibel. Wichtige DD zum Pankreaskarzinom — dort umschriebene echoarme Raumforderung mit Gangabbruch (double-duct sign).",
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
  .bf{border-top:1px solid var(--rule)}
  .bf>summary{cursor:pointer;list-style:none;padding:12px 16px;font-family:'Manrope',sans-serif;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--key);display:flex;align-items:center;gap:8px}
  .bf>summary::-webkit-details-marker{display:none}
  .bf>summary::before{content:"▸";color:var(--key);font-weight:700}
  .bf[open]>summary::before{content:"▾"}
  .bf[open]>summary{border-bottom:1px dashed var(--rule)}
  .bf-inner{padding:14px 18px 18px}
  .dx{font-family:'Fraunces',serif;font-weight:600;font-size:18px;line-height:1.3;color:var(--ink);margin-bottom:4px}
  .flag{display:inline-block;font-family:'Manrope',sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--warn);background:var(--warn-soft);border:1px solid #f2d9b3;padding:2px 7px;border-radius:4px;margin-bottom:10px}
  .flag.done{color:var(--key);background:var(--key-soft);border-color:#bfe0c6}
  h4{font-family:'Manrope',sans-serif;font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-muted);margin:12px 0 6px}
  ul{list-style:none;padding-left:2px;margin-bottom:4px}
  li{position:relative;padding-left:18px;margin-bottom:5px;line-height:1.5;font-size:15px;font-family:'Manrope',sans-serif}
  li::before{content:"";position:absolute;left:4px;top:8px;width:6px;height:6px;border-radius:50%;background:var(--accent)}
  .kp{margin-top:10px;background:var(--key-soft);border-left:3px solid var(--key);border-radius:0 6px 6px 0;padding:9px 13px;font-family:'Manrope',sans-serif;font-size:13.5px;line-height:1.45}
  .kp .lab{font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--key);display:block;margin-bottom:3px}
  .folgt{font-family:'Manrope',sans-serif;font-size:14px;color:var(--ink-soft);font-style:italic}
  strong{font-weight:600}
  footer{margin-top:46px;padding-top:20px;border-top:1px solid var(--rule);font-family:'Manrope',sans-serif;font-size:11.5px;color:var(--ink-soft);text-align:center}
  @media(max-width:600px){.container{padding:28px 16px 60px}.imgwrap img{max-height:70vh}}
"""

def render_bf(num):
    e = EXPL.get(num)
    if not e:
        return ('<span class="modtag todo">Befund folgt</span>',
                '<details class="bf"><summary>Befund aufdecken</summary>'
                '<div class="bf-inner"><p class="folgt">Befund wird in einem '
                'geprüften Durchgang ergänzt.</p></div></details>')
    modtag = f'<span class="modtag">{html.escape(e["mod"])}</span>'
    ok = e.get("ok")
    flag = ('<span class="flag done">bestätigt</span>' if ok
            else '<span class="flag">Erstlesung · bitte bestätigen</span>')
    parts = [f'<div class="dx">{html.escape(e["dx"])}</div>', flag]
    if e.get("look"):
        parts.append('<h4>Worauf achten</h4><ul>'
                     + ''.join(f'<li>{x}</li>' for x in e["look"]) + '</ul>')
    if e.get("kp"):
        parts.append(f'<div class="kp"><span class="lab">KP-Anschluss</span>{e["kp"]}</div>')
    inner = ''.join(parts)
    return (modtag,
            f'<details class="bf"><summary>Befund aufdecken</summary>'
            f'<div class="bf-inner">{inner}</div></details>')

def main():
    cards = []
    for i in range(1, N + 1):
        img = f"hoffart/p{i:03d}.jpg"
        modtag, bf = render_bf(i)
        cards.append(
            f'<div class="card" id="bild-{i}">'
            f'<div class="card-top"><span class="num">Bild {i}</span>{modtag}</div>'
            f'<div class="imgwrap"><a href="{img}" target="_blank" rel="noopener">'
            f'<img src="{img}" loading="lazy" alt="Prüfungsbild {i}"></a></div>'
            f'{bf}</div>'
        )
    done = sum(1 for i in range(1, N + 1) if i in EXPL)
    body = "\n".join(cards)
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
    <div class="meta"><span>{N} Bilder</span><span>Sono · CT · Röntgen · Klinik</span><span>Befunde wachsen laufend</span></div>
  </header>

  <div class="howto"><span class="lab">So nutzen</span>
  Das ist ein <b>Erkennungs-Drill</b>, kein Text zum Durchlesen: Bild anschauen, in einem Satz den Befund und die Verdachtsdiagnose sagen (<i>„Ich sehe … das spricht für …"</i>), <b>dann</b> „Befund aufdecken". Zum Vergrößern aufs Bild tippen.</div>

  <div class="disc"><span class="lab">Wichtig</span>
  Die aufgedeckten Befunde sind Claudes <b>Erstlesung</b> und tragen bis zu deiner fachlichen Bestätigung den Hinweis „bitte bestätigen". Bilder ohne Befund zeigen „Befund folgt" — die ergänze ich batch-weise nach geprüftem Durchgang.</div>

  <p class="progress">Befunde ergänzt: <b>{done}</b> von {N} · Sono-Batch läuft — als Nächstes die reinen Ultraschall-Serien (Niere · Leber · Galle).</p>

{body}

  <footer>Hoffart-Bildatlas · {N} Prüfungsbilder · Quelle: Bilder Dr. Hoffart (WhatsApp-Gruppe) · Befunde: Claude-Erstlesung, fachlich zu bestätigen</footer>
</div>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}  ({N} cards, {done} Befunde seeded)")

if __name__ == "__main__":
    main()
