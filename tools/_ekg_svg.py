#!/usr/bin/env python3
"""Erzeugt EKG-Kurven als Inline-SVG für drills/ekg-komplett.html.

Massstab wie im Original: 25 mm/s und 10 mm/mV.
1 mm = 40 ms horizontal, 1 mm = 0,1 mV vertikal.
Koordinaten werden in Millimetern gerechnet, Baseline y = 0, positiv nach oben.
"""
import math

PX = 4.0          # Pixel je Millimeter
H_MM = 26.0       # Hoehe der Zeichenflaeche in mm
BASE = 17.0       # Baseline von oben in mm


def _grid(w_mm):
    """EKG-Millimeterpapier."""
    o = []
    o.append(f'<rect width="{w_mm*PX}" height="{H_MM*PX}" fill="#FFF8F6"/>')
    for x in range(0, int(w_mm) + 1):
        maj = x % 5 == 0
        o.append(f'<line x1="{x*PX}" y1="0" x2="{x*PX}" y2="{H_MM*PX}" '
                 f'stroke="{"#F2B8B0" if maj else "#F9DCD8"}" stroke-width="{1 if maj else 0.5}"/>')
    for y in range(0, int(H_MM) + 1):
        maj = y % 5 == 0
        o.append(f'<line x1="0" y1="{y*PX}" x2="{w_mm*PX}" y2="{y*PX}" '
                 f'stroke="{"#F2B8B0" if maj else "#F9DCD8"}" stroke-width="{1 if maj else 0.5}"/>')
    return ''.join(o)


def _poly(pts, color="#1A1A1A", w=1.7):
    d = ' '.join(f'{x*PX:.1f},{(BASE-y)*PX:.1f}' for x, y in pts)
    return (f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


# ---- Wellenbausteine, jeweils Liste relativer (dx, y) ----------------------
def p_wave(x, amp=1.5, wid=2.0, inv=False, notched=False):
    a = -amp if inv else amp
    if notched:
        return [(x, 0), (x+wid*0.25, a*0.9), (x+wid*0.5, a*0.5), (x+wid*0.75, a*0.9), (x+wid, 0)]
    return [(x, 0), (x+wid*0.35, a), (x+wid*0.65, a), (x+wid, 0)]


def qrs(x, r=10.0, q=0.0, s=2.5, wid=2.0, delta=False, rsr=False, mono=False):
    if delta:
        return [(x, 0), (x+0.9, 1.6), (x+1.6, r*0.9), (x+2.4, -s), (x+3.1, 0)]
    if rsr:
        return [(x, 0), (x+0.5, r*0.42), (x+1.0, -s*0.5), (x+1.6, r*0.55),
                (x+2.4, -s*0.4), (x+3.2, 0)]
    if mono:
        return [(x, 0), (x+0.6, -1.2), (x+1.4, r*0.75), (x+2.6, r*0.7), (x+3.6, 0.6), (x+4.2, 0)]
    pts = [(x, 0)]
    if q:
        pts.append((x+0.3, -q))
    pts += [(x+wid*0.35, r), (x+wid*0.72, -s), (x+wid, 0)]
    return pts


def t_wave(x, amp=3.0, wid=4.0, inv=False, peaked=False):
    a = -amp if inv else amp
    if peaked:
        return [(x, 0), (x+wid*0.42, a), (x+wid*0.58, a), (x+wid, 0)]
    return [(x, 0), (x+wid*0.3, a*0.75), (x+wid*0.5, a), (x+wid*0.72, a*0.75), (x+wid, 0)]


def seg(x1, x2, y=0.0):
    return [(x1, y), (x2, y)]


# ---- Rhythmusgeneratoren --------------------------------------------------
def normal_beat(x, pq=3.5, st=0.0, tamp=3.0, tinv=False, q=0.0,
                rsr=False, mono=False, delta=False, pamp=1.5, pnotch=False, tpeak=False):
    pts = []
    if pamp:
        pts += p_wave(x, amp=pamp, notched=pnotch)
        pts += seg(x+2.0, x+pq)
        cx = x+pq
    else:
        cx = x+0.5
    body = qrs(cx, q=q, rsr=rsr, mono=mono, delta=delta)
    pts += body
    end = body[-1][0]
    pts += seg(end, end+2.0, st)
    pts += [(end+2.0, st)]
    pts += [(px, py+st*0.5) for px, py in t_wave(end+2.0, amp=tamp, inv=tinv, peaked=tpeak)]
    pts += seg(end+6.0, x+25.0 if False else end+6.6)
    return pts, end+6.6


def build(kind, w_mm=100.0):
    """Liefert die Punktliste fuer ein Muster."""
    pts, x = [], 1.0
    if kind == 'normal':
        while x < w_mm-8:
            b, x = normal_beat(x); pts += b; x += 7.0
    elif kind == 'vhf':
        import random
        random.seed(7)
        while x < w_mm-8:
            f = [(x+i*0.35, (0.5 if i % 2 else -0.4)*0.9) for i in range(int(random.uniform(6, 14)))]
            pts += f
            x = f[-1][0]
            b, x = normal_beat(x, pamp=0)
            pts += b
            x += random.uniform(0.5, 4.5)
    elif kind == 'flattern':
        saw = []
        xx = 1.0
        while xx < w_mm-2:
            saw += [(xx, -1.2), (xx+1.4, 2.2)]
            xx += 1.4
        pts += saw
        for k in (14.0, 34.0, 54.0, 74.0):
            b = qrs(k, r=7.0)
            pts += b
    elif kind == 'av1':
        while x < w_mm-10:
            b, x = normal_beat(x, pq=7.5); pts += b; x += 5.0
    elif kind == 'wenckebach':
        for pq in (3.5, 5.5, 7.5):
            b, x = normal_beat(x, pq=pq); pts += b; x += 4.0
        pts += p_wave(x); pts += seg(x+2.0, x+8.0); x += 8.0
        for pq in (3.5, 5.5):
            b, x = normal_beat(x, pq=pq); pts += b; x += 4.0
    elif kind == 'mobitz':
        for _ in range(2):
            b, x = normal_beat(x, pq=4.5); pts += b; x += 4.0
        pts += p_wave(x); pts += seg(x+2.0, x+9.0); x += 9.0
        for _ in range(2):
            b, x = normal_beat(x, pq=4.5); pts += b; x += 4.0
    elif kind == 'av3':
        px_ = 1.0
        while px_ < w_mm-3:
            pts += p_wave(px_); pts += seg(px_+2.0, px_+5.2); px_ += 5.2
        for k in (6.0, 30.0, 54.0, 78.0):
            pts += qrs(k, r=8.0, wid=3.0)
            pts += t_wave(k+3.0, amp=2.5)
    elif kind == 'stemi':
        while x < w_mm-9:
            b, x = normal_beat(x, st=3.5, tamp=3.5); pts += b; x += 6.0
    elif kind == 'nstemi':
        while x < w_mm-9:
            b, x = normal_beat(x, st=-2.2, tamp=2.0, tinv=True); pts += b; x += 6.0
    elif kind == 'qzacke':
        while x < w_mm-9:
            b, x = normal_beat(x, q=4.5, tamp=2.0, tinv=True); pts += b; x += 6.0
    elif kind == 'lsb':
        while x < w_mm-10:
            b, x = normal_beat(x, mono=True, tamp=2.5, tinv=True); pts += b; x += 5.0
    elif kind == 'rsb':
        while x < w_mm-10:
            b, x = normal_beat(x, rsr=True, tamp=2.0, tinv=True); pts += b; x += 5.0
    elif kind == 'wpw':
        while x < w_mm-9:
            b, x = normal_beat(x, pq=2.4, delta=True, tamp=2.5); pts += b; x += 6.0
    elif kind == 'vt':
        while x < w_mm-4:
            pts += [(x, 0), (x+1.2, 8.5), (x+2.6, -6.5), (x+3.8, 0)]
            x += 4.0
    elif kind == 'vf':
        import random
        random.seed(3)
        xx = 1.0
        while xx < w_mm-1:
            pts.append((xx, random.uniform(-5.5, 6.5)))
            xx += 0.7
    elif kind == 'torsade':
        xx = 1.0
        i = 0
        while xx < w_mm-1:
            env = 6.5*abs(math.sin(xx/13.0))+1.0
            pts.append((xx, env*(1 if i % 2 else -1)))
            xx += 0.85
            i += 1
    elif kind == 'ves':
        for _ in range(2):
            b, x = normal_beat(x); pts += b; x += 6.0
        pts += [(x, 0), (x+1.4, 9.0), (x+3.0, -7.0), (x+4.4, 0)]
        pts += t_wave(x+4.4, amp=3.0, inv=True)
        x += 12.0
        for _ in range(2):
            b, x = normal_beat(x); pts += b; x += 6.0
    elif kind == 'sves':
        for _ in range(2):
            b, x = normal_beat(x); pts += b; x += 6.0
        b, x = normal_beat(x-2.5, pamp=1.0)
        pts += b
        x += 5.0
        for _ in range(2):
            b, x = normal_beat(x); pts += b; x += 6.0
    elif kind == 'hyperkaliaemie':
        while x < w_mm-9:
            b, x = normal_beat(x, tamp=7.5, tpeak=True, pamp=0.6); pts += b; x += 6.0
    return pts


LABEL = ('<text x="{x}" y="{y}" font-family="Manrope,system-ui,sans-serif" font-size="11" '
         'font-weight="700" fill="{c}">{t}</text>')


def svg(kind, w_mm=100.0, marks=()):
    body = _grid(w_mm) + _poly(build(kind, w_mm))
    for mx, my, txt, col in marks:
        body += LABEL.format(x=mx*PX, y=my*PX, t=txt, c=col)
    return (f'<svg viewBox="0 0 {w_mm*PX} {H_MM*PX}" class="ekg" role="img" '
            f'preserveAspectRatio="xMidYMid meet">{body}</svg>')


if __name__ == '__main__':
    print(svg('normal')[:200])
