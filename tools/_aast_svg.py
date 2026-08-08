#!/usr/bin/env python3
"""AAST-Gradeinteilung der Milzverletzung als Inline-SVG.
Bohnenform mit Hilusnische, segmentaler Gefaessbaum, Risse als verjuengte Keile."""

CAPSULE = ("M 66 16 C 90 21 102 50 100 82 C 98 114 80 138 58 138 "
           "C 43 138 32 126 30 110 C 29 101 33 95 34 86 "
           "L 20 80 L 34 74 C 34 62 26 48 32 35 C 38 22 52 13 66 16 Z")
VESSELS_A = "M 20 78 C 34 78 44 70 56 62 M 44 74 C 54 78 62 86 70 98 M 42 79 C 50 90 54 104 56 118"
VESSELS_V = "M 20 84 C 32 86 40 84 50 80"
INK="#1A1A1A"; CAPS="#7E4A40"; BLOOD="#A32B1C"; BLOOD_D="#7A1F14"
HEMA="#D79A8E"; DEVASC="#B9B3AC"; ART="#C0392B"; VEN="#4A6FA5"

def _defs(i):
    return f'''<defs>
    <clipPath id="c{i}"><path d="{CAPSULE}"/></clipPath>
    <radialGradient id="g{i}" cx="58%" cy="40%" r="72%">
      <stop offset="0%" stop-color="#FAE9E4"/><stop offset="70%" stop-color="#F0D5CD"/>
      <stop offset="100%" stop-color="#E3BFB4"/>
    </radialGradient>
  </defs>'''

def _base(i, vessels=True):
    v = (f'  <g clip-path="url(#c{i})" fill="none" stroke-linecap="round">\n'
         f'    <path d="{VESSELS_V}" stroke="{VEN}" stroke-width="4.6" opacity=".55"/>\n'
         f'    <path d="{VESSELS_A}" stroke="{ART}" stroke-width="3.4" opacity=".62"/>\n'
         f'  </g>\n') if vessels else ''
    return (f'  <path d="{CAPSULE}" fill="url(#g{i})"/>\n' + v +
            f'  <path d="{CAPSULE}" fill="none" stroke="{CAPS}" stroke-width="3"/>\n')

def _tear(pts):
    return f'<path d="{pts}" fill="{BLOOD}" stroke="{BLOOD_D}" stroke-width="0.8" stroke-linejoin="round"/>'

def _panel(i, grade, label, sub, inner, vessels=True):
    return f'''<figure class="aast">
<svg viewBox="0 0 120 168" role="img" aria-label="AAST Grad {grade}">
  {_defs(i)}
{_base(i, vessels)}{inner}
  <text x="60" y="160" text-anchor="middle" font-family="Manrope,system-ui,sans-serif"
        font-size="16" font-weight="800" fill="{INK}">Grad {grade}</text>
</svg>
<figcaption>{label}<span>{sub}</span></figcaption>
</figure>'''

def build():
    g1=_panel(1,'I','Kapselriss unter 1 cm','subkapsuläres Hämatom unter 10 %',
      f'''  <g clip-path="url(#c1)">
    <path d="M 84 26 C 96 38 101 54 100 70 C 94 58 88 42 78 30 Z" fill="{HEMA}" opacity=".9"/>
    {_tear("M 80 23 L 88 28 L 79 39 Z")}
  </g>''')
    g2=_panel(2,'II','Riss 1 bis 3 cm','Hämatom 10 bis 50 %',
      f'''  <g clip-path="url(#c2)">
    <path d="M 76 20 C 96 36 104 62 102 92 C 92 66 84 40 68 24 Z" fill="{HEMA}" opacity=".9"/>
    {_tear("M 78 24 L 88 30 L 72 52 Z")}
    {_tear("M 94 76 L 99 86 L 84 92 Z")}
  </g>''')
    g3=_panel(3,'III','Riss über 3 cm','Hämatom über 50 %',
      f'''  <g clip-path="url(#c3)">
    <path d="M 62 12 C 96 30 108 66 104 118 C 88 82 76 44 52 18 Z" fill="{HEMA}" opacity=".9"/>
    {_tear("M 70 17 L 82 25 L 50 72 Z")}
    {_tear("M 97 94 L 101 108 L 70 120 Z")}
  </g>''')
    g4=_panel(4,'IV','Hilusgefäße beteiligt','Devaskularisierung über 25 %',
      f'''  <g clip-path="url(#c4)">
    <path d="M 34 78 L 112 44 L 118 118 L 40 112 Z" fill="{DEVASC}" opacity=".82"/>
    {_tear("M 66 15 L 78 22 L 42 66 Z")}
  </g>
  <path d="M 18 78 L 27 78" stroke="{BLOOD}" stroke-width="4.4" stroke-linecap="round"/>
  <path d="M 35 78 L 42 78" stroke="{BLOOD}" stroke-width="4.4" stroke-linecap="round"/>
  <circle cx="27" cy="78" r="2.8" fill="{BLOOD_D}"/><circle cx="35" cy="78" r="2.8" fill="{BLOOD_D}"/>''')
    g5=_panel(5,'V','zertrümmerte Milz','oder kompletter Hilusabriss',
      f'''  <g clip-path="url(#c5)" fill="none" stroke-linecap="round">
    <g stroke="#FBEFEA" stroke-width="4.5">
      <path d="M 60 8 L 24 62"/><path d="M 100 30 L 36 108"/>
      <path d="M 26 100 L 96 142"/><path d="M 108 86 L 58 146"/>
    </g>
    <g stroke="{BLOOD_D}" stroke-width="2.4" opacity=".92">
      <path d="M 60 8 L 24 62"/><path d="M 100 30 L 36 108"/>
      <path d="M 26 100 L 96 142"/><path d="M 108 86 L 58 146"/>
    </g>
    <g stroke="{BLOOD}" stroke-width="5" stroke-linecap="round" opacity=".7">
      <path d="M 44 40 L 34 54"/><path d="M 74 74 L 62 90"/><path d="M 52 116 L 66 124"/>
    </g>
  </g>
  <path d="M 20 78 L 34 78" stroke="{BLOOD}" stroke-width="4.4" stroke-linecap="round"/>
  <circle cx="17" cy="78" r="4.4" fill="{BLOOD_D}"/>''',vessels=False)
    return ('<div class="aastwrap">'+g1+g2+g3+g4+g5+'</div>\n'
      '<p class="aastnote"><b>Der Grad allein entscheidet nicht — die Kreislaufstabilität entscheidet.</b> '
      'Rot sind Risse und Gefäßabrisse, rosa das subkapsuläre Hämatom, grau das devaskularisierte Segment. '
      'Die Nische links ist der Hilus, dort treten Arteria und Vena splenica ein.</p>')

CSS = '''
  .aastwrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(124px,1fr));gap:10px;margin:14px 0 4px}
  .aast{margin:0;background:#FFFDF8;border:1px solid rgba(15,23,42,.10);border-radius:12px;padding:8px 6px 10px}
  .aast svg{width:100%;height:auto;display:block}
  .aast figcaption{font-size:11.5px;line-height:1.35;color:#1A1A1A;font-weight:700;text-align:center;margin-top:2px}
  .aast figcaption span{display:block;font-weight:500;color:#5C5C5C;margin-top:2px}
  .aastnote{font-size:12.5px;color:#5C5C5C;line-height:1.55;margin:8px 0 0}
'''
