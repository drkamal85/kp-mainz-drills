#!/usr/bin/env python3
# Enforce the Fragen-answer standard (Option A): every Fragen & Protokolle answer must be a
# flowing, speakable candidate-voice sentence. Flags telegraphic label-style answers
# ("Symptome: …, Therapie: …"), arrow/semicolon chains, and one-word fragments.
# Seit 09/2026 (Tab-6-Audit) sind auch Laenge (> 24 W), Satzlaenge (> 18 W), ausgeschriebene Zahlen,
# <strong> in Antworten, Fragenzahl ausserhalb 12-18 und Blockkoepfe ohne Pruefer/Datum/Fall FAIL.
# Regelwerk: tools/TAB6-ANTWORTFORMAT.md. Scope: alle Reviews mit Tab 6. Exit 1 on any violation.
import re, html, glob, io, sys

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

LABEL = re.compile(r'\b(Symptome|Therapie|Diagnostik|Klinik|Ätiologie|Komplikationen|Diagnose|'
                   r'Befund|Ursachen?|Pathophysiologie|Klassifikation|Einteilung|Mechanismus|'
                   r'Trias|Indikation|Kontraindikation|Labor)\s*:')
# A capitalized word + colon at the start of a sentence = telegraphic label (e.g. "Primär:", "Ziel:")
LABELCOLON = re.compile(r'(?:^|\. |\? )([A-ZÄÖÜ][A-Za-zäöüÄÖÜ.-]{2,}):\s')
INTRO_OK = {'Wichtig', 'Cave', 'Merke', 'Achtung', 'Beispiel', 'Definition', 'Faustregel'}

def violations(answer):
    at = clean(answer); wc = len(at.split())
    flowing = bool(re.search(r'\b(ich|wir|man|sie|er|es)\b', at.lower())) and at.count('.') >= 1
    reasons = []
    if LABEL.search(at): reasons.append('label-style')
    if '→' in at: reasons.append('arrow')
    if re.search(r'=\s', at): reasons.append('equals')
    if re.search(r'\s\+\s', at): reasons.append('plus')
    lc = [x for x in LABELCOLON.findall(at) if x not in INTRO_OK]
    if lc: reasons.append('label-colon(%s)' % '/'.join(lc))
    if not flowing and (at.count(';') >= 2): reasons.append('telegraphic')
    if wc < 5 or (at and at[-1] not in '.!?'): reasons.append('fragment')
    # --- verschaerft 09/2026 ---
    if wc > 24: reasons.append('zu-lang(%dW)' % wc)
    for sent in re.split(r'(?<=[.!?])\s+(?=[\u201e"A-Z\u00c4\u00d6\u00dc0-9])', at):
        if len(sent.split()) > 18: reasons.append('langer-Satz(%dW)' % len(sent.split()))
    n = NUMWORD.findall(at)
    if n: reasons.append('ausgeschriebene-Zahl(%s)' % '/'.join(n[:2]))
    if re.search(r'<(strong|b|em)\b', answer): reasons.append('strong-im-Antworttext')
    return reasons


META = re.compile(r'(wurde[^.]{0,30}(gefragt|gebohrt)|Zwischenfragen|im Protokoll|Der Prüfer wollte|der Kandidat|Mainzer Fall|wie im Fall)', re.I)

NUMWORD = re.compile(r'\b(zwei|drei|vier|f\u00fcnf|sechs|sieben|acht|neun|zehn|elf|zw\u00f6lf|dreizehn|vierzehn|f\u00fcnfzehn|sechzehn|siebzehn|achtzehn|neunzehn|zwanzig|drei\u00dfig|vierzig|f\u00fcnfzig|sechzig|siebzig|achtzig|neunzig|hundert|tausend|(?:ein|zwei|drei|vier|f\u00fcnf|sechs|sieben|acht|neun)und(?:zwanzig|drei\u00dfig|vierzig|f\u00fcnfzig|sechzig|siebzig|achtzig|neunzig))\b', re.I)

def style_warnings(answer):
    """Hausstil-Pruefungen laut tools/TAB6-ANTWORTFORMAT.md. Warnung, kein FAIL."""
    at = clean(answer); w = []
    if META.search(at): w.append('Meta-Kommentar')
    for sent in re.split(r'(?<=[.!?])\s+', at):
        glieder = sent.count(',') + len(re.findall(r'\b(und|sowie|oder)\b', sent))
        if glieder > 3: w.append('lange-Aufzaehlung(%d)' % glieder)
    return w

HEADER_OK = re.compile(r'(Dr\.|Prof\.|Frau |Herr |PD |\bFall\s*\d+|Pr(ü|\u00fc)fer(name)? nicht (ü|\u00fc)berliefert|\d{1,2}\.\d{1,2}\.\d{2,4}|\b\d{2}/20\d\d\b|'
                       r'\b(Januar|Februar|M\u00e4rz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+20\d\d)')
THEMATIC = re.compile(r'Lernstoff|Kontext|Definition &|Klassiker|h\u00e4ufige Pr\u00fcfungsfragen|weitere dokumentierte Fragen')
PANEL = re.compile(r'<section class="panel[^"]*" data-panel="protokoll".*?\n\s*</section>', re.S)

def deck_violations(h):
    """Fragenzahl 12-18 und Blockkoepfe mit Pruefer/Datum/Fall (Regel 1 und 5, 09/2026)."""
    out = []
    m = PANEL.search(h)
    if not m: return out
    panel = m.group(0)
    n = len(re.findall(r'<div class="pq-frage">', panel))
    if n and not 12 <= n <= 18: out.append('Fragenzahl %d (Ziel 12-18)' % n)
    for i, meta in enumerate(re.findall(r'<div class="pk-meta">(.*?)</div>', panel, re.S), 1):
        hdr = clean(re.sub(r'<span class="pk-badge">.*?</span>', '', meta))
        if not HEADER_OK.search(hdr): out.append('Block %d ohne Pruefer/Datum/Fall: %s' % (i, hdr[:60]))
        if THEMATIC.search(hdr): out.append('Block %d thematischer Kopf: %s' % (i, hdr[:60]))
    return out

files = glob.glob('reviews/**/*.html', recursive=True)
bad = []
warn = []
total = 0
for f in sorted(set(files)):
    h = io.open(f, encoding='utf-8').read()
    for dv in deck_violations(h):
        bad.append((f.split('/')[-1], '(Deck)', [dv], ''))
    for q, a in re.findall(r'<div class="pq-frage">(.*?)</div>.*?<div class="ans">(.*?)</div>', h, re.S):
        total += 1
        v = violations(a)
        if v:
            bad.append((f.split('/')[-1], clean(q)[:50], v, clean(a)[:80]))
        sw = style_warnings(a)
        if sw:
            warn.append((f.split('/')[-1], clean(q)[:46], sw))

print('Fragen answers checked: %d across %d files' % (total, len(set(files))))
if bad:
    print('VIOLATIONS (%d):' % len(bad))
    for fn, q, v, a in bad:
        print('  [%s] %s :: %s' % ('/'.join(v), fn, q))
        print('      A: %s' % a)
else:
    print('  all answers are flowing speakable sentences (Option A)')
if warn:
    print('STIL-WARNUNGEN (%d) -- siehe tools/TAB6-ANTWORTFORMAT.md:' % len(warn))
    for fn, q, w in warn[:25]:
        print('  [%s] %s :: %s' % ('/'.join(w), fn, q))
    if len(warn) > 25:
        print('  ... und %d weitere' % (len(warn) - 25))
else:
    print('  Hausstil: Zahlen, Laenge und Aufzaehlungen in Ordnung')
print('RESULT:', 'PASS' if not bad else 'FAIL')
sys.exit(0 if not bad else 1)
