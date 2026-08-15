#!/usr/bin/env python3
"""
tools/_build-pdf.py — Standard-Drucklayout (A4) für alle Themenseiten.

Ein Layout für die ganze Bibliothek: /print.css (auch für Ctrl+P im Browser).
Die Seite wird vor dem Rendern entfaltet (alle Tabs sichtbar, alle
<details> offen, Bildschirm-Chrome entfernt), dann via WeasyPrint gesetzt.

    python3 tools/_build-pdf.py reviews/chirurgie/cholezystitis.html
    python3 tools/_build-pdf.py --all
    python3 tools/_build-pdf.py reviews/kardiologie/*.html --merge kardiologie.pdf
    python3 tools/_build-pdf.py --all --mode quiz          # Antworten verdeckt
    python3 tools/_build-pdf.py --all --flow               # ohne Seitenumbruch je Station

Abhängigkeit:  pip install weasyprint --break-system-packages
Schriften:     Fraunces + Manrope müssen systemweit installiert sein
               (sonst fällt WeasyPrint auf Serif/Sans zurück — Layout bleibt gültig).
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRINT_CSS = ROOT / "print.css"

# Stationsname + Farbklasse je data-panel
STATIONS = {
    "retrieval":  "Retrieval",
    "grundlagen": "Grundlagen",
    "klinik":     "Klinik",
    "diagnostik": "Diagnostik",
    "therapie":   "Therapie",
    "fragen":     "KP-Fragen",
    "perlen":     "KP-Perlen",
    "protokoll":  "Fragen & Protokolle",
    "nachfragen": "Nachfragen",
}
LEGACY_COLOR = ["grundlagen", "klinik", "diagnostik", "therapie",
                "fragen", "perlen", "protokoll"]

QUIZ_NOTE = ('<p class="quiz-note">Prüfmodus — Antworten verdeckt. '
             'Erst laut antworten, dann auf der Volldruck-Version kontrollieren.</p>')


def _strip(html: str) -> str:
    """Bildschirm-Chrome und alles Interaktive entfernen."""
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<script\b[^>]*/?>", "", html)
    html = re.sub(r'<div class="tabs">.*?</div>', "", html, flags=re.S)
    html = re.sub(r"<footer\b.*?</footer>", "", html, flags=re.S)
    html = re.sub(r'<a[^>]*class="back"[^>]*>.*?</a>', "", html, flags=re.S)
    html = re.sub(r'<div class="ctrl">.*?</div>\s*</div>\s*</div>', "", html, flags=re.S)
    # Webfont-Links: offline nutzlos, kosten nur Renderzeit
    html = re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>', "", html)
    return html


def _band(key: str, label: str, idx: int, total: int) -> str:
    return (f'<div class="stationband sb-{key}"><span class="sb-t">{label}</span>'
            f'<span class="sb-n">{idx} / {total}</span></div>')


def _stations(html: str) -> str:
    """Alle Panels sichtbar machen und je Station ein Farbband einziehen."""
    keys = re.findall(r'<section class="panel[^"]*" data-panel="([a-z0-9-]+)"', html)
    if keys:
        total = len(keys)
        seq = iter(range(1, total + 1))

        def sub(m):
            key = m.group(1)
            label = STATIONS.get(key, key.capitalize())
            return (f'<section class="panel" data-panel="{key}">'
                    + _band(key, label, next(seq), total))

        return re.sub(r'<section class="panel[^"]*" data-panel="([a-z0-9-]+)"\s*>',
                      sub, html)

    # Legacy-Variante: <section class="station" id="sN"> + Tab-Beschriftungen
    labels = re.findall(r'<button class="tab[^"]*"[^>]*>(.*?)</button>', html, flags=re.S)
    labels = [re.sub(r"<[^>]+>", "", x).strip() for x in labels]
    ids = re.findall(r'<section class="station[^"]*" id="(s\d+)"', html)
    total = len(ids)

    def sub2(m):
        n = int(m.group(1)[1:])
        label = labels[n - 1] if n <= len(labels) else f"Station {n}"
        key = LEGACY_COLOR[(n - 1) % len(LEGACY_COLOR)]
        return (f'<section class="panel station" id="{m.group(1)}">'
                + _band(key, label, n, total))

    return re.sub(r'<section class="station[^"]*" id="(s\d+)"\s*>', sub2, html)


def to_print_html(path: pathlib.Path, mode: str = "full", flow: bool = False) -> str:
    html = path.read_text(encoding="utf-8")
    html = _strip(html)
    html = _stations(html)
    # jedes <details> aufklappen
    html = re.sub(r"<details(?![^>]*\sopen)", "<details open", html)
    # .station wie .panel behandeln (Legacy)
    html = html.replace('class="station active"', 'class="panel"')

    css = PRINT_CSS.read_text(encoding="utf-8")
    html = html.replace("</head>", f"<style>\n{css}\n</style>\n</head>", 1)

    cls = " ".join(c for c in (mode if mode != "full" else "", "flow" if flow else "") if c)
    html = html.replace("<body>", f'<body class="{cls}">', 1)
    if mode == "quiz":
        html = re.sub(r'(<div class="stationband[^>]*>.*?</div>)', r"\1" + QUIZ_NOTE,
                      html, count=0, flags=re.S)
    return html


def render(paths, out_dir: pathlib.Path, mode: str, flow: bool, merge):
    from weasyprint import HTML

    out_dir.mkdir(parents=True, exist_ok=True)
    docs, names = [], []
    for p in paths:
        html = to_print_html(p, mode, flow)
        doc = HTML(string=html, base_url=str(p)).render()
        docs.append(doc)
        names.append(p)
        if not merge:
            suffix = "" if mode == "full" else f"-{mode}"
            target = out_dir / f"{p.stem}{suffix}.pdf"
            doc.write_pdf(target)
            print(f"  ✓ {p.relative_to(ROOT)} → {target.name}  ({len(doc.pages)} S.)")

    if merge:
        pages = [pg for d in docs for pg in d.pages]
        target = out_dir / merge
        docs[0].copy(pages).write_pdf(target)
        print(f"  ✓ {len(names)} Themen → {target.name}  ({len(pages)} S.)")


def main():
    ap = argparse.ArgumentParser(description="Standard-PDF-Layout für Themenseiten")
    ap.add_argument("files", nargs="*", help="Pfade zu reviews/*/*.html")
    ap.add_argument("--all", action="store_true", help="alle Themenseiten")
    ap.add_argument("--out", default="/mnt/user-data/outputs/pdf", help="Zielordner")
    ap.add_argument("--mode", choices=["full", "quiz"], default="full",
                    help="full = mit Antworten (Standard), quiz = Antworten verdeckt")
    ap.add_argument("--flow", action="store_true",
                    help="fortlaufend statt eine neue Seite je Station")
    ap.add_argument("--merge", metavar="DATEI.pdf", help="alles in eine PDF zusammenführen")
    a = ap.parse_args()

    paths = sorted(ROOT.glob("reviews/*/*.html")) if a.all else \
        [pathlib.Path(f).resolve() for f in a.files]
    if not paths:
        ap.error("keine Datei angegeben (--all oder Pfade)")

    print(f"Drucklayout: {a.mode} · {'fortlaufend' if a.flow else 'Seite je Station'} "
          f"· {len(paths)} Datei(en)")
    render(paths, pathlib.Path(a.out), a.mode, a.flow, a.merge)


if __name__ == "__main__":
    main()
