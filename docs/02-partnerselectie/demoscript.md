# Demoscript voor de partners (drie uur)

> **Wat dit is:** het script dat elke partner op de shortlist moest volgen, met onze artikelen en onze moeilijkste gevallen. **Voor wie:** de partners (vooraf toegestuurd) en het beoordelingspanel. **Terug naar:** [partnerselectie](README.md).

## Spelregels

- Elke partner krijgt dezelfde data een week vooraf: 10 artikelen (2 eindproducten, 2 halffabricaten, 4 grondstoffen, 2 verpakkingen), 2 recepturen, 3 klanten waarvan één retailer met een eis op resterende houdbaarheid.
- Geen slides na de eerste tien minuten. Wat niet getoond wordt, scoort 1.
- "Dat kan met maatwerk" mag, maar dan met een inschatting in dagen en de vraag of zij het zouden afraden.
- Panel: COO, QA-manager, controller, hoofd planning, teamleider klantendienst, IT Manager, projectmanager. Iedereen scoort zelf, daarna bespreken we de verschillen.

## Het script

| # | Wat de partner toont | Waar we op letten | Eis |
|---|---|---|---|
| 1 | EDI-order van retailer R1 komt binnen als verkooporder, met prijsafspraak en kredietcontrole | hoe gaat een fout in de order naar een mens? | VK-01, VK-04, VK-06 |
| 2 | Planningsvoorstel voor een week met die order erin; productie- en aankooporders aanmaken | kan de planner zien welke lijn overbelast is? | PR-03, AK-01 |
| 3 | Ontvangst van mosterdzaad met leverancierslot en vervaldatum | wordt de vervaldatum verplicht? | AK-03 |
| 4 | Productieorder voor saus: verbruik per lot, output met lot en berekende vervaldatum | waar komt de vervaldatum vandaan? | PR-05, PR-06 |
| 5 | Het nieuwe lot is geblokkeerd tot QA het vrijgeeft | standaard of maatwerk? | KW-01 |
| 6 | Picken voor R1, die minstens twee derde resterende houdbaarheid eist; het oudste lot voldoet niet | wat gebeurt er? (in de standaard: niets — eerlijk antwoord verwacht) | VK-05, KW-04 |
| 7 | Levering met SSCC-label en leverbericht | welke app, wie onderhoudt de mapping? | VK-02, VR-04 |
| 8 | **Recall:** de leverancier meldt dat het mosterdzaadlot uit stap 3 verontreinigd kan zijn. Toon alle afgeleide lots, de voorraad en de klanten. | hoe snel, hoeveel klikken, en wat met lots van vóór de go-live? | KW-02 |
| 9 | Kostprijsafwijking van de productieorder uit stap 4 | kan de controller het uitleggen zonder IT? | FIN-08 |
| 10 | Vraag van het panel: "welke drie van onze wensen zou u ons afraden, en waarom?" | durft de partner nee te zeggen? | C2 |

## Wat het script opleverde

- Partner C kon stap 8 alleen tonen voor lots die in de demo-omgeving gemaakt waren, en had geen antwoord voor lots van vóór de go-live. Dat werd later een ontwerpbeslissing: lotnummers ongewijzigd overnemen en de SAP-genealogie in het archief bewaren ([ADR-003](../adr/adr-003-geen-historiek-wel-archief.md), [ADR-008](../adr/adr-008-lotnummers-behouden.md)).
- Partner B toonde stap 6 met de eigen food-app; Partner A zei dat de standaard dit niet doet en stelde een kleine extensie voor (5 dagen). Dat werd VK-05.
- Op vraag 10 noemde Partner A het grafische planbord. Dat kwam later terug als CR-03 en werd afgewezen.
