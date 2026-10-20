# ADR-001 — Standaard eerst; extensies alleen met akkoord van de stuurgroep

**Status:** aanvaard (W9, DEC-03) · **Beslist door:** stuurgroep · **Terug naar:** [ADR's](README.md)

## Context

Vaerdal heeft 146 eigen SAP-objecten. In de eerste twee workshops eindigde elke discussie met "dat konden we in SAP ook". Elke extensie in Business Central moet bij elke halfjaarlijkse update getest worden, door iemand die er dan nog is.

## Opties

1. **Elke SAP-functie terugbouwen.** Iedereen blij in de workshop, duur en traag, en we hebben over vijf jaar opnieuw een systeem dat niemand durft bij te werken.
2. **Alleen standaard, geen extensies.** Zuiver, maar twee eisen zijn wettelijk of contractueel en de standaard dekt ze niet (VK-05, KW-03).
3. **Standaard eerst, met een vaste volgorde en een harde grens.** Standaard → configuratie → app → procesaanpassing → extensie. Een extensie gaat altijd naar de stuurgroep, ongeacht het bedrag. Ten hoogste drie.

## Besluit

Optie 3. Elke extensie moet drie vragen overleven: is het wettelijk of contractueel nodig? lost een app of procesaanpassing het niet op? wie onderhoudt het?

## Gevolgen

- Twee extensies (VK-05, KW-03), samen 9 bouwdagen.
- Het grafische planbord (CR-03, €41.800) werd afgewezen. Dat kostte goodwill bij planning ([verandering](../07-verandering/README.md#scenario-het-excel-planbord-werkt-al-22-jaar)).
- De test [`tests/test_programme.py`](../../tests/test_programme.py) faalt als het register meer dan drie extensies bevat.

## Opnieuw bekijken

Na één BBQ-seizoen: is het planbord nog een probleem? Dan een app evalueren, geen extensie.
