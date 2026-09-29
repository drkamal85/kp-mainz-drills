# Leistenhernie (Hernia inguinalis) — AMBOSS

- **Artikel-ID:** zh0rgf
- **URL:** https://next.amboss.com/de/article/zh0rgf
- **Zuletzt bearbeitet (AMBOSS):** 31.08.2026
- **Erfasst:** 2026-09-26
- **Methode:** Browser-Automatisierung (device bridge, AMBOSS-Suche "Leistenhernie" → Kapitel "Leistenhernie"), Abschnitte einzeln per Anker-Navigation (URL#Anker) geöffnet, Text per get_page_text extrahiert (find → scroll_to/Anker-Navigation → get_page_text Muster gemäß `amboss-scraping` Skill). Wortwörtliche Übernahme, keine Paraphrasierung.
- **Bekannte Lücken:**
  - Unterabschnitt "Häufigkeit der operativen Versorgung [4]" (unter Epidemiologie) — Navigationslink/Überschrift vorhanden, Fließtext-Inhalt beim wiederholten Rendern nicht extrahierbar geworden (vermutlich zusätzliche Statistik zur OP-Häufigkeit, Referenz [4] = Lorenz et al. 2015, siehe Quellen).
  - Satz "Ca. 30% der Personen mit Leistenhernie haben zum Zeitpunkt der Untersuchung keine Begleitsymptomatik" — im Abschnitt Symptomatik per Suche lokalisiert, aber nicht im linear extrahierten Fließtext enthalten (vermutlich Popup/Highlight-Box); Inhalt hier dennoch ergänzt, da wortwörtlich vorgefunden.
  - Navigationslink "Folgekomplikationen der operativen Therapie" existiert im Artikel-Menü, führte aber beim Aufrufen zu keinem separat auffindbaren Fließtext unterhalb von "Komplikationen" (dort erscheint nur "Inkarzeration"); möglicherweise Bestandteil des separaten Grundlagenkapitels "Hernien" (nicht Teil dieser Erfassung).
  - "Sportlerleiste" wird im Artikel als verlinktes verwandtes Thema erwähnt (Referenz [41]: Muschaweck, Koch: Sportlerleiste), ist aber ein eigenständiges AMBOSS-Kapitel und wurde hier nicht mit erfasst.
  - Bilder/Illustrationen (Sagittalschnitt, Anatomie Leistenkanal, intraoperative Fotos, Operationsvideo) nur als Bildunterschriften/Titel erfasst, keine Bildinhalte extrahierbar.
  - Hinweis: Im Zusammenfassungstext wird auf ein separates "Grundlagenkapitel Hernien" verwiesen (allgemeine Ätiologie, Terminologie, Grundprinzipien der Therapie) — dieses Grundlagenkapitel ist NICHT Teil dieser Erfassung (nur die spezifische Leistenhernie-Seite wurde erfasst).

---

## Zusammenfassung

Eine Leistenhernie ist eine Ausstülpung von parietalem Bauchfell (Bruchsack), ggf. mit intraabdominellen Strukturen (Bruchinhalt), durch eine Schwachstelle der Bauchwand (Bruchpforte) im Bereich der Leiste. Das Krankheitsbild ist häufig. Männer haben aufgrund der anatomischen Gegebenheiten (Descensus testis mit resultierendem Processus vaginalis) ein erhöhtes Risiko. Leitsymptom der Leistenhernie ist eine inguinale Schwellung bzw. Vorwölbung, die häufig von einem Fremdkörpergefühl bzw. von Schmerzen begleitet wird.

Leistenhernien heilen nicht spontan aus. Bei Frauen sollte jede Leistenhernie operativ versorgt werden, bei Männern ist eine Operation insb. bei symptomatischem oder progredientem Befund indiziert. Bei der operativen Versorgung werden offene von minimalinvasiven und nahtbasierte von netzbasierten Verfahren unterschieden. Bei akuter Einklemmung mit nachfolgender Unterbrechung der Durchblutung des Bruchinhalts (Inkarzeration) ist aufgrund der akuten Lebensgefahr eine Notfalloperation indiziert.

*Allgemeine Informationen zu Ätiologie, Terminologie und Grundprinzipien der Therapie finden sich im Grundlagenkapitel Hernien (nicht Teil dieser Erfassung).*

## Definition

**Allgemeine Definition**
- Ausstülpung des Peritoneum parietale (Bruchsack)
- Häufig zusammen mit intraabdominellen Strukturen (Bruchinhalt)
- Durch eine Schwachstelle der Bauchwand (Bruchpforte) im Bereich der Leiste

**Mögliche Differenzierungen**

*Nach Bruchform*
- Direkte Leistenhernie: Direkter Durchtritt des Bruchsacks durch die Bauchwand (im Bereich des muskelarmen Trigonum Hesselbach) medial der epigastrischen Gefäße
- Indirekte Leistenhernie: Indirekter Durchtritt des Bruchsacks durch die Bauchwand (über den Leistenkanal) lateral der epigastrischen Gefäße
- Skrotalhernie: Sonderform der Leistenhernie, bei der der Bruchsack bis in das Skrotum reicht
- Gleithernie
- Schenkelhernie: Keine Leistenhernie im eigentlichen Sinn

*Nach Reponierbarkeit/Inkarzeration*
- Reponible Hernie
- Irreponible Hernie
- Inkarzerierte Hernie

*Nach Zeitpunkt des Auftretens*
- Primäre Leistenhernie: Erstmalig in Erscheinung tretende Leistenhernie
- Rezidivleistenhernie: Nach operativer Versorgung erneut auftretende Leistenhernie

## Epidemiologie

- **Inzidenz:** Alters- und geschlechtsabhängig
  - Steigendes Risiko mit zunehmendem Lebensalter
  - Auftreten anatomisch bedingt bei ♂ deutlich häufiger als bei ♀
- **Spezifische Häufigkeit**
  - Nach Bruchform: Indirekt > direkt (Verhältnis ca. 2:1)
  - Nach Lokalisation: Rechts > links > beidseitig

> Die Inzidenz der Leistenhernie nimmt mit dem Alter zu!

> Anatomisch bedingt treten Leistenhernien mit einem Verhältnis von ca. 9:1 bei Männern deutlich häufiger auf als bei Frauen!

*Wenn nicht anders angegeben, beziehen sich die epidemiologischen Daten auf Deutschland.*

*(Unterabschnitt "Häufigkeit der operativen Versorgung [4]" — Inhalt nicht extrahierbar, siehe Bekannte Lücken)*

## Übersicht

**QUIZ – Leistenhernien - Übersicht**

|  | Direkte (mediale) Leistenhernie | Indirekte (laterale) Leistenhernie |
|---|---|---|
| **Innere Bruchpforte** | Trigonum Hesselbach (medial der Vasa epigastrica) | Innerer Leistenring (lateral der Vasa epigastrica) |
| **Äußere Bruchpforte** | Äußerer Leistenring | Äußerer Leistenring |
| **Bruchsack bzw. Bruchhüllen** | Anteile: Peritoneum parietale sowie Hüllen von Bauchwand und Hoden (ohne Anteile des M. cremaster); Verlauf: „Direkt" durch die Fascia transversalis (senkrecht zur Bauchwand) | Anteile: Peritoneum parietale und Hüllen des Samenstrangs (inkl. Anteile des M. cremaster); Verlauf: „Indirekt" durch den Leistenkanal, innerhalb des Funiculus spermaticus (♂), entlang des Lig. teres uteri (♀) |
| **Bruchinhalt** | Häufig: Omentum majus, Dünndarmanteile; Selten: Dickdarmanteile, Harnblasenwand, Ovarien | Häufig: Omentum majus, Dünndarmanteile; Selten: Dickdarmanteile, Harnblasenwand, Ovarien |
| **Ätiologie** | Immer erworben | Angeboren oder erworben |

*Für Informationen zu Risikofaktoren siehe: Risikofaktoren für das Auftreten äußerer Hernien*

> Dr. med. immer erworben → Direkte Leistenhernie, medial der epigastrischen Gefäße, immer erworben!

## Klassifikation

**Aachener Klassifikation der Leistenhernie**

Die Aachener Klassifikation war in Deutschland lange Zeit gebräuchlich. Sie bildet die Grundlage für die aktuell gebräuchlichere EHS-Klassifikation.

**QUIZ – Leistenhernien - Aachener Klassifikation**

| Aspekt | Bewertung |
|---|---|
| Lokalisation der Bruchpforte | L = lateral; indirekte Leistenhernie<br>M = medial; direkte Leistenhernie<br>F = femoral; Schenkelhernie<br>C/ML = kombinierte Hernie<br>Rx = Rezidivanzahl |
| Größe der Bruchpforte | I = <1,5 cm<br>II = 1,5–3 cm<br>III = >3 cm |

**EHS-Klassifikation der Leistenhernie**

Die Klassifikation der EHS (European Hernia Society) ist international gültig und sollte bevorzugt angewendet werden (auch zur besseren Vergleichbarkeit von Studien).

**QUIZ – Leistenhernien - EHS-Klassifikation**

| Aspekt | Bewertung |
|---|---|
| Art der Hernie | Primär / Rezidiv |
| Größe der Bruchpforte | 0 = keine Hernie<br>1 = mit 1 Finger passierbar (<1,5 cm)<br>2 = mit 2 Fingern passierbar (1,5–3 cm)<br>3 = mit mehr als 2 Fingern passierbar (>3 cm)<br>x = nicht untersucht |
| Lokalisation der Hernie | Lateral / Medial / Femoral |

## Symptomatik

- **Leitsymptom:** Inguinale Schwellung bzw. Vorwölbung
- **Typische Begleitsymptome:** Fremdkörpergefühl bzw. Schmerzen
- **Bei Inkarzeration:** Ileussymptomatik (siehe auch: Ileus - Symptome)
- Ca. 30% der Personen mit Leistenhernie haben zum Zeitpunkt der Untersuchung keine Begleitsymptomatik

> Das Ausmaß von Schmerzen bzw. Fremdkörpergefühl korreliert nicht mit der Größe der Leistenhernie!

## Diagnostik

**Anamnese**
- Anamnestische Hinweise auf das Vorliegen einer Leistenhernie
  - Schilderung der typischen Begleitsymptome
  - Beschwerdezunahme bei Belastung
  - Familiäre Disposition und weitere Risikofaktoren für das Auftreten äußerer Hernien

**Körperliche Untersuchung**
- Hinweise zur Durchführung
  - Nach Möglichkeit vergleichende Untersuchung im Liegen und im Stehen
  - Immer beidseitig untersuchen
- Inspektion und Palpation
  - Inguinale Schwellung bzw. Vorwölbung → Reponierbarkeit überprüfen
  - Leistenkanal tasten und Hustenanprall testen

> Anamnese und körperliche Untersuchung sind bei der Diagnostik einer Leistenhernie wegweisend und i.d.R. ausreichend!

**Bildgebende Verfahren**
- Verfahren der Wahl: (Dynamische) Sonografie

## Differenzialdiagnosen

**Allgemeine Differenzialdiagnosen**

Alle Erkrankungen mit inguinaler Schwellung (mit oder ohne Schmerzen), bspw.:
- Schenkelhernie
- Lymphknotenschwellung
- Leistenabszess bzw. Senkungsabszess

**Differenzialdiagnosen zur Skrotalhernie**
- Hydrocele testis
- Varicocele testis

*AMBOSS erhebt für die hier aufgeführten Differenzialdiagnosen keinen Anspruch auf Vollständigkeit.*

## Therapie

**Konservative Therapie der Leistenhernie**

*Therapieoptionen und Indikationen*
- Beobachtendes Abwarten
  - Ausschließlich bei Männern mit primären, asymptomatischen, nicht-progredienten Leistenhernien
- Repositionsversuch: Bei akuter Einklemmung einer nicht spontan reponiblen (nicht inkarzerierten) Leistenhernie
- Tragen eines Bruchbandes: Nicht mehr empfohlen!

> Primäre, asymptomatische und nicht-progrediente Leistenhernien bei Männern können prinzipiell konservativ behandelt werden!

> Spontane Rückbildungen werden bei Leistenhernien nicht beobachtet!

**Operative Therapie der Leistenhernie**

*Therapieoptionen: Grundsätzliche Unterscheidung zwischen*
- Offenen (anterioren) und minimalinvasiven (posterioren) Verfahren
- Naht- und netzbasierten Verfahren

*Indikationen zur Operation bei Leistenhernie*
- Elektive Versorgung bei
  - Frauen (unabhängig von Bruchform, Symptomatik und Progredienz)
  - Primären, symptomatischen bzw. progredienten, reponiblen Leistenhernien
  - Rezidivleistenhernien
  - Ggf. intraoperativer Zufallsbefund bei minimalinvasiver OP der Gegenseite
- Umgehende Versorgung bei
  - Irreponiblen Leistenhernien → Dringliche Operation
  - Inkarzerierten Leistenhernien → Sofortiger Notfalleingriff

> Bei Frauen sollten Leistenhernien unabhängig von Bruchform, Symptomatik und Progredienz primär operativ versorgt werden!

> Eine inkarzerierte Leistenhernie muss umgehend (notfallmäßig) operativ versorgt werden!

*Übersicht der Operationsverfahren*

**Offene Operationsverfahren (immer mit anteriorem Operationszugang)**
- Nahtbasiert nach Shouldice
  - Verstärken der Hinterwand des Leistenkanals durch Dopplung der Fascia transversalis
  - Fixierung des M. obliquus internus und M. transversus am Leistenband mit nicht-resorbierbarer Naht
- Netzbasiert nach Lichtenstein
  - Einlage eines Kunststoffnetzes zwischen M. obliquus internus abdominis und Externusaponeurose
  - Fixierung des Netzes mit nicht-resorbierbarer Naht → Bildung einer Stabilität verleihenden Narbe

**Minimalinvasive Operationsverfahren (immer netzbasiert mit posteriorem Operationszugang)**
- TAPP (Transabdominelle präperitoneale Plastik): Minimalinvasive, präperitoneale Netzeinlage von intraperitoneal
- TEPP (Total extraperitoneale Patch-Plastik) bzw. TEP (Total extraperitoneale Plastik): Minimalinvasive, komplett extraperitoneale Netzeinlage

> „Shouldice twice" = Fasziendopplung
> „Nach Lichtenstein kommt etwas rein" = Einlage eines Kunststoffnetzes

*(Bildmaterial: Hernioplastik nach Shouldice, Hernioplastik nach Lichtenstein, Transabdominale Präperitoneale Plastik (TAPP), Totale Extraperitoneale (Patch) Plastik (TEP bzw. TEPP), Netzbasierte Verfahren zur Hernienreparation, Offene OP einer indirekten Leistenhernie, Indirekte Leistenhernie links (intraoperativer Laparoskopiebefund), Netzplatzierung bei endoskopischer Leistenherniotomie, Video: Extraperitoneale laparoskopische Leistenherniotomie - GeSRU - AMBOSS Video — nur Titel/Bildunterschriften erfasst)*

## Komplikationen

**Inkarzeration**
- **Definition:** Akute Einklemmung des Bruchinhalts mit Unterbrechung der Durchblutung
- **Folge:** Ischämie → Gewebeuntergang → Akutes Abdomen
- **Risikofaktor:** Kleine Bruchpforte
- **Typische klinische Zeichen**
  - Schmerzen und Rötung im Bereich des Unterbauchs
  - Irreponible inguinale (bzw. skrotale) Schwellung bzw. Vorwölbung
  - Pressstrahlgeräusche in der Auskultation
  - Ileussymptomatik (bspw. Übelkeit, Erbrechen, Stuhlverhalt)
- **Therapie:** Umgehende operative Versorgung (Notfalleingriff) — siehe auch: Leistenhernie - Operative Therapie
- **Letalität:** Ca. 20%

> Eine inkarzerierte Leistenhernie stellt eine akute Lebensbedrohung dar und muss daher umgehend operativ versorgt werden!

*Es werden die wichtigsten Komplikationen genannt. Kein Anspruch auf Vollständigkeit.*

## Kinder und Jugendliche [10][35][36]

**Epidemiologie**
- Inzidenz (je nach Quelle): Ca. 1–4% aller Kinder (bei Frühgeborenen 30%, Reifgeborenen 0,8–5%)
- Geschlecht: ♂ > ♀ (ca. 5:1)

**Symptome/Klinik**
- Inguinale Vorwölbung, insb. beim Schreien

**Diagnostik**
- Körperliche Untersuchung
- Sonografie

**Therapie**
- **Indikation:** Immer Operation
- **Operationszeitpunkt**
  - Bei inkarzerierter (und irreponibler) Leistenhernie: Notfallmäßig sofort
  - Bei symptomatischer (reponibler) Leistenhernie: Sofort bzw. innerhalb von 24–48 h nach Reposition in Sedierung
  - Bei asymptomatischer Leistenhernie: Möglichst zeitnah, max. 4 Wochen nach Diagnosestellung
  - Bei Frühgeborenen: Meist OP erst nach Entlassung aus der neonatologischen stationären Behandlung
- **Operationsverfahren:** Offen / Minimalinvasiv

## Tipps & Links

- GeSRU-Operationsvideos, Extraperitoneale laparoskopische Leistenherniotomie

## Quellen

1. Berger: *Evidenzbasierte Behandlung der Leistenhernie des Erwachsenen (Evidence-based hernia treatment in adults)*. In: Dtsch Arztebl Int. Band: 113, 2016, doi: 10.3238/arztebl.2016.0150, p.150–8.
2. Schwarz et al.: *Allgemein- und Viszeralchirurgie essentials*. Georg Thieme Verlag 2009, ISBN: 978-3-131-26346-9.
3. Schumpelick: *Hernienchirurgie: Leistenhernien bei Erwachsenen und Kindern*. In: Dt Ärztebl. Band: 48, Nummer: 94, 1997, p.3268-3276.
4. Lorenz et al.: *Ambulante und stationäre Hernienchirurgie in Deutschland – aktueller Stand*. In: Chirurgische Allgemeine Zeitung. Band: 16, Nummer: 5, 2015, p.268-275.
5. Raakow et al.: *Elektive Versorgung von Leistenhernien in der universitären Chirurgie – eine ökonomische Herausforderung*. In: Der Chirurg. Band: 90, Nummer: 12, 2019, doi: 10.1007/s00104-019-1008-z, p.1011-1018.
6. Wirth et al.: *Ambulanter transabdomineller präperitonealer Leistenhernienverschluss (TAPP) – um welchen Preis?* In: Der Chirurg. Band: 88, Nummer: 9, 2017, doi: 10.1007/s00104-017-0429-9, p.792-798.
7. Köckerling et al.: *Hernienregister*. In: Chirurgische Allgemeine Zeitung. Band: 13, Nummer: 5, 2012, p.1-3.
8. Schumpelick et al.: *Praxis der Viszeralchirurgie: Gastroenterologische Chirurgie*. Springer 2006, ISBN: 978-3-540-29040-7.
9. Simons et al.: *European Hernia Society guidelines on the treatment of inguinal hernia in adult patients*. In: Hernia. Band: 13, Nummer: 4, 2009, doi: 10.1007/s10029-009-0529-7.
10. Bittner et al.: *Laparo-endoskopische Hernienchirurgie*. Springer 2018, ISBN: 978-3-662-56089-1.
11. Alabraba et al.: *The role of ultrasound in the management of patients with occult groin hernias*. In: International Journal of Surgery. Band: 12, Nummer: 9, 2014, doi: 10.1016/j.ijsu.2014.07.266, p.918-922.
12. Sæter et al.: *Mortality after emergency versus elective groin hernia repair: a systematic review and meta-analysis*. In: Surgical Endoscopy. Band: 36, Nummer: 11, 2022, doi: 10.1007/s00464-022-09327-2, p.7961-7973.
13. Cirocchi et al.: *Asymptomatic inguinal hernia: does it need surgical repair? A systematic review and meta‐analysis*. In: ANZ Journal of Surgery. Band: 92, Nummer: 10, 2022, doi: 10.1111/ans.17594, p.2433-2441.
14. Hirner, Weise (Hrsg.): *Chirurgie*. 2. Auflage Thieme 2008, ISBN: 978-3-131-30842-9.
15. Schumpelick: *Hernien*. 5. Auflage Thieme 2015, ISBN: 978-3-131-17365-2.
16. Miserez et al.: *Update with level 1 studies of the European Hernia Society guidelines on the treatment of inguinal hernia in adult patients*. In: Hernia. Band: 18, Nummer: 2, 2014, doi: 10.1007/s10029-014-1236-6, p.151-163.
17. Hajibandeh et al.: *Meta-analysis of the outcomes of Trans Rectus Sheath Extra-Peritoneal Procedure (TREPP) for inguinal hernia*. In: Hernia. Band: 26, Nummer: 4, 2022, doi: 10.1007/s10029-021-02554-x, p.989-997.
18. Jähne et al.: *Was gibt es Neues in der Chirurgie?*. ecomed-Storck 2019, ISBN: 978-3-609-76940-0.
19. Mayer et al.: *Is the age of >65 years a risk factor for endoscopic treatment of primary inguinal hernia? Analysis of 24,571 patients from the Herniamed Registry*. In: Surgical Endoscopy. Band: 30, Nummer: 1, 2015, doi: 10.1007/s00464-015-4209-7, p.296-306.
20. Matikainen et al.: *Impact of Mesh and Fixation on Chronic Inguinal Pain in Lichtenstein Hernia Repair: 5-Year Outcomes from the Finn Mesh Study*. In: World Journal of Surgery. Band: 45, Nummer: 2, 2020, doi: 10.1007/s00268-020-05835-1, p.459-464.
21. Phoa et al.: *Comparison of glue versus suture mesh fixation for primary open inguinal hernia mesh repair by Lichtenstein technique: a systematic review and meta-analysis*. In: Hernia. Band: 26, Nummer: 4, 2022, doi: 10.1007/s10029-022-02571-4, p.1105-1120.
22. Weyhe et al.: *HerniaSurge: internationale Leitlinie zur Therapie der Leistenhernie des Erwachsenen*. In: Der Chirurg. Band: 89, Nummer: 8, 2018, doi: 10.1007/s00104-018-0673-7, p.631-638.
23. Bittner et al.: *Guidelines for laparoscopic (TAPP) and endoscopic (TEP) treatment of inguinal Hernia [International Endohernia Society (IEHS)]*. In: Surgical Endoscopy. Band: 25, Nummer: 9, 2011, doi: 10.1007/s00464-011-1799-6, p.2773-2843.
24. Matikainen et al.: *A randomized clinical trial comparing early patient-reported pain after open anterior mesh repair versus totally extraperitoneal repair of inguinal hernia*. In: British Journal of Surgery. Band: 108, Nummer: 12, 2021, doi: 10.1093/bjs/znab354, p.1433-1437.
25. Singh et al.: *Chronic groin pain following inguinal hernia repair in the laparoscopic era: Systematic review and meta-analysis*. In: The American Journal of Surgery. Band: 224, Nummer: 4, 2022, doi: 10.1016/j.amjsurg.2022.05.005, p.1135-1149.
26. Niebuhr et al.: *Differenzierter Einsatz der empfohlenen Guideline-Techniken zur Versorgung einer Leistenhernie*. In: Der Chirurg. Band: 88, Nummer: 4, 2017, doi: 10.1007/s00104-017-0379-2, p.276-280.
27. Dieterich, Eichhorn: *Ambulante Hernioplastik nach Lichtenstein*. In: Der Chirurg. Band: 75, Nummer: 9, 2004, doi: 10.1007/s00104-004-0856-2, p.890-895.
28. Lorenz et al.: *Shouldice standard 2020: review of the current literature and results of an international consensus meeting*. In: Hernia. 2021, doi: 10.1007/s10029-020-02365-6.
29. Malik et al.: *Recurrence of inguinal hernias repaired in a large hernia surgical specialty hospital and general hospitals in Ontario, Canada*. In: Canadian Journal of Surgery. Band: 59, Nummer: 1, 2016, doi: 10.1503/cjs.003915, p.19-25.
30. Kokotovic et al.: *Long-term Recurrence and Complications Associated With Elective Incisional Hernia Repair*. In: JAMA. Band: 316, Nummer: 15, 2016, doi: 10.1001/jama.2016.15217, p.1575.
31. von Schweinitz et al.: *Kinderchirurgie: Viszerale und allgemeine Chirurgie des Kindesalters*. Springer 2013, ISBN: 978-3-642-29779-3.
32. *S1-Leitlinie Leistenhernie, Hydrozele*. Stand: 2020. Abgerufen am: 04.02.2021.
33. Provinciatto et al.: *Early versus delayed inguinal hernia repair in preterm infants: A systematic review and meta-analysis*. In: Journal of Neonatal-Perinatal Medicine. Band: 18, Nummer: 1, 2025, doi: 10.1177/19345798251318594, p.3-8.
34. Blakely et al.: *Effect of Early vs Late Inguinal Hernia Repair on Serious Adverse Event Rates in Preterm Infants*. In: JAMA. Band: 331, Nummer: 12, 2024, doi: 10.1001/jama.2024.2302, p.1035-1044.
35. Masoudian et al.: *Optimal timing for inguinal hernia repair in premature infants: a systematic review and meta-analysis*. In: Journal of Pediatric Surgery. Band: 54, Nummer: 8, 2019, doi: 10.1016/j.jpedsurg.2018.11.002, p.1539-1545.
36. Novotny et al.: *The Burnia: Laparoscopic Sutureless Inguinal Hernia Repair in Girls*. In: Journal of Laparoendoscopic & Advanced Surgical Techniques. Band: 27, Nummer: 4, 2017, doi: 10.1089/lap.2016.0234, p.430-433.
37. Finn et al.: *Medium-Term Outcomes of the Godoy Burnia Repair: Durability of a Sutureless Laparoscopic Inguinal Hernia Repair in Girls*. In: Journal of Laparoendoscopic & Advanced Surgical Techniques. Band: 34, Nummer: 1, 2024, doi: 10.1089/lap.2023.0266, p.92-96.
38. *S3-Leitlinie Prophylaxe der venösen Thromboembolie (VTE)*. Stand: 2015. Abgerufen am: 06.11.2017.
39. Giebel, Blöchl: *Allgemeinchirurgie*. Springer 1999, ISBN: 978-3-642-64234-0.
40. Siewert: *Chirurgie*. 9. Auflage Springer 2012, ISBN: 978-3-642-11330-7.
41. Muschaweck, Koch: *Sportlerleiste*. In: Der Radiologe. Band: 59, Nummer: 3, 2019, doi: 10.1007/s00117-019-0499-4, p.224-233.
