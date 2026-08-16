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


def to_print_html(path: pathlib.Path, mode: str = "full", flow: bool = False,
                  fit: int = 0) -> str:
    html = path.read_text(encoding="utf-8")
    html = _strip(html)
    html = _stations(html)
    # jedes <details> aufklappen
    html = re.sub(r"<details(?![^>]*\sopen)", "<details open", html)
    # .station wie .panel behandeln (Legacy)
    html = html.replace('class="station active"', 'class="panel"')

    css = PRINT_CSS.read_text(encoding="utf-8")
    html = html.replace("</head>", f"<style>\n{css}\n</style>\n</head>", 1)

    cls = " ".join(c for c in (mode if mode != "full" else "",
                               "flow" if flow else "",
                               f"fit-{fit}" if fit else "") if c)
    # Die Themenseiten tragen eine fest eingebackene fit-Klasse fuer den
    # Browserdruck. Beim Rendern wird sie ersetzt, nicht ergaenzt.
    html = re.sub(r'<body[^>]*>', f'<body class="{cls}">', html, count=1)
    if mode == "quiz":
        html = re.sub(r'(<div class="stationband[^>]*>.*?</div>)', r"\1" + QUIZ_NOTE,
                      html, count=0, flags=re.S)
    return html



# Sollwerte je Station: Tabs 1-4 und Perlen und Rapid-Fire je eine Seite.
# Tab 6 (Fragen & Protokolle) darf mehrere Seiten belegen, wird aber mitgezaehlt,
# damit die Automatik auch dort die kompakteste Stufe waehlt.
_HEADS = ("GRUNDLAGEN", "KLINIK", "DIAGNOSTIK", "THERAPIE",
          "KP-PERLEN", "FRAGEN & PROTOKOLLE", "RETRIEVAL", "NACHFRAGEN")


def _page_heads(doc):
    """Erste Textfragmente je Seite — daraus laesst sich die Station ablesen."""
    out = []
    for pg in doc.pages:
        txt = []

        def walk(b):
            if getattr(b, "text", None):
                txt.append(b.text)
            for c in getattr(b, "children", None) or []:
                walk(c)

        for b in pg._page_box.children:
            walk(b)
        out.append(" ".join(txt[:8]))
    return out


def _overflow(doc):
    """Zaehlt Stationen, die mehr als eine Seite belegen (Tab 6 ausgenommen)."""
    cur, bad, rapid, inrapid = None, 0, 0, False
    seen = {}
    for h in _page_heads(doc):
        up = h.upper()
        # Rapid-Fire nur erkennen, wenn die Seite damit BEGINNT. Manche
        # Perlen-Intros erwaehnen das Wort ("Acht Stolpersteine und die
        # Rapid-Fire ..."), was sonst die Perlen-Seite falsch zaehlt.
        if re.match(r"^(SCHNELLFRAGEN[^A-Z]{0,4})?RAPID-FIRE", up):
            inrapid, rapid = True, rapid + 1
            continue
        # Nur ein Stationsband am Seitenanfang zaehlt. Der Eyebrow auf Seite 1
        # enthaelt Woerter wie "KURZ + KP-PERLEN + PROTOKOLLE" und wuerde sonst
        # faelschlich als Stationswechsel gelten.
        key = next((k for k in _HEADS
                    if re.match(rf"^{re.escape(k)}\s+\d+\s*/\s*\d+", up)), None)
        if key:
            cur, inrapid = key, False
        if inrapid:
            rapid += 1
            continue
        if cur:
            seen[cur] = seen.get(cur, 0) + 1
    for k, n in seen.items():
        if k != "FRAGEN & PROTOKOLLE" and n > 1:
            bad += n - 1
    if rapid > 1:
        bad += rapid - 1
    return bad, sum(seen.values()) + rapid


# Safari und Chrome setzen etwas grosszuegiger als WeasyPrint. Fuer die
# eingebackene Klasse wird deshalb gegen ein um SAFETY_MM verkuerztes Blatt
# geprueft — was so noch passt, passt auch im Browser.
SAFETY_MM = 12


def render_fitted(path, mode, flow, max_fit=4, safety=0):
    """Rendert mit der lockersten Stufe, bei der keine Station umbricht."""
    from weasyprint import HTML
    best = None
    for fit in range(0, max_fit + 1):
        html = to_print_html(path, mode, flow, fit)
        if safety:
            html = html.replace("</head>",
                                f"<style>@page{{margin-bottom:{16 + safety}mm}}</style></head>", 1)
        doc = HTML(string=html, base_url=str(path)).render()
        bad, _ = _overflow(doc)
        if best is None:
            best = (doc, fit, bad)
        if bad < best[2]:
            best = (doc, fit, bad)
        if bad == 0:
            return doc, fit, 0
    return best


def render(paths, out_dir: pathlib.Path, mode: str, flow: bool, merge):
    from weasyprint import HTML

    out_dir.mkdir(parents=True, exist_ok=True)
    docs, names = [], []
    for p in paths:
        doc, fit, bad = render_fitted(p, mode, flow)
        docs.append(doc)
        names.append(p)
        if not merge:
            suffix = "" if mode == "full" else f"-{mode}"
            target = out_dir / f"{p.stem}{suffix}.pdf"
            doc.write_pdf(target)
            note = f" · fit-{fit}" if fit else ""
            warn = f"  ⚠ {bad} Station(en) laufen ueber" if bad else ""
            print(f"  ✓ {p.relative_to(ROOT)} → {target.name}  "
                  f"({len(doc.pages)} S.{note}){warn}")

    if merge:
        pages = [pg for d in docs for pg in d.pages]
        target = out_dir / merge
        docs[0].copy(pages).write_pdf(target)
        print(f"  ✓ {len(names)} Themen → {target.name}  ({len(pages)} S.)")


def write_fit(paths, max_fit=4):
    """Schreibt class="fit-N" in das <body> jeder Themenseite.

    Der Browserdruck (Safari, Chrome) kennt die Fit-Stufen sonst nicht — er
    saehe immer fit-0, und die 25 Decks, die eine engere Stufe brauchen,
    liefen ueber. Die Klasse wirkt nur im Druck, weil print.css mit
    media="print" eingebunden ist.
    """
    import re as _re
    changed = 0
    for p in paths:
        _, fit, bad = render_fitted(p, "full", False, max_fit, safety=SAFETY_MM)
        src = p.read_text(encoding="utf-8")
        want = f' class="fit-{fit}"' if fit else ""
        new = _re.sub(r'<body[^>]*>', f"<body{want}>", src, count=1)
        if new != src:
            p.write_text(new, encoding="utf-8")
            changed += 1
        flag = f"  ⚠ {bad} Überlauf" if bad else ""
        print(f"  {p.stem:<34} fit-{fit}{flag}")
    print(f"\n  {changed} Datei(en) geaendert")


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
    ap.add_argument("--write-fit", action="store_true",
                    help="fit-Klasse fest in die HTML-Dateien schreiben (fuer Browserdruck)")
    a = ap.parse_args()

    paths = sorted(ROOT.glob("reviews/*/*.html")) if a.all else \
        [pathlib.Path(f).resolve() for f in a.files]
    if not paths:
        ap.error("keine Datei angegeben (--all oder Pfade)")

    if a.write_fit:
        print(f"fit-Klassen schreiben · {len(paths)} Datei(en) "
              f"· Sicherheitsreserve {SAFETY_MM} mm")
        write_fit(paths)
        return

    print(f"Drucklayout: {a.mode} · {'fortlaufend' if a.flow else 'Seite je Station'} "
          f"· {len(paths)} Datei(en)")
    render(paths, pathlib.Path(a.out), a.mode, a.flow, a.merge)


if __name__ == "__main__":
    main()
