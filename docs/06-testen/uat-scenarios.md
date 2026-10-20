# UAT-scenario's en traceerbaarheid

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Terug naar [de teststrategie](README.md). Elke eis in scope heeft minstens één scenario; de test `tests/test_programme.py` faalt als dat niet zo is. Buiten scope en dus zonder test: AK-04, PR-04, PR-07, PR-08, KW-05, IT-03.

| Scenario | Wat de key user doet | Eigenaar | Bewijst eisen |
|---|---|---|---|
| UAT-01 | EDI-order retailer → verkooporder met juiste prijs en kredietcontrole | Klantendienst | VK-01, VK-04, VK-06 |
| UAT-02 | Weekplanning: planningsvoorstel → productie- en aankooporders | Planning | AK-01, AK-05, PR-03 |
| UAT-03 | Ontvangst grondstof met leverancierslot en vervaldatum (scanner) | Magazijn | AK-03, VR-02 |
| UAT-04 | Picken volgens FEFO met controle op minimale resterende houdbaarheid | Magazijn | VK-05, KW-04, VR-02 |
| UAT-05 | Productieorder: verbruik per lot, output met lot en vervaldatum, QA-vrijgave | Productie + QA | PR-01, PR-02, PR-05, PR-06, KW-01 |
| UAT-06 | Kostprijsafwijking van een afgewerkte productieorder | Controller | FIN-08 |
| UAT-07 | Levering met SSCC-label en DESADV naar retailer | Magazijn + klantendienst | VK-02, VR-04 |
| UAT-08 | Factuur via Peppol (BE) en via EDI (retailer) | Finance | FIN-03, VK-03 |
| UAT-09 | Retour van een lot met blokkering | Klantendienst + QA | VK-07 |
| UAT-10 | Goedkeuring bestelling boven €10.000 en functiescheiding bij betaling | Finance | AK-02, IT-01 |
| UAT-11 | Btw-aangifte en grootboek met dimensies | Finance | FIN-01, FIN-02 |
| UAT-12 | CODA inlezen en afletteren, SEPA-betaalbestand | Finance | FIN-04 |
| UAT-13 | Intrastat en afschrijving vaste activa | Finance | FIN-05, FIN-06 |
| UAT-14 | Maandafsluiting en Power BI-margerapport | Controller | FIN-07, FIN-09, IT-02 |
| UAT-15 | Mock recall: grondstoflot voorwaarts en eindproductlot achterwaarts | QA | KW-02 |
| UAT-16 | Allergenen van een nieuwe receptuur | QA | KW-03 |
| UAT-17 | Voorraadmelding koelhuis en cyclische telling | Magazijn | VR-01, VR-03 |

Resultaat UAT (W23): 17 scenario's uitgevoerd, 15 geslaagd, 2 geslaagd met een open defect, 0 gefaald.

## Defects

Ernst 1 = blokkeert een kernproces zonder omweg · 2 = kernproces met omweg · 3 = hinderlijk, geen impact op levering of boekhouding.

| Defect | Ernst | Domein | Omschrijving | Status (W25) | Workaround |
|---|---|---|---|---|---|
| DEF-07 | 2 | Productie | Outputboeking rondt uitval af per eenheid in plaats van per kg | open | uitval handmatig corrigeren in het outputdagboek tot de fix |
| DEF-11 | 2 | EDI | DESADV van retailer R4 wordt geweigerd: SSCC-segment in verkeerde volgorde | open | leverbericht voor R4 via het webportaal van de retailer |
| DEF-14 | 3 | Labels | Paletlabel toont houdbaarheidsdatum in Amerikaans formaat | open | geen nodig: datum leesbaar, cosmetisch |
| DEF-15 | 3 | Planning | Planningsvoorstel stelt order voor op lijn in onderhoud | open | kalender machinecentrum aanpassen |
| DEF-16 | 3 | Rapportering | Power BI-margerapport mist promotiekortingen | open | kortingen apart tonen |
| DEF-17 | 3 | Kwaliteit | Allergenen-extensie toont ‘sporen van’ niet op de afdruk | open | QA voegt de vermelding handmatig toe op de specificatie |
| DEF-18 | 3 | Verkoop | Retourorder neemt het lot niet over uit de oorspronkelijke levering | open | lot handmatig kiezen |
| DEF-19 | 3 | Financiën | SEPA-bestand: naam begunstigde afgekapt op 35 tekens | open | bank aanvaardt het bestand |
| DEF-20 | 3 | Voorraad | Telformulier sorteert niet per gang | open | sorteren in Excel |
| DEF-02 | 1 | Financiën | Btw-boekingsgroep ontbreekt bij Franse klanten na migratie | opgelost | — |
| DEF-05 | 2 | Financiën | Peppol-factuur geweigerd door access point: ontbrekend ondernemingsnummer | opgelost | — |
