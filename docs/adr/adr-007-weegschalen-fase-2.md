# ADR-007 — Koppeling controleweegschalen naar fase 2

**Status:** aanvaard (W12, DEC-07) · **Beslist door:** COO · **Terug naar:** [ADR's](README.md)

## Context

De controleweegschalen aan het einde van elke lijn wegen elke pot of fles. Die gewichten automatisch als output in Business Central boeken zou de operator een stap besparen en de outputboeking nauwkeuriger maken.

## Opties

1. **In fase 1 koppelen.** Vraagt een integratie met vier types weegschalen van twee leveranciers, op de vloer, met netwerk in de koelcel. Een nieuwe afhankelijkheid op het kritieke pad.
2. **Fase 2.** In fase 1 boekt de operator de output op een terminal aan het einde van de ploeg, met het lotnummer uit Business Central.

## Besluit

Optie 2.

## Gevolgen

- 25 minuten per ploeg manuele outputboeking (gemeten na de go-live). Eerste item op de [roadmap](../10-it-roadmap/README.md), Q+1.
- Een fout bij de outputboeking (DEF-07, uitval afgerond per eenheid) werd in de UAT gevonden, niet in productie.
