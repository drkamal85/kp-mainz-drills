#!/usr/bin/env python3
# Enforce the Fragen-answer standard (Option A): every Fragen & Protokolle answer must be a
# flowing, speakable candidate-voice sentence. Flags telegraphic label-style answers
# ("Symptome: …, Therapie: …"), arrow/semicolon chains, and one-word fragments.
# Long-but-flowing multi-part answers are allowed (they are still speakable).
# Scope: all individual R3 reviews. Exit 1 on any violation.
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
    return reasons


NUMWORD = re.compile(r'\b(zwanzig|drei\u00dfig|vierzig|f\u00fcnfzig|sechzig|siebzig|achtzig|neunzig|hundert|tausend|zweihundert|dreihundert|vierhundert|f\u00fcnfhundert|vierundzwanzig|achtundvierzig|zweiundsiebzig|zweihundertf\u00fcnfzig|f\u00fcnfundsechzig|f\u00fcnfundzwanzig)\\w*', re.I)

def style_warnings(answer):
    """Hausstil-Pruefungen laut tools/TAB6-ANTWORTFORMAT.md. Warnung, kein FAIL."""
    at = clean(answer); w = []
    n = NUMWORD.findall(at)
    if n: w.append('ausgeschriebene-Zahl(%s)' % '/'.join(n[:2]))
    wc = len(at.split())
    if wc > 36: w.append('zu-lang(%dW)' % wc)
    for sent in re.split(r'(?<=[.!?])\s+', at):
        glieder = sent.count(',') + len(re.findall(r'\b(und|sowie|oder)\b', sent))
        if glieder > 4: w.append('lange-Aufzaehlung(%d)' % glieder)
        if len(sent.split()) > 22: w.append('langer-Satz(%dW)' % len(sent.split()))
    return w

files = glob.glob('reviews/**/*.html', recursive=True)
bad = []
warn = []
total = 0
for f in sorted(set(files)):
    h = io.open(f, encoding='utf-8').read()
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
