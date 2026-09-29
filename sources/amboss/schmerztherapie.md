# Grundlagen der Schmerztherapie (AMBOSS)

- **Artikel-ID:** xN0EWg
- **URL:** https://next.amboss.com/de/article/xN0EWg
- **Zuletzt bearbeitet (AMBOSS):** 30.07.2026
- **Erfasst:** 2026-09-26
- **Methode:** Browser-Automatisierung (device bridge, AMBOSS-Suche "Schmerztherapie" → Kapitel "Grundlagen der Schmerztherapie"), Abschnitte einzeln per Klick/Anker-Navigation expandiert, Text per get_page_text extrahiert (find → scroll_to/Anker-Navigation → get_page_text Muster gemäß `amboss-scraping` Skill). Wortwörtliche Übernahme, keine Paraphrasierung.
- **Bekannte Lücken:**
  - "AMBOSS-Podcast zum Thema": nur Titel/Metadaten erfasst ("Cannabis als Medizin – Indikationen und praktische Anwendung", Mai 2021), kein Transkript verfügbar.
  - "Meditricks": Abschnitt vorhanden, aber beim Expandieren keine über den bereits im Haupttext erfassten Inhalt hinausgehenden Video-Inhalte/Titel im Rendering sichtbar geworden — falls das Kapitel ein eigenes Meditricks-Video hat, wurde dessen Titel hier nicht erfasst.
  - "Tipps & Links": nur generische AMBOSS-Verweise erfasst (Newsletter/Podcast-Anmeldungen, Leitlinien-Telegramm); ein spezifischer Link "Schmerzskalen" wird im Abschnitt "Schmerzbeurteilung" erwähnt, aber das verlinkte Zusatzmaterial selbst wurde nicht separat aufgerufen.
  - Icon-only "Mehr anzeigen"-Erweiterungen (kleine Kästchen-Icons neben einzelnen Stichpunkten wie "Langwirksame (retardierte) Analgetika 🗒", "Phantomempfindung 🗒", "Telescoping 🗒", "NMDA-Antagonisten 🗒", "Glucocorticoide 🗒", "Laxantien 🗒") wurden nicht einzeln geöffnet — dies sind AMBOSS-interne Popup-Definitionen/Verlinkungen, keine fehlenden Fließtext-Inhalte.
  - Bild "Darstellung der Head'schen Zonen wichtiger innerer Organe" — nur Bildunterschrift, kein Bildinhalt extrahierbar (visuelle Grafik).

---

## Zusammenfassung

In der Schmerztherapie wird der akute vom chronischen Schmerz unterschieden. Das WHO-Stufenschema wurde zur Behandlung von Tumorschmerzen entwickelt, wird heutzutage aber auch grundsätzlich bei der Therapie chronischer Schmerzen berücksichtigt. Das Schema gibt einen definierten Behandlungsalgorithmus vor, in dem Nicht-Opioid-Analgetika mit Opioiden kombiniert verabreicht werden. Ziel ist die Schmerzfreiheit der betroffenen Person, die mithilfe einer standardisierten Schmerzanalyse evaluiert wird. Reicht die Medikation aus Basistherapie und Bedarfsmedikation in einer Stufe nicht mehr aus, muss ein Step-up innerhalb des Schemas erfolgen. In allen drei Stufen können Koanalgetika verabreicht werden, die über eine supportive Behandlung (bspw. Hemmung des Knochenabbaus bei osteolytischen Metastasen oder Gabe von Anfallssuppressiva bei neuropathischen Beschwerden) Schmerzen und den Bedarf an Schmerzmitteln reduzieren.

## Schmerz und Schmerzformen

### Weitergeleitete Schmerzen

**Anatomischer/physiologischer Hintergrund: Viszerokutaner Reflexbogen**
- An denselben Neuronen des Rückenmarks enden verschiedene Schmerznervenfasern → Nervenfasern für den viszeralen Schmerz von inneren Organen konvergieren auf Höhe des Rückenmarkhinterhorns mit Nervenfasern für den somatischen Schmerz aus den verschiedenen Dermatomen → Von dort gemeinsame Weiterleitung in Richtung zentrales Nervensystem → Strikte Zuordnung von Schmerzentstehung und Schmerzwahrnehmung geht verloren
- Dieses Phänomen manifestiert sich als weitergeleiteter Schmerz (auch „übertragener Schmerz" bzw. „referred pain")
- Andererseits beruhen die Effekte von reflextherapeutischen Verfahren auf diesem Zusammenhang

**Klinische Manifestation: Head'sche Zone und MacKenzie-Zone**
- Übertragung von Schmerzen aus einem Organ auf ein bestimmtes, fest definiertes Hautareal (Dermatom) → Das zugehörige Areal wird als Head'sche Zone bezeichnet
- Analog: Schmerzübertragung in die vom entsprechenden Rückenmarkssegment innervierte Muskulatur (Myotom) → MacKenzie-Zone (bspw. Schmerzen im linken Arm bei Herzinfarkt)

**Weitere Phänomene der Schmerzübertragung**
- Gallenblase: Unter anderem sensibel vom rechten N. phrenicus (C4) versorgt → Bspw. bei Cholezystolithiasis Schmerzausstrahlung in die rechte Schulter und Hyperästhesie unter dem rechten Schulterblatt/Rücken (= Boas-Zeichen)
- Milz: Unter anderem sensibel vom linken N. phrenicus (C4) versorgt → Bei Milzruptur Schmerzausstrahlung in die linke Schulter (= Kehr-Zeichen) und Druckschmerz an der linken Halsseite (= Saegesser-Zeichen)

**QUIZ – Übersicht Head'sche Zonen**

| Organ | Dermatom | Projektion |
|---|---|---|
| Diaphragma | C4 | Schulter |
| Herz | Th3–4 | Linker Thorax |
| Ösophagus | Th4–5 | Retrosternal |
| Magen | Th6–7 | Epigastrium |
| Leber/Gallenblase | Th8–L1 | Rechter Oberbauch |
| Dünndarm | Th10–L1 | Paraumbilikal |
| Dickdarm | Th11–L1 | Unterbauch |
| Harnblase | Th11–L1 | Suprapubisch |
| Nieren/Hoden | Th10–L1 | Leiste |

*(Bildunterschrift: Darstellung der Head'schen Zonen wichtiger innerer Organe — Bildinhalt nicht extrahierbar)*

### Phantomsensationen

- **Ätiologie:** Phantomsensationen sind eine wichtige und häufige Komplikation nach Amputation
  - Mehr als 50% der Patient:innen haben Empfindungen in den Bereichen, die amputiert wurden
- **Definition**
  - Phantomschmerz
    - Schmerzqualität: Intermittierender Schmerz, der verschiedene Qualitäten haben kann, bspw. brennend, kribbelnd, juckend, quetschend
  - Phantomempfindung
  - Telescoping
  - Ursache: „Erlernen eines Schmerzes" durch Sensibilisierung nozizeptiver Strukturen in peripheren, spinalen und supraspinalen Strukturen → Übererregung an glutamatergen NMDA-Rezeptoren
- **Prophylaxe bzw. spezielle Therapie**
  - Frühzeitige Regionalanästhesie: Eine perioperative Regionalanästhesie senkt die Wahrscheinlichkeit für das Auftreten von Phantomschmerzen
  - NMDA-Antagonisten
  - Koanalgetika (bspw. trizyklische Antidepressiva)
  - Spiegeltherapie
    - Hintergrund: Zum Teil beruht der Phantomschmerz darauf, dass die Betroffenen das Gefühl haben, die amputierte Extremität befinde sich in einer schmerzhaften Position, könne aber nicht bewegt werden.
    - Durchführung
      - Mithilfe von Spiegeln wird eine gesunde Gliedmaße der betroffenen Person so gespiegelt, dass es für sie so aussieht, als wäre die amputierte wieder vorhanden.
      - Die Person wird nun aufgefordert, die nicht-amputierte Extremität zu bewegen, um bei der gespiegelten die schmerzhafte Position zu verändern. Durch den visuellen Effekt kann es zu einer Schmerzlinderung kommen.
      - Ziel ist es, dass die Betroffenen lernen, imaginär eine schmerzhafte Position zu verändern.

### Schmerzbeurteilung

- **Schmerzskala:** Objektivierung der Schmerzintensität anhand einer subjektiven Einstufung des Schmerzes, bspw. mithilfe einer numerischen Rangskala (Numeric Rating Scale, NRS), visuellen Analogskala (bei Kindern: Smiley-Skala) (Visual Analogue Scale, VAS) oder einer verbalen deskriptiven Skala
- **Schmerztagebuch:** Dokumentation des zeitlichen Verlaufs der Schmerzintensität, um Schmerzspitzen und Schmerzauslöser zu erkennen und ggf. Therapieanpassungen vorzunehmen
- **Beurteilung der Schmerzchronifizierung:** Mainzer Stadiensystem der Schmerzchronifizierung (MPSS)
  - Achse I: Zeitliche Aspekte des Schmerzes
  - Achse II: Räumliche Aspekte des Schmerzes
  - Achse III: Medikamenteneinnahmeverhalten
  - Achse IV: Inanspruchnahme des Gesundheitswesens
  - Die Punkte aus den einzelnen Achsen werden zu einem Score addiert und in drei Stadien eingeteilt
- Weiterführende Informationen siehe: Tipps & Links zum Thema — Schmerzskalen

## Medikamentöse Schmerztherapie

**QUIZ – Prinzipien der medikamentösen Schmerztherapie**

| Prinzip | Erläuterung |
|---|---|
| „By the mouth" | Orale Applikation bevorzugen; Langwirksame (retardierte) Analgetika |
| „By the clock" | Regelmäßiges und festgelegtes Einnahme-Zeitschema |
| „By the ladder" | Entsprechend des WHO-Stufenschemas symptomorientierte Schmerzmedikation |

> Merkwort für die Prinzipien der Schmerztherapie: „DNA" – „Durch den Mund" – „Nach der Uhr" – „Auf der Leiter"!

Auch hier werden zur Beurteilung des Verlaufs und des Therapieerfolgs regelmäßig Schmerzskalen wie die NRS oder VAS angewendet. Gleichzeitig sollten die Patient:innen immer über ihre Zufriedenheit mit der Schmerztherapie befragt werden.

> Jeder Schmerztherapie geht eine gründliche Anamnese zu Schmerzintensität und -qualität voraus!

### WHO-Stufenschema

**QUIZ – WHO-Stufenschema**

| Stufe | Medikation |
|---|---|
| Stufe I | Nicht-Opioid-Analgetikum (± Koanalgetikum ± Adjuvans) |
| Stufe II | Nicht-Opioid-Analgetikum + niedrigpotente Opioide (± Koanalgetikum ± Adjuvans) |
| Stufe III | Nicht-Opioid-Analgetikum + hochpotente Opioide (± Koanalgetikum ± Adjuvans) |

Die Therapie chronischer Schmerzen orientiert sich am WHO-Stufenschema. Die Medikation besteht aus einer Basistherapie (retardierte Präparate, die nach festem Schema und Dosierung eingenommen werden) und einer adäquaten Bedarfsmedikation (unretardierte Analgetika, die Schmerzspitzen therapieren). Weiterhin kann eine Begleitmedikation mit Koanalgetika und Adjuvanzien erfolgen, um spezielle Schmerzformen wirkungsvoller zu behandeln bzw. um Nebenwirkungen der Therapie entgegenzuwirken. Sind Patient:innen nicht schmerzfrei, muss in die nächsthöhere Stufe übergegangen werden.

> Ein häufiger „Fehler" in der Schmerztherapie ist die Durchführung einer analgetischen Therapie mittels alleiniger Gabe eines Opioids. Um eine effektive und ausbalancierte Analgesie zu erreichen, sollte in jeder Behandlungsstufe die (zusätzliche) Gabe eines Nicht-Opioid-Analgetikums sowie ggf. eines Koanalgetikums erfolgen!

**QUIZ – Kurzübersicht Analgetika (beispielhaft)**

| Nicht-Opioid-Analgetika | Niedrigpotente Opioide | Hochpotente Opioide |
|---|---|---|
| Diclofenac | Tramadol | Morphin |
| Ibuprofen | Tilidin | Oxycodon |
| Acetylsalicylsäure | Dihydrocodein | Levomethadon |
| Celecoxib | | Fentanyl |
| Paracetamol | | Pethidin |
| Metamizol | | Buprenorphin |
| | | Piritramid |

*Genaue Informationen zu den Substanzen befinden sich in den jeweiligen Kapiteln*

### Bedarfsmedikation

Um Schmerzspitzen und Durchbruchschmerzen adäquat zu behandeln, sollte allen Schmerzpatient:innen eine Bedarfsmedikation bereitgestellt werden. Für diese gilt:
- Unretardiertes, schnellwirksames Analgetikum bevorzugen
- Bei bereits bestehender Opioidtherapie der WHO-Stufe III: Bedarfsdosis 1/6 der Opioid-Gesamttagesdosis
- Bei Einsatz der Bedarfsmedikation ≥3×/d oder unzureichender Analgesie durch diese sollte die Basismedikation überprüft und ggf. eine höhere Stufe nach dem WHO-Stufenschema oder eine Dosiserhöhung der Basistherapie erwogen werden.

### Koanalgetika

Koanalgetika können in jeder Stufe des WHO-Stufenschemas als Begleitmedikation gegeben werden.
- **Neuropathische Schmerzen** (bspw. diabetische Neuropathie, Post-Zoster-Neuralgie)
  - Trizyklische Antidepressiva: Amitriptylin, Doxepin, Clomipramin, Imipramin
  - Anfallssuppressiva: Carbamazepin, Gabapentin, Pregabalin
- **Hirndruck und Nervenkompression**
  - Glucocorticoide
- **Knochenmetastasen und -schmerzen**
  - Bisphosphonate (bspw. Pamidronat)

### Adjuvanzien

Mit Adjuvanzien wird den Nebenwirkungen der Therapie mit Analgetika sowohl prophylaktisch als auch therapeutisch entgegengewirkt.
- Laxantien
- Antiemetika
- Protonenpumpeninhibitoren

## Weitere Verfahren der Schmerztherapie

Supportiv können zahlreiche Verfahren eine Schmerzreduktion erzielen. Die Erfolge können dabei interindividuell sehr unterschiedlich sein.
- Regionalanästhesie-Verfahren: Lokalanästhetika
  - Bspw. bei myofaszialem Schmerzsyndrom: Lokal begrenzte, schmerzhafte Funktionsstörungen der Muskulatur, die als Schmerz-/Triggerpunkte fungieren
- Physikalische Maßnahmen: Massagen, Thermotherapie, Physiotherapie, Desensibilisierung etc.
- Psychotherapie
- Entspannungsverfahren
  - Progressive Muskelrelaxation nach Jacobson
  - Autogenes Training
  - Biofeedback
  - Kognitive Verhaltenstherapie
- Patientenedukation
- Hypnose
- Akupunktur

## AMBOSS-Podcast zum Thema

- Cannabis als Medizin – Indikationen und praktische Anwendung (Mai 2021)
  - AMBOSS-Podcast: Cannabis als Medizin – Indikationen und praktische Anwendung (23.05.2021)
  - "Interesse an noch mehr Medizinwissen zum Hören? Abonniere jetzt den AMBOSS-Podcast über deinen Podcast-Anbieter oder den Link am Seitenende unter 'Tipps & Links'"

## Tipps & Links

- Anmeldung Studientelegramm Innere Medizin
- Anmeldung One-Minute Telegram
- AMBOSS-Podcast
- AMBOSS Leitlinien-Telegramm

## Quellen

1. Vickers, Linde: *Acupuncture for Chronic Pain*. In: JAMA. Band: 311, Nummer: 9, 2014, doi: 10.1001/jama.2013.285478, p.955.
2. Kumle et al.: *Schmerztherapie in der Notfallmedizin*. In: Der Anaesthesist. Band: 62, Nummer: 11, 2013, doi: 10.1007/s00101-013-2247-x, p.902-913.
3. Häske et al.: *Analgesie bei Traumapatienten in der Notfallmedizin*. In: Der Anaesthesist. Band: 69, Nummer: 2, 2020, doi: 10.1007/s00101-020-00735-4, p.137-148.
4. Michael et al.: *Analgesie, Sedierung und Anästhesie in der Notfallmedizin*. In: Anästhesiologie & Intensivmedizin. Band: 61, Nummer: 2, 2020, doi: 10.19224/ai2020.051, p.51-65.
5. Lüllmann et al.: *Pharmakologie und Toxikologie*. 15. Auflage Thieme 2002, ISBN: 3-133-68515-5.
6. Karow, Lang-Roth: *Allgemeine und Spezielle Pharmakologie und Toxikologie 2012*. 20. Auflage Eigenverlag 2012.
7. Bähr, Frotscher: *Neurologisch-topische Diagnostik*. 10. Auflage Thieme 2014, ISBN: 978-3-135-35810-9.
8. Schmidt, Schaible: *Neuro- und Sinnesphysiologie*. 5. Auflage Springer 2005, ISBN: 978-3-540-25700-4.
