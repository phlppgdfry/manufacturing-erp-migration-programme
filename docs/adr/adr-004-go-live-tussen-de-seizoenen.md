# ADR-004 — Go-live tussen soep- en BBQ-seizoen

**Status:** aanvaard (W2) · later verschoven van 1 maart naar 1 april (DEC-10) · **Beslist door:** stuurgroep · **Terug naar:** [ADR's](README.md)

## Context

Hal 1 draait op volle kracht van oktober tot februari, Hal 2 bouwt vanaf april voorraad op voor het BBQ-seizoen. Een go-live vraagt een productiestop van ongeveer 30 uur en een hypercare van vier tot zes weken.

## Opties

1. **1 januari** (begin boekjaar): midden in het soepseizoen. Uitgesloten door de COO.
2. **1 maart:** tussen de seizoenen, begin van een periode. Ontwerp en test vallen wel in het soepseizoen.
3. **1 september:** na het BBQ-seizoen, ruim tijd. Vijf maanden langer SAP, en het onderhoudscontract was al verlengd tot het voorjaar.

## Besluit

Optie 2, 1 maart. Begin van een periode, niet van het boekjaar: de saldi van januari en februari worden per maand overgezet.

## Gevolgen

- Interim-vervanging voor vier key users in het soepseizoen (B7, R-01).
- Toen de go-live vier weken opschoof (1 april), viel de hypercare in de start van het BBQ-seizoen (R-10). Daarom de maatregelen in het [go/no-go-voorstel](../08-go-live/go-no-go.md#mijn-voorstel-aan-de-stuurgroep-één-pagina). September bleef een optie, maar kostte vijf maanden SAP en waarschijnlijk het partnerteam.
