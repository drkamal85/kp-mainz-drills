#!/usr/bin/env python3
"""
tools/_stamp-rank.py — schreibt den Korpus-Rang in die Meta-Zeile jeder Themenseite.

Quelle ist api/themen.json, also dieselbe Rangliste wie in der Themenliste und
auf der Startseite. Eingefügt wird ein Span der Form

    <span class="rk">Rang 32 · 132 Treffer</span>

als erstes Element der Meta-Zeile. Der Lauf ist idempotent: ein vorhandener
Span wird ersetzt, nicht gedoppelt. Seiten ohne Rangeintrag (Drills, Extras
wie Pleuraerguss und Notfallpharmakologie) bleiben unberuehrt.

Nach jeder Rangaenderung erneut laufen lassen:
    python3 tools/_build-master.py && python3 tools/_stamp-rank.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPAN = re.compile(r'\s*<span class="rk">[^<]*</span>')


def load_ranks() -> dict[str, tuple[int, int]]:
    data = json.loads((ROOT / "api" / "themen.json").read_text(encoding="utf-8"))
    out = {}
    for t in data["topics"]:
        rid = t.get("reviewId")
        if not rid or not t.get("covered"):
            continue
        out[rid.rsplit("-r", 1)[0]] = (t["rank"], t["treffer"])
    return out


def main():
    ranks = load_ranks()
    changed = skipped = missing = 0

    for p in sorted(ROOT.glob("reviews/*/*.html")):
        r = ranks.get(p.stem)
        if not r:
            missing += 1
            continue

        src = p.read_text(encoding="utf-8")
        m = re.search(r'<div class="meta">', src)
        if not m:
            print(f"  UEBERSPRUNGEN (keine Meta-Zeile): {p.name}")
            continue

        rang, treffer = r
        span = f'\n      <span class="rk">Rang {rang} · {treffer} Treffer</span>'

        # vorhandenen Span entfernen, dann neu setzen — so bleibt der Lauf idempotent
        head, tail = src[: m.end()], src[m.end():]
        tail = SPAN.sub("", tail, count=1)
        new = head + span + tail

        if new == src:
            skipped += 1
        else:
            p.write_text(new, encoding="utf-8")
            changed += 1

    print(f"  Rang gesetzt: {changed} geaendert · {skipped} unveraendert · "
          f"{missing} ohne Rangeintrag (Drills und Extras)")


if __name__ == "__main__":
    main()
