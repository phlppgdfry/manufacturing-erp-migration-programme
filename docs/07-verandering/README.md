# Verandering: mensen meenemen van SAP en Excel naar Business Central

> **Wat dit is:** wie wat verliest en wint, het key-usernetwerk, de opleiding en hoe we met weerstand omgingen. **Voor wie:** COO, proceseigenaars, key users. **Vorige:** [testen](../06-testen/README.md) · **Volgende:** [go/no-go](../08-go-live/go-no-go.md).

## Impact per groep

| Groep | Aantal | Wat verandert | Impact | Houding bij de start | Aanpak |
|---|---:|---|---|---|---|
| Klantendienst | 6 | werklijst met EDI-uitzonderingen in plaats van elke order controleren | hoog | positief | key user in het ontwerp; zij schrijven UAT-01, -07, -08 |
| Planning | 2 | planningsvoorstel + Power BI in plaats van het Excel-planbord | **hoog** | **weerstand** | zie scenario hieronder |
| Productie (lijnverantwoordelijken, operatoren) | ±60 | lots scannen bij verbruik, output boeken op een terminal | midden | afwachtend | één scan extra, korte opleiding per lijn aan de lijn |
| QA | 4 | vrijgave in het systeem, recall zelf doen | hoog | positief | eigenaar van traceerbaarheid; tekent de mock recall af |
| Magazijn | 9 | scanner, FEFO, controle per klant | hoog | positief | key user test met de echte scanner in de koelcel |
| Finance | 7 | dagelijkse voorraadwaardering, afsluitkalender, Peppol | midden | positief | CFO als sponsor; controller als key user kostprijs |
| Aankoop | 3 | bestellen vanuit het planningsvoorstel | midden | afwachtend | samen met planning opgeleid |

## Key-usernetwerk

<!--n:org.erpUsers-->58<!--/n--> ERP-gebruikers, 14 key users: twee per domein, telkens één ervaren en één jongere collega. Key users ontwerpen mee, schrijven de testscenario's, trainen hun collega's en zijn de eerste lijn in de hypercare. Vier van hen krijgen tijdens het soepseizoen interim-vervanging (budgetlijn B7, R-01): zonder vrijgemaakte tijd is "key user" een titel en geen rol.

## Opleiding

| Golf | Wanneer | Wie | Door wie | Vorm |
|---|---|---|---|---|
| 1 | W14–W17 | 14 key users | partner | in de sandbox, rond de CRP's |
| 2 | W22–W25 | 64 eindgebruikers | key users | per rol, 2 tot 4 uur, op eigen data van proefmigratie 2; per taak één kaart van één pagina |
| 3 | W27–W29 | wie golf 2 miste of opnieuw wil | key users | inhaalsessies en "vraag het aan de key user"-uur |

Stand: key users 14/14; eindgebruikers 54/64 (84%) bij go/no-go 1 en 61/64 (95%) bij go/no-go 2. De extra vier weken door het no-go werden gebruikt om de inhaalsessies te geven.

## Communicatie

| Wanneer | Wat | Aan wie | Door |
|---|---|---|---|
| W2 | Waarom we overstappen, wat het voor jou betekent | iedereen | CEO, personeelsvergadering |
| elke 4 weken | Eén pagina: waar staan we, wat komt er, wat vraagt het van jou | iedereen | projectmanager, via de teamleiders |
| W19 | Brief aan retailers en leveranciers: nieuwe ordernummers, ongewijzigde artikel- en lotnummers | klanten, leveranciers | klantendienst, aankoop |
| W25 | Nieuwe datum en waarom | iedereen | COO |
| W29 | Go-live, wat er die eerste week anders loopt, wie je belt | iedereen | projectmanager |

Bij het no-go in W25 vertelde de COO het zelf, met de echte reden: "we gaan pas live als we elk lot kunnen terugvinden". Dat werd geen tegenslag maar een signaal dat de criteria ernstig genomen worden.

## Scenario: "Het Excel-planbord werkt al 22 jaar"

De hoofdplanner werkt sinds 22 jaar met hetzelfde planbord. Het is snel, visueel, en de formules bevatten regels die nergens anders staan: welke allergenen na elkaar op een lijn mogen, hoeveel reinigingstijd na selder. Haar reactie in workshop 2: "Business Central kan dit niet, en ik heb geen tijd om het te leren in volle soepweek."

Wat ik niet deed: haar overtuigen dat het nieuwe systeem beter is.

Wat ik wel deed:

1. **Luisteren naar wat het planbord echt doet.** In twee sessies van een uur liepen we samen de formules door. Resultaat: 11 regels, waarvan 4 in de routing en de planningsparameters kunnen, 5 kennis zijn die bij haar blijft, en 2 door niemand meer gebruikt werden.
2. **Haar eigen week laten plannen.** In CRP2 plande ze een echte soepweek van het vorige jaar met het planningsvoorstel. Het voorstel was niet beter dan haar planning, wel sneller in het rekenen, en de zichtbaarheid per lijn ontbrak.
3. **Het gemis oplossen in plaats van wegpraten.** Een Power BI-overzicht van de capaciteit per lijn per dag, gebouwd op haar vraag. Het grafische slepen bleef een wens: CR-03 werd afgewezen door de stuurgroep, met de belofte om het na één BBQ-seizoen opnieuw te bekijken met data in plaats van gewoonte.
4. **Haar positie erkennen.** Zij werd key user planning en tekende UAT-02 af. In de hypercare beantwoordde zij de planningsvragen, niet de partner.

Resultaat drie maanden na de go-live: weekplanning in <!--n:kpi.K3.measured-->5<!--/n--> uur (was <!--n:kpi.K3.baseline-->11<!--/n-->, doel <!--n:kpi.K3.target-->4<!--/n-->). Het planbord in Excel bestaat nog, als kladblok. Dat is goed genoeg: de waarheid staat in Business Central.

## Hoe we adoptie meten

- Aantal handmatige correcties op productieorders per week (daalt = mensen boeken op het moment zelf).
- Aantal hypercare-tickets van het type "opleiding" per week ([hypercare](../08-go-live/hypercare.md)).
- Wordt het planningsvoorstel elke week goedgekeurd in Business Central, of wordt er buiten het systeem gepland?
