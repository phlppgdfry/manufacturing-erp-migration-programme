# Go/no-go: resultaten per criterium

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Terug naar [het besluit](go-no-go.md). De criteria en drempels zijn in W16 door de stuurgroep vastgelegd, vóór er resultaten waren. Een hard criterium kan op de dag zelf niet worden kwijtgescholden. Ten hoogste twee zachte criteria mogen falen, elk met een eigenaar en een aanvaarde workaround.

## GNG-1 — week 25, voor go-live op 1 maart (mock-3)

**Uitkomst: NO-GO** · harde criteria gefaald: G1, G2, G3 · zachte criteria gefaald: G8, G9

|  | Criterium | Soort | Drempel | Gemeten |  |
|---|---|---|---|---|---|
| G1 | Mock recall volledig: elk afgeleid lot in voorraad terug te vinden met lotnummer en vervaldatum | hard | 100% | 96,7% (1.041 van 1.077) | ✗ |
| G2 | Geen blokkerende datakwaliteitsfouten in de migratiescope | hard | 0 | 107 | ✗ |
| G3 | Voorraadwaarde Business Central vs SAP: verschil ten hoogste 0,1% | hard | ≤ 0,1% | 2,131% | ✗ |
| G4 | Openstaande klant- en leveranciersposten sluiten tot op de cent | hard | €0,00 | €0,00 | ✓ |
| G5 | Geen open defect van ernst 1 | hard | 0 | 0 | ✓ |
| G6 | Ten hoogste twee open defects van ernst 2, elk met een aanvaarde workaround | zacht | ≤ 2 | 2 | ✓ |
| G7 | Key users opgeleid | hard | 100% | 14/14 | ✓ |
| G8 | Eindgebruikers opgeleid | zacht | ≥ 90% | 54/64 (84%) | ✗ |
| G9 | Alle EDI-partners end-to-end getest | zacht | 7 / 7 | 6 / 7 | ✗ |
| G10 | Draaiboek in de generale repetitie binnen het cutovervenster (≤ 40 u) | hard | ≤ 40 u | 37 u | ✓ |
| G11 | Terugvalplan getest en afgetekend | hard | ja | ja | ✓ |
| G12 | Hypercareteam, ticketing en escalatie klaar | zacht | ja | ja | ✓ |

## GNG-2 — week 29, voor go-live op 1 april (mock-4)

**Uitkomst: GO** · harde criteria gefaald: geen · zachte criteria gefaald: geen

|  | Criterium | Soort | Drempel | Gemeten |  |
|---|---|---|---|---|---|
| G1 | Mock recall volledig: elk afgeleid lot in voorraad terug te vinden met lotnummer en vervaldatum | hard | 100% | 100,0% (1.124 van 1.124) | ✓ |
| G2 | Geen blokkerende datakwaliteitsfouten in de migratiescope | hard | 0 | 0 | ✓ |
| G3 | Voorraadwaarde Business Central vs SAP: verschil ten hoogste 0,1% | hard | ≤ 0,1% | 0,011% | ✓ |
| G4 | Openstaande klant- en leveranciersposten sluiten tot op de cent | hard | €0,00 | €0,00 | ✓ |
| G5 | Geen open defect van ernst 1 | hard | 0 | 0 | ✓ |
| G6 | Ten hoogste twee open defects van ernst 2, elk met een aanvaarde workaround | zacht | ≤ 2 | 0 | ✓ |
| G7 | Key users opgeleid | hard | 100% | 14/14 | ✓ |
| G8 | Eindgebruikers opgeleid | zacht | ≥ 90% | 61/64 (95%) | ✓ |
| G9 | Alle EDI-partners end-to-end getest | zacht | 7 / 7 | 7 / 7 | ✓ |
| G10 | Draaiboek in de generale repetitie binnen het cutovervenster (≤ 40 u) | hard | ≤ 40 u | 34 u | ✓ |
| G11 | Terugvalplan getest en afgetekend | hard | ja | ja | ✓ |
| G12 | Hypercareteam, ticketing en escalatie klaar | zacht | ja | ja | ✓ |
