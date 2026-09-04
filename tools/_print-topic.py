#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/_print-topic.py — rendert eine Themenseite als A4-PDF in Graustufen.

    python3 tools/_print-topic.py <slug> [ziel.pdf]

Layout: eine Themenseite, alle Stationen ausgeklappt, ohne Farbe.
Jede Station beginnt auf einer neuen Seite. Karten, Tabellen, Perlen und
Fragen werden nie ueber einen Seitenumbruch zerrissen.

Grundlage ist print.css. Die Graustufenregeln stehen hier, weil sie nur
fuer den Papierdruck gelten und die Bildschirmfassung farbig bleiben soll.
"""
import glob
import hashlib
import io
import json
import os
import re
import sys

REG = 'tools/.print-register.json'   # slug -> {"hash":..., "pdf":..., "seiten":...}


def _hash(path):
    return hashlib.sha256(io.open(path, 'rb').read()).hexdigest()[:16]


def bereits_gedruckt(slug):
    """Gibt (pdf, seiten) zurueck, wenn das Deck seit dem letzten Druck
    unveraendert ist - sonst None. Verhindert doppelte Ausdrucke."""
    if not os.path.exists(REG):
        return None
    reg = json.loads(io.open(REG, encoding='utf-8').read())
    e = reg.get(slug)
    if not e:
        return None
    hits = glob.glob('reviews/*/%s.html' % slug)
    if not hits or _hash(hits[0]) != e.get('hash'):
        return None
    return e.get('pdf'), e.get('seiten')


def vermerken(slug, pdf, seiten):
    reg = json.loads(io.open(REG, encoding='utf-8').read()) if os.path.exists(REG) else {}
    hits = glob.glob('reviews/*/%s.html' % slug)
    reg[slug] = {'hash': _hash(hits[0]), 'pdf': pdf, 'seiten': seiten}
    io.open(REG, 'w', encoding='utf-8').write(json.dumps(reg, indent=1, ensure_ascii=False))

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
/* Jede Station beginnt auf einer neuen Seite - so aus print.css uebernommen
   (.panel + .panel sowie .sf-wrap). body.flow wird bewusst NICHT gesetzt. */
.stationhead {
  font-family: 'Manrope', sans-serif; font-size: 11pt; font-weight: 800;
  letter-spacing: .06em; text-transform: uppercase; color: #1a1a1a;
  border-bottom: 1.4pt solid #1a1a1a; padding-bottom: 1.6mm;
  margin: 0 0 5mm 0;
  break-before: page; break-after: avoid; page-break-after: avoid;
}
.panel:first-of-type .stationhead { break-before: avoid; }
/* Nie mitten durch eine Karte, Tabelle, Perle oder Einzelfrage umbrechen */
.card, details.card, .pearl, .sf, .pq, table, .callout {
  break-inside: avoid !important; page-break-inside: avoid !important;
}
/* Protokollbloecke und Rapid-Fire duerfen umbrechen - sonst springt ein Block
   mit sechs Fragen komplett auf die naechste Seite und laesst die halbe leer.
   Die Fallvignette bleibt bei der ersten Frage. */
.pk, .sf-wrap { break-inside: auto !important; page-break-inside: auto !important; }
.pk-meta, .pk-akte { break-after: avoid !important; page-break-after: avoid !important; }
.pk-q { break-after: avoid !important; }
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
    io.open('/tmp/_print_%s.html' % slug, 'w', encoding='utf-8').write(t)
    from weasyprint import HTML
    HTML('/tmp/_print_%s.html' % slug, base_url='.').write_pdf(out)
    try:
        import subprocess
        n = subprocess.run(['pdfinfo', out], capture_output=True, text=True).stdout
        seiten = int(re.search(r'Pages:\s+(\d+)', n).group(1))
    except Exception:
        seiten = 0
    vermerken(slug, out, seiten)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Aufruf: python3 tools/_print-topic.py <slug> [ziel.pdf]')
    s = sys.argv[1]
    o = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/%s.pdf' % s
    alt = bereits_gedruckt(s)
    if alt and '--force' not in sys.argv:
        print('  SCHON GEDRUCKT: %s (%s Seiten), Deck seither unveraendert.' % (alt[0], alt[1]))
        print('  Erneut drucken mit --force')
        sys.exit(0)
    print('  gedruckt:', render(s, o))
