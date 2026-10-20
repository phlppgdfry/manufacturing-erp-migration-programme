# Datamigratie: wat gaat mee, wie beslist, hoe weten we dat het klopt

> **Wat dit is:** de migratiestrategie, het verloop van de vier proefmigraties en het verhaal van de halffabricaatlots. **Voor wie:** data-eigenaars, controller, QA, partner. **Vorige:** [fit-gap](../04-fit-gap/README.md) · **Volgende:** [testen](../06-testen/README.md).

**Detail:** [mapping SAP → Business Central](mapping.md) · [datakwaliteit per proefmigratie](datakwaliteit.md) · [afstemming](afstemming.md) · [cutover-draaiboek](cutover.md) · code: [`erpcase/`](../../erpcase/)

## Wat gaat mee en wat niet

| Gaat mee | Gaat niet mee | Waarom |
|---|---|---|
| Actieve klanten, leveranciers, artikels | Artikels gemarkeerd voor verwijdering (312) | wat niemand meer gebruikt, veroorzaakt alleen fouten |
| Recepturen (productiestuklijsten) en routings | Oude versies van recepturen | historiek in het archief |
| Lots in voorraad met lotnummer, vervaldatum, blokkering | Verbruikte en geleverde lots | genealogie in het archief, lotnummers ongewijzigd ([ADR-008](../adr/adr-008-lotnummers-behouden.md)) |
| Openstaande klant- en leveranciersposten per document | Betaalde posten, oude facturen | archief; de bewaarplicht is tien jaar |
| Grootboeksaldi op de migratiedatum (+ saldi per maand van het lopende boekjaar) | Boekingen uit SAP | archief ([ADR-003](../adr/adr-003-geen-historiek-wel-archief.md)) |
| Openstaande verkoop- en aankooporders | Afgesloten orders | Power BI leest archief en Business Central samen |

## Rollen

- **Data-eigenaar** (business): beslist hoe een record verbeterd wordt en tekent af. Per regel staat de eigenaar in [datakwaliteit](datakwaliteit.md).
- **Partner**: extractie, transformatie, laden, en de rapporten.
- **Projectmanager (ik)**: de regels, de opvolging per eigenaar, de afstemming organiseren en de resultaten naar de go/no-go brengen.
- **Controller en QA-manager**: tekenen de afstemming (financieel) en de mock recall (lots) af.

## De pijplijn

```text
SAP-extract (CSV per tabel)          erpcase/sap_extract.py — in deze case gegenereerd
   ↓
15 datakwaliteitsregels              erpcase/rules.py — blokkerend, waarschuwing of filter, met eigenaar
   ↓
Transformatie naar Business Central  erpcase/transform.py — posting groups, eenheden, lots met vervaldatum
   ↓
Afstemming                           voorraadwaarde, openstaande posten, grootboek
   ↓
Mock recall                          25 grondstoflots voorwaarts: elk afgeleid lot terug te vinden?
   ↓
Go/no-go-criteria G1–G4              erpcase/programme.py
```

Eén voorbeeldextract staat in de repo ([`data/sap-extract/mock-3/`](../../data/sap-extract/mock-3/)); de andere maakt `python3 scripts/build.py` opnieuw aan. Zelfde seed, zelfde data.

## Vier proefmigraties

| | Week | Doel | Blokkerende fouten | Voorraadverschil | Recall |
|---|---|---|---:|---:|---:|
| Proefmigratie 1 | W18 | volledigheid van extracten en mapping | <!--n:mock1.blocking-->417<!--/n--> | <!--n:mock1.stockDiffPct-->17,656%<!--/n--> | <!--n:mock1.recall-->76,5%<!--/n--> |
| Proefmigratie 2 | W21 | opschoning meten, eerste afstemming met finance | <!--n:mock2.blocking-->146<!--/n--> | <!--n:mock2.stockDiffPct-->4,783%<!--/n--> | <!--n:mock2.recall-->95,3%<!--/n--> |
| Proefmigratie 3 (generale repetitie) | W24 | volledig draaiboek op tijd, afstemming, mock recall | <!--n:mock3.blocking-->107<!--/n--> | <!--n:mock3.stockDiffPct-->2,131%<!--/n--> | <!--n:mock3.recall-->96,7%<!--/n--> |
| Proefmigratie 4 | W29 | herhaling na herstel van de bron | <!--n:mock4.blocking-->0<!--/n--> | <!--n:mock4.stockDiffPct-->0,011%<!--/n--> | <!--n:mock4.recall-->100,0%<!--/n--> |

## Het verhaal van de halffabricaatlots (DQ-10)

- **Proefmigratie 1:** <!--n:mock1.DQ-10-->214<!--/n--> lots in voorraad zonder vervaldatum, eindproducten en halffabricaten. QA berekent de vervaldatum opnieuw uit productiedatum en houdbaarheid en verbetert ze in SAP.
- **Proefmigratie 2:** nog <!--n:mock2.DQ-10-->104<!--/n-->, allemaal halffabricaten. Toegewezen aan QA, "op te lossen vóór proefmigratie 3".
- **Proefmigratie 3:** <!--n:mock3.DQ-10-->107<!--/n-->. **Meer** dan de vorige keer, en het zijn **andere** lots. Alle <!--n:mock3.DQ-10-->107<!--/n--> zijn halffabricaten uit Hal 2.

Daar viel het kwartje. QA had de oude lots wel verbeterd, maar een eigen SAP-transactie voor de ontvangst van halffabricaten in Hal 2 sloeg het veld vervaldatum over. Elke dag productie maakte nieuwe lots zonder vervaldatum. Opschonen zonder de bron te herstellen is dweilen met de kraan open.

Wat ik anders had moeten doen: bij proefmigratie 2 niet alleen het **aantal** volgen maar ook **welke** lots. Dezelfde telling met andere sleutels had al in W21 getoond dat het probleem nieuw aanwas. Sindsdien vergelijkt de rapportering per regel ook de sleutels tussen twee proefmigraties.

Het herstel (I-03): de ABAP-freelancer paste de transactie aan (zijn contract liep nog op afroep: R-02), QA herberekende de vervaldatum voor de bestaande lots met een steekproef van 20 lots op papier, en proefmigratie 4 bevestigde nul fouten. Kost en planning: [go/no-go-besluit](../08-go-live/go-no-go.md).

## Waarschuwingen die bewust bleven

- **DQ-08 receptuur buiten 95–115%** (<!--n:mock4.DQ-08-->4<!--/n--> in proefmigratie 4): vier soepconcentraten waarbij water verdampt. De technoloog bevestigde dat de recepturen kloppen.
- **DQ-12 vervallen lot niet geblokkeerd** (<!--n:mock4.DQ-12-->3<!--/n-->): worden geblokkeerd gemigreerd; QA beslist over vernietiging.
- **DQ-14 artikel zonder standaardprijs** (<!--n:mock4.DQ-14-->2<!--/n-->): in SAP op nul gewaardeerd; Business Central gebruikt de gemiddelde prijs. Verschil <!--n:mock4.fallback-->€551<!--/n-->, verklaard en afgetekend door de controller.
