# Hypercare: de eerste zes weken

> **Wat dit is:** hoe de eerste weken na de go-live georganiseerd waren, wat er binnenkwam en wanneer we stopten. **Voor wie:** IT Manager, key users, partner. **Vorige:** [go/no-go](go-no-go.md) · **Volgende:** [batenreview](../09-baten/README.md).

*Ticketaantallen zijn gesimuleerd.*

## Organisatie

- **Eerste lijn:** key users op de vloer, in week 1 en 2 vrijgesteld van hun gewone werk.
- **Tweede lijn:** partner, on site in week 1 en 2, daarna op afstand.
- **Dagelijks om 9u en 16u:** 15 minuten met key users, partner en mij: nieuwe tickets, ernst, wie lost op.
- **Elk ticket krijgt een oorzaak:** data, inrichting, opleiding, bug of integratie. Die oorzaak bepaalt de structurele maatregel, niet alleen de oplossing van het ticket.

## Tickets per week en per oorzaak

| Week | Data | Inrichting | Opleiding | Bug | Integratie | Totaal |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 6 | 11 | 2 | 4 | 32 |
| 2 | 5 | 4 | 7 | 1 | 3 | 20 |
| 3 | 2 | 3 | 4 | 1 | 1 | 11 |
| 4 | 1 | 1 | 3 | 0 | 1 | 6 |
| 5 | 1 | 1 | 1 | 1 | 0 | 4 |
| 6 | 0 | 1 | 1 | 0 | 0 | 2 |

Samen <!--n:hc.total-->75<!--/n--> tickets, waarvan <!--n:hc.bug-->5<!--/n--> bugs (<!--n:hc.bugShare-->7%<!--/n-->). De grootste groep is opleiding (<!--n:hc.training-->27<!--/n-->): dat is geen softwareprobleem maar een signaal voor de key users welke taakkaarten beter moeten.

## Voorbeelden met structurele maatregel

| Ticket | Oorzaak | Opgelost | Structureel |
|---|---|---|---|
| Operator boekt output op de verkeerde productieorder (twee lijnen, zelfde product) | opleiding | correctieboeking door key user | lijnnummer groot op de terminal; taakkaart aangepast |
| Retailer R3 weigert een EDI-factuur: hun bestelreferentie ontbreekt | inrichting | referentie ingevuld, factuur opnieuw verstuurd | externe documentnummer verplicht gemaakt voor de zeven EDI-klanten |
| Planningsvoorstel plant op een lijn die in onderhoud is | inrichting | kalender machinecentrum | onderhoudsplanning maandelijks in de kalender (eigenaar: technische dienst) |
| Labelprinter in de koelcel drukt niet af na een stroomonderbreking | integratie | printerservice herstart | monitoring op de printerservice |

## Exitcriteria

1. Twee weken op rij minder dan vijf nieuwe tickets.
2. Geen open ticket van ernst 1 of 2.
3. Eerste maandafsluiting in Business Central afgerond.
4. Overdracht naar de supportdesk van de partner en de interne application owner getekend.

Gehaald in week 6 (W36). Het ingehouden bedrag van 10% werd vrijgegeven aan de partner (DEC-12).
