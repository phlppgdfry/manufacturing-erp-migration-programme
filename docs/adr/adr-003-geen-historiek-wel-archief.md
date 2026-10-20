# ADR-003 — Geen SAP-historiek migreren; read-only archief voor tien jaar

**Status:** aanvaard (W10, DEC-04) · **Beslist door:** CFO · **Terug naar:** [ADR's](README.md)

## Context

Finance en verkoop wilden "alles meenemen". SAP bevat zeventien jaar boekingen, orders en lots. De boekhoudkundige bewaarplicht in België is tien jaar. Traceerbaarheid vraagt dat lots van vóór de go-live terug te vinden zijn.

## Opties

1. **Alle historiek migreren.** Duur, traag, en historische data past slecht in de nieuwe inrichting (andere rekeningen, dimensies, posting groups). Elke afstemming wordt groter.
2. **Twee jaar historiek migreren.** Halve oplossing: voor oudere vragen blijft toch een archief nodig.
3. **Geen historiek migreren**, wel openstaande posten, saldi en voorraad; alle SAP-data in een read-only archief dat tien jaar raadpleegbaar is (documenten, boekingen, batch-genealogie).

## Besluit

Optie 3. Budgetlijn B6 (€36.000). SAP-licentie en hosting stoppen na de go-live.

## Gevolgen

- Power BI leest archief en Business Central samen voor vergelijkingen over jaren heen (CR-04 voor een rapport in Business Central werd daarom afgewezen).
- De recall moet over twee bronnen kunnen: daarom [ADR-008](adr-008-lotnummers-behouden.md).
