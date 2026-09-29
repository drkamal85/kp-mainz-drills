# Meningitis (Hirnhautentzündung) (AMBOSS)

**Artikel-ID:** ZR0Zlf
**URL:** https://next.amboss.com/de/article/ZR0Zlf
**Zuletzt bearbeitet (AMBOSS):** 18.08.2026
**Erfasst am:** 26.09.2026
**Methode:** Verbatim-Capture via Browser-Tool. Direkte Suche "Meningitis" → dedizierter Artikel ZR0Zlf ("Meningitis", Hirnhautentzündung). Nach "Öffne/schließe alle Abschnitte"-Toggle: keine zusätzlichen lazy-loaded Abschnitte identifiziert (thin-section-Check ergab nur legitime kurze Verweis-/Ausschluss-Abschnitte: Antibiotika-Dosierungen [DOSIS-Konvention], AMBOSS-Pflegewissen-Box, Besondere Patientengruppen [nur Meditricks-Verweis], ICD-10-Kodierung). Volltext-Extraktion via DOM-`textContent`-Walk (window.__extract/__full), in 6 Slices (0–8000, 8000–16000, 16000–24000, 24000–32000, 32000–40000, 40000–49336 Zeichen) verifiziert.
**KP-Zuordnung:** RAND-Tier Thema #83 – Meningitis/Enzephalitis
**Bekannte Lücken:** Der Artikel behandelt primär die Meningitis; Enzephalitis wird im Artikel nur im Rahmen der Definitionsabgrenzung (Meningoenzephalitis) sowie als Komplikation/Differenzialaspekt erwähnt (u.a. "Sofortige Gabe von Aciclovir bei (Meningo-)Enzephalitis"), ist aber selbst NICHT als eigenständiges AMBOSS-Kapitel in dieser Erfassung enthalten — für eine vollständige Abdeckung des KP-Themas "Meningitis/Enzephalitis" sollte ergänzend das separate AMBOSS-Kapitel zur (viralen) Enzephalitis bzw. "Virale Meningoenzephalitis" (siehe Quelle [3] im Quellenverzeichnis dieses Artikels: S1-Leitlinie Virale Meningoenzephalitis 2025) in einer Folgesitzung gezielt gesucht und erfasst werden. "Meningitisches Syndrom - AMBOSS-SOP" (das Notfallmanagement-Kapitel) sowie "Postexpositionsprophylaxe bei invasiver Hib-Infektion" sind nur als Verweise vorhanden, nicht separat erfasst. Alle DOSIS-Marker bei Medikamenten nicht aufgelöst, konsistent mit Ausschlusskonvention. "Besondere Patientengruppen" ist im Quellartikel nur eine Verweis-Überschrift ohne eigenen Fließtext (Meditricks-Box folgt direkt darauf).

---

## Zusammenfassung

Die Meningitis ist eine Entzündung der Hirn- und Rückenmarkshäute, wobei die Abgrenzung einer isolierten Meningitis von einer kombinierten Entzündung der Hirnhäute und des Hirngewebes (Meningoenzephalitis) insb. bei Kindern oft nicht möglich ist. Als Ursache kommen zahlreiche Viren infrage; bei den bakteriellen Erregern dominieren v.a. Meningokokken und Pneumokokken. Klinisch muss auf die Leitsymptome Fieber, Kopfschmerzen, Meningismus und Bewusstseinstrübung geachtet werden, die bei Kleinkindern und Säuglingen allerdings oft fehlen. Bedeutende Sonderformen sind die tuberkulöse Meningitis und die Neuroborreliose, die sich beide zumeist mit einem subakuten Verlauf über Wochen bis Monate präsentieren. Diagnostisch wegweisend sind insb. die klinischen Symptome und die Liquoruntersuchung. Zum Ausschluss eines erhöhten intrakraniellen Drucks wird bei entsprechenden Symptomen vor der Liquorpunktion eine kraniale CT durchgeführt. Während eine bakterielle Meningitis sowie Meningoenzephalitiden durch HSV oder VZV absolute Notfälle darstellen und so schnell wie möglich kalkuliert antiinfektiv therapiert werden müssen, heilt eine unkomplizierte virale Meningitis meist spontan und folgenlos aus. Die gefürchtetste Komplikation der bakteriellen Meningitis (insb. der Meningokokken-Meningitis) ist das Waterhouse-Friderichsen-Syndrom, das mit einer schweren Verbrauchskoagulopathie, Nebennierenrindeninsuffizienz und meist mit einem letalen Verlauf einhergeht.

Für das Notfallmanagement des meningitischen Syndroms siehe: Meningitisches Syndrom - AMBOSS-SOP.

## Definition

- **Meningitis:** Entzündung der Hirnhäute (genauer: Inflammation der Pia mater und der Arachnoidea mater), ggf. auch der Rückenmarkshäute
  - Basale Meningitis: Entzündung der Hirnhäute der Schädelbasis, oft gekennzeichnet durch Hirnnervenausfälle und ausgelöst durch Mykobakterien
- **Enzephalitis (im allgemeinen pathophysiologischen Sinne):** Entzündung des Hirngewebes
- **Meningoenzephalitis:** Koinzidenz von Meningitis und Enzephalitis
- **Meningoradikulitis:** Entzündung der die Nervenwurzeln umgebenden Ausziehungen der Rückenmarkshäute

## Epidemiologie

- **Bakterielle Meningitis [1]:** Inzidenz ca. 1,6/100.000 Personen/Jahr (Niederlande, Zahlen vermutlich übertragbar auf Deutschland) [2]
  - Meningokokken-Meningitis [3]: Inzidenz <0,4 Fälle/100.000 Personen/Jahr (Deutschland); Serogruppen: In Deutschland insb. B (ca. 50%), und Y (ca. 40%), deutlich seltener C und W; Altersgipfel: Säuglinge und Kleinkinder <2 Jahre; Jugendliche und junge Erwachsene von ≥15 bis <20 Jahre
- **Tuberkulöse Meningitis [4]:** Inzidenz etwa 2 Fälle/100.000 Personen/Jahr; Altersgipfel: 6 Monate bis 4 Jahre [5]
- **Virale Meningitis [6]:** Inzidenz etwa 3,5–7,5 Fälle/100.000 Personen/Jahr (gemäßigte Breiten)

Wenn nicht anders angegeben, beziehen sich die epidemiologischen Daten auf Deutschland.

## Ätiologie

### Bakterielle Meningitis

- **Infektionsweg**
  - Direkte Übertragung von Mensch zu Mensch über Tröpfcheninfektion (10% der europäischen Bevölkerung haben eine Besiedelung mit Meningokokken im Nasen-Rachen-Raum, ohne Krankheitserscheinungen zu entwickeln)
  - Hämatogene Streuung (insb. bei Nasen-Rachen-Infekt)
  - Kontinuierliche Ausbreitung: Infektionen angrenzender Regionen, insb. Ohr oder Augenhöhle; offenes Schädel-Hirn-Trauma oder perioperativ
- **Erregerspektrum abhängig vom Erkrankungsalter [2] [7]**
  - Kinder: Alter ≤6 Wochen: Streptococcus agalactiae (Gruppe-B-Streptokokken) und E. coli, gefolgt von Listerien, Staphylokokken, Klebsiellen, Pseudomonas, Salmonellen und gramnegativen Erregern; Alter >6 Wochen: Pneumokokken, Meningokokken (und Haemophilus influenzae)
  - Erwachsene: Pneumokokken, Meningokokken, Listerien, Haemophilus influenzae, Staphylokokken, gramnegative Enterobakterien, Pseudomonas aeruginosa

**Meningitiden durch atypische Bakterien**
- Tuberkulöse Meningitis: Ausgelöst durch das Mycobacterium tuberculosis
- Meningitis bei Neuroborreliose

### Virale Meningitis

- **Infektionsweg**
  - Direkte Übertragung von Mensch zu Mensch über Tröpfcheninfektion oder Schmierinfektionen
  - Direkte Übertragung durch Tiere, insb. Zecken und andere Arthropoden
  - Reinfektionen durch reaktivierte Viren in bereits infizierten Zellen
  - Opportunistische Infektion bei Immunsuppression
- **Erregerspektrum:** Theoretisch können fast alle humanpathogenen Viren eine virale Meningitis auslösen. Häufigste: Enteroviren (bzw. Coxsackieviren), Mumpsvirus, Arboviren (FSME), Herpesviren (HSV, siehe: HSV-Enzephalitis, CMV, VZV, EBV), Influenzaviren, HIV

**Sonderform der viralen Meningitis**
- Mollaret-Meningitis: Benigne, d.h. ohne Folgeschäden verlaufende, Erkrankung mit rezidivierenden Episoden eines meningitischen Syndroms; lymphozytäre Pleozytose im Liquor mit PCR-Nachweis von HSV-1, HSV-2 oder seltener VZV; vollständige Rückbildung der Episoden unter symptomatischer Therapie

### Andere infektiöse Meningitiden

Siehe: Erregerbedingte Meningoenzephalitiden im Kontext von
- Pilzerkrankungen, bspw. Candidose, Aspergillose, Kryptokokkose
- Parasitären Erkrankungen, bspw. Echinokokkose, Toxoplasmose

### Nicht-infektiöse Meningitiden (aseptische Meningitis, Meningitis ohne Erregernachweis; Auswahl)

Autoimmunologische oder neoplastische Erkrankungen können mit einer entzündlichen Beteiligung der Hirnhäute verlaufen, werden aber meist nicht zu den Meningitiden im engeren Sinne gezählt.
- Neurosarkoidose: Kann zu einem Befall der Hirnhäute mit Sarkoidose-Granulomen und ggf. zu einer Entzündungsreaktion im Liquor führen
- Meningeosis neoplastica (carcinomatosa, leucaemica, lymphomatosa): Kann, muss aber nicht zu entzündlichen Veränderungen der Hirnhäute (Meningitis durch Meningeosis) führen

## Symptomatik

- **Allgemein**
  - Meningitische Symptomtrias: Kopfschmerzen, Meningismus und hohes Fieber
  - Weitere mögliche Symptome: Übelkeit, Erbrechen, Fotophobie, Hyperakusis, Hyperästhesie, Unruhe, Opisthotonus
  - Insb. bei bakterieller Meningitis und/oder Meningoenzephalitis: Qualitative Bewusstseinsstörung, Vigilanzminderung, epileptische Anfälle, weitere fokal-neurologische Symptome wie Paresen
  - Bei Meningokokken-Meningitis in ca. 60% der Fälle Hautveränderungen: Makulopapulöse oder petechiale Exantheme bis hin zur ausgedehnten Purpura fulminans mit Hautnekrosen [2]
- **Bei Säuglingen und Kleinkindern [8]**
  - Fieber, Erbrechen
  - In ca. 40% der Fälle gespannte Fontanelle(n)
  - Weitere mögliche Symptome: Unruhe oder Apathie, Lichtscheu, Trinkschwäche, plötzliches Schielen, Hautblutungen, blasses Hautkolorit, schrilles Schreien, Wimmern, Bewegungsarmut, Berührungsempfindlichkeit, Vigilanzminderung, epileptische Anfälle
  - Der sonst typische Meningismus kann fehlen
- **Bei Neugeborenen**
  - Atemstörung, blass-graues Hautkolorit, epileptische Anfälle, Erbrechen
  - In ca. 20% der Fälle Berührungsempfindlichkeit oder Fieber
  - Weitere mögliche Symptome: Gespannte Fontanelle(n), Opisthotonus, Schlaffheit, Hyperexzitabilität, schrilles Schreien, Trinkschwäche, Vigilanzstörung, Ödeme, geblähtes Abdomen, Hypothermie, Ikterus
  - Der sonst typische Meningismus kann fehlen
- Insb. bei Neugeborenen, Säuglingen und Kleinkindern kann der sonst typische Meningismus fehlen!

**Charakteristika der wichtigsten Manifestationsformen der Meningitis**

| Form | Inkubationszeit | Zeitlicher Verlauf | Klinische Manifestation |
|---|---|---|---|
| Bakterielle Meningitis | Etwa 2–4(–10) Tage | Hochakuter Verlauf; untherapiert meist innerhalb von Stunden bis Tagen letal; Synonym: Konvexitäts- oder Haubenmeningitis | Beim Waterhouse-Friderichsen-Syndrom: Petechiale Hauteinblutungen/Purpura |
| Virale Meningitis | Etwa 2–14 Tage | Akuter Verlauf über wenige Stunden bis Tage; bei Immunkompetenten oft spontanes Abklingen der Symptome (auch ohne kausale Therapie) | Typische meningitische Symptomtrias, Fieber häufig moderater ausgeprägt |
| Tuberkulöse Meningitis | Etwa 6–8 Wochen | Eher schleichender Beginn mit Fieberschüben; langsam progredienter Verlauf über mehrere Wochen; Inflammation durch Tuberkulose-Granulome typischerweise an den Hirnhäuten der Schädelbasis | Hirnnervenausfälle (durch die basale Meningitis); typische meningitische Symptomtrias steht oft nicht im Vordergrund; fokal-neurologische Defizite durch hämatogene Streuung bei kranialer Arteriitis; ggf. Hydrocephalus malresorptivus; ggf. Hypophysenvorderlappeninsuffizienz; Therapie siehe: Tuberkulosetherapie |
| Meningitis bei Neuroborreliose | Wochen bis Monate | Progredienter Verlauf innerhalb der Stadienentwicklung der Neuroborreliose; Meningitis und Meningoradikulitis als Teil des frühen disseminierten Stadiums der Neuroborreliose (komplikative Form der Lyme-Borreliose) | Typische meningitische Symptomtrias oft eingebettet in weitere Symptome der Neuroborreliose; Meningoradikulitis insb. mit radikulären Schmerzen (Bannwarth-Syndrom) |

## Diagnostik

### Anamnese/Fremdanamnese

- Frage nach Kardinalsymptomen, insb. Kopfschmerzen, siehe auch: Strukturierte Kopfschmerzanamnese
- Fieber: Beginn, Höhe, evtl. bereits Einnahme antipyretischer Medikamente
- Frage nach Begleitsymptomen: Übelkeit, Erbrechen, Unruhe, Verwirrtheit, Paresen, Sensibilitätsstörungen, epileptische Anfälle
- Frage nach Vorerkrankungen: Bekannte Kopfschmerzerkrankungen (siehe: Kopfschmerzen); schwere Degeneration der HWS; Parkinson-Syndrome; vorangegangene infektiöse Erkrankungen; vorangegangene Eingriffe am Nervensystem; Immunsuppression

### Klinische Untersuchung

- Prüfen auf Meningismus
  - Reflektorische Nackensteifigkeit
  - Brudzinski-Zeichen: Bei der Prüfung auf Nackensteifigkeit kommt es zum reflexartigen Anziehen der Beine. Dadurch wird die mit Schmerzen verbundene Spannung der Meningen und v.a. der lumbosakralen Nervenwurzeln reduziert.
  - Kernig-Zeichen
  - Lasègue-Zeichen
  - Kniekuss
  - Dreifuß-Zeichen (auch: Amoss-Zeichen)
- Inspektion der Haut
- Siehe auch: Orientierende neurologische Notfalluntersuchung

### Blutuntersuchung

- CRP, ggf. Procalcitonin
- Elektrolyte, Glucose
- Gerinnung: INR/Quick, pTT
- Differenzialblutbild
- Blutkultur
- Serologie für spezielle Erreger (insb. IgG, IgA, IgM) mittels ELISA, Blot und Immunfluoreszenztest oder AI (Antikörper-spezifischer Index; Nachweis der intrathekalen Synthese spezifischer Antikörper)
- Typischerweise zeigen sich im Falle einer bakteriellen Meningitis eine Leukozytose mit Neutrophilie und Linksverschiebung der Granulopoese sowie eine CRP- (und Procalcitonin-)Erhöhung!

### Liquoruntersuchung [1] [9] [10]

- Bei schwerer Bewusstseinsstörung, neuem fokal-neurologischen Defizit oder epileptischen Anfällen ist vor der Lumbalpunktion eine cCT zum Ausschluss einer intrakraniellen Druckerhöhung indiziert! [2]
- Unverzichtbar: Zellzahl, Zelldifferenzierung, Protein, Grampräparat, Glucose, Lactat
- **Erregerdiagnostik**
  - Direkter Nachweis mittels Kultur (Bakterien) oder PCR (insb. Viren, auch atypische Bakterien)
  - Nachweis erregerspezifischer IgM-Antikörper mittels ELISA
  - Ggf. ergänzend: Multiplex-PCR oder Next-Generation-Sequencing [2] [6]
  - Bei Erregernachweis immer Resistogramm und Bestimmung der Serogruppen bzw. -typen, bei Pneumokokken zusätzlich MIC

**Typische Liquordiagnostik bei verschiedenen Meningitisformen**

| Form | Erscheinung | Zellzahl/μL | Zellart | Lactat | Eiweiß (Gesamtprotein) | Glucose |
|---|---|---|---|---|---|---|
| Referenzwerte [11] | Klare Flüssigkeit | <5 | Wird nicht bestimmt | 0,9–2,7 mmol/L | <500 mg/L | Liquor/Serum-Quotient: >0,5 |
| Bakterielle Meningitis | Trübe, eitrige Flüssigkeit | 1.000–6.000 | Massive granulozytäre Pleozytose mit über 1.000 Zellen/μL, insb. Neutrophile | Deutlich erhöht (>3,5 mmol/L) | Erhöht, meist >2.000 mg/L | Vermindert, meist <30 mg/dL; Liquor-/Serum-Glucose-Quotient <0,3 |
| Virale Meningitis¹ | Klare Flüssigkeit | 10–500 | Lymphozytose, ggf. Monozytose | Normal | Normal bis leicht erhöht | Normal |
| Tuberkulöse Meningitis²[12] | Klare Flüssigkeit mit Spinngewebsgerinnseln | 10–1.000 | „Buntes Bild": Lymphozytose, Monozytose, Granulozytose | Erhöht (>2,5 mmol/L) | Erhöht, oft 2.000–10.000 mg/L | Vermindert |
| Neuroborreliose | Klare Flüssigkeit | 100–500 | Lymphozytose | Normal | Erhöht | Normal |

¹ Die tuberkulöse Meningitis kann aufgrund des ähnlichen Zellbefundes leicht mit einer Virusmeningitis verwechselt werden
² Zusätzliche Diagnostik bei tuberkulöser Meningitis: PCR

- Bei Therapiebeginn mit Antibiotika vor initialer bzw. bei verzögerter Liquorpunktion: Latexagglutinationstest zum Antigennachweis insb. von Meningokokken, Haemophilus influenzae b und Pneumokokken
- Mikroskopische Untersuchung: Meningokokken: Gramnegative Diplokokken; Pneumokokken: Grampositive Diplokokken; Listerien: Grampositive Stäbchen; Haemophilus influenzae: Gramnegative Stäbchen; Mycobacterium tuberculosis: Säurefeste Stäbchen in Ziehl-Neelsen-Färbung
- Die Liquorproben müssen sofort bei Raumtemperatur ins Labor transportiert werden! Es sollten sowohl nativer Liquor als auch mit Liquor beimpfte Blutkulturflaschen eingesendet werden!

### Bildgebende Diagnostik

- Ausschluss von Begleitkomplikationen, insb. radiologische Zeichen des erhöhten intrakraniellen Drucks, Ventrikulitis, Hirnabszess, Übergreifen auf das Parenchym
  - CT vor Lumbalpunktion zwingend bei Vigilanzminderung, qualitativer Bewusstseinsstörung, Übelkeit mit Erbrechen, neuen fokal-neurologischen Symptomen, siehe: Klinische Hirndruckzeichen
  - MRT bei V.a. Enzephalitis
- Ausschluss von Differenzialdiagnosen: Blutungen (insb. SAB), septische Sinusvenenthrombose, Ischämien, Tumoren
- Suche nach einem möglichen Eintrittsfokus v.a. im HNO-Bereich: CT der Nasennebenhöhlen bei jeder bakteriellen Meningitis zum frühestmöglichen Zeitpunkt
- Ggf. zur Diagnoseunterstützung bei unklarer Befundkonstellation: Idealerweise MRT (nach Lumbalpunktion und initialer medikamentöser Therapie), alternativ CT [13]; Nachweis typischer entzündlicher Verteilungsmuster insb. nach Kontrastmittelgabe

## Therapie

### Initiales Management [2]

Für das Notfallmanagement des meningitischen Syndroms siehe: Meningitisches Syndrom - AMBOSS-SOP.

- Vorsorgliche Isolierung bis zum Erregernachweis
- **Grundsätzliches Vorgehen bei noch unbekannter (!) Ätiologie**
  - Bei kompliziertem klinischen Bild (mit Bewusstseinsstörung und/oder bei klinischen Hinweisen auf gesteigerten intrakraniellen Druck und/oder bei neuen fokal-neurologischen Defiziten)
    - Blutkultur
    - Dexamethason-Gabe i.v.: Erwachsene: Immer DOSIS; Kinder: Nur bei eindeutigen Hinweisen auf eine akute bakterielle Meningitis und <3 Hib-Impfungen [14]
    - Kalkulierte Antibiotikatherapie plus Aciclovir, siehe auch: Kalkulierte antiinfektive Therapie bei V.a. ZNS-Infektion; Kalkulierte Antibiotikatherapie bei Meningitis; Kalkulierte Virustatikatherapie bei Meningitis
    - Bildgebung (bspw. CT) inkl. Darstellung der Nasennebenhöhlen
    - Lumbalpunktion und Liquordiagnostik, siehe: Liquordiagnostik bei Meningitis: Per Lumbalpunktion nach Ausschluss radiologischer Hirndruckzeichen; per externer Ventrikeldrainage bei Nachweis radiologischer Hirndruckzeichen
    - Intensivmedizinische Versorgung, ggf. Therapie des erhöhten intrakraniellen Drucks beginnen (Oberkörperhochlagerung um 30°, ggf. Liquordrainage)
  - Bei unkompliziertem klinischen Bild: Gleiches Vorgehen, aber Liquorpunktion noch vor erster Antibiotikagabe und Bildgebung möglich
- Die Antibiotikagabe ist bei bakterieller Meningitis die absolut wichtigste, weil einzig lebensrettende Maßnahme! Sie sollte möglichst innerhalb der 1. Stunde (spätestens 3 h) nach Krankenhausaufnahme begonnen werden! [2]

### Weiteres Vorgehen

- **Überwachung und supportive Therapie**
  - Aufnahme auf die Intensivstation und Behandlung von Komplikationen (bspw. Ausgleich evtl. auftretender Elektrolytstörungen, Behandlung eines Endotoxinschocks bei Meningokokken-Meningitis)
  - Analgetika/Antipyretika: Ibuprofen DOSIS oder Paracetamol DOSIS; siehe auch: Medikamentöse Antipyrese bei Kindern
  - Ggf. Volumensubstitution
  - Bei epileptischen Anfällen/epilepsietypischen Potenzialen im EEG: Anfallssuppressive Therapie
  - Bei septischer Sinusvenenthrombose: Antikoagulation; siehe auch: Therapeutische Antikoagulation - Klinische Anwendung
- **Fokussuche**
  - Insb. HNO-ärztliche Konsiliaruntersuchung und Suche nach einem parameningealen Entzündungsherd im CT oder MRT (bspw. Sinusitis)
  - Ggf. operative Fokussanierung noch am Aufnahmetag
- **Schutz von Kontaktpersonen**
  - Isolation Erkrankter bis 24 h nach Beginn einer wirksamen Antibiotikatherapie
  - Postexpositionsprophylaxe bei Meningitis bedenken und Kontaktpersonen dokumentieren (Postexpositionsprophylaxe von Kontaktpersonen o.ä. wird nach Meldung durch das Gesundheitsamt organisiert)
  - Bei Nachweis von oder V.a. Meningokokken: Transportierenden Rettungsdienst, etwaige Vorbehandler:innen und Gemeinschaftseinrichtungen sowie enge Kontaktpersonen informieren
- **Reevaluation nach 2 Tagen** unter laufender resistogrammgerechter antiinfektiver Therapie
  - Bei Symptomverbesserung: Therapie fortführen
  - Bei Symptomverschlechterung: Infektfokussuche auch außerhalb des ZNS, erneute Komplikationsabklärung, ggf. Therapieanpassung nach Resistogramm
- **Reevaluation nach Bestimmung des Erregers mit Resistogramm**: Ggf. Anpassung der Medikation
  - Antibiotika entsprechend Resistogramm anpassen
  - Dexamethason-Therapie bis zum Erregernachweis 4×/Tag fortsetzen, dann bei Pneumokokken-Nachweis: Über insg. 4 Tage geben, dann absetzen
  - Nachweis eines anderen Erregers: Absetzen [2]

### Bei Therapieende

- Bei komplikationsloser Heilung keine Lumbalpunktion zur Kontrolle nötig
- Bei Kindern: Immer EEG und Hörprüfung

### Kalkulierte Antibiotikatherapie bei Meningitis

**Kalkuliertes Therapieschema nach klinischer Konstellation**

Aufgrund der Gefährlichkeit und relativen Häufigkeit einer HSV- oder VZV-Meningitis wird mind. bis zum Erregernachweis immer auch antiviral mit Aciclovir i.v. anbehandelt! Siehe dazu: Kalkulierte Virustatikatherapie bei Meningitis.

*Kalkulierte Antibiotikatherapie bei ambulant erworbener Meningitis*
- Kombinationstherapie [2] [15]
  - Cephalosporin der 3. Generation i.v. (bspw. Ceftriaxon oder Cefotaxim): Wirksam gegen Meningokokken, Pneumokokken, Haemophilus
  - Und Ampicillin i.v. bei Erwachsenen und Neugeborenen: Zur Abdeckung von Listerien
  - Bei Herkunft aus oder nach Reisen in Gegenden mit hoher Cephalosporin-Resistenz von Pneumokokken: Ceftriaxon und Ampicillin plus Vancomycin oder Rifampicin
  - Bei Nachweis von Listerien: Ampicillin oder Trimethoprim/Sulfamethoxazol oder Meropenem plus Gentamicin [2]
- Siehe auch: Antibiotikadosierung bei Meningitis

*Kalkulierte Antibiotikatherapie bei nosokomial erworbener Meningitis*
- Indikation: Bspw. nach neurochirurgischer Operation, Schädel-Hirn-Trauma oder bei Shunt-Infektion
- Kombinationstherapie [15]
  - Vancomycin + Meropenem oder Vancomycin + Ceftazidim: Wirksam bspw. gegen Enterococcus spp., Pseudomonas spp., Staphylococcus spp., auch: Klebsiella spp., E. coli
  - Zusätzlich Metronidazol (bei Meningitis infolge einer Operation, bei der ein Zugang über die Schleimhäute erfolgte): Wirksam bspw. gegen Bacteroides fragilis
- Siehe auch: Antibiotikadosierung bei Meningitis

**Kalkuliertes Therapieschema nach Altersgruppen [2] [14]**

Für Dosierungen siehe Antibiotikadosierungen bei Meningitis.

- Neugeborenenmeningitis: Neugeborene ≤72 Lebensstunden siehe: Kalkulierte Antibiotikatherapie der Early-Onset-Sepsis; Neugeborene >72 Lebensstunden siehe: Kalkulierte Antibiotikatherapie der ambulant erworbenen Late-Onset-Sepsis
- Meningitis im Säuglings-, Kindes- und Jugendalter: Monotherapie mit einem Cephalosporin der 3. Generation (Cefotaxim oder Ceftriaxon); bei Herkunft aus oder nach Reisen in Gegenden mit hoher Penicillinresistenz von Pneumokokken [16]: Zusätzlich Vancomycin oder Rifampicin erwägen
- Im Erwachsenenalter: Kombination Ampicillin + Cephalosporin der 3. Generation (bspw. Ceftriaxon oder Cefotaxim) [15]; bei Herkunft aus oder nach Reisen in Gegenden mit hoher Cephalosporinresistenz von Pneumokokken: Ceftriaxon und Ampicillin plus Vancomycin oder Rifampicin
- Bei nosokomialen Infektionen oder Shunt-Infektionen: Vancomycin + Meropenem oder Vancomycin + Ceftazidim (bei Infektion infolge einer Operation mit Zugang durch die Schleimhäute zusätzlich Metronidazol)
- Nach einer Cephalosporin-Therapie über 24 h gelten Patienten nicht mehr als kontagiös!

**Mindestdauer der Antibiotikatherapie im Kindesalter [14] [17]**
- Neugeborene: ≥14 Tage; Enterobacteriaceae (bspw. E. coli): ≥21 Tage
- Säuglinge/Kinder: Kein Erregernachweis (ab dem Alter von 6 Wochen): ≥7–10 Tage; Enterobacteriaceae (bspw. E. coli): ≥21 Tage; Haemophilus influenzae Typ b: ≥7–10 Tage; Pneumokokken: ≥7–10 Tage; Meningokokken: ≥5 Tage

**Mindestdauer der Antibiotikatherapie bei Erwachsenen [2]**
- Abhängig von Therapieansprechen und Erreger
- Bei unkomplizierten Verläufen: Haemophilus influenzae: 7–10 Tage; Pneumokokken: 10–14 Tage; Meningokokken: 7–10 Tage; Listerien, gramnegative Enterobakterien: Häufig ≥3 Wochen

**Gezielte Antibiotikatherapie bei Meningitis mit Erregernachweis [14]**

Für Dosierungen siehe Antibiotikadosierungen bei Meningitis.

- Neugeborene/Säuglinge (0–6 Wochen)
  - B-Streptokokken: Ampicillin (oder Penicillin G) + Gentamicin
  - Listerien: Ampicillin + Gentamicin
  - E. coli, Klebsiellen: Cefotaxim + Gentamicin; oder Piperacillin/Tazobactam + Aminoglykosid
  - MRGN: Meropenem (oder Imipenem/Cilastatin) + Aminoglykosid
  - Pseudomonas aeruginosa: Ceftazidim (oder Piperacillin/Tazobactam oder Meropenem) + Tobramycin (oder Amikacin)
  - Staphylokokken: Koagulasenegative Staphylokokken: Vancomycin (oder Teicoplanin); MSSA: Cefuroxim (oder Cefazolin oder Flucloxacillin) + Gentamicin; MRSA: Vancomycin (oder Teicoplanin oder Linezolid)
- Kinder >6 Wochen [14]: Haemophilus influenzae Typ b: Cefotaxim bzw. Ceftriaxon; Meningokokken: Cefotaxim bzw. Ceftriaxon (oder Penicillin G); Pneumokokken: Cefotaxim bzw. Ceftriaxon (oder Penicillin G)
- Erwachsene
  - Haemophilus influenzae Typ b: Cefotaxim bzw. Ceftriaxon
  - Meningokokken: Cefotaxim bzw. Ceftriaxon (alternativ und nur nach vorheriger Resistenztestung: Penicillin G) [2]; bei Therapie mit Penicillin G: Anschließend Eradikation aus Nasen-Rachen-Raum äquivalent zu Postexpositionsprophylaxe bei Meningitis
  - Pneumokokken: Cefotaxim bzw. Ceftriaxon (oder Penicillin G); bei Penicillinresistenz (MIC >0,06 μg/mL): Cefotaxim (bzw. Ceftriaxon) + Vancomycin; oder Cefotaxim (bzw. Ceftriaxon) + Rifampicin; oder Cefotaxim (bzw. Ceftriaxon) + Meropenem
  - Staphylokokken (Methicillin-sensibel, MSSA): Cefazolin oder Flucloxacillin; oder Vancomycin + Fosfomycin; oder Vancomycin + Rifampicin; oder Vancomycin + Linezolid
  - MRSA: Vancomycin + Fosfomycin; oder Vancomycin + Rifampicin; oder Vancomycin + Linezolid
  - Pseudomonas aeruginosa: Fosfomycin + Ceftazidim; oder Fosfomycin + Meropenem; oder Fosfomycin + Cefepim
  - Bacteroides fragilis: Metronidazol oder Meropenem oder Clindamycin
  - Vancomycin-resistente Enterokokken: Linezolid
  - Multiresistente Enterobacteriaceae: Meropenem

**Therapie der tuberkulösen Meningitis [12]**
- Tuberkulostatische Kombinationstherapie: Gesamttherapiedauer mind. 12 Monate
  - Initial 4er-Kombination über 2 Monate: Isoniazid + Rifampicin + Pyrazinamid + Ethambutol [18]
  - Anschließend 2er-Kombination über weitere 10 Monate: Isoniazid + Rifampicin [19]
  - Plus adjuvante Steroidgabe, bspw. Prednisolon DOSIS
- Operative Therapie: Erwägen bei therapierefraktären, raumfordernden Läsionen; Vorliegen eines Hydrocephalus occlusus oder malresorptivus
- Siehe auch Therapie der Tuberkulose

### Antivirale Therapie bei Meningitis

**Kalkulierte Virustatikatherapie bei Meningitis**
- Sofortige Gabe von Aciclovir bei (Meningo-)Enzephalitis
- Aufgrund der Gefährlichkeit und relativen Häufigkeit einer HSV- oder VZV-Meningitis wird mind. bis zum Erregernachweis immer mit Aciclovir i.v. anbehandelt!

**Gezielte Virustatikatherapie bei Meningitis mit Erregernachweis**
- Bei HSV oder VZV: Aciclovir bei (Meningo-)Enzephalitis
  - Standarddosierung bei Erwachsenen DOSIS
  - Pädiatrische Dosierung: Zugelassen ab Geburt [14]: Neugeborene DOSIS; Säuglinge und Kinder ≤12 Jahre DOSIS; Jugendliche DOSIS
  - Für weitere Informationen siehe auch: Aciclovir (pädiatrisch)
- Bei CMV: Ganciclovir i.v. DOSIS in Kombination mit Foscarnet i.v. DOSIS für 3 Wochen, im Anschluss Ganciclovir-Monotherapie für weitere 3 Wochen bzw. 6 Wochen; oder Valganciclovir p.o. DOSIS in Kombination mit Foscarnet i.v. DOSIS für 3 Wochen, im Anschluss Valganciclovir-Monotherapie (Dauer abhängig von Erkrankungsschwere und Immunstatus)
- Bei HIV: Siehe HIV-Therapie

## Komplikationen

**Komplikationen der bakteriellen Meningitis (Auswahl)**
- Akute, potenziell lebensbedrohliche Komplikationen: Enzephalitis; Hirnödem; Sepsis, Verbrauchskoagulopathie; ARDS; Waterhouse-Friderichsen-Syndrom; epileptische Anfälle, Status epilepticus; seltener: Hirnabszess, Arteriitis (Gefahr für Hirninfarkte und Sinusvenenthrombose), Ventrikulitis, Zerebritis
- Langfristige Komplikationen mit ggf. behindernden Residuen: Strukturelle Epilepsie; Paresen; Koordinationsstörungen; Vestibulokochleäre Schädigung (Taubheit, Schwindel), insb. nach Pneumokokken-Meningitis [24]; seltener: Hydrozephalus, subdurales Empyem

**Komplikationen der viralen Meningitis (Auswahl)**
- Übergang in eine virale Enzephalitis mit dauerhafter Behinderung, insb. mit Neurokognitiven Defiziten und/oder struktureller Epilepsie

Es werden die wichtigsten Komplikationen genannt. Kein Anspruch auf Vollständigkeit.

## Waterhouse-Friderichsen-Syndrom

Das Waterhouse-Friderichsen-Syndrom ist eine gefürchtete Komplikation verschiedener Erkrankungen; es tritt aber meist in Zusammenhang mit der Meningokokken-Meningitis auf. Das Syndrom beruht pathophysiologisch auf einer durch Endotoxine ausgelösten Verbrauchskoagulopathie mit massiven Blutungen in der Haut, Schleimhaut und inneren Organen sowie einem septischen Schock. Infolge der Blutungen kommt es zur Nekrose der Nebennierenrinden mit entsprechender Nebennierenrindeninsuffizienz. Die Entzündungsreaktion im Gehirn führt zum Hirnödem mit neuronaler Schädigung und schließlich zur Atemlähmung. Auch eine Beteiligung des Herzmuskels kann infolge einer toxischen myokardialen Dysfunktion zum Tod führen.

### Epidemiologie

- In jedem Alter möglich
- Insb. Kleinkinder und Menschen mit Immunsuppression oder funktioneller/anatomischer Asplenie

### Ätiologie

Meist bei schweren Infektionen durch Meningokokken, aber auch bei Pneumokokken-, Hämophilus-influenzae- oder schweren Staphylokokken-Infektionen möglich

### Pathophysiologie

Freisetzung von Endotoxinen → Bindung an Zielzellen → Zytokinfreisetzung → Aktivierung des Gerinnungs- und Komplementsystems → Septischer Schock
- Disseminierte intravasale Gerinnung (DIC) → Thrombosen und Embolien, ggf. Schlaganfall und Einblutung in Haut, Schleimhaut und parenchymale Organe, insb. der Nebennierenrinde → Nekrose → Akute Nebennierenrindeninsuffizienz
- Bei Herzbeteiligung: Toxische myokardiale Dysfunktion
- Bei Überschreiten der Blut-Hirn-Schranke durch die Erreger: Bindung der Endotoxine an zerebrale Endothelzellen, Astrozyten und Makrophagen im Subarachnoidalraum → Zytokinfreisetzung → Meningeale Entzündungsreaktion mit Einwandern von Granulozyten → Freisetzen von entzündungsaktiven Substanzen durch die Granulozyten → Blut-Hirn-Schranken-Störung → Vasogenes Hirnödem → Spasmolytische Gefäßveränderungen und Vasospasmen → Kapilläre Minderperfusion → Ischämie und zytotoxisches Hirnödem → Zellnekrosen und Hirndruckanstieg → Neuronale Schädigung und Einklemmung → Tod durch Atemlähmung

Die Schwere der Dysregulation korreliert mit der Erregerlast im Blut!

### Klinische Symptome

- Klassische Meningitissymptome (insb. Kopfschmerzen, Fieber, Meningismus, Fotophobie, Übelkeit)
- Petechiale Haut- und Schleimhauteinblutungen bis zur Purpura fulminans mit ausgedehnten Nekrosen
- Schocksymptomatik mit Multiorganversagen
- Bewusstseinstrübung
- Respiratorische und/oder kardiale Insuffizienz
- Bei Verdacht auf Meningitis muss immer das gesamte Integument nach Petechien untersucht werden!

### Diagnostik und Therapie

- Immer intensivmedizinische Behandlung!
- Kalkulierte Antibiotikatherapie: Cephalosporin der 3. Generation i.v. (bspw. Ceftriaxon oder Cefotaxim) plus Ampicillin
- Weitere Maßnahmen
  - Volumenersatztherapie
  - Hochdosierte Gabe von Hydrocortison zur Substitution der Nebennierenrindeninsuffizienz (siehe auch: Nebennierenkrise)
  - Katecholamine, insb. Noradrenalin (zur Kreislaufstabilisierung, siehe auch: Therapie mit kreislaufwirksamen Substanzen bei Sepsis)
  - Ultima Ratio bei schweren Nekrosen: Amputation von Gliedmaßen

### Prognose (Waterhouse-Friderichsen-Syndrom)

- Unbehandelt immer letal, i.d.R. innerhalb von 12–24 h
- Unter Maximaltherapie meist auch letal
- Da die Letalität auch unter adäquater Maximaltherapie extrem hoch ist, sind das frühzeitige Erkennen und die sofortige Einleitung einer antibiotischen Therapie bei Verdacht auf eine bakterielle Meningitis entscheidend!

## Prognose

- **Bakterielle Meningitis [2]**
  - Letalität: Bei Meningokokken-Meningitis: 3–10%; bei Pneumokokken-Meningitis: 15–20%; bei Listerien-Meningitis: 20–30%
  - Neurologische Residuen: ca. 20%, siehe auch: Langfristige Komplikationen der Meningitis
- **Tuberkulöse Meningitis [5]**
  - Letalität: Unbehandelt fast 100%, unter Therapie bis zu 30%, abhängig von Therapiebeginn, Allgemeinzustand, Immunkompetenz und Alter
  - Prognose insgesamt: Stadium I: Fast immer folgenlose Abheilung; Stadium II: 75% folgenlose Abheilung; Stadium III: Schlechte Prognose; Überlebende haben meist neurologische Residuen
- **Virale Meningitis:** Bei unkompliziertem Verlauf meist spontane Abheilung

## Prävention [25]

### Impfungen

- Meningokokken-Impfung: Aufgrund des fulminanten Verlaufs der Meningokokken-Meningitis von besonderer Bedeutung. Siehe: Meningokokken-Impfung
- Haemophilus-influenzae-Typ-b-Impfung: Starker Rückgang Hib-bedingter bakterieller Meningitiden seit Aufnahme der Hib-Impfung in den Impfkalender. Siehe: Haemophilus-influenzae-Typ-b-Impfung
- Pneumokokken-Impfung: Starker Rückgang invasiver Pneumokokken-Infektionen seit Aufnahme der Pneumokokken-Impfung in den Impfkalender. Siehe: Pneumokokken-Impfung
- FSME-Impfung: Siehe: FSME-Impfung

### Expositionsprophylaxe [3] [26]

- Isolation Erkrankter: Bis 24 h nach Beginn einer wirksamen Antibiotikatherapie
- Wiederzulassung zu Gemeinschaftseinrichtungen [27]
  - Bei Erkrankung und Krankheitsverdacht: Nach Genesung
  - Enge Kontaktpersonen: Hib-Meningitis: 24–48 h nach Einleitung einer Chemoprophylaxe; Meningokokken-Meningitis: 24 h nach Einleitung einer Chemoprophylaxe
- Zur Prävention der FSME siehe: FSME-Prävention

### Postexpositionsprophylaxe

Siehe: Meningitis-Postexpositionsprophylaxe

## Meningokokken-Impfung

### STIKO-Empfehlungen [25]

**Standardimpfung**
- Meningokokken-B-Impfung: Grundimmunisierung aller Kinder ≥2 Monate mit 3 Impfdosen (je 1 Impfdosis im Alter von 2, 4 und 12 Monaten); begleitend: Prophylaktische Gabe von Paracetamol DOSIS [25]
- Meningokokken-ACWY-Impfung: Grundimmunisierung aller Jugendlichen im Alter von 12–14 Jahren mit einzelner Impfdosis
- Auffrischungsimpfung: Nicht empfohlen

**Nachholimpfung**
- Meningokokken-B-Impfung: Bis zum Alter von <5 Jahren; Alter <2 Jahre: 3 Impfdosen (begleitend: Prophylaktische Gabe von Paracetamol bei <2-Jährigen DOSIS [25]); Alter ≥2 Jahre: 2 Impfdosen
- Meningokokken-ACWY-Impfung: Einmalige Impfung bis zum Alter von <25 Jahren

**Indikationsimpfung**
- Bei angeborener oder erworbener Immundefizienz: Meningokokken-B- und Meningokokken-ACWY-Impfung, insb. bei Komplement- oder Properdindefizienz; Hypogammaglobulinämie; funktioneller oder anatomischer Asplenie; Therapie mit C5-Komplementinhibitoren (bspw. Eculizumab, Ravulizumab)
- Bei Epidemien: Nach Empfehlung der Gesundheitsbehörden
- Impfschema siehe: Impfschemata der Meningokokken-Impfung

**Berufsbedingte Impfung**
- Bei exponiertem Laborpersonal: Meningokokken-B- und Meningokokken-ACWY-Impfung
- Impfschema siehe: Impfschemata der Meningokokken-Impfung

**Reiseimpfung (nach STIKO und DTG) [28]**
- Bei Reisen in Gebiete mit Epidemierisiko bzw. Länder mit allgemeiner Impfempfehlung, insb. bei engem Kontakt zur Bevölkerung, v.a. im Meningitisgürtel: Meningokokken-ACWY-Impfung
- Langzeitaufenthalten, v.a. junger Menschen (bspw. Schüler:innen, Studierende, Freiwilligendienstleistende): Meningokokken-B- und Meningokokken-ACWY-Impfung bzw. Impfung nach Empfehlungen der Zielländer [29] [30]
- Ausbruchsgeschehen mit lokaler Impfempfehlung: Impfung abhängig von ursächlicher Serogruppe
- Beruflichem Einsatz in der Katastrophenhilfe (ggf. auch Entwicklungszusammenarbeit, Gesundheitswesen): Meningokokken-B- und Meningokokken-ACWY-Impfung bzw. nach Empfehlungen der Zielländer
- Pilgerreisen nach Saudi-Arabien (bspw. Mekka): Meningokokken-ACWY-Impfung vorgeschrieben
- Impfschema siehe: Impfschemata der Meningokokken-Impfung

**Impfschemata der Meningokokken-Impfung (für Indikationsimpfungen, berufsbedingte Impfungen, Reiseimpfungen und zur Postexpositionsprophylaxe)**

| Impfstoff | Alter bei Beginn der Impfung | Grundimmunisierung (Anzahl Impfdosen, Mindestabstände) | Auffrischungsimpfungen |
|---|---|---|---|
| **Meningokokken-B-Impfstoffe** | | | |
| Bexsero® | Säuglinge ≥2 bis <6 Monate | 3 Impfdosen (1./2.: 2 Monate; 2./3.: 6 Monate) oder 4 Impfdosen (1.–3.: je 1 Monat; 3./4.: 6 Monate) | — |
| Bexsero® | Säuglinge ≥6 bis <12 Monate | 3 Impfdosen (je 2 Monate) | — |
| Bexsero® | Kinder ≥12 bis <24 Monate | 3 Impfdosen (1./2.: 2 Monate; 2./3.: 12–23 Monate) | — |
| Bexsero® | Kinder ≥2 Jahre, Jugendliche und Erwachsene | 2 Impfdosen (1 Monat) | — |
| Trumenba® | Kinder ≥10 Jahre, Jugendliche und Erwachsene | 2 Impfdosen (6 Monate) oder 3 Impfdosen (1./2.: 1 Monat; 2./3.: 4 Monate) | Bei anhaltendem Infektionsrisiko nach 5 Jahren erwägen |
| **Meningokokken-C-Impfstoffe** | | | |
| NeisVac-C® | Säuglinge ≥2 bis <4 Monate | 3 Impfdosen (1./2.: 2 Monate; 2./3.: 6 Monate) | — |
| NeisVac-C® | Säuglinge ≥4 bis <12 Monate | 2 Impfdosen (6 Monate) | — |
| NeisVac-C® | Kinder ≥12 Monate, Jugendliche und Erwachsene | 1 Impfdosis | — |
| Menjugate® 10 Mikrogramm | Säuglinge ≥2 bis <12 Monate | 3 Impfdosen (1./2.: 2 Monate; 3.: Zeitpunkt gemäß offiziellen Empfehlungen) | — |
| Menjugate® 10 Mikrogramm | Kinder ≥12 Monate, Jugendliche und Erwachsene | 1 Impfdosis | — |
| **Meningokokken-ACWY-Impfstoffe [28]** | | | |
| Nimenrix® | Säuglinge ≥6 Wochen bis <6 Monate | 2 Impfdosen (2 Monate) | Bei Grundimmunisierung im Alter von <12 Monaten: 1 Impfdosis im Alter von 12 Monaten (Mindestabstand 2 Monate); bei anhaltendem Infektionsrisiko: 1 Impfdosis (Mindestabstand 10 Jahre); kann als Auffrischungsimpfung an Personen mit vorheriger Meningokokken-C-Grundimmunisierung verabreicht werden |
| Nimenrix® | Säuglinge ≥6 Monate, Kinder, Jugendliche und Erwachsene | 1 Impfdosis | — |
| MenQuadfi® | Kinder ≥12 Monate, Jugendliche und Erwachsene | 1 Impfdosis | 1 Impfdosis (Mindestabstand 5 Jahre); kann als Auffrischungsimpfung an Personen mit vorheriger Meningokokken-C-Grundimmunisierung verabreicht werden |
| Menveo® | Kinder ≥2 Jahre, Jugendliche und Erwachsene | (Angabe im Quelltext unvollständig) | — |

**Postexpositionelle Impfung:** Siehe: Postexpositionsprophylaxe bei Meningokokken-Meningitis

### Impfschutz

- Meningokokken-ACWY-Impfung: Wirkbeginn innerhalb eines Monats nach Grundimmunisierung [31]; Dauer des Impfschutzes unbekannt

### Impfstoffe

- Meningokokken-B-Impfstoff: Totimpfstoff (Adsorbatimpfstoff)
- Meningokokken-C-Impfstoff: Totimpfstoff (Konjugatimpfstoff, Adsorbatimpfstoff)
- Meningokokken-ACWY-Impfstoff: Totimpfstoff (Konjugatimpfstoff)

Das RKI bietet ein Faktenblatt mit den wichtigsten Informationen zur Meningokokken-Impfung an, bspw. für Aufklärungsgespräche! [32]

## Postexpositionsprophylaxe bei Meningitis [25]

### Überblick der Postexpositionsprophylaxe bei Meningokokken- und Hib-Meningitis

- Indikation: Enger Kontakt zu einer erkrankten Person
- Art der Postexpositionsprophylaxe
  - Chemoprophylaxe: Zeitpunkt: Schnellstmöglich; Meningokokken-Meningitis: Max. 10 Tage nach Kontakt mit der Indexperson; Hib-Meningitis: Max. 7 Tage nach Symptombeginn der Indexperson
  - Ggf. zusätzlich postexpositionelle Aktivimpfung: Bei impfpräventabler Meningokokken-Serogruppe; bei Haemophilus influenzae b: Ggf. Nachholimpfung bei Kindern <5 Jahre

**Überblick der Chemoprophylaxe nach Meningitis-Exposition**

| Altersgruppe | Bei Meningokokken [2] | Bei Haemophilus influenzae b [33] |
|---|---|---|
| Erwachsene | Rifampicin (Mittel der Wahl): Für 2 Tage; Ciprofloxacin unter Beachtung des Rote-Hand-Briefes zu Ciprofloxacin: Einmalgabe; Ceftriaxon: Einmalgabe | Rifampicin (Mittel der Wahl): Für 4 Tage; Ceftriaxon: Für 2 Tage; Levofloxacin: Für 2 Tage |
| Säuglinge, Kinder und Jugendliche | Rifampicin; Ceftriaxon | Rifampicin; Ceftriaxon; Levofloxacin |
| Schwangere | Ceftriaxon (Mittel der Wahl); Azithromycin | Ceftriaxon |

### Postexpositionsprophylaxe bei Meningokokken-Meningitis oder -Sepsis

**Antibiotische Postexpositionsprophylaxe**
- Indikation: Enger Kontakt zu einer an Meningokokken-Meningitis erkrankten Person innerhalb von 7 Tagen vor Symptombeginn bis 24 h nach Beginn einer antibiotischen Therapie
- Zeitpunkt: So schnell wie möglich, sinnvoll bis max. 10 Tage nach entsprechendem Kontakt
- Wirkstoffe
  - Für alle Personen, ausgenommen Schwangere: Rifampicin — Neugeborene (Off-Label Use) DOSIS [25]; Kinder ≥1 Monat (Off-Label Use bis <6 Jahre), Jugendliche und Erwachsene ≤60 kg DOSIS [25]; Jugendliche und Erwachsene >60 kg DOSIS
  - Alternativen: Personen ≥18 Jahre: Ciprofloxacin unter Beachtung des Rote-Hand-Briefes zu Ciprofloxacin DOSIS; Personen ≥2 Jahre: Ceftriaxon — Kinder ≥2 Jahre bis <12 Jahre DOSIS; Kinder ≥12 Jahre, Jugendliche und Erwachsene DOSIS
  - Schwangere: Ceftriaxon DOSIS; oder Azithromycin DOSIS
- Beachte: Aktuelle Empfehlungen des RKI [3]

**Postexpositionelle Impfung**
- Indikation: Zusätzlich zur Chemoprophylaxe bei
  - Einzelner Infektion durch impfpräventable Stämme: Impfung ungeimpfter Haushaltskontakte und enger Kontakte mit haushaltsähnlichem Charakter
  - Ausbrüchen von Meningokokken-Erkrankungen durch impfpräventable Stämme: Impfung enger Kontaktpersonen in Haushalt und Gemeinschaftseinrichtungen
  - Bei regional gehäuftem Auftreten ggf. ausgedehntere Impfempfehlung durch die Gesundheitsbehörden
- Impfstoffe: Serogruppe B: Meningokokken-B-Impfstoff; Serogruppe C: Meningokokken-C-Impfstoff; Serogruppen A, W, Y: Meningokokken-ACWY-Impfstoff
- Impfschema siehe: Impfschemata der Meningokokken-Impfung
- Bei Meningokokken-Nachweis oder -Verdacht sollten der transportierende Rettungsdienst, etwaige Vorbehandler:innen und Gemeinschaftseinrichtungen sowie enge Kontaktpersonen informiert werden!

### Postexpositionsprophylaxe bei Meningitis durch Haemophilus influenzae b

Siehe: Postexpositionsprophylaxe bei invasiver Hib-Infektion

## Pathologie

### Bakterielle Meningitis

- **Eitrige Meningitis**
  - Makroskopie: Veränderungen typischerweise über der frontalen und parietalen Großhirnrinde; verdickte und trübe erscheinende grünlich-gelbe Hirnhäute: Sog. Haubenmeningitis; ödematöse Schwellung des Hirnparenchyms; ggf. gestaute Gefäße und Einblutungen (bspw. in Form von Petechien) im Bereich der Hirnhäute und/oder des Hirnparenchyms
  - Mikroskopie: Massenhaft granulozytäre Infiltrate im Subarachnoidalraum
- **Hirnabszess**
  - Makroskopie: Gelblich-grüne, abgekapselte Nekroseherde, meist in den Großhirnhemisphären und im Kleinhirn
  - Mikroskopie: Granulozyten und abgestorbene Zellbestandteile (Zelldetritus) in der Abszesshöhle, außen fibrotischer Randsaum

*(Bildverweise: Eitrige Meningitis (Leptomeningitis purulenta); Bakterielle Meningitis; Multiple Hirnabszesse nach eitriger Meningitis; Bakterielle Meningoenzephalitis; Kleinhirn und Hirnstammanteile mit Hämorrhagien und petechialen Einblutungen; Paukenhöhlenbefund bei Meningoenzephalitis)*

### Tuberkulöse Meningitis

- Makroskopie: Basale Meningitis: Veränderungen sind v.a. in den basalen Zisternen lokalisiert; weißlich-grünes, gelatineartiges Netz, das die basale Hirnoberfläche bedeckt
- Mikroskopie: Verkäsende Granulome, Epitheloidzellen, lymphozytäres Infiltrat

*(Bildverweis: Tuberkulöse Leptomeningitis)*

### Virale Meningitis

- Sehr vielfältig in der Morphologie
- Makroskopie: Evtl. generalisiertes Hirnödem
- Mikroskopie: Lymphozytäre Infiltrate
- Je nach Virus: Enzephalitis als Komplikation (bspw. HSV, VZV)

### Sonstige Meningitiden

- **Zerebrale Toxoplasmose:** Makroskopie: Multiple Abszesse im Marklager der Großhirnhemisphären; Mikroskopie: Umschriebene Gewebsnekrosen
- **Kryptokokken-Meningitis:** Makroskopisch: Basale Meningitis (ähnlich der tuberkulösen Meningitis); Mikroskopisch: PAS-positive Kryptokokken

## Meldepflicht

- **Arztmeldepflicht**
  - Nach § 6 IfSG: Namentliche Meldepflicht bei Verdachts-, Krankheits- oder Todesfällen einer Meningokokken-Meningitis oder -Sepsis
  - Nach IfSGMeldeVO (nur in Sachsen): Namentliche Meldepflicht bei Erkrankungs- und Todesfällen durch Listerien
- **Labormeldepflicht nach § 7 IfSG**
  - Namentliche Meldepflicht nur bei direktem Nachweis von Meningokokken, Pneumokokken und Listerien aus Liquor, Blut, hämorrhagischen Hautinfiltraten oder anderen normalerweise sterilen Substraten
  - Haemophilus influenzae aus Liquor oder Blut
- **Meldepflicht für Leiter von Gemeinschaftseinrichtungen § 33 und § 34 IfSG**
  - Namentliche Meldepflicht bei Verdachts- und Krankheitsfällen von Meningokokken- oder Haemophilus-influenzae-b-Meningitis (§ 34 (1) IfSG)

## Besondere Patientengruppen

*(Im Quellartikel nur als Verweis-Überschrift ohne eigenen Fließtext vorhanden; direkt gefolgt von der Meditricks-Box.)*

## Kodierung nach ICD-10-GM Version 2026

*(Im Quellartikel nur als Verweis-Überschrift ohne eigenen Fließtext vorhanden.)*

**Tipps & Links** *(Linktitel, nicht die verlinkten Inhalte selbst)*
- Aktueller AMBOSS-Impfkalender
- Vertonung dieses Kapitels – AMBOSS Audio: Neurologie – Meningitis
- Anmeldung Kongress-Telegramm Innere Medizin
- Anmeldung One-Minute Telegram
- AMBOSS-Podcast
- AMBOSS Leitlinien-Telegramm

## Quellen

1. S1-Leitlinie Nicht-eitrige ZNS Infektionen von Gehirn und Rückenmark im Kindes- und Jugendalter. Stand: 2015. Abgerufen am: 14.10.2016.
2. S2k-Leitlinie Ambulant erworbene bakterielle Meningoenzephalitis im Erwachsenenalter. Stand: 2023. Abgerufen am: 02.06.2023.
3. S1-Leitlinie Virale Meningoenzephalitis. Stand: 2025. Abgerufen am: 17.03.2025.
4. Speer, Gahr: Pädiatrie. 4. Auflage Springer 2013, ISBN: 3-642-34268-x.
5. Laborlexikon.de. Abgerufen am: 01.01.2012.
6. Schmid: Ambulanzmanual Pädiatrie von A–Z. Springer 2014, ISBN: 978-3-642-41892-1.
7. Herold: Innere Medizin 2017. Herold 2016, ISBN: 3-981-46606-3.
8. S1-Leitlinie Lumbalpunktion und Liquordiagnostik. Stand: 2019. Abgerufen am: 26.07.2021.
9. Tuberkulose im Erwachsenenalter. Abgerufen am: 23.08.2024.
10. Swanson, McGavern: Viral diseases of the central nervous system. In: Current Opinion in Virology. Band: 11, 2015, doi: 10.1016/j.coviro.2014.12.009, p.44-54.
11. Berner et al.: DGPI-Handbuch: Infektionen bei Kindern und Jugendlichen. 7. Auflage Deutsche Gesellschaft für Pädiatrische Infektiologie (DGPI) 2018, ISBN: 978-3-132-40790-9.
12. Marx et al.: Die Intensivmedizin. 12. Auflage Springer-Verlag 2015, ISBN: 978-3-642-54952-6.
13. Rieger et al.: Pädiatrische Pneumologie. Springer 2013, ISBN: 978-3-662-09182-1.
14. Ständige Impfkommission (STIKO): Empfehlungen der Ständigen Impfkommission (STIKO) beim Robert Koch-Institut 2026. In: Robert Koch-Institut. 2026, doi: 10.25646/13636.
15. RKI Ratgeber Haemophilus influenzae, invasive Infektion. Stand: 2021. Abgerufen am: 12.03.2025.
16. Meningokokken, invasive Erkrankungen (Neisseria meningitidis), RKI-Ratgeber. Stand: 2021. Abgerufen am: 14.06.2023.
17. Empfehlungen für die Wiederzulassung zu Gemeinschaftseinrichtungen gemäß §34 IfSG. Stand: 2023. Abgerufen am: 25.03.2025.
18. Monographie Ceftriaxon. Stand: 2023. Abgerufen am: 19.06.2023.
19. S2k-Leitlinie Bakterielle Infektionen bei Neugeborenen. Stand: 2018. Abgerufen am: 05.10.2020.
20. Hacke (Hrsg.): Neurologie. 14. Auflage Springer 2016, ISBN: 978-3-662-46891-3.
21. Staphylex® Infusion Fachinformation. Stand: 2018. Abgerufen am: 06.10.2020.
22. Monographie Imipenem + Cilastatin. Stand: 2023. Abgerufen am: 11.01.2024.
23. S2k-Leitlinie Kalkulierte parenterale Initialtherapie bakterieller Erkrankungen bei Erwachsenen – Update 2018. Abgerufen am: 10.01.2018.
24. Antibiotic Resistance. Stand: 2022. Abgerufen am: 20.06.2022.
25. Tuberkulose, RKI-Ratgeber für Ärzte. Stand: 2022. Abgerufen am: 08.06.2022.
26. Guidelines for Treatment of Drug-Susceptible Tuberculosis and Patient Care. Stand: 2017. Abgerufen am: 30.06.2018.
27. Piechotta et al.: Beschluss und wissenschaftliche Begründung zur Erweiterung der STIKO-Empfehlung zur Indikationsimpfung und postexpositionellen Chemoprophylaxe gegen Haemophilus influenzae Typ b. In: Epid Bull. Band: 2025, Nummer: 34, 2025, doi: 10.25646/13361, p.3-18.
28. Berlit: Basiswissen Neurologie. Springer 2013, ISBN: 978-3-642-37784-6.
29. Empfehlungen der Ständigen Impfkommission (STIKO) und der Deutschen Gesellschaft für Tropenmedizin, Reisemedizin und Globale Gesundheit e.V. (DTG) zu Reiseimpfungen. Stand: 2026. Abgerufen am: 06.08.2026.
30. Vaccine schedules in all countries in the EU/EEA. Stand: 2025. Abgerufen am: 14.04.2025.
31. Vaccination schedule. Stand: 2025. Abgerufen am: 14.04.2025.
32. Rothe et al.: Reiseimpfungen – Hinweise und Empfehlungen. In: Flugmedizin · Tropenmedizin · Reisemedizin - FTR. Band: 31, Nummer: 02, 2024, doi: 10.1055/a-2256-7855, p.54-86.
33. Faktenblatt zur Meningokokken-Impfung. Stand: 2024. Abgerufen am: 25.03.2025.
34. Al-Abtah et al.: I care Pflege. Georg Thieme Verlag KG 2020, ISBN: 978-3-132-41828-8.
35. Menche et al.: Pflege Heute. 8. Auflage Urban & Fischer Verlag / Elsevier GmbH 2023, ISBN: 978-3-437-26779-6.
36. Fley, Schneider: Pflege Heute - Pädiatrische Pflege. 2. Auflage Urban & Fischer Verlag / Elsevier GmbH 2024, ISBN: 978-3-437-25004-0.

**Hinweis zur Quellennummerierung:** Die im Text zitierten Quellenzahlen [1]–[19] und die im Quellenverzeichnis aufgeführten Einträge 20–36 zeigen eine gewisse Diskrepanz in der Reihenfolge/Thematik (bspw. erscheint Eintrag 25 im Text sowohl im Kontext STIKO-Impfempfehlungen als auch im Quellenverzeichnis als "Tuberkulose, RKI-Ratgeber"). Dies spiegelt die Originalnummerierung des AMBOSS-Quellartikels wider und wurde unverändert übernommen.
