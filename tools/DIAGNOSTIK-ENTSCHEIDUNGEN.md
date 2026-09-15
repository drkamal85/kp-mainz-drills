# Diagnostik-Umstellung — Entscheidungsprotokoll

Stand 15.09.2026. Ergänzt `DIAGNOSTIK-REGELN.md`: das Regelwerk sagt, **wie**
eine Diagnostik-Station gebaut wird, dieses Protokoll hält fest, **was** bei der
Umstellung von 88 Decks entschieden wurde und **woraus**.

**Warum es diese Datei gibt:** Die Begründung des Bucket-D-Umbaus stand in einer
Commit-Message, die bei einem Rebase auf die generierten Feeds verlorenging. Der
Inhalt ist korrekt publiziert, die Begründung war weg. Steht sie nicht im Repo,
öffnet die nächste Sitzung längst getroffene Entscheidungen erneut.

**Endstand: 88 von 88 Decks mit Stern.**

> **Der Stern hat seit 15.09.2026 eine erweiterte Bedeutung.** Waehrend der
> Umstellung hiess er „nach Untersuchungsart umgestellt". Jetzt heisst er
> **„Diagnostik geprueft und freigegeben"** — das schliesst die neun
> Bucket-C-Decks ein, die bewusst NICHT umgestellt wurden, weil ihre
> Gruppierung selbst die Pruefungsantwort traegt.
>
> **Wer ein Deck aus Abschnitt 1 mit Stern sieht und darin eine Eskalationskette
> oder ein Kriterienpaar findet, hat keinen Verstoss gefunden, sondern die
> Ausnahme aus Regel 1.** Nicht umbauen. Genau das ist im August bei khk
> passiert und musste zurueckgesetzt werden.

---

## 1 · Bucket C — neun Decks, die so bleiben

Regel 1 gliedert nach Untersuchungsart, **außer** die vorhandene Gruppierung
trägt selbst Prüfungsbedeutung. Diese neun fallen unter die Ausnahme. Sie sind
geprüft, nicht übersehen. **Nicht umbauen, nicht neu triagieren.**

Diese neun tragen den Stern, sind aber **nicht nach Untersuchungsart gegliedert**
— sie sind geprueft und in dieser Form freigegeben.

| Deck | Warum die Gruppierung die Antwort ist |
|---|---|
| khk | Ruhe-EKG → Belastungstest → Koronarangiografie. Die Eskalation *ist* die Antwort auf „Wie klären Sie ab?" (nennt das Regelwerk selbst) |
| infektioese-endokarditis | „Die zwei Säulen: Blutkulturen + TEE" sind die beiden Duke-Hauptkriterien (nennt das Regelwerk selbst) |
| schock | Die ZVD/HZV/SVR-Tabelle trennt die vier Schockformen — genau danach wird gefragt |
| tvt | Wells → D-Dimer → Kompressionssonografie, die Leitlinienkette |
| tuberkulose | Indirekte Tests zeigen nur Kontakt, nur der direkte Nachweis beweist — dokumentierte Prüferkorrektur |
| schilddruesenkarzinom | Sonografie → Szintigrafie → FNP, die Eskalation am Knoten |
| cushing-syndrom | Bestätigen → ACTH → lokalisieren, Bildgebung zuletzt wegen der Inzidentalome |
| hyponatriaemie-siadh | SIADH ist Ausschlussdiagnose: erst Schilddrüse, Nebenniere, Medikamente |
| bluttransfusion | Die drei vorgeschriebenen Tests und die Trennung Labor/Bett sind die Richtlinie; der Bedside-Test wurde in vier Protokollen gefragt |

`bluttransfusion` ist der schwächste Fall der neun — die Kartennamen „Vor der
Gabe" und „Bedside" sind Zeitmarken, keine Verfahren. Wer ihn nach B umsortieren
will, braucht eine Umbenennung, keinen Umbau.

---

## 2 · Bucket D — sechs umgebaute Stationen

Vor jedem Umbau wurden die Klinik gegengelesen (Regel 3) und der Protokollkorpus
gezählt. Zahlen und Grenzwerte sind überall geblieben (Regel 9).

### reanimation-cpr · 268 → 141 W
Drei Karten — etCO₂, Steuerung, ROSC — beschrieben **ein** Verfahren und
verstießen gegen Regel 4. Zusammengezogen zu einer Karte `Kapnografie`.
- **Korpus:** `etCO₂`, `Kapnografie`, `ROSC` **null Treffer**; Reanimation 23,
  Defibrillation 19, 4H/HITS je 3.
- **Doppelung:** Die ROSC-Karte stand schon in der **Therapie**
  („Nach ROSC beginnt die Arbeit erst"), die Kapnografie teilweise in der
  **Klinik** („Kapnografie sichert die Tubuslage").
- **Geblieben:** alle sechs Zahlen — 35–45, 25, 30, 10 nach 20 min, 40 mmHg.
- **Nicht ergänzt:** Rhythmusanalyse (schockbar/nicht schockbar) — steht in den
  **Grundlagen**, trotz 19 Defibrillations-Treffern.

### leberzirrhose · 260 → 167 W
Jetzt Labor · Sonografie · ÖGD · Punktion · Child-Pugh.
- **Gestrichen:** Elastografie/FibroScan, Duplex, Leberbiopsie — **null Treffer**.
- **Zusammengelegt:** die eigene MELD-Karte (1 Treffer) zu einer Zeile in der
  Child-Pugh-Schlusskarte; Child-Pugh wird namentlich gefragt (3 Treffer).
- **Neu:** knappe `ÖGD`-Karte fürs Varizenscreening — **Ösophagusvarizen 7
  Treffer**, und die Station hatte überhaupt keine Endoskopie-Karte.
- **Gestrichen, weil redundant:** die Aufzählung „Die fünf Parameter"
  wiederholte die erste Spalte der Child-Pugh-Tabelle.

### hueft-knie-tep · 125 → 103 W
Jetzt Röntgen · Punktion · Labor. Die Karte `Klinisch` wurde **entfernt**.
- **Grund:** reine körperliche Untersuchung (Gangbild, Neutral-Null,
  Trendelenburg, Thomas-Handgriff, tanzende Patella) — Regel 3 weist sie der
  Klinik zu. Korpus: Trendelenburg, Thomas, Gelenkpunktion **null Treffer**.
- **Nicht übernommen:** „vor jedem Wechsel punktieren" — steht schon in der Klinik.
- **→ siehe offener Punkt 4.1. Der Inhalt wurde gelöscht, nicht verschoben.**

### non-hodgkin-lymphome · 128 → 130 W
Zwei Sammelkarten → die Form des Referenzdecks **morbus-hodgkin**:
Labor · Bildgebung · Biopsie · Ann-Arbor. **Nichts gestrichen**, nur nach
Untersuchungsart sortiert; Labor und Staging-Bildgebung saßen vorher in der
Sicherungs-Karte. Korpus dünn: Ann-Arbor 1, Non-Hodgkin 4.

### akute-leukaemien · 80 → 101 W
Eine überladene Karte (Blutbild, Knochenmark, Immunphänotyp, Zytogenetik,
Liquor) → Blutbild · Knochenmark · Labor · Liquor. **Nichts gestrichen.**
Korpus: Leukämie 8, AML 4, Blasten 2, Hiatus leucaemicus 2.

### akuttoxikologie · 91 → 117 W
Jetzt Fremdanamnese · Labor · BGA · EKG · Spiegel.
- **Behobene Doppelung:** BGA stand in der Merksatzliste **und** hatte eine
  eigene Karte. Die Liste nennt jetzt die Blutwerte und verweist auf die Karten
  BGA und EKG — die Rezitierliste bleibt damit vollständig.
- Die Fremdanamnese (Blister, Flaschen, Abschiedsbrief) steht zuerst, weil sie
  beim Bewusstlosen zuerst kommt.

---

## 3 · Korpuszählung — wie, und wo sie täuscht

Gezählt wurde über `sources/protokolle*.md` und `sources/PARKED-fuer-R2-R3.md`.

**Zwei Fallen, beide real aufgetreten:**

1. **Teilstring-Treffer.** Eine naive Suche nach `Child` trifft **Schild**drüse,
   `MELD` trifft **Meld**epflicht. Der erste Durchlauf meldete so 41 Child- und
   23 MELD-Treffer; mit Wortgrenzen blieben 3 und 1 übrig. **Immer mit
   `\b`-Grenzen oder vollem Begriff (`Child-Pugh`) zählen und die Fundstellen
   im Kontext ansehen.**
2. **Null Treffer heißt nicht „wird nicht gefragt".** Es heißt: kein Protokoll
   dokumentiert es. Der Korpus ist eine Stichprobe mitgeschriebener Prüfungen,
   kein Lehrplan. Null Treffer rechtfertigt das Streichen von **Messtechnik und
   Redundanz** (Regel 10), nicht das Streichen eines Verfahrens, das in der
   Prüfung selbstverständlich erwartet wird.

Der Präzedenzfall aus Regel 10 bleibt gültig: Simpson-Methode und PLAX/PSAX
hatten null Treffer und wurden zu Recht gestrichen.

---

## 4 · Offen

### 4.1 hueft-knie-tep — die gelöschte Karte `Klinisch`
**Nicht entschieden.** Trendelenburg und Thomas-Handgriff sind die
Standarduntersuchung der Hüfte. Null Korpustreffer heißt hier nur, dass kein
Protokoll sie dokumentiert — nicht, dass kein Prüfer danach fragt. Die Karte
wurde entfernt, nicht in die Klinik verschoben.

Drei Möglichkeiten: in die **Klinik** übernehmen (regelkonform, Regel 3), in der
Diagnostik wiederherstellen (widerspricht Regel 3), oder gestrichen lassen.
**Mohamed entscheidet.** Bis dahin nicht eigenmächtig wiederherstellen.

### 4.2 Wortzahl über dem Korridor
Regel 8 nennt 70–140 Wörter, über 170 nur bei Top-20-Themen. Diese Decks liegen
darüber, ohne Top-20 zu sein — beim nächsten Anfassen kürzen, kein eigener
Durchgang: verbrennung 216, aufklaerung-einwilligung-betreuung 198,
schaedel-hirn-trauma 193, meningitis 189.

---

## 5 · Merksatz für die nächste Sitzung

Die Diagnostik-Umstellung ist **abgeschlossen**, alle 88 Decks tragen den Stern.
Wer hier wieder anfängt, triagiert nichts neu: die neun C-Decks aus Abschnitt 1
sind geprüft und bleiben in ihrer Form, die sechs D-Decks sind gebaut und
freigegeben. Offen sind nur 4.1 und 4.2.
