#!/usr/bin/env python3
"""Append a .pk block of newly mined, real documented Mainz questions to a review's
tab 6 (Fragen & Protokolle). Add-only: never removes or edits existing questions.

Usage (from repo root):
    python3 tools/_retrofit_add.py <path-to-review.html> <block.json>

block.json = {"meta": ["Mainz · Quelle", "Kurztitel"], "qa": [["Frage","Antwort"], ...]}
"""
import json, re, sys, io

def build(meta, qa):
    head = ('    <div class="pk">\n'
            '      <div class="pk-meta"><span>%s</span><span>%s</span>'
            '<span class="pk-badge">Protokoll</span></div>\n'
            '      <div class="pk-q"><span class="lab">Gefragt wurde — einzeln beantworten</span></div>\n'
            % (meta[0], meta[1]))
    rows = []
    for q, a in qa:
        rows.append('      <div class="pq"><div class="pq-frage">%s</div>'
                    '<details class="reveal"><summary>Antwort</summary>'
                    '<div class="ans">%s</div></details></div>\n' % (q, a))
    return head + ''.join(rows) + '    </div>\n'

def main():
    path, blockfile = sys.argv[1], sys.argv[2]
    spec = json.load(io.open(blockfile, encoding='utf-8'))
    h = io.open(path, encoding='utf-8').read()
    m = re.search(r'(<section class="panel[^"]*" data-panel="protokoll".*?)(\n  </section>)', h, re.S)
    if not m:
        sys.exit('FAIL: no protokoll panel in %s' % path)
    before = len(re.findall(r'<div class="pq-frage">', m.group(1)))
    block = build(spec['meta'], spec['qa'])
    h2 = h[:m.end(1)] + '\n' + block + h[m.end(1):]
    io.open(path, 'w', encoding='utf-8').write(h2)
    after = before + len(spec['qa'])
    print('%s: %d -> %d Fragen (+%d)' % (path.split('/')[-1], before, after, len(spec['qa'])))

if __name__ == '__main__':
    main()
