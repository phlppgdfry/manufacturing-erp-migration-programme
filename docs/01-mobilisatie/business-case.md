# Business case: drie opties naast elkaar

> **Wat dit is:** de afweging die de raad van bestuur maakte vóór de start, opnieuw opgezet zodat het programma weet waarop het later wordt afgerekend. **Voor wie:** CFO, stuurgroep. **Vorige:** [charter](project-charter.md) · **Volgende:** [governance](governance.md).

*Illustratieve aannames — geen echte bedrijfsgegevens. Bedragen afgerond.*

## De opties

| | A. SAP ECC houden tot 2030 | B. Naar SAP S/4HANA | C. Naar Business Central |
|---|---|---|---|
| Wat | verlengd onderhoud kopen, hosting verlengen, freelancer houden | conversie of herimplementatie met een SAP-partner | herimplementatie met een Business Central-partner |
| Eenmalig | ±€150k (hosting-migratie, contracten) | €2,4 – 3,1 miljoen (offerte) | <!--n:budget.total-->€865.950<!--/n--> incl. reserve |
| Runkost per jaar | ±€310k (onderhoud stijgt, hosting, ABAP) | ±€360k | <!--n:kpi.K6.target-->168<!--/n-->k doel |
| Wat lost het op | uitstel | alles, maar groot voor 58 gebruikers | planning, traceerbaarheid, vrijgave, EDI in één systeem |
| Grootste risico | in 2030 opnieuw voor dezelfde keuze, met minder SAP-kennis in de markt | budget en doorlooptijd | productie-eisen die de standaard niet dekt (fit-gap) |

## Waarom C

1. **Omvang past.** Business Central is gemaakt voor bedrijven van deze grootte; S/4HANA is dat ook, maar met een implementatie- en beheerkost die bij een veel grotere organisatie past.
2. **De kernvraag is beantwoordbaar vóór het contract.** Een fit-gap op de productie- en kwaliteitseisen ([register](../04-fit-gap/fit-gap.md)) toont dat <!--n:fg.stdConfPct-->74%<!--/n--> standaard of configuratie is. De rest is een app, een procesaanpassing of één van twee kleine extensies.
3. **Runkosten dalen** van €<!--n:kpi.K6.baseline-->286<!--/n-->k naar een doel van €<!--n:kpi.K6.target-->168<!--/n-->k per jaar: geen hosting, geen ABAP, SaaS-licenties.
4. **Optie A koopt alleen tijd** en maakt het probleem groter: in 2030 is er minder SAP ECC-kennis beschikbaar en is de data vijf jaar ouder.

## Vijf jaar naast elkaar (illustratief)

| | A | B | C |
|---|---:|---:|---:|
| Eenmalig | 150 | 2.750 | 866 |
| 5 × runkost | 1.550 | 1.800 | 840 |
| **Totaal 5 jaar (k€)** | **1.700** | **4.550** | **1.706** |

Over vijf jaar kosten A en C ongeveer evenveel; na vijf jaar zit Vaerdal bij A opnieuw voor de keuze, bij C niet. Dat is het eigenlijke argument, niet het bedrag.

## Baten die niet in euro's staan

- Een recall in minder dan een uur in plaats van een halve dag: dat is wat een auditor en een retailer willen zien.
- Minder afhankelijkheid van één persoon: de ABAP-freelancer, de planner met het Excel-bestand.
- Eén bron voor kostprijs en marge per retailer.

## Waarop het programma wordt afgerekend

De KPI's uit het [charter](project-charter.md#succescriteria-gemeten-drie-maanden-na-go-live), gemeten in de [batenreview](../09-baten/README.md), en het budget: eindprognose <!--n:budget.eac-->€842.400<!--/n--> tegen <!--n:budget.total-->€865.950<!--/n--> toegekend ([budgetopvolging](../governance/README.md#budget)).

## Wat deze business case niet doet

- Geen netto contante waarde: de beslissing hing niet aan een rentevoet maar aan het einde van het SAP-onderhoud.
- Geen bandbreedte per aanname; voor het programma was het verschil B ↔ A/C groot genoeg om niet te verfijnen.
