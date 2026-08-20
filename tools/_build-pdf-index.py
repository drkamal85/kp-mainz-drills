#!/usr/bin/env python3
"""
tools/_build-pdf-index.py — erzeugt print-pdf.html, die Druckseite der Bibliothek.

Liest, welche PDFs unter pdf/ tatsaechlich liegen, und baut daraus eine Seite
mit Downloadlinks: je Thema die Vollversion und den Pruefmodus, dazu die
Sammel-PDFs je Fachgruppe.

Wird von der Action build-pdfs.yml aufgerufen, nachdem gerendert wurde.
"""
import json
import pathlib
import re
import html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "pdf"

FACH = {
    "kardiologie": "Kardiologie",
    "chirurgie": "Allgemein- und Viszeralchirurgie",
    "pneumologie": "Pneumologie",
    "unfallchirurgie": "Unfallchirurgie",
    "drittes-fach": "Drittes Fach",
    "notfallmedizin": "Notfallmedizin",
    "gefaesschirurgie": "Gefäßchirurgie",
    "neurologie": "Neurologie",
    "endokrinologie": "Endokrinologie",
    "haematologie": "Hämatologie",
    "gastroenterologie": "Gastroenterologie",
}


def titel(p: pathlib.Path) -> str:
    """Titel aus der Themenseite ziehen, sonst den Dateinamen aufhübschen."""
    src = ROOT / "reviews"
    for f in src.glob(f"*/{p.stem}.html"):
        m = re.search(r"<title>([^<·]+)", f.read_text(encoding="utf-8"))
        if m:
            # Der Titel im Quelltext ist bereits HTML-kodiert ("GERD &amp; ...").
            # Erst dekodieren, dann einmal sauber kodieren — sonst steht
            # "&amp;amp;" auf der Seite.
            return H.escape(H.unescape(m.group(1).strip()))
    return p.stem.replace("-", " ").title()


def fach_of(stem: str) -> str:
    for f in (ROOT / "reviews").glob(f"*/{stem}.html"):
        return f.parent.name
    return "sonstige"


def kb(p: pathlib.Path) -> str:
    return f"{p.stat().st_size // 1024} KB"


def main():
    if not PDF.is_dir():
        raise SystemExit("pdf/ fehlt — erst rendern lassen")

    voll = sorted(p for p in PDF.glob("*.pdf"))
    quiz = {p.stem.removesuffix("-quiz"): p for p in (PDF / "quiz").glob("*.pdf")}
    sammel = sorted((PDF / "fach").glob("*.pdf"))

    gruppen: dict[str, list[pathlib.Path]] = {}
    for p in voll:
        gruppen.setdefault(fach_of(p.stem), []).append(p)

    rows = []
    for key in list(FACH) + [k for k in gruppen if k not in FACH]:
        items = gruppen.get(key)
        if not items:
            continue
        name = FACH.get(key, key.replace("-", " ").title())
        merged = PDF / "fach" / f"{key}.pdf"
        head = f'<h2>{H.escape(name)} <span class="n">{len(items)}</span>'
        if merged.exists():
            head += (f' <a class="all" href="pdf/fach/{key}.pdf">'
                     f'Alle als eine Datei · {kb(merged)}</a>')
        head += "</h2>"
        li = []
        for p in items:
            q = quiz.get(p.stem)
            extra = (f'<a class="q" href="pdf/quiz/{q.name}">Prüfmodus</a>' if q else "")
            li.append(
                f'<li><a class="t" href="pdf/{p.name}">{titel(p)}</a>'
                f'<span class="s">{kb(p)}</span>{extra}</li>'
            )
        rows.append(head + '<ul class="grid">' + "".join(li) + "</ul>")

    page = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Druckfassungen · KP Mainz Drills</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Manrope', sans-serif; background: #F7F4EE; color: #23201D;
         line-height: 1.5; padding: 28px 18px 60px; }}
  .wrap {{ max-width: 860px; margin: 0 auto; }}
  .back {{ display: inline-block; font-size: 13px; color: #6B6358;
           text-decoration: none; margin-bottom: 18px; }}
  .back:hover {{ color: #23201D; }}
  .eyebrow {{ font-size: 11px; font-weight: 800; letter-spacing: .18em;
              text-transform: uppercase; color: #0F766E; margin-bottom: 8px; }}
  h1 {{ font-family: 'Fraunces', serif; font-weight: 500; font-size: 34px;
        line-height: 1.06; letter-spacing: -.01em; }}
  h1 .accent {{ font-style: italic; color: #B45309; }}
  .sub {{ font-family: 'Fraunces', serif; font-size: 15px; color: #6B6358;
          margin-top: 10px; line-height: 1.45; }}
  .note {{ background: #FFFDF8; border: 1px solid #DCD5C6; border-left: 3px solid #1E5F9E;
           border-radius: 8px; padding: 12px 15px; margin: 22px 0 8px; font-size: 13.5px; }}
  .note b {{ display: block; font-size: 11px; letter-spacing: .12em; text-transform: uppercase;
             color: #1E5F9E; margin-bottom: 5px; }}
  h2 {{ font-family: 'Fraunces', serif; font-weight: 500; font-size: 21px;
        margin: 32px 0 12px; padding-bottom: 7px; border-bottom: 2px solid #23201D;
        display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }}
  h2 .n {{ font-family: 'Manrope', sans-serif; font-size: 11px; font-weight: 700;
           background: #EDE7DA; color: #6B6358; border-radius: 999px; padding: 2px 9px; }}
  h2 .all {{ font-family: 'Manrope', sans-serif; font-size: 12px; font-weight: 700;
             color: #0F766E; text-decoration: none; margin-left: auto; }}
  h2 .all:hover {{ text-decoration: underline; }}
  ul.grid {{ list-style: none; display: grid; gap: 7px; }}
  ul.grid li {{ background: #FFFDF8; border: 1px solid #DCD5C6; border-radius: 8px;
                padding: 10px 13px; display: flex; align-items: center; gap: 10px; }}
  a.t {{ font-weight: 700; font-size: 14.5px; color: #23201D; text-decoration: none; flex: 1; }}
  a.t:hover {{ color: #B45309; }}
  .s {{ font-size: 11.5px; color: #A8A093; }}
  a.q {{ font-size: 11.5px; font-weight: 700; color: #7B3F9E; text-decoration: none;
         border: 1px solid #E2D5EE; border-radius: 999px; padding: 3px 10px; }}
  a.q:hover {{ background: #F6EFFB; }}
  footer {{ margin-top: 44px; padding-top: 16px; border-top: 1px solid #DCD5C6;
            font-size: 12px; color: #A8A093; }}
</style>
</head>
<body>
<div class="wrap">

  <a href="index.html" class="back">← Zurück zur Library</a>

  <div class="eyebrow">KP Mainz Drills</div>
  <h1>Druck<span class="accent">fassungen</span></h1>
  <div class="sub">Fertig gesetzte PDFs im A4-Standardlayout — laufende Kopfzeile, Seitenzahl,
  Stationsbänder in Stationsfarbe und Lesezeichen. Jede Station auf einer Seite,
  KP-Perlen und Rapid-Fire getrennt.</div>

  <div class="note"><b>Warum nicht einfach drucken</b>
  Safari und Chrome ignorieren die Kopf- und Fußzeilen des Seitenlayouts. Diese Dateien
  werden bei jeder Änderung serverseitig neu gesetzt und enthalten das vollständige Format.
  Im <b style="display:inline;color:#7B3F9E">Prüfmodus</b> sind die Antworten in
  Fragen &amp; Protokolle und Rapid-Fire verdeckt.</div>

  {"".join(rows)}

  <footer>Automatisch gebaut aus den Themenseiten · Layout siehe HANDOFF Abschnitt 11</footer>

</div>
</body>
</html>
"""
    out = ROOT / "print-pdf.html"
    out.write_text(page, encoding="utf-8")
    print(f"  print-pdf.html: {len(voll)} Themen, {len(quiz)} Prüfmodus, "
          f"{len(sammel)} Sammel-PDFs, {len(page)} bytes")


if __name__ == "__main__":
    main()
