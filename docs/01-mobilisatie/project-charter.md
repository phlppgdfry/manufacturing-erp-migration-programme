# Programmacharter: SAP → Business Central

> **Wat dit is:** de afspraak tussen de stuurgroep en het programma over doel, scope, succes en spelregels. Getekend in W2. **Voor wie:** stuurgroep, proceseigenaars, partner. **Vorige:** [context](../00-context/README.md) · **Volgende:** [business case](business-case.md).

*Fictieve organisatie; alle cijfers zijn illustratieve aannames.*

## Doel in één zin

Vaerdal Foods draait vóór de start van het BBQ-seizoen op Microsoft Dynamics 365 Business Central, met minstens dezelfde traceerbaarheid als vandaag, zonder dat een retailer een levering mist, en met een ERP dat Vaerdal zelf kan beheren.

## Waarom

1. SAP ECC 6.0 verliest zijn standaardonderhoud; de enige SAP-ontwikkelaar stopt; hosting loopt af.
2. Planning, traceerbaarheid en kwaliteitsvrijgave draaien naast het ERP (Excel, papier, mail). Een recall-oefening duurt <!--n:kpi.K2.baseline-->220<!--/n--> minuten.
3. De maandafsluiting duurt <!--n:kpi.K1.baseline-->9<!--/n--> werkdagen; 7,5% van de EDI-orders wordt manueel gecorrigeerd.

## Scope

| In scope | Buiten scope |
|---|---|
| Financiën (grootboek, btw BE/NL/FR, Peppol, CODA/SEPA, vaste activa, kostprijs) | Loonadministratie (blijft bij het sociaal secretariaat) |
| Verkoop incl. EDI met zes retailers en Peppol | CRM (blijft) |
| Aankoop en ontvangst met lots | Labo-informatiesysteem (fase 2, KW-05) |
| Productie: recepturen, routings, productieorders, planningsvoorstel | Koppeling controleweegschalen (fase 2, ADR-007) |
| Kwaliteit: lotblokkering, vrijgave, FEFO, traceren, allergenen | Elektronisch batchrecord (fase 2) |
| Voorraad: twee hallen, magazijn, extern koelhuis | Migratie van SAP-historiek (archief, ADR-003) |
| Datamigratie, test, opleiding, cutover, hypercare | Nieuwe processen die niets met de ERP-wissel te maken hebben |

**Eén go-live voor alle processen** ([ADR-002](../adr/adr-002-een-go-live.md)): voorraad, productie en financiën in twee systemen tegelijk is in een voedingsbedrijf geen optie.

## Succescriteria (gemeten drie maanden na go-live)

| KPI | Nu | Doel | Eigenaar |
|---|---|---|---|
| Maandafsluiting | <!--n:kpi.K1.baseline-->9<!--/n--> werkdagen | <!--n:kpi.K1.target-->5<!--/n--> | CFO |
| Mock recall grondstof → klant | <!--n:kpi.K2.baseline-->220<!--/n--> minuten | <!--n:kpi.K2.target-->60<!--/n--> | QA-manager |
| Weekplanning opstellen | <!--n:kpi.K3.baseline-->11<!--/n--> uur | <!--n:kpi.K3.target-->4<!--/n--> | COO |
| Manueel gecorrigeerde EDI-orders | <!--n:kpi.K4.baseline-->7,5<!--/n-->% | <!--n:kpi.K4.target-->2<!--/n-->% | Teamleider klantendienst |
| Voorraadnauwkeurigheid | <!--n:kpi.K5.baseline-->94,1<!--/n-->% | <!--n:kpi.K5.target-->98<!--/n-->% | Magazijnverantwoordelijke |
| Jaarlijkse runkosten ERP | €<!--n:kpi.K6.baseline-->286<!--/n-->k | €<!--n:kpi.K6.target-->168<!--/n-->k | IT Manager |

Plus twee voorwaarden die geen KPI zijn maar wel harde grenzen: **geen gemiste levering aan een retailer door de systeemwissel** en **een geslaagde BRCGS-audit in mei**.

## Budget en beslisrechten

- Programmabudget <!--n:budget.subtotal-->€753.000<!--/n--> + <!--n:budget.contingency-->€112.950<!--/n--> reserve (15%) = <!--n:budget.total-->€865.950<!--/n-->. Interne loonkost zit er niet in. Details: [business case](business-case.md).
- Uitgaven uit de reserve boven <!--n:budget.threshold-->€25.000<!--/n--> per beslissing: stuurgroep. Daaronder: IT Manager, op voorstel van de projectmanager.
- Scopewijzigingen: altijd via change request ([register](../governance/change-requests.md)).

## Organisatie

Zie [governance en RACI](governance.md). Kort: stuurgroep elke vier weken (CEO, CFO, COO, IT Manager, engagement manager van de partner), projectteam wekelijks, ontwerpautoriteit voor elke afwijking van de standaard.

## Spelregels

1. **Standaard eerst.** Elke afwijking van de standaard krijgt een eigenaar die de meerkost verdedigt ([ADR-001](../adr/adr-001-standaard-eerst.md)).
2. **Wie de data bezit, schoont ze op.** IT en partner leveren de controles; de business beslist en verbetert.
3. **Go/no-go-criteria liggen vast vóór de resultaten er zijn** (W16) en worden op de dag zelf niet versoepeld.
4. **Slecht nieuws reist snel.** Een risico met score ≥ 12 staat binnen een week op de agenda van de stuurgroep.
5. **Key users testen hun eigen werk** met hun eigen data, niet met demodata.

## Mijlpalen (plan bij de start)

| Mijlpaal | Week |
|---|---|
| Partner gekozen en contract getekend | W6 |
| Ontwerp afgetekend | W12 |
| Configuratie en extensies klaar | W17 |
| Proefmigraties 1–3 | W18, W21, W24 |
| Go/no-go | W25 |
| Go-live | W26 (1 maart, tussen soep- en BBQ-seizoen: [ADR-004](../adr/adr-004-go-live-tussen-de-seizoenen.md)) |
| Einde hypercare | W32 |

Wat er echt gebeurde: [planning, plan vs werkelijk](planning.md).
