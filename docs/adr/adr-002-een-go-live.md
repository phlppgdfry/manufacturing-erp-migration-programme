# ADR-002 — Eén go-live voor alle processen

**Status:** aanvaard (W2, DEC-01) · **Beslist door:** stuurgroep · **Terug naar:** [ADR's](README.md)

## Context

Een gefaseerde uitrol (eerst financiën, dan productie) lijkt minder riskant. In een voedingsbedrijf hangen voorraad, productie, kostprijs en traceerbaarheid aan elkaar: een lot wordt gemaakt, verbruikt, gewaardeerd en geleverd.

## Opties

1. **Gefaseerd per domein.** Twee systemen voor voorraad en kostprijs gedurende maanden, met een tijdelijke interface die niemand na het project wil onderhouden. Traceerbaarheid over twee systemen.
2. **Gefaseerd per hal.** Twee systemen voor dezelfde grondstoffen en hetzelfde koelhuis.
3. **Eén go-live**, goed voorbereid: vier proefmigraties, een generale repetitie, harde go/no-go-criteria en een terugvalplan tot de laatste call.

## Besluit

Optie 3.

## Gevolgen

- Het risico verschuift naar de voorbereiding: datakwaliteit, test en draaiboek. Dat is waar het budget en de aandacht naartoe gaan.
- Toen de halffabricaatlots in W25 niet klaar waren, was "dan die toch later" (optie B in het [go/no-go-voorstel](../08-go-live/go-no-go.md)) uitgesloten door dit besluit. Dat maakte de discussie korter.
