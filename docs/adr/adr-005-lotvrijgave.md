# ADR-005 — Lotvrijgave met de standaardblokkering, geen kwaliteitsapp in fase 1

**Status:** aanvaard (W12, DEC-06) · **Beslist door:** QA-manager · **Terug naar:** [ADR's](README.md)

## Context

Vandaag geeft QA lots vrij via Excel en mail; het systeem weet niet of een lot vrij is. QA wil dat een lot niet gepickt kan worden voor het vrijgegeven is. Kwaliteitsapps uit AppSource doen dat en veel meer (inspectieplannen, laboresultaten, certificaten).

## Opties

1. **Kwaliteitsapp in fase 1.** Alles in één keer, maar een extra app om in te richten, te testen en op te leiden in een project dat al vol zit.
2. **Standaard:** elk nieuw lot krijgt bij de output automatisch *Geblokkeerd* in de lotnummerinformatie; QA haalt het vinkje weg na de analyse. Laboresultaten blijven in de Excel van QA.
3. **Extensie** die de vrijgave koppelt aan laboresultaten. Maatwerk voor iets waar apps voor bestaan.

## Besluit

Optie 2 voor de go-live; de kwaliteitsapp in Q+2 ([roadmap](../10-it-roadmap/README.md)).

## Gevolgen

- Het doel (een niet-vrijgegeven lot kan niet weg) is gehaald op dag één, met standaardfunctionaliteit.
- QA doet nog dubbel werk (Excel + vinkje). Aanvaard voor één seizoen.
