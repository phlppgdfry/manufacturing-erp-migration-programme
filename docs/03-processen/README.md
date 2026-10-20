# Processen: workshops, as-is en to-be

> **Wat dit is:** hoe de procesanalyse liep, wat er in de workshops naar boven kwam, en de procesmodellen. **Voor wie:** proceseigenaars, partner, wie de fit-gap wil begrijpen. **Vorige:** [partnerselectie](../02-partnerselectie/README.md) · **Volgende:** [fit-gap](../04-fit-gap/README.md).

## Workshopplan (W7–W12)

Zes workshops van een halve dag, elk met de proceseigenaar, de key users, de lead consultant van de partner en mij. Elke workshop vertrekt van een **echt document van vorige week** (een order, een batchrecord, een factuur) dat we samen van begin tot eind volgen. Pas daarna kijken we in Business Central.

| # | Workshop | Eigenaar | Vertrekpunt | Wat we moesten weten |
|---|---|---|---|---|
| W1 | Order tot levering | Teamleider klantendienst | EDI-order van R1 met een correctie | waar en waarom orders manueel aangepast worden |
| W2 | Planning | COO + hoofd planning | het Excel-planbord van een soepweek | welke regels in de formules zitten |
| W3 | Productie en lots | Plantmanager + QA | een batchrecord van een sauslot | hoe een lot ontstaat, waar de vervaldatum vandaan komt |
| W4 | Kwaliteit en recall | QA-manager | de laatste recall-oefening (3u40) | waar de tijd in de oefening naartoe ging |
| W5 | Aankoop, ontvangst, voorraad, koelhuis | Aankoper + magazijn | een ontvangst met een afwijkende leverancierslot | hoe leverancierslots en het koelhuis aansluiten |
| W6 | Financiën en kostprijs | CFO + controller | de maandafsluiting van januari | waarom de afsluiting negen dagen duurt |

Afspraken voor elke workshop: we scheiden **wat we zien** (observatie), **wat iemand wil** (wens) en **wat we voorstellen** (voorstel). Elke open vraag krijgt een eigenaar en een datum.

## Wat de workshops opleverden

| Workshop | Observatie | Tegenstrijdigheid of verrassing | Wat ermee gebeurde |
|---|---|---|---|
| W1 | 7,5% van de EDI-orders wordt aangepast; meestal eenheid (doos ↔ stuk) bij twee retailers | klantendienst wil "alles automatisch", de CFO wil elke prijsafwijking zien | uitzonderingen naar een werklijst; prijsafwijking blokkeert, eenheid wordt omgerekend → VK-01, DQ-04 |
| W2 | het planbord bevat 22 jaar aan regels in formules (allergenenvolgorde op een lijn, reinigingstijd na selder) | de planner: "Business Central kan dit niet"; de COO: "dan moet het" | regels uitgeschreven; allergenenvolgorde wordt een routing- en planningsregel, de rest blijft kennis van de planner → PR-03, R-07 |
| W3 | halffabricaten van Hal 2 krijgen hun lot via een eigen SAP-transactie | niemand wist wie die transactie onderhoudt | gemeld als datakwaliteitsrisico R-04; werd later issue I-03 |
| W4 | van de 3u40 recall-oefening ging 2u50 naar papieren batchrecords zoeken | QA wil alles elektronisch, productie wil geen extra stap aan de lijn | fase 1: lots scannen bij verbruik (één scan), batchrecord blijft papier → PR-05, PR-08 naar fase 2 |
| W5 | het koelhuis meldt voorraad per pallet, Vaerdal boekt per lot | wie is eigenaar van de voorraad in het koelhuis? | Vaerdal is eigenaar, koelhuis is locatie; dagelijkse afstemming → VR-01 |
| W6 | twee van de negen afsluitdagen gaan naar wachten op de voorraadwaardering | finance wil maandelijkse waardering behouden "zoals in SAP" | dagelijkse waardering in Business Central, afsluitkalender → FIN-07 |

## De 146 Z-objecten

Elk eigen SAP-object kreeg in de ontwerpfase één van vijf uitkomsten. Niet "alles wat bestaat, moet terug", maar "wat lost dit object op, en hoe doet de standaard dat?".

| Uitkomst | Aantal | Voorbeelden |
|---|---:|---|
| Standaard Business Central doet het | 61 | eigen rapporten voor openstaande posten, kredietlimietcontrole, prijslijsten per periode |
| Power BI of een standaardrapport | 38 | 26 van de 41 eigen rapporten |
| Procesaanpassing | 21 | maandelijkse herwaardering → dagelijks; eigen goedkeuringsscherm → standaardworkflow |
| Niet meer nodig | 24 | interfaces naar systemen die al weg zijn, eenmalige conversies |
| App of extensie | 2 | allergenen doorrekenen (KW-03), resterende houdbaarheid per klant (VK-05) |

*Illustratieve verdeling.*

## Procesmodellen

- [Order tot levering: as-is → to-be](order-tot-levering.md) (BPMN 2.0)
- [Recall van een grondstoflot](recall.md) (BPMN 2.0)

De modellen zijn gemaakt uit [`data/processes.json`](../../data/processes.json) door [`erpcase/bpmn.py`](../../erpcase/bpmn.py): geldige BPMN 2.0 met diagram (opent in Camunda Modeler of bpmn.io) en een SVG voor de site. De test controleert dat elke stroom een bron en doel heeft en dat elk element een plaats in het diagram heeft.
