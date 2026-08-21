#!/usr/bin/env python3
"""
tools/_clean-meta.py — reduziert die Meta-Zeile jeder Themenseite auf Rang und Stufe.

Vorher standen dort bis zu fuenf Angaben, davon zwei fehlerhaft:

- "R1 von 4"      falsch, die Leiter hat fuenf Stufen (R1-R5)
- "~12-14 Min"    geschaetzt, nie nachgezogen nach Kuerzungen
- "Stand 07/2026" Baudatum, ohne Nutzen beim Lernen
- "Amboss ..."    Quellenangabe, auf jeder Seite identisch

Behalten werden nur:

    <span class="rk lo">Rang 71 von 97</span>
    <span>R1 von 5</span>

Die Stufenangabe war ueber 19 Varianten zersplittert ("R3 von 5 - Superset von R2",
"R3 - 6 Tabs - Kurz + KP-Perlen + Protokolle", blosses "R3" ...). Sie wird auf die
Form "RN von 5" vereinheitlicht; die R-Nummer stammt aus der vorhandenen Angabe,
ersatzweise aus dem Eyebrow.

Idempotent: ein zweiter Lauf meldet null Aenderungen.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = re.compile(r'(<div class="meta">)(.*?)(</div>)', re.S)
RK = re.compile(r'<span class="rk[^"]*">[^<]*</span>')
SPAN = re.compile(r'<span(?![^>]*class="rk)[^>]*>(.*?)</span>', re.S)


def index_levels() -> dict[str, str]:
    """Massgeblich ist das Badge in index.html, nicht die Meta-Zeile.

    Bei R4-Befoerderungen wurde bisher nur der Index nachgezogen — 47 Seiten
    trugen deshalb eine veraltete Stufe im Kopf.
    """
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'href="reviews/[a-z-]+/([a-z0-9-]+)\.html"[^>]*data-lvl="(\d)"', idx):
        out[m.group(1)] = m.group(2)
    return out


def level_of(inner: str, page: str, slug: str, idx: dict) -> str | None:
    """Stufe: erst aus dem Index, sonst aus Meta-Zeile oder Eyebrow."""
    if slug in idx:
        return idx[slug]
    for raw in SPAN.findall(inner):
        m = re.match(r'\s*R(\d)', re.sub(r"<[^>]+>", "", raw).strip())
        if m:
            return m.group(1)
    m = re.search(r'<div class="eyebrow">[^<]*?R(\d)', page)
    return m.group(1) if m else None


def main():
    idx = index_levels()
    changed = skipped = 0
    for p in sorted(ROOT.glob("reviews/*/*.html")):
        src = p.read_text(encoding="utf-8")
        m = META.search(src)
        if not m:
            continue

        inner = m.group(2)
        rk = RK.search(inner)
        lvl = level_of(inner, src, p.stem, idx)

        keep = []
        if rk:
            keep.append("\n      " + rk.group(0))
        if lvl:
            keep.append(f'\n      <span>R{lvl} von 5</span>')
        new_inner = "".join(keep) + "\n    "

        new = src[: m.start(2)] + new_inner + src[m.end(2):]
        if new == src:
            skipped += 1
        else:
            p.write_text(new, encoding="utf-8")
            changed += 1

    print(f"  Meta-Zeile: {changed} geaendert · {skipped} unveraendert")


if __name__ == "__main__":
    main()
