# Partnerselectie: van zes kandidaten naar één contract

> **Wat dit is:** hoe Vaerdal de implementatiepartner koos: criteria en gewichten vóór de offertes, dezelfde demo voor elke partner, een gevoeligheidsanalyse, en wat er in het contract kwam. **Voor wie:** stuurgroep, IT Manager, aankoop. **Vorige:** [planning](../01-mobilisatie/planning.md) · **Volgende:** [processen](../03-processen/README.md).

*Partners A, B en C zijn fictief. Scores en prijzen zijn illustratief.*

## Waarom dit belangrijk is

Bij een ERP-wissel koop je geen software maar een team voor negen maanden. De meeste ERP-problemen die later "een softwareprobleem" heten, beginnen bij een partner die het proces niet kent, een team dat halverwege wisselt of een contract waarin niemand de acceptatie heeft uitgeschreven. De selectie is dus mijn eerste kwaliteitsbewaking, niet een aankoopformaliteit.

## Verloop

| Week | Stap | Resultaat |
|---|---|---|
| W1 | Longlist uit eigen netwerk, Microsoft-partnerzoeker, referenties van andere voedingsbedrijven | 6 partners |
| W2 | Eisen in één document: scope, processen, volumes, de vijf moeilijkste eisen (lots, houdbaarheid per klant, recall, EDI, planning) | RFP |
| W2 | **Criteria en gewichten vastgelegd door de stuurgroep, vóór er één offerte binnen was** | tabel hieronder |
| W3 | Schriftelijke antwoorden; twee partners zonder productiereferentie vallen af, één trekt zich terug | shortlist van 3 |
| W4 | Gescripte demo van drie uur per partner, op ons script en met onze artikelen ([demoscript](demoscript.md)) | scores C4 |
| W5 | Twee referentiebezoeken per partner bij een voedingsproducent; gesprek met de benoemde consultants | scores C1, C3 |
| W6 | Scoring, gevoeligheidsanalyse, onderhandeling | keuze Partner A |
| W7 | Contract getekend (één week later dan gepland: I-01) | M1 |

## Criteria en gewichten

| | Criterium | Gewicht | Hoe gemeten |
|---|---|---:|---|
| C1 | Referenties in voedingsproductie | 20% | twee referentiebezoeken; vragen naar traceerbaarheid en lotbeheer |
| C2 | Aanpak: standaard eerst, methode | 15% | "welke maatwerkwensen zou u ons afraden?" |
| C3 | Benoemd team | 15% | cv's, beschikbaarheid, Nederlandstalig, wie blijft na de go-live |
| C4 | Demo op ons script | 20% | zelfde script voor iedereen ([demoscript](demoscript.md)) |
| C5 | Aanpak datamigratie uit SAP | 10% | ervaring met SAP-extracten, aantal proefmigraties, wie stemt af |
| C6 | Prijs en kosten over drie jaar | 15% | op dezelfde scope genormaliseerd |
| C7 | Ondersteuning na go-live | 5% | hypercare, SLA, wie neemt de telefoon op |

Prijs weegt 15%, niet 40%. Dat is een bewuste keuze van de stuurgroep: het verschil tussen de goedkoopste en de duurste offerte was kleiner dan de kost van één maand vertraging in een seizoensbedrijf.

## Scores (1–5)

| | C1 | C2 | C3 | C4 | C5 | C6 | C7 | **Gewogen** | Implementatie | 3 jaar |
|---|---|---|---|---|---|---|---|---:|---:|---:|
| Partner A — regionaal, sterk in productie | 4 | 4 | 4 | 4 | 3 | 3 | 4 | **<!--n:partner.A.score-->3,75<!--/n-->** | <!--n:partner.A.offer-->€476.000<!--/n--> | <!--n:partner.A.tco-->€612.000<!--/n--> |
| Partner B — groot, eigen food-app | 5 | 3 | 3 | 4 | 4 | 2 | 3 | <!--n:partner.B.score-->3,55<!--/n--> | <!--n:partner.B.offer-->€558.000<!--/n--> | <!--n:partner.B.tco-->€724.000<!--/n--> |
| Partner C — laagste prijs, deels offshore | 2 | 3 | 2 | 3 | 3 | 5 | 2 | <!--n:partner.C.score-->2,90<!--/n--> | <!--n:partner.C.offer-->€371.000<!--/n--> | <!--n:partner.C.tco-->€498.000<!--/n--> |

## Gevoeligheid: hoe stevig is de keuze?

Ik heb per criterium het gewicht van 0 tot 100% laten variëren (de andere gewichten schalen mee) en gekeken wanneer een andere partner bovenaan komt. Berekend in [`erpcase/programme.py`](../../erpcase/programme.py); interactief in de [control room](../../site/room/index.html#partners).

| Criterium | Huidig | Partner A blijft eerste tot | Daarna wint |
|---|---:|---:|---|
| C1 Referenties voeding | 20% | <!--n:sens.C1.to-->33%<!--/n--> | Partner B |
| C5 Datamigratie | 10% | <!--n:sens.C5.to-->25%<!--/n--> | Partner B |
| C6 Prijs | 15% | <!--n:sens.C6.to-->40%<!--/n--> | Partner C |
| C2, C3, C4, C7 | | bij elk gewicht | — |

**Wat ik de stuurgroep zei:** de keuze is stevig. Partner C wint pas als prijs meer dan 40% weegt, en dan kies je bewust voor het team dat het slechtst scoort op referenties en demo. Partner B wint als je referenties zwaarder laat wegen dan een derde. Dat is verdedigbaar, maar B had het zwakste benoemde team en de hoogste prijs. Het verschil tussen A en B is klein, dus het contract moet afdekken wat B beter deed: SAP-migratie-ervaring (zie de regie-afspraak voor de migratie hieronder).

## Wat in het contract kwam

1. Vaste prijs voor de kernscope (€412.000), betaald per mijlpaal **na aftekening van vooraf uitgeschreven acceptatiecriteria**.
2. Datamigratie in regie met een plafond van €64.000 en een wekelijks verbruiksoverzicht. Vaste prijs voor migratie zou de partner aanzetten om weinig proefmigraties te doen.
3. 10% van elke mijlpaalfactuur wordt ingehouden tot het einde van de hypercare.
4. De lead consultant en de migratieconsultant staan bij naam in het contract; vervanging alleen met akkoord en twee weken overlap.
5. Wijzigingen alleen via een change request met impactanalyse binnen vijf werkdagen.

Waarom deze vorm en geen volledige regie of volledige vaste prijs: [ADR-006](../adr/adr-006-contractvorm.md). Verdeling van taken en de acceptatiecriteria per mijlpaal: [contractafspraken](contractafspraken.md).

## Achteraf

De keuze hield stand; de migratie-afspraak in regie bleek nodig: het plafond werd met €14.000 overschreden door de extra opschoningsronde voor lotgegevens, en de vierde proefmigratie kostte nog eens €9.500 ([budget](../governance/README.md#budget)). Met een vaste prijs voor migratie was er waarschijnlijk discussie geweest over wie die vierde ronde betaalt, op het moment dat er geen tijd voor discussie was.
