#!/usr/bin/env python3
"""Erzeugt die AAST-Gradeinteilung der Milzverletzung als schematische Inline-SVG.

Fuenf Panels, je 100x128 viewBox. Bewusst schematisch: Es geht um Risstiefe,
Haematomausdehnung und Hilusbeteiligung, nicht um anatomische Realistik.
"""

CAPSULE = "M 52 12 C 30 15 16 40 18 68 C 20 96 38 116 58 114 C 78 112 86 86 84 58 C 82 30 72 10 52 12 Z"
HILUM = "M 18 60 L 6 54 M 18 68 L 6 68 M 18 76 L 6 82"

TISSUE = "#F2DCD6"
EDGE = "#B5766A"
BLOOD = "#A03A2C"
HEMA = "#D9A79C"
DEVASC = "#BFBAB4"


def _panel(idx, grade, label, extra, sub):
    return f'''<figure class="aast">
<svg viewBox="0 0 100 148" role="img" aria-label="AAST Grad {grade}">
  <defs><clipPath id="sp{idx}"><path d="{CAPSULE}"/></clipPath></defs>
  <path d="{CAPSULE}" fill="{TISSUE}" stroke="{EDGE}" stroke-width="2.4"/>
  <path d="{HILUM}" stroke="{EDGE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>
{extra}
  <text x="50" y="136" text-anchor="middle" font-family="Manrope,system-ui,sans-serif"
        font-size="15" font-weight="800" fill="#1A1A1A">Grad {grade}</text>
</svg>
<figcaption>{label}<span>{sub}</span></figcaption>
</figure>'''


def build():
    g1 = _panel(1, 'I', 'Kapselriss unter 1 cm',
        f'''  <g clip-path="url(#sp1)"><path d="M 70 26 C 76 34 78 42 77 50" fill="none" stroke="{HEMA}" stroke-width="9" opacity=".85"/></g>
  <path d="M 74 24 L 79 33" stroke="{BLOOD}" stroke-width="2.6" stroke-linecap="round"/>''',
        'subkapsuläres Hämatom unter 10 %')

    g2 = _panel(2, 'II', 'Riss 1 bis 3 cm',
        f'''  <g clip-path="url(#sp2)"><path d="M 66 22 C 80 38 84 60 80 82" fill="none" stroke="{HEMA}" stroke-width="15" opacity=".85"/></g>
  <path d="M 72 30 L 80 48" stroke="{BLOOD}" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M 60 66 L 70 78" stroke="{BLOOD}" stroke-width="2.8" stroke-linecap="round"/>''',
        'Hämatom 10 bis 50 %')

    g3 = _panel(3, 'III', 'Riss über 3 cm',
        f'''  <g clip-path="url(#sp3)"><path d="M 58 16 C 84 34 90 66 78 104" fill="none" stroke="{HEMA}" stroke-width="26" opacity=".85"/></g>
  <path d="M 70 22 L 56 62" stroke="{BLOOD}" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M 78 70 L 62 96" stroke="{BLOOD}" stroke-width="3.2" stroke-linecap="round"/>''',
        'Hämatom über 50 %')

    g4 = _panel(4, 'IV', 'Hilusgefäße beteiligt',
        f'''  <g clip-path="url(#sp4)"><path d="M 14 52 L 92 26 L 92 104 L 14 88 Z" fill="{DEVASC}" opacity=".8"/></g>
  <path d="M 60 18 L 30 58" stroke="{BLOOD}" stroke-width="3.4" stroke-linecap="round"/>
  <path d="M 18 68 L 6 68" stroke="{BLOOD}" stroke-width="3.4" stroke-linecap="round"/>
  <circle cx="10" cy="68" r="4" fill="{BLOOD}"/>''',
        'Devaskularisierung über 25 %')

    g5 = _panel(5, 'V', 'zertrümmerte Milz',
        f'''  <g clip-path="url(#sp5)">
    <path d="M 52 12 L 20 52" stroke="{BLOOD}" stroke-width="3.4"/>
    <path d="M 30 20 L 84 74" stroke="{BLOOD}" stroke-width="3.4"/>
    <path d="M 84 40 L 34 100" stroke="{BLOOD}" stroke-width="3.4"/>
    <path d="M 18 84 L 66 116" stroke="{BLOOD}" stroke-width="3.4"/>
  </g>
  <path d="M 18 54 L 4 46 M 18 68 L 4 68 M 18 82 L 4 90" stroke="{BLOOD}" stroke-width="2.8" stroke-linecap="round"/>
  <circle cx="7" cy="68" r="4" fill="{BLOOD}"/>''',
        'oder kompletter Hilusabriss')

    return ('<div class="aastwrap">' + g1 + g2 + g3 + g4 + g5 + '</div>\n'
            '<p class="aastnote">Der Grad allein entscheidet nicht — die Kreislaufstabilität entscheidet. '
            'Rot sind Risse und Gefäßabrisse, rosa das subkapsuläre Hämatom, grau das devaskularisierte Areal.</p>')


CSS = '''
  .aastwrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));gap:10px;margin:14px 0 4px}
  .aast{margin:0;background:#FFFDF8;border:1px solid rgba(15,23,42,.10);border-radius:12px;padding:8px 6px 10px}
  .aast svg{width:100%;height:auto;display:block}
  .aast figcaption{font-size:11.5px;line-height:1.35;color:#1A1A1A;font-weight:700;text-align:center;margin-top:2px}
  .aast figcaption span{display:block;font-weight:500;color:#5C5C5C;margin-top:2px}
  .aastnote{font-size:12.5px;color:#5C5C5C;line-height:1.5;margin:6px 0 0}
'''

if __name__ == '__main__':
    print(build()[:300])
