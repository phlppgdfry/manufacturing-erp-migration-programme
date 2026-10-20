# Planning: plan en werkelijkheid

> **Wat dit is:** de fasen en mijlpalen, en waar het afweek. **Voor wie:** stuurgroep en projectteam. **Vorige:** [governance](governance.md) · **Volgende:** [partnerselectie](../02-partnerselectie/README.md).

## Fasen

```text
W1–W6    Mobilisatie en partnerselectie      charter · RFP · demo's · referenties · contract
W7–W13   Analyse en ontwerp                   6 workshops · Z-objecten · fit-gap · oplossingsontwerp
W14–W17  Configuratie en bouw                 CRP1 (W14) · extensies · integraties · CRP2 (W17)
W18–W24  Migratie en test                     proefmigratie 1–3 · SIT (W20) · UAT (W23) · opleiding
W25      Go/no-go 1                           → NO-GO
W26–W29  Correctie en proefmigratie 4         bron hersteld · data herberekend · recall herhaald
W29      Go/no-go 2                           → GO
W30      Go-live (1 april)
W30–W36  Hypercare                            6 weken
W43      Batenreview                          3 maanden na go-live
```

Het ontwerp en de testen vallen in het soepseizoen (oktober – februari). Dat is geen planningsfout maar een gevolg van de go-live tussen de seizoenen ([ADR-004](../adr/adr-004-go-live-tussen-de-seizoenen.md)); de prijs is interim-vervanging voor vier key users (R-01, budgetlijn B7).

## Mijlpalen

| Mijlpaal | Plan | Werkelijk | Afwijking | Waarom |
|---|---|---|---|---|
| M0 Programmastart, charter | W1 | W1 | — | |
| M1 Partner gekozen, contract | W6 | W7 | +1 | referentiebezoek bij Partner B verschoven (I-01); twee ontwerpworkshops samengevoegd om het in te halen |
| M2 Ontwerp afgetekend | W12 | W13 | +1 | doorgeschoven van M1 |
| M3 Configuratie en extensies klaar | W17 | W17 | — | ingehaald |
| M4 Proefmigratie 1 | W18 | W18 | — | |
| M5 SIT en proefmigratie 2 | W21 | W21 | — | |
| M6 UAT en generale repetitie | W24 | W24 | — | |
| M7 Go/no-go 1 | W25 | W25 | — | uitkomst NO-GO |
| M8 Proefmigratie 4 en go/no-go 2 | — | W29 | nieuw | gevolg van het no-go |
| M9 **Go-live** | **W26 (1 maart)** | **W30 (1 april)** | **+4** | [go/no-go-besluit](../08-go-live/go-no-go.md) |
| M10 Einde hypercare | W32 | W36 | +4 | |
| M11 Batenreview | W39 | W43 | +4 | |

## Kritiek pad

Lots en houdbaarheid → mock recall → go/no-go. Alles wat de lotgegevens raakt (datakwaliteit DQ-10 tot DQ-12, output met vervaldatum, FEFO, de extensie voor minimale resterende houdbaarheid) zat op het kritieke pad. Daarom liepen die regels vanaf proefmigratie 1 mee, en daarom was de recall een hard criterium.

Het tweede kritieke pad: **EDI-certificering per retailer** (vier tot zes weken per retailer, R-05). Gestart in W14, parallel aan de bouw. Eén retailer (R4) was in W25 nog niet rond; daar ligt een terugval klaar via het webportaal van de retailer.
