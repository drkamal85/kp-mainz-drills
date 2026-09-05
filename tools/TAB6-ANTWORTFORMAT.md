# Tab-6-Antwortformat — verbindlich ab 07/2026

Entschieden von Mohamed: **Format folgt dem Fragetyp, Länge bleibt gedeckelt.**
Der 3-Zug ist eine Struktur, keine Wortzahl. Er darf die Antwort nicht verlängern.

---

## Die vier Fragetypen

| Typ | Erkennungsmerkmal | Format | Länge |
|---|---|---|---|
| **Einstieg** | „Wie gehen Sie vor?", „Patient mit X — was tun Sie?" | 3-Zug | 20–24 W |
| **Entscheidungsgrenze** | „Wann A, wann B?", „Ab wann operieren Sie?" | Antwort zuerst | 16–24 W |
| **Bildbefund** | „Was sehen Sie?", „Beschreiben Sie das CT" | Antwort zuerst | 16–24 W |
| **Kurzabfrage** | Zahl, Klassifikation, Antidot, Zeitfenster | ein Satz | 10–16 W |

**Deckel (verschärft 09/2026 nach dem Tab-6-Audit, vorher 07/2026):**
Median über das ganze Deck **16–22 W**, keine Einzelantwort **> 24 W**,
längster Satz **≤ 18 W**, durchschnittliche Satzlänge **10–13 W**.
**Eine Antwort, eine Aussage.** Steckt in einer Antwort eine Diagnose- und eine Prognoseaussage,
wird gekürzt — nicht in zwei Fragen zerlegt.

Im Zweifel kürzen. Eine Antwort, die im Drill flüssig gesprochen wird, schlägt eine
vollständige, die stockt. Fehlende Details holt die Nebenfrage.

---

## 3-Zug (nur Einstiegsfragen)

1. **Rahmen** — ein kurzer Satz, der die Struktur benennt. Kauft Denkzeit, signalisiert System.
   Maximal 10 Wörter. *„Ich gehe strukturiert vor mit Labor, Sonografie und Schnittbildgebung."*
2. **Kern** — 1–2 Sätze, **Gefährlichstes zuerst**.
   *„Zuerst schließe ich die bedrohlichen Ursachen aus: Koronarsyndrom, Lungenembolie, Dissektion."*
3. **Konsequenz** — ein Satz mit einer **echten Entscheidung**, nicht mit einer Aufzählung.
   *„Ist der Tumor resektabel, melde ich ihn zur Whipple-Operation an, ohne Biopsie."*

Behebt die dokumentierte Fehlerform „alles genannt, nichts entschieden".

## Antwort zuerst (Entscheidung, Bildbefund)

Satz 1 ist die Antwort. Danach erst die Begründung.
*„Das ist ein T2-Tumor. Er hat die Submukosa überschritten und die Muskelschicht erreicht, ohne sie zu durchbrechen."*

## Ein Satz (Kurzabfrage)

Keine Einleitung, keine Begründung, kein Rahmen.
*„Ab 5,5 cm beim Mann und ab 5,0 cm bei der Frau."*

---

## Sprachregeln (gelten für alle Typen)

- **Ziffern, keine ausgeschriebenen Zahlen.** „48 Stunden", nicht „achtundvierzig Stunden".
  „200 µg/g", nicht „zweihundert Mikrogramm pro Gramm". Hausbefund 07/2026: ausgeschriebene
  Zahlen blähten die Länge auf und machten Sätze zäh.
- **Höchstens 3 Aufzählungsglieder je Satz.** Mehr sprengt den Sprechatem.
- **Jeder Satz braucht ein finites Verb.** Keine Nominalketten wie „Metamizol 1000 mg als Basis,
  bei stärkeren Schmerzen Piritramid" — daraus wird „Ich gebe Metamizol 1000 mg intravenös,
  bei stärkeren Schmerzen Piritramid."
- **Kandidatenstimme**, also „Ich gebe…", „Ich schließe aus…".
- **Fachbegriffe im Fließtext**, keine Hervorhebung (entschieden 07/2026).
- Keine telegrafischen Marker (`=`, `→`, `+`, Label-Doppelpunkte, Semikolonketten).
- Ø Satzlänge 10–13 Wörter, längster Satz ≤ 18.

---

## Die fünf Regeln für Tab 6 (verbindlich seit 09/2026)

1. **Nur Dokumentiertes.** Jede Frage geht auf ein echtes Mainzer Protokoll zurück — kein Lehrbuch,
   kein „high-yield". Der Blockkopf (`pk-meta`) nennt **Prüfer, Datum oder Fallnummer**
   („Dr. Hennekes · 10.01.2024", „Fall 28"). Thematische Köpfe („Definition & Einteilung",
   „Lernstoff", „häufige Prüfungsfragen") sind das Warnzeichen für Erfundenes.
2. **Nicht in erfundene Nachfragen zerlegen.** Zu lange Antwort → Wortlaut kürzen, nie in Stücke
   schneiden und je Stück eine Frage erfinden („Und dann?", „Was noch?", „Warum?").
3. **Länge** wie oben. Speakable in einem Atem.
4. **Sprache.** Kandidatenstimme, jeder Satz mit finitem Verb, Ziffern, keine telegrafischen Marker,
   höchstens 3 Aufzählungsglieder, Fachbegriffe im Fließtext ohne `<strong>`.
5. **Umfang und Dubletten.** 12–18 Fragen je Deck, nur Fragen zu DIESEM Thema, keine Frage
   doppelt in Nachbardecks (Varizen → leberzirrhose, Forrest → gastroduodenales-ulkus,
   Kompartment → allgemeine-frakturlehre, VT → reanimation-cpr, SVT → vorhofflimmern,
   Hirnblutung → schaedel-hirn-trauma).

Audit 09/2026: 818 Fragen in 51 Decks geprüft, 33 erfundene entfernt, alle Antworten auf den
Deckel gebracht. Bericht: Projektdokument `claude/TAB6-AUDIT-2026-09-04.md`.

## Prüfung vor jedem Commit

`python3 tools/_check-fragen.py` prüft Zahlenschreibweise, Antwortlänge (> 24 W = FAIL), Satzlänge
(> 18 W = FAIL), Aufzählungslänge, `<strong>` in Antworten, Fragenzahl 12–18 und den Blockkopf
(Prüfer, Datum oder Fall — sonst FAIL). Er ersetzt aber nicht den **fachlichen** Check — der bleibt Handarbeit
und gehört in dieselbe Runde, nicht auf Nachfrage danach.

Reihenfolge: mining → Entwurf → **Länge und Fachcheck** → einfügen → Validatoren →
Kreuz-Deck-Duplikate → Build-Kette → Push.
