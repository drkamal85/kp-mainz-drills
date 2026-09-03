#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/_print-topic.py — rendert eine Themenseite als A4-PDF in Graustufen.

    python3 tools/_print-topic.py <slug> [ziel.pdf]

Layout: eine Themenseite, alle Stationen ausgeklappt, ohne Farbe.
Der Inhalt fliesst durch — Stationen beginnen NICHT auf einer neuen Seite,
sonst entstehen halbleere Blaetter. Karten und Tabellen werden aber nie
ueber einen Seitenumbruch zerrissen.

Grundlage ist print.css. Die Graustufenregeln stehen hier, weil sie nur
fuer den Papierdruck gelten und die Bildschirmfassung farbig bleiben soll.
"""
import glob
import io
import re
import sys

GRAY = '''
/* ---------- Graustufen: Hierarchie ueber Linien statt Farbe ---------- */
*, *::before, *::after { color: #1a1a1a !important; }
strong, b { color: #000 !important; }
a { color: #1a1a1a !important; text-decoration: none !important; }
.accent { color: #1a1a1a !important; }
.eyebrow, .subtitle, .panel-intro { color: #3a3a3a !important; }

.card, details.card { border-left-color: #4a4a4a !important; }
.card.grundlagen, .card.klinik, .card.diagnostik, .card.therapie { border-left-width: 2.4pt !important; }
.callout, .cal { background: #F2F2F2 !important; border-left: 2pt solid #4a4a4a !important; }
.callout.critical { border-left-color: #1a1a1a !important; background: #EAEAEA !important; }
.callout.warn { border-left-color: #4a4a4a !important; background: #F0F0F0 !important; border-left-style: dashed !important; }
.callout.fact { background: #F6F6F6 !important; }
.lab { color: #3a3a3a !important; font-weight: 700 !important; }
table.dd th, table th { background: #EDEDED !important; color: #1a1a1a !important; }
table.dd td, table td { border-color: #C8C8C8 !important; }
.pk { border-left: 2.4pt solid #4a4a4a !important; background: #FAFAFA !important; }
.pk-badge { background: #DEDEDE !important; }
.sf-wrap, .sf-wrap *, .sf, .sfa, .sf-intro { background: transparent !important; color: #1a1a1a !important; }
.sf-wrap { background: #F4F4F4 !important; border: .5pt solid #C8C8C8 !important; }
.sf { border-bottom: .4pt solid #D2D2D2 !important; }
.sf summary { color: #000 !important; font-weight: 700 !important; }
.sfa { color: #333 !important; }
.pearl { background: #F7F7F7 !important; border-left: 2.4pt solid #4a4a4a !important; }
.ph { color: #1a1a1a !important; }
.mn { background: #EBEBEB !important; }
.pt { color: #262626 !important; }

/* print.css setzt die Marken mit !important - hier ueberschreiben */
.meta .rk, .meta .rk.hi, .meta .rk.mid, .meta .rk.lo,
.meta .tier, .meta .tier.kern, .meta .tier.std, .meta .tier.rand, .meta > span {
  background: #E4E4E4 !important; color: #1f1f1f !important; border: .5pt solid #AFAFAF !important;
}
.meta .tier .zt { color: #454545 !important; }

/* ---------- alles ausklappen, Bedienelemente weg ---------- */
.panel { display: block !important; }
.tabs, .back, .plus, .toggle { display: none !important; }
details, details.card, details.reveal, details.sf { display: block !important; }
details > summary { list-style: none !important; }
details > * { display: revert !important; }
.body, .card-body, .sfa, .ans, .pqa { display: block !important; height: auto !important; }

/* ---------- Seitenausnutzung ---------- */
/* print.css erzwingt .panel+.panel und .sf-wrap auf neue Seiten und bietet dafuer
   den Schalter body.flow an. Der wird unten gesetzt; hier zusaetzlich der
   Rapid-Fire-Block, den flow nicht erfasst. */
.sf-wrap { break-before: auto !important; page-break-before: auto !important; margin-top: 6mm; }
.stationhead {
  font-family: 'Manrope', sans-serif; font-size: 11pt; font-weight: 800;
  letter-spacing: .06em; text-transform: uppercase; color: #1a1a1a;
  border-bottom: 1.4pt solid #1a1a1a; padding-bottom: 1.6mm;
  margin: 6mm 0 3.4mm 0;
  break-before: auto; break-after: avoid; page-break-after: avoid;
}
.panel:first-of-type .stationhead { margin-top: 0; }
/* Nie mitten durch eine Karte, Tabelle, Perle oder Frage umbrechen */
.card, details.card, .pearl, .pk, .sf, table, .callout {
  break-inside: avoid !important; page-break-inside: avoid !important;
}
.sf-wrap { break-inside: auto !important; }
header { break-after: avoid; }
'''


def render(slug, out):
    hits = glob.glob('reviews/*/%s.html' % slug)
    if not hits:
        sys.exit('Kein Deck gefunden: %s' % slug)
    t = io.open(hits[0], encoding='utf-8').read()
    css = io.open('print.css', encoding='utf-8').read()

    labels = [('grundlagen', 'Grundlagen'), ('klinik', 'Klinik'),
              ('diagnostik', 'Diagnostik'), ('therapie', 'Therapie'),
              ('perlen', 'KP-Perlen'), ('protokoll', 'Fragen &amp; Protokolle')]
    for panel, label in labels:
        t = re.sub(r'(<section class="panel[^"]*" data-panel="%s">)' % panel,
                   r'\1\n    <h2 class="stationhead">' + label + '</h2>', t, count=1)
    # Reiterbeschriftung des Decks bevorzugen, falls abweichend benannt
    for panel, _ in labels:
        m = re.search(r'data-tab="%s">([^<]+)</button>' % panel, t)
        if m and m.group(1).strip() not in ('', 'Diagnostik \u2605'):
            t = re.sub(r'(data-panel="%s">\s*<h2 class="stationhead">)[^<]*' % panel,
                       r'\1' + m.group(1).replace('\u2605', '').strip(), t, count=1)

    t = t.replace('</style>', css + GRAY + '</style>', 1)
    # body.flow aktiviert den Fliesssatz aus print.css (keine Station pro Seite)
    t = re.sub(r'<body([^>]*)class="([^"]*)"', r'<body\1class="\2 flow"', t, count=1)
    if 'class="flow' not in t and ' flow"' not in t:
        t = t.replace('<body>', '<body class="flow">', 1)
    io.open('/tmp/_print_%s.html' % slug, 'w', encoding='utf-8').write(t)
    from weasyprint import HTML
    HTML('/tmp/_print_%s.html' % slug, base_url='.').write_pdf(out)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Aufruf: python3 tools/_print-topic.py <slug> [ziel.pdf]')
    s = sys.argv[1]
    o = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/%s.pdf' % s
    print('  gedruckt:', render(s, o))
