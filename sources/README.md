# sources/ — canonical tab-6 mining sources

When building, retrofitting, or coverage-checking ANY R3 **tab 6 (Fragen & Protokolle)**,
mine these ALONGSIDE the /mnt/project protocol files (Protokolle-2024-2026, 00003043,
_chat_3.txt). This folder is part of the canonical tab-6 source set.

## protokolle-sortiert.md
Subject-SORTED topic/question index of the Mainz KP (~12k words), extracted from the
project file `00002492ProtokollenSortieren.pdf` — which is actually a **ZIP archive**
(PK header; `pdftotext` returns nothing). To re-extract from the raw file:
`unzip 00002492ProtokollenSortieren.pdf` → `1.txt … 68.txt` (+ manifest.json).

It lists, per topic, the SUBPOINTS examiners ask (e.g. Pneumothorax → Monaldi / Bülau /
Einteilung / Ätiologie / Notmaßnahmen). Use it to (a) top up missing tab-6 questions and
(b) run gap analysis of built-vs-asked topics.

Note: this file is high-value — supersedes any earlier note that called the
ProtokollenSortieren archive unreadable/deletable.
