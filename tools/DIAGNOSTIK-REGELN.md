# Diagnostik-Stationen — Autorenregeln

Stand 29.08.2026. Entstanden aus Mohameds Durchsicht der Kardiologie-Umstellung
(9 Themen, 6 zunächst abgelehnt). Referenzdecks: **cholezystitis**, **morbus-hodgkin**,
**diarrhoe**. Gegenbeispiele, wo der Umbau schadete: **khk**, **infektioese-endokarditis**.

---

## 1 · Nach Untersuchungsart gliedern — mit einer Ausnahme

`Labor · Bildgebung · Biopsie · Einteilung`, nicht `Sicherung · Staging · Goldstandard`.

Begründung: Der Prüfer fragt *„Welche Laborwerte?"* und *„Was sehen Sie im CT?"* — nie
*„Was ist Ihr Goldstandard zur Sicherung?"*

**Die Ausnahme ist wichtiger als die Regel:** Trägt die vorhandene Gruppierung selbst
Prüfungsbedeutung, bleibt sie stehen.

- **khk** — „Strategie" zeigt die Eskalation Ruhe-EKG → Belastungstest → Koronarangiografie.
  Diese Logik *ist* die Antwort auf „Wie klären Sie ab?". Aufsplitten zerstört sie.
- **infektioese-endokarditis** — „Die zwei Säulen: Blutkulturen + TEE" sind die beiden
  Duke-Hauptkriterien. Das Paar ist der Inhalt.
- **synkope** — „Basisdiagnostik = Anamnese + Untersuchung + EKG + Schellong" ist eine
  Leitlinienaussage, keine willkürliche Bündelung.
- **arterielle-hypertonie** — „Endorgane" und „Sekundäre Ursachen" sind die klinische
  Logik der Abklärung, nicht Zufall.

**Prüffrage vor jedem Umbau:** Ist das Original eine formlose Textwand oder zeigt es eine
Logik? Textwand → umbauen. Logik → stehenlassen, höchstens innen aufräumen.

## 2 · Jede Karte ist eine Untersuchungsart oder eine bedeutungstragende Gruppe

Keine Karten wie „Wann testen", „Grenzen", „Ergänzend" — das sind Indikationen und
Restekategorien. Erlaubt sind zusätzlich Klassifikationen als Schlusskarte
(Ann-Arbor, Duke, Fontaine, WHO-Grade).

## 3 · Vorher die Klinik gegenlesen

Die teuerste Regel — ihre Missachtung erzeugte drei Fehler in einem Durchgang.

- **herzklappenerkrankungen** — die Auskultations-Landkarte stand schon in der Klinik
- **synkope** — Prodromi und Trigger standen schon in der Klinik
- **herzinsuffizienz** — Rasselgeräusche und Halsvenenstauung standen schon in der Klinik

**Steht es in der Klinik, gehört es nicht in die Diagnostik.** Körperliche
Untersuchungsbefunde gehören grundsätzlich in die Klinik, nicht in die Diagnostik.

## 4 · Nur eine Karte je Untersuchungsart

Nicht „Labor" und „Begleitlabor". Ist beides Blut, ist es eine Karte.

Umgekehrt gilt: **verschiedene Verfahren nicht zusammenlegen.** „EKG und Röntgen" als
eine Karte wurde zu Recht beanstandet.

## 5 · Bullets, kein Fließtext

Eine Zeile je Verfahren mit einem Halbsatz wozu. Keine Merksatzkästen für Inhalte, die
auch eine Bullet-Zeile sein können.

## 6 · Tabellen nur bei echtem Vergleich

Heiß gegen kalt, Ann-Arbor-Stadien, Defibrillation gegen Kardioversion. Nicht als Ersatz
für eine Liste.

## 7 · Reihenfolge folgt dem Ablauf am Patienten

Erst was sofort verfügbar ist, dann was dazukommt. EKG vor Langzeit-EKG (dasselbe
Verfahren gehört zusammen). Sono vor MRCP. Röntgen vor CT.

## 8 · Zielkorridor 70 bis 140 Wörter

Bibliotheksmedian vor der Umstellung: 114. Kardiologie nach der Umstellung: 77.
Über 170 nur bei Top-20-Themen, und dann mit Grund.

## 9 · Zahlen und Grenzwerte bleiben immer

Beim Kürzen fällt Prosa weg, nie eine Zahl.
`3 mm Wandverdickung · DHC 7 mm · Gradient 40 mmHg · KÖF 1 cm² · 10 und 25 mmHg ·
Xanthochromie nach 6 bis 12 Stunden`

## 10 · Messtechnik ist keine Prüfungsfrage

Bernoulli-Formel, Vmax-Definition, Schallkopfwahl, Schnittebenen-Namen: streichen.
Gefragt wird der **Befund und seine Konsequenz**, nicht wie das Gerät ihn errechnet.
Vergleiche den Echo-Drill, wo Simpson-Methode und PLAX/PSAX null Korpustreffer hatten.

## 11 · Was nicht indiziert ist, ist auch Diagnostik

Wenn ein Verfahren ausdrücklich *nicht* dazugehört, sag es. Bei Synkope gehören EEG, CT
und Doppler der Halsgefäße nicht zur Basisdiagnostik. Weglassen ist so viel wert wie wissen.

---

## Fortschrittsmarke

Ein überarbeiteter Tab trägt einen Stern in der Reiterbeschriftung:

```html
<button class="tab" data-c="diagnostik" data-tab="diagnostik">Diagnostik ★</button>
```

Nur setzen, wenn tatsächlich umgestellt wurde. Bleibt das Original stehen (khk), bleibt
auch der Stern weg.

## Ablauf je Deck

1. Diagnostik-Tab lesen — Textwand oder Logik?
2. **Klinik gegenlesen** — was steht dort schon?
3. Umbauen oder stehenlassen, entscheiden und begründen
4. Zahlen gegenprüfen, Messtechnik streichen
5. Wortzahl gegen den Korridor prüfen
6. Stern setzen, Build-Kette, Push
