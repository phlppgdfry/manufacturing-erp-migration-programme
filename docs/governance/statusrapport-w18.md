# Statusrapport stuurgroep — week 18

> **Wat dit is:** een voorbeeld van het rapport van één pagina dat de stuurgroep elke vier weken kreeg. **Terug naar:** [governance](README.md).

*Fictieve organisatie, illustratieve cijfers.*

**Algemeen: 🟠 oranje** — planning op schema, één risico op het kritieke pad.

| | Status | Toelichting |
|---|---|---|
| Planning | 🟢 | M3 (configuratie klaar) gehaald in W17; de week vertraging van de partnerkeuze is ingehaald |
| Budget | 🟢 | gefactureerd <!--n:budget.spentW18-->€368.300<!--/n-->; prognose binnen budget + reserve |
| Scope | 🟢 | 2 CR's goedgekeurd (€16.200), 1 afgewezen; CR-03 planbord ligt bij de stuurgroep (W19) |
| Kwaliteit | 🟠 | proefmigratie 1: <!--n:mock1.blocking-->417<!--/n--> blokkerende datafouten, waarvan <!--n:mock1.DQ-10-->214<!--/n--> lots zonder vervaldatum |
| Mensen | 🟠 | key users planning en productie onder druk in het soepseizoen; interim-vervanging loopt |

## Wat ik van de stuurgroep vraag

1. **Beslissing over CR-03** (grafisch planbord als extensie, €41.800, 38 dagen). Advies: afwijzen; het planningsvoorstel met Power BI-capaciteitsoverzicht een seizoen gebruiken en daarna een app evalueren.
2. **Steun voor de opschoning van lotgegevens.** QA heeft drie dagen nodig om de vervaldatum van de bestaande lots te herberekenen. Vraag aan de COO: twee QA-technici vrijmaken in W19–W20.

## Top-3 risico's

| | Risico | Score | Maatregel |
|---|---|---:|---|
| R-04 | Lotgegevens onvolledig (vervaldatum) | 15 | opschoning door QA vóór proefmigratie 2; regel DQ-10 bij elke proefmigratie |
| R-01 | Key users niet vrij in het soepseizoen | 16 | interim-vervanging (B7) |
| R-09 | Scope creep vanuit Z-objecten | 16 | ontwerpautoriteit; alles via CR |

## Volgende vier weken

SIT (W20) · proefmigratie 2 (W21) · UAT (W23) · start opleiding eindgebruikers (W22)

## Mijlpalen

M0 ✓ · M1 ✓ (+1 week) · M2 ✓ (+1 week) · M3 ✓ · M4 ✓ · M5 W21 · M6 W24 · go/no-go W25 · go-live W26
