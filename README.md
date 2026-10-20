# Van SAP naar Business Central bij een voedingsproducent

**Een ERP-migratieprogramma geleid vanuit de klant: partnerkeuze, fit-gap, datamigratie, test, go/no-go en uitrol.**

> In de generale repetitie hadden <!--n:mock3.DQ-10-->107<!--/n--> lots halffabricaat geen vervaldatum. Een eigen SAP-transactie bleef nieuwe foute lots maken, dus opschonen hielp niet. Drie harde go/no-go-criteria faalden; ik stelde de stuurgroep vier weken uitstel voor (<!--n:budget.delay-->€55.700<!--/n--> uit de reserve). Vier weken later: recall <!--n:mock4.recall-->100,0%<!--/n-->, go.

> *Onafhankelijke portfoliocase over een fictieve organisatie (Vaerdal Foods). Bevat geen vertrouwelijke informatie van een echte werkgever, klant of leverancier. Alle cijfers zijn illustratieve aannames; resultaten na de go-live zijn gesimuleerd.*

**[Live site](https://phlppgdfry.github.io/manufacturing-erp-migration-programme/)** · **[Rondleiding van 2 minuten](https://phlppgdfry.github.io/manufacturing-erp-migration-programme/room/?tour)** · **[Start hier](START-HERE.md)** · **[Bewijs per eis](EVIDENCE.md)** · **[Executive brief (PDF)](application-kit/exports/executive-brief.pdf)**

## Het traject

```text
Mobilisatie            charter · business case · governance · planning        docs/01-mobilisatie
   ↓
Partnerkeuze           criteria vóór offertes · demoscript · contract          docs/02-partnerselectie
   ↓
Processen              6 workshops · BPMN as-is → to-be · recall               docs/03-processen
   ↓
Fit-gap                41 eisen · klasse · beslisser · UAT-scenario            docs/04-fit-gap
   ↓
Datamigratie           15 regels · 4 proefmigraties · afstemming · recall      docs/05-datamigratie + erpcase/
   ↓
Testen en verandering  UAT door key users · opleiding · weerstand              docs/06-testen, docs/07-verandering
   ↓
Go/no-go               12 criteria vooraf vastgelegd · 2 momenten              docs/08-go-live
   ↓
Na de go-live          hypercare · batenreview · IT-roadmap                    docs/08-go-live, docs/09-baten, docs/10-it-roadmap
```

## Het probleem

Vaerdal Foods (<!--n:org.employees-->185<!--/n--> medewerkers) maakt gekoelde sauzen en soepen, grotendeels als huismerk voor supermarkten in België, Nederland en Frankrijk. Het standaardonderhoud van SAP ECC loopt af en de enige SAP-ontwikkelaar stopt. De raad van bestuur koos Microsoft Dynamics 365 Business Central. Planning draait in een Excel-planbord, traceerbaarheid op papier, kwaliteitsvrijgave per mail; een recall-oefening duurt <!--n:kpi.K2.baseline-->220<!--/n--> minuten. Soep loopt van oktober tot februari, BBQ-sauzen vanaf april.

## Wat ik deed (als IT-projectmanager / business analist aan de klantkant)

- **Partner gekozen op vooraf vastgelegde criteria** — dezelfde demo voor elke partner, gevoeligheidsanalyse op de gewichten, contract met acceptatie per mijlpaal ([partnerselectie](docs/02-partnerselectie/README.md), [demoscript](docs/02-partnerselectie/demoscript.md), [contract](docs/02-partnerselectie/contractafspraken.md)).
- **Processen vanuit echte documenten** — zes workshops, BPMN 2.0 as-is en to-be, recall als apart proces ([processen](docs/03-processen/README.md)).
- **Fit-gap met een beslisser per regel** — <!--n:fg.total-->41<!--/n--> eisen, <!--n:fg.stdConfPct-->74%<!--/n--> standaard of configuratie, <!--n:fg.extensions-->2<!--/n--> extensies ([register](docs/04-fit-gap/fit-gap.md)).
- **Datamigratie als code** — synthetische SAP-extracten, <!--n:dq.rules-->15<!--/n--> kwaliteitsregels met een eigenaar in de business, mapping naar Business Central, afstemming en mock recall ([migratie](docs/05-datamigratie/README.md), [`erpcase/`](erpcase/)).
- **Partner, budget en scope bewaakt** — RAID, change requests, reserve met beslisdrempel, statusrapport ([governance](docs/governance/README.md)).
- **Testen en opleiden met de business** — <!--n:uat.scenarios-->17<!--/n--> UAT-scenario's geschreven door key users, opleiding in drie golven, weerstand van de planner ([testen](docs/06-testen/README.md), [verandering](docs/07-verandering/README.md)).
- **Go/no-go voorgesteld, stuurgroep besliste** — 12 criteria vastgelegd in week 16; no-go op 1 maart, go op 1 april ([go/no-go](docs/08-go-live/go-no-go.md)).
- **Na de go-live** — hypercare per oorzaak, een eerlijke batenreview en een IT-roadmap met de IT Manager ([hypercare](docs/08-go-live/hypercare.md), [baten](docs/09-baten/README.md), [roadmap](docs/10-it-roadmap/README.md)).

## Belangrijkste keuzes

1. **Criteria vóór offertes, prijs weegt 15%.** Partner A blijft eerste tot prijs meer dan <!--n:sens.C6.to-->40%<!--/n--> weegt ([partnerselectie](docs/02-partnerselectie/README.md), [ADR-006](docs/adr/adr-006-contractvorm.md)).
2. **Standaard eerst; elke extensie naar de stuurgroep.** Van 146 SAP-maatwerkobjecten naar twee extensies ([ADR-001](docs/adr/adr-001-standaard-eerst.md)).
3. **Geen historiek migreren, lotnummers ongewijzigd.** De recall loopt van Business Central door in het SAP-archief ([ADR-003](docs/adr/adr-003-geen-historiek-wel-archief.md), [ADR-008](docs/adr/adr-008-lotnummers-behouden.md)).
4. **Go/no-go-criteria vooraf, hard is hard.** Daardoor was het no-go in week 25 geen discussie maar een vaststelling ([go/no-go](docs/08-go-live/go-no-go.md)).

## Wat dit aantoont

| Wat de rol vraagt | Bewijs |
|---|---|
| Een ERP-migratie leiden van analyse tot uitrol | [charter](docs/01-mobilisatie/project-charter.md), [planning](docs/01-mobilisatie/planning.md), [proefmigraties](docs/05-datamigratie/README.md), [cutover](docs/05-datamigratie/cutover.md), [go/no-go](docs/08-go-live/go-no-go.md), [hypercare](docs/08-go-live/hypercare.md) |
| Bedrijfsprocessen vertalen naar IT-oplossingen | [workshops](docs/03-processen/README.md), [as-is → to-be](docs/03-processen/order-tot-levering.md), [fit-gap](docs/04-fit-gap/fit-gap.md) |
| Implementatiepartners en leveranciers aansturen | [selectie](docs/02-partnerselectie/README.md), [contract](docs/02-partnerselectie/contractafspraken.md), [change requests](docs/governance/change-requests.md), [budget](docs/governance/README.md#budget) |
| Workshops en testfases met finance en productie | [workshopplan](docs/03-processen/README.md), [UAT](docs/06-testen/uat-scenarios.md), [opleiding](docs/07-verandering/README.md) |
| Productie en supply chain begrijpen | [order tot levering](docs/03-processen/order-tot-levering.md), [recall](docs/03-processen/recall.md), [mapping](docs/05-datamigratie/mapping.md) |
| Technologisch beleid met de IT Manager | [IT-roadmap](docs/10-it-roadmap/README.md), [business case](docs/01-mobilisatie/business-case.md) |

Volledige mapping met "getoond / niet geclaimd": [EVIDENCE.md](EVIDENCE.md).

## Openen en controleren

**Zonder iets te installeren:** de [live site](https://phlppgdfry.github.io/manufacturing-erp-migration-programme/) en de [control room met rondleiding](https://phlppgdfry.github.io/manufacturing-erp-migration-programme/room/?tour).

**Lokaal** (Python 3.10 of nieuwer, geen extra pakketten):

```bash
python3 scripts/build.py                          # extracten, regels, mapping, afstemming, go/no-go → site-data en documenten
python3 -m unittest discover -s tests -t .        # alle testen
python3 scripts/build.py --check                  # elk getal in docs en site = het model
python3 scripts/check-links.py                    # alle relatieve links
python3 -m http.server -d site 8000               # site op http://localhost:8000
```

Wat je moet zien: `build ok`, alle testen `OK`, `check ok` en geen kapotte links. CI draait hetzelfde bij elke push ([ci.yml](.github/workflows/ci.yml)).

**Wat de testen bewijzen:** elke datakwaliteitsregel vindt precies de fouten die in de extracten zitten; het voorraadverschil is volledig verklaard; de recall is pas 100% na het herstel; de go/no-go-regels geven NO-GO in week 25 en GO in week 29; elke eis in scope heeft een UAT-scenario; ten hoogste drie extensies; de BPMN-bestanden zijn geldig; elk getal in de documenten komt uit het model.

## Als de demo niet laadt

[Screenshots van elke stap van de rondleiding](docs/screenshots/) en de [executive brief als PDF](application-kit/exports/executive-brief.pdf).

## Repository

| Pad | Inhoud |
|---|---|
| [`docs/`](docs/00-context/README.md) | de case, genummerd volgens het traject |
| [`data/programme.json`](data/programme.json) | het programmamodel: partners, eisen, budget, RAID, testen, go/no-go, KPI's |
| [`data/processes.json`](data/processes.json) | procesdefinities → BPMN 2.0 en SVG |
| [`data/sap-extract/mock-3/`](data/sap-extract/mock-3/) | voorbeeld van een gegenereerd SAP-extract (generale repetitie) |
| [`erpcase/`](erpcase/) | generator, kwaliteitsregels, mapping, afstemming, recall, programmaberekeningen, BPMN |
| [`scripts/build.py`](scripts/build.py) | bouwt alles; `--check` voor CI |
| [`tests/`](tests/) | testen |
| [`site/`](site/) | GitHub Pages: landingspagina, control room, executive brief, deck |
| [`application-kit/`](application-kit/README.md) | de case in 90 seconden, 2, 5 en 10 minuten |

## Bronnen, data en licenties

Alle data is gegenereerd of zelf opgesteld; geen echte bedrijfs- of persoonsgegevens. Bronnen voor Business Central, SAP-onderhoud, e-facturatie en traceerbaarheid: [context § data en bronnen](docs/00-context/README.md#data-en-bronnen). Geen externe bibliotheken: Python-stdlib en vanilla JavaScript. Code onder MIT, documentatie, diagrammen en data onder CC BY 4.0 ([LICENSE](LICENSE)).

## Beperkingen en aannames

- Er draait niets in een echte Business Central-omgeving. De migratie maakt records met Business Central-veldnamen, stemt af en traceert, maar laadt niets.
- De SAP-data is gegenereerd, met bewust ingebouwde fouten; echte SAP-data is rommeliger.
- Partners A, B en C, het budget, de defects, de hypercare en de KPI's zijn illustratief. Geen echt contract, geen echte stuurgroep.
- Wat de case niet toont: Business Central zelf inrichten of uitbreiden. Daarvoor is er een aparte case over de partnerkant: [business-central-implementation-case](https://github.com/phlppgdfry/business-central-implementation-case).
