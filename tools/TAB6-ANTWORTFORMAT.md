# Tab-6-Antwortformat — verbindlich ab 07/2026

Entschieden von Mohamed: **Format folgt dem Fragetyp, Länge bleibt gedeckelt.**
Der 3-Zug ist eine Struktur, keine Wortzahl. Er darf die Antwort nicht verlängern.

---

## Die vier Fragetypen

| Typ | Erkennungsmerkmal | Format | Länge |
|---|---|---|---|
| **Einstieg** | „Wie gehen Sie vor?", „Patient mit X — was tun Sie?" | 3-Zug | 24–30 W |
| **Entscheidungsgrenze** | „Wann A, wann B?", „Ab wann operieren Sie?" | Antwort zuerst | 20–28 W |
| **Bildbefund** | „Was sehen Sie?", „Beschreiben Sie das CT" | Antwort zuerst | 20–28 W |
| **Kurzabfrage** | Zahl, Klassifikation, Antidot, Zeitfenster | ein Satz | 10–16 W |

**Deckel (verschärft 07/2026 auf Mohameds Anweisung „always short, simple, speakable"):**
Median über das ganze Deck **≤ 24 W**, keine Einzelantwort **> 30 W**,
längster Satz **≤ 18 W**, durchschnittliche Satzlänge **10–13 W**.

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

## Prüfung vor jedem Commit

`python3 tools/_check-fragen.py` prüft jetzt zusätzlich Zahlenschreibweise, Antwortlänge
und Aufzählungslänge. Er ersetzt aber nicht den **fachlichen** Check — der bleibt Handarbeit
und gehört in dieselbe Runde, nicht auf Nachfrage danach.

Reihenfolge: mining → Entwurf → **Länge und Fachcheck** → einfügen → Validatoren →
Kreuz-Deck-Duplikate → Build-Kette → Push.
