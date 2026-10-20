# Go/no-go: waarom we niet op 1 maart live gingen

> **Wat dit is:** de criteria, de uitkomst van twee go/no-go-momenten en het voorstel dat ik de stuurgroep deed. **Voor wie:** stuurgroep, iedereen die wil weten hoe een go-live-beslissing genomen wordt. **Vorige:** [verandering](../07-verandering/README.md) · **Volgende:** [hypercare](hypercare.md). **Alle metingen:** [go-no-go-resultaten.md](go-no-go-resultaten.md).

*Fictieve organisatie; alle cijfers zijn illustratief en komen uit het model van deze repo.*

## De regels, vastgelegd in W16

- Twaalf criteria, waarvan acht **hard** en vier **zacht**.
- **GO** als alle harde criteria slagen en ten hoogste twee zachte falen, elk met eigenaar en workaround.
- De stuurgroep legde criteria en drempels vast **in W16, vóór er resultaten waren**. Een hard criterium wordt op de dag zelf niet kwijtgescholden. Wie een drempel wil veranderen, doet dat met een voorstel dat los staat van de cijfers van de week.

Waarom zo streng: op de dag van een go/no-go is de druk om "ja" te zeggen enorm. Iedereen heeft maanden gewerkt, de partner heeft een team klaarstaan, de datum is gecommuniceerd. Criteria die je op voorhand vastlegt, beschermen de stuurgroep tegen die druk.

## Go/no-go 1 — week 25, voor 1 maart

**Uitkomst volgens de regels: <!--n:gng1.decision-->NO-GO<!--/n-->.** Harde criteria gefaald: <!--n:gng1.hardFail-->G1, G2, G3<!--/n-->. Zachte criteria gefaald: <!--n:gng1.softFail-->G8, G9<!--/n-->.

| | Criterium | Gemeten | |
|---|---|---|---|
| G1 | Mock recall volledig | <!--n:mock3.recall-->96,7%<!--/n--> | ✗ |
| G2 | Geen blokkerende datakwaliteitsfouten | <!--n:mock3.blocking-->107<!--/n--> | ✗ |
| G3 | Voorraadwaarde: verschil ≤ 0,1% | <!--n:mock3.stockDiffPct-->2,131%<!--/n--> | ✗ |
| G4–G7, G10–G12 | posten, defects, key users, draaiboek, terugval, support | in orde | ✓ |
| G8, G9 | eindgebruikers opgeleid (84%), EDI-partners getest (6/7) | zacht, met workaround | ✗ |

G1, G2 en G3 hebben **één oorzaak**: <!--n:mock3.DQ-10-->107<!--/n--> lots halffabricaat uit Hal 2 zonder vervaldatum ([het verhaal](../05-datamigratie/README.md#het-verhaal-van-de-halffabricaatlots-dq-10)). Zonder vervaldatum laden ze niet (verplicht veld in de artikeltracering), dus ontbreken ze in de voorraad (G3, <!--n:mock3.excluded-->€106.717<!--/n--> aan voorraad), in de recall (G1) en als blokkerende fout (G2).

## Mijn voorstel aan de stuurgroep (één pagina)

**Vraag:** gaan we op 1 maart live?

**Advies: nee. Nieuwe datum 1 april, op voorwaarde dat de bron vóór W27 hersteld is.**

| Optie | Wat | Kost | Risico | Advies |
|---|---|---|---|---|
| A. Toch live op 1 maart, halffabricaten na de go-live handmatig invoeren | 107 lots met de hand inboeken in de eerste week | geen extra | een week waarin halffabricaten niet traceerbaar zijn; handmatige invoer onder hypercaredruk; BRCGS-audit in mei; harde criteria worden achteraf versoepeld | ✗ |
| B. Live op 1 maart zonder de halffabricaten, ze opgebruiken in SAP | 107 lots in SAP laten en eerst opgebruiken | geen extra | twee systemen voor voorraad en productie; precies wat ADR-002 uitsloot | ✗ |
| **C. Uitstel tot 1 april** | bron herstellen, vervaldatum herberekenen, proefmigratie 4, recall opnieuw | **<!--n:budget.delay-->€55.700<!--/n-->** uit de reserve | BBQ-seizoen start in april; hypercare valt in de voorraadopbouw (R-10) | **✓** |
| D. Uitstel tot september | na het BBQ-seizoen | ±€190.000 + vijf maanden langer SAP | partnerteam valt uiteen, motivatie, SAP-hosting | ✗ |

**Kost van optie C (<!--n:delay.weeks-->4<!--/n--> weken):**

| Post | Bedrag |
|---|---:|
| Interim-vervanging key users vier weken langer | €16.000 |
| Partnerteam in afgeslankte bezetting (de go-live-datum lag vast in het contract) | €22.400 |
| SAP-hosting één maand langer | €7.800 |
| Vierde proefmigratie en herhaalde mock recall | €9.500 |
| **Totaal** | **<!--n:budget.delay-->€55.700<!--/n-->** |

Na deze beslissing blijft er <!--n:budget.left-->€23.550<!--/n--> in de reserve. Boven <!--n:budget.threshold-->€25.000<!--/n--> beslist de stuurgroep; dat is hier het geval.

**Wat het uitstel ook oplost:** de opleiding van eindgebruikers (G8) en de EDI-certificering van R4 (G9) lopen af in dezelfde vier weken.

**Wat het niet oplost:** de hypercare valt nu in de start van het BBQ-seizoen. Maatregel: key users twee weken vrijgesteld na de go-live, partner on site in week 1 en 2, productieplanning voor april één week vooruit vastgelegd.

**Besluit van de stuurgroep (W25):** optie C. DEC-10 in de [beslissingenlog](../governance/decision-log.md).

## Go/no-go 2 — week 29, voor 1 april

**Uitkomst: <!--n:gng2.decision-->GO<!--/n-->.** Harde criteria gefaald: <!--n:gng2.hardFail-->geen<!--/n-->. Zachte criteria gefaald: <!--n:gng2.softFail-->geen<!--/n-->.

- Mock recall <!--n:mock4.recall-->100,0%<!--/n--> (<!--n:mock4.recallFound-->1.124<!--/n--> van <!--n:mock4.recallDerived-->1.124<!--/n-->), blokkerende fouten <!--n:mock4.blocking-->0<!--/n-->, voorraadverschil <!--n:mock4.stockDiffPct-->0,011%<!--/n--> (<!--n:mock4.fallback-->€551<!--/n-->, verklaard door DQ-14).
- Eindgebruikers 61/64 opgeleid, zeven van zeven EDI-partners getest, open defects van ernst 2: nul.

Live op 1 april; [hypercare](hypercare.md).

## Wat ik hiervan meeneem

1. **Een criterium dat je niet durft te laten falen, is geen criterium.** De recall op 100% zetten voelde in W16 overdreven. In W25 was het de reden dat niemand hoefde te discussiëren.
2. **Tel niet alleen fouten, kijk welke.** Hetzelfde aantal fouten met andere sleutels betekent een lek in de bron, niet trage opschoning.
3. **Reken het uitstel voor de stuurgroep uit.** "We zijn niet klaar" is een gevoel; "vier weken, €55.700, dit lossen we op en dit niet" is een beslissing.
