#!/usr/bin/env python3
"""Schreibt die Fragenzahl in das Tab-6-Label jedes Reviews.

Aus "Fragen & Protokolle" wird "Fragen & Protokolle · 14".
Idempotent — eine bereits vorhandene Zahl wird ersetzt, nicht angehaengt.
Nach jedem R3-Bau oder Tab-6-Retrofit erneut laufen lassen.
"""
import glob, io, os, re

# Drei Altdecks beschriften den Tab "Pruefungsfragen" — wird mit normalisiert.
LABEL = re.compile(
    r'(<button class="tab[^"]*" data-c="protokoll" data-tab="protokoll">)'
    r'(?:Fragen &amp; Protokolle|Prüfungsfragen)(?:\s*·\s*\d+)?'
    r'(</button>)')

PANEL = re.compile(
    r'<section class="panel[^"]*" data-panel="protokoll".*?\n\s*</section>', re.S)

QUESTION = re.compile(r'<div class="pq-frage">')


def main():
    changed, total, skipped = 0, 0, []
    for f in sorted(glob.glob('reviews/*/*.html')):
        h = io.open(f, encoding='utf-8').read()
        panel = PANEL.search(h)
        if not panel:
            # '.pq-frage' steht auch im Stylesheet — nur echte Fragen zaehlen
            if QUESTION.search(h):
                skipped.append(os.path.basename(f)[:-5] + ' (Panel fehlt)')
            continue
        n = len(QUESTION.findall(panel.group(0)))
        if not n:
            continue
        h2, k = LABEL.subn(r'\g<1>Fragen &amp; Protokolle · %d\g<2>' % n, h)
        total += n
        if k and h2 != h:
            io.open(f, 'w', encoding='utf-8').write(h2)
            changed += 1
        elif not k:
            skipped.append(os.path.basename(f)[:-5] + ' (kein Tab-Label)')
    # Sonderfall notfallpharmakologie: station-basiert statt data-panel
    sp = 'reviews/notfallmedizin/notfallpharmakologie.html'
    if os.path.exists(sp):
        h = io.open(sp, encoding='utf-8').read()
        n = len(QUESTION.findall(h))
        pat = re.compile(r'(<div class="station-title">)Fragen &amp; Protokolle(?:\s*·\s*\d+)?(</div>)')
        h2, k = pat.subn(r'\g<1>Fragen &amp; Protokolle · %d\g<2>' % n, h)
        if k and h2 != h:
            io.open(sp, 'w', encoding='utf-8').write(h2)
            changed += 1
        total += n
        skipped[:] = [x for x in skipped if not x.startswith('notfallpharmakologie')]

    print('Tab-6-Label aktualisiert: %d Decks, %d Fragen gesamt' % (changed, total))
    if skipped:
        print('Sonderfaelle:', ', '.join(skipped))


if __name__ == '__main__':
    main()
