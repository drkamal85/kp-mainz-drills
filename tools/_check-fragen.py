#!/usr/bin/env python3
# Enforce the Fragen-answer standard (Option A): every Fragen & Protokolle answer must be a
# flowing, speakable candidate-voice sentence. Flags telegraphic label-style answers
# ("Symptome: …, Therapie: …"), arrow/semicolon chains, and one-word fragments.
# Long-but-flowing multi-part answers are allowed (they are still speakable).
# Scope: all individual R3 reviews + the aggregated sammel page. Exit 1 on any violation.
import re, html, glob, io, sys

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

LABEL = re.compile(r'\b(Symptome|Therapie|Diagnostik|Klinik|Ätiologie|Komplikationen|Diagnose|'
                   r'Befund|Ursachen?|Pathophysiologie|Klassifikation|Einteilung|Mechanismus|'
                   r'Trias|Indikation|Kontraindikation|Labor)\s*:')

def violations(answer):
    at = clean(answer); wc = len(at.split())
    flowing = bool(re.search(r'\b(ich|wir|man|sie|er|es)\b', at.lower())) and at.count('.') >= 1
    reasons = []
    if LABEL.search(at): reasons.append('label-style')
    if not flowing and (at.count('→') >= 2 or at.count(';') >= 2): reasons.append('telegraphic')
    if wc < 5 or (at and at[-1] not in '.!?'): reasons.append('fragment')
    return reasons

files = [f for f in glob.glob('reviews/**/*-r3.html', recursive=True)] \
      + glob.glob('reviews/sammel/*.html')
bad = []
total = 0
for f in sorted(set(files)):
    h = io.open(f, encoding='utf-8').read()
    for q, a in re.findall(r'<div class="pq-frage">(.*?)</div>.*?<div class="ans">(.*?)</div>', h, re.S):
        total += 1
        v = violations(a)
        if v:
            bad.append((f.split('/')[-1], clean(q)[:50], v, clean(a)[:80]))

print('Fragen answers checked: %d across %d files' % (total, len(set(files))))
if bad:
    print('VIOLATIONS (%d):' % len(bad))
    for fn, q, v, a in bad:
        print('  [%s] %s :: %s' % ('/'.join(v), fn, q))
        print('      A: %s' % a)
else:
    print('  all answers are flowing speakable sentences (Option A)')
print('RESULT:', 'PASS' if not bad else 'FAIL')
sys.exit(0 if not bad else 1)
