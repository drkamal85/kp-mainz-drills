# sources/ — canonical tab-6 mining sources

When building, retrofitting, or coverage-checking ANY R3 **tab 6 (Fragen & Protokolle)**,
mine these ALONGSIDE the /mnt/project protocol files (Protokolle-2024-2026, 00003043,
_chat_3.txt). This folder is part of the canonical tab-6 source set.

**Coverage is only complete when ALL files below have been mined.** The 2026 band and the
Hoffart/ASRAWI files were added in July 2026 — every R3 built BEFORE that date was mined
against the older corpus only and is therefore presumed INCOMPLETE until re-checked.

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


## protokolle-2026-01-06.md  ← NEU Juli 2026
Protokollband **07.01.–10.06.2026** (108 S., ~19 200 Wörter), von Ibraheem aus der Gruppe
zusammengetragen. **Nahtlose Fortsetzung** von `Protokolle-2024-2026` (endet 07.01.2026) —
kein Überlappungsbereich, also reiner Zugewinn. Enthält die aktuellsten Prüferkonstellationen,
Fallformate und Fragestellungen. **Jede tab-6-Prüfung muss diese Datei einschließen.**

## protokolle-hoffart.md  ← NEU Juli 2026
Prüferspezifischer Katalog zu **Dr. med. Jürgen Hoffart** (aktiver Mainz-Prüfer, Autor des
149-Bilder-Bildatlas). Strukturiert nach Modalität (Röntgen / CT / MRT / Sono / Szintigramm /
Klinische Bilder / Hämatoonkologie) mit den konkret gezeigten Befunden und Anschlussfragen.
Für alle bildlastigen Themen und für den Bildatlas die maßgebliche Quelle.

## asrawi-protokollthemen.md  ← NEU Juli 2026
Unabhängige, nach Fachgebiet gegliederte Themenliste (Abdullah Asrawi) mit den je Thema
abgefragten Unterpunkten. Nutzung: **Gegenprobe** zur eigenen Themenliste (Lückenanalyse)
und als Checkliste, ob ein tab-6-Deck die typischen Unterfragen eines Themas abdeckt.
Enthält u. a. den kompletten Abschnitt **Anästhesie & Notfallmedizin** — das häufigste
Dritte Fach in Mainz.

## KP-Themenliste-flach.md
Die kanonische Themen-Rangliste (96 Themen, Stand Juli 2026), gespiegelt aus dem Project
Knowledge, damit sie versioniert vorliegt. Datenquelle für `tools/_build-master.py`.
