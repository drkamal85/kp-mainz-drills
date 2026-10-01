# AMBOSS-Validierung — Übersicht

Regeln: `tools/AMBOSS-VALIDATE.md`. Referenz ausschließlich `sources/amboss/`.

| Deck | Erfassung | ✓ | ✗ korrigiert | ? | Diagnostik-Queue | Status |
|---|---|--:|--:|--:|--:|---|
| diarrhoe | diarrhoe.md (AMBOSS e1axfj, erfasst 26.09.2026) | 14 | 0 | 29 | 1 | done |
| antikoagulation-bridging | antikoagulation-bridging.md (AMBOSS Tm06Ug, erfasst 26.09.2026) | 33 | 0 | 12 | 0 | done |

**diarrhoe:** Die Erfassung deckt nur den Artikel „Akute Gastroenteritis" (Erwachsene) ab; C. difficile,
erregerspezifische DD, Pädiatrie und Meldepflicht sind bekannte Lücken — alles dazu ist `?`, nicht `✗`.
Kein klarer Widerspruch außerhalb der Diagnostik. Ein Diagnostik-Widerspruch in der Queue.

**antikoagulation-bridging:** Deck auf Grundlage der Erfassung gebaut, deshalb kein Widerspruch. Die `?` betreffen
Heparin, NMH und HIT — das Kapitel „Parenterale Antikoagulanzien" ist eine bekannte Lücke — sowie INR-Zielbereich,
Scores und Therapiedauer.
