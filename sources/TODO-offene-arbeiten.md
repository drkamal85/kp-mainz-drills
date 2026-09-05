# Offene Arbeiten

Stand-Liste für Themen, die besprochen, aber noch nicht erledigt sind.

---


## Tab 6 auf erfundene Fragen prüfen — ERLEDIGT 05.09.2026 (aufgenommen 29.08.2026)

**Erledigt:** Alle 51 Decks mit Tab 6 geprüft (818 Fragen), 33 erfundene gestrichen, 59 themenfremde
Fragen entfernt oder in Nachbardecks verschoben, alle Blockköpfe auf Prüfer/Datum/Fall, alle Antworten
auf ≤ 24 W. Bericht: Projektdokument `claude/TAB6-AUDIT-2026-09-04.md`. Geparkte Fragen für Decks ohne
Tab 6 stehen in `PARKED-fuer-R2-R3.md`. `_check-fragen.py` erzwingt die Regeln jetzt (FAIL statt Warnung).

**Anlass:** Bei `non-hodgkin-lymphome` waren **12 von 19 Fragen erfunden**. Die Blöcke trugen
keine Protokollquelle, sondern Themenüberschriften wie „KP-Prüfung Hämatologie · Definition
& Paradox". Der Korpusabgleich ergab null Treffer für „indolent", „watch and wait" und
„therapeutisches Paradox".

**Regel, gegen die verstossen wurde:** Tab 6 enthält ausschliesslich dokumentierte
Mainz-Fragen — nie erfunden, nie kuratiert, nie „allgemein high-yield".

**Umfang:** 59 Decks mit Tab 6, insgesamt rund 900 Fragen.

**Was der Schnelltest schon fand** (Beschriftung ohne Quellenhinweis):
- `aortendissektion` (Rang 64) — 3 von 5 Blöcken heißen nur „Mündliche Prüfung · dokumentiert"
- `pleuraerguss` — 1 von 4 Blöcken heißt nur „Internistischer Fall"

**Warum das nicht genügt:** Der Test prüft nur die Blockbeschriftung. Bei NHL trugen die
erfundenen Blöcke durchaus eine Beschriftung — sie war nur keine echte Quelle. Die
belastbare Prüfung ist der **Korpusabgleich je Frage**: Kommen die Schlüsselbegriffe der
Frage im Protokollkorpus überhaupt vor?

**Vorgehen, wenn es drankommt:**
1. Je Deck die Schlüsselbegriffe aller Tab-6-Fragen gegen den Korpus zählen
2. Fragen mit null oder ein bis zwei Treffern markieren
3. Kontext lesen — manche Begriffe kommen anders formuliert vor
4. Erfundene streichen, thematisch fremde ins richtige Deck parken
5. Sinkt ein Deck unter 12 Fragen: ehrlich lassen, nicht auffüllen
6. Ergebnis vorlegen, bevor gestrichen wird

**Erwartung:** Die früh gebauten R3-Decks sind am ehesten betroffen. Bei NHL entstand der
Fehler, weil das Thema kaum dokumentiert ist und der Tab trotzdem gefüllt wurde.

---

## Diagnostik-Umstellung — 79 Decks offen

- **6 bereits konform**, nur Stern setzen: ileus, pavk, akutes-abdomen, pankreaskarzinom, gicht
- **13 fast konform**, ein Kartentitel daneben — z.B. `sprunggelenksfraktur` und
  `beckenringfrakturen` mit zusammengelegtem „Bildgebung + Labor", `nierenversagen` mit „Zuerst"
- **61 brauchen echten Umbau** — stapelweise nach Fach, Kardiologie ist fertig

## Therapie — gezielte Eingriffe statt Umstellung

Kein Rasterumbau. Die Station ist bereits besser strukturiert als die Diagnostik war; Gerüste
wie „Zwei Ziele" (khk), „Vier Säulen" (herzinsuffizienz) und „A-B-C" (vorhofflimmern) bleiben.

- **22 „★ Anker"-Karten auflösen** — eine Karte für alles ist nie richtig
- **Fremdinhalte umziehen** — z.B. `synkope` hat eine DD-Karte in der Therapie, gehört in die Klinik
- **9 Decks über 216 W kürzen** — `vorhofflimmern` mit 217 W auf Rang 2 ist der Extremfall

## Morbus Hodgkin auf R2 und R3

6 Fragen aus dem NHL-Deck sind in PARKED vermerkt. Zusammen mit dem dort bereits geparkten
Material ergeben sich 12 bis 14 dokumentierte Fragen. Das Deck steht auf R1, war aber zweimal
Prüfungsfall.


---

## Tab 6 · Audit auf erfundene Fragen (aufgenommen 29.08.2026) — ERLEDIGT 05.09.2026, siehe oben

**Anlass:** Bei `non-hodgkin-lymphome` waren 12 von 19 Fragen erfunden — vier Bloecke trugen
keine Protokollquelle, sondern Themenueberschriften wie „KP-Pruefung Haematologie · Definition
& Paradox". Korpusabgleich: „indolent", „watch and wait" und „therapeutisches Paradox" haben
null Treffer. Das verstoesst gegen die stehende Regel, dass Tab 6 ausschliesslich dokumentierte
Mainz-Fragen enthaelt.

**Umfang:** 60 Decks haben einen Tab 6.

**Was NICHT funktioniert:** Eine Metadaten-Heuristik ueber die `pk-meta`-Zeile. Der Versuch
lieferte 35 Decks mit angeblich 326 verdaechtigen Fragen — fast alles Fehlalarme, weil
Pruefername und Datum in getrennten Spans stehen.

**Was funktioniert:** Korpusabgleich pro Frage. Schluesselwoerter der Frage gegen den
Protokollkorpus pruefen. Ein erster Durchlauf mit Schwelle 0,34 liefert **22 Decks mit
29 korpusfernen Fragen** — eine handhabbare Liste, die manuell nachgeprueft werden muss.

Auffaellig zuerst: akute-leukaemien (3 von 22), aufklaerung-einwilligung-betreuung (2 von 22),
leberzirrhose (2 von 21), schlaganfall (2 von 26), polytrauma-abcde (2 von 16),
hueft-knie-tep (2 von 17).

**Vorgehen, wenn drangenommen:**
1. Die 29 Treffer einzeln gegen den Korpus pruefen — Automatik nur als Vorfilter
2. Bestaetigte Erfindungen streichen, nicht umformulieren
3. Faellt ein Deck dabei unter 12 Fragen, ist das die ehrliche Zahl (siehe NHL mit 7)
4. Bloecke ohne Pruefername, Datum oder Fallbezug beim Anfassen mit Quelle versehen

**Verwandt:** Fragen, die inhaltlich in ein Nachbardeck gehoeren, sind ein anderer Fehler —
siehe gi-blutung (28 auf 18) und non-hodgkin-lymphome (Hodgkin-Fragen umgezogen).
Beide Pruefungen gehoeren in denselben Durchgang.
