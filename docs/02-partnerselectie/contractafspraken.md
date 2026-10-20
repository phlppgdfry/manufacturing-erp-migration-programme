# Contractafspraken: wie doet wat, en wanneer is iets af

> **Wat dit is:** de taakverdeling tussen Vaerdal en de partner, de mijlpalen met hun acceptatiecriteria en betaling, en hoe wijzigingen lopen. **Voor wie:** IT Manager, CFO, partner. **Terug naar:** [partnerselectie](README.md).

*Hoe ik het zou afspreken; geen juridisch advies.*

## Taakverdeling

| Onderwerp | Partner | Vaerdal |
|---|---|---|
| Methode, planning van de bouw | levert en bewaakt | keurt goed, bewaakt het geheel |
| Workshops | levert de Business Central-kennis | levert proceseigenaars en key users, leidt de discussie over het eigen proces |
| Fit-gap en oplossingsontwerp | schrijft | tekent af per domein |
| Configuratie, extensies, apps | doet het | test en tekent af |
| Datamigratie: extractie, transformatie, laden | doet het | — |
| Datamigratie: opschonen en afstemmen | levert rapporten | **doet het** (data-eigenaars), tekent af |
| Integraties (EDI, labels, koelhuis, Peppol) | coördineert de connectoren in Business Central | beheert de contracten met de derde partijen |
| Testscenario's | levert sjablonen | schrijft en voert uit |
| Opleiding | traint key users | key users trainen eindgebruikers |
| Cutover | voert technische stappen uit | leidt het draaiboek, beslist |
| Hypercare | tweede lijn | eerste lijn (key users) |

Datakwaliteit ligt bewust bij Vaerdal. Een partner die data "opschoont", beslist zonder het te weten over klanten, recepturen en lots. Dat is niet zijn rol.

## Mijlpalen, acceptatie en betaling (vaste prijs kernscope €412.000)

| Mijlpaal | Betaling | Acceptatiecriteria (vooraf uitgeschreven) | Wie tekent af |
|---|---:|---|---|
| Ontwerp afgetekend | 20% | fit-gap per domein afgetekend door de proceseigenaar; elke extensie goedgekeurd door de stuurgroep; oplossingsontwerp verwijst naar elke fit-gap-regel | IT Manager |
| Configuratie klaar (CRP2) | 20% | alle UAT-scenario's één keer doorlopen door de key users; geen open defect van ernst 1 | IT Manager |
| SIT geslaagd | 25% | alle integraties end-to-end met echte berichten; afstemming proefmigratie 2 opgeleverd | IT Manager |
| Go-live | 25% | positief go/no-go-besluit van de stuurgroep | Stuurgroep |
| Einde hypercare | 10% | exitcriteria hypercare gehaald; overdracht naar support getekend | IT Manager |

Van elke factuur wordt 10% ingehouden tot het einde van de hypercare.

## Change requests

1. Wie een wijziging wil, vult een CR in: wat, waarom, wat als we het niet doen.
2. De partner levert binnen vijf werkdagen een impactanalyse: dagen, kost, planning, risico.
3. De projectmanager zet er een advies bij. Tot <!--n:budget.threshold-->€25.000<!--/n--> beslist de IT Manager, daarboven de stuurgroep. Een extensie gaat altijd naar de stuurgroep.
4. Niets wordt gebouwd zonder getekende CR.

[Register van de change requests](../governance/change-requests.md)

## Benoemd team

De lead consultant en de migratieconsultant staan bij naam in het contract. Vervanging alleen met akkoord van Vaerdal, met twee weken overlap en zonder meerkost. Beschikbaarheid in uren per week staat in de bijlage van het contract en is een vast punt op het maandelijkse contractoverleg.
