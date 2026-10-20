# Case study: een ERP-migratie die vier weken later live ging, en waarom dat goed was

*Onafhankelijke portfoliocase over een fictieve organisatie (Vaerdal Foods). Alle cijfers zijn illustratieve aannames; resultaten na de go-live zijn gesimuleerd. Leestijd: tien minuten.*

## 1. Het vertrekpunt

Vaerdal Foods maakt gekoelde sauzen, dressings en soepen, grotendeels als huismerk voor supermarkten in België, Nederland en Frankrijk. <!--n:org.employees-->185<!--/n--> medewerkers, twee productiehallen, een extern koelhuis. Sinds 2009 draait alles op SAP ECC 6.0, met 146 eigen objecten en één ABAP-freelancer die één dag per week komt. Het standaardonderhoud van SAP ECC loopt af, de hosting ook, en de freelancer stopt. De raad van bestuur koos Microsoft Dynamics 365 Business Central en keurde <!--n:budget.total-->€865.950<!--/n--> goed, reserve inbegrepen ([business case](docs/01-mobilisatie/business-case.md)).

Wat er naast SAP draaide, was belangrijker dan SAP zelf: een Excel-planbord met 22 jaar aan regels, papieren batchrecords, vrijgave van lots via mail. Een recall-oefening duurde <!--n:kpi.K2.baseline-->220<!--/n--> minuten, het grootste deel ervan dossiers zoeken.

En er waren twee seizoenen: soep van oktober tot februari, BBQ-sauzen vanaf april. Elke week productiestop kost leveringen aan retailers die daar boetes voor rekenen.

## 2. Mijn rol

Ik ben in deze case de IT-projectmanager en business analist aan de kant van Vaerdal, met de IT Manager als leidinggevende. Mijn werk: de partner mee kiezen en aansturen, de processen vertalen naar een oplossing, planning, budget en kwaliteit bewaken, de business meenemen in workshops, testen en opleiding, en de stuurgroep een onderbouwde go/no-go voorleggen. Configureren doet de partner. Beslissen doen de proceseigenaars en de stuurgroep.

## 3. De partner: criteria vóór de offertes

Ik liet de stuurgroep in week 2 de criteria en gewichten vastleggen, vóór er één offerte binnen was. Prijs kreeg 15%, referenties in voeding en een demo op ons eigen script elk 20%. Het script volgde één order van EDI tot factuur, met een lot dat geblokkeerd moet blijven tot QA het vrijgeeft, een retailer die twee derde resterende houdbaarheid eist, en een recall ([demoscript](docs/02-partnerselectie/demoscript.md)).

Partner A won met <!--n:partner.A.score-->3,75<!--/n--> tegen <!--n:partner.B.score-->3,55<!--/n--> en <!--n:partner.C.score-->2,90<!--/n-->. De gevoeligheidsanalyse toonde dat prijs meer dan <!--n:sens.C6.to-->40%<!--/n--> moest wegen om de goedkoopste partner te laten winnen ([partnerselectie](docs/02-partnerselectie/README.md)). Het contract: vaste prijs voor de kernscope per mijlpaal, pas betaalbaar na aftekening door de key users; datamigratie in regie met een plafond; 10% ingehouden tot het einde van de hypercare ([ADR-006](docs/adr/adr-006-contractvorm.md)).

## 4. Processen en fit-gap: standaard eerst

Zes workshops, elk vertrekkend van een echt document van vorige week. Wat bovenkwam: 7,5% van de EDI-orders wordt met de hand aangepast; het planbord bevat regels over allergenenvolgorde die nergens anders staan; een eigen SAP-transactie maakt de lots van halffabricaten in Hal 2, en niemand wist wie die onderhoudt ([workshops](docs/03-processen/README.md)).

Elk van de 146 Z-objecten kreeg een uitkomst: 61 doet de standaard, 38 worden een rapport, 21 een procesaanpassing, 24 zijn niet meer nodig, 2 een extensie. De fit-gap telde <!--n:fg.total-->41<!--/n--> eisen; <!--n:fg.stdConfPct-->74%<!--/n--> van wat in scope is, is standaard of configuratie ([register](docs/04-fit-gap/fit-gap.md)). De twee extensies zijn allebei verplicht: resterende houdbaarheid per klant (contract met de retailers) en allergenen doorrekenen uit de receptuur (wetgeving). Het grafische planbord als extensie (€41.800) werd afgewezen; daarover meer bij de verandering.

Het to-be-proces draait rond lots: elk nieuw lot geblokkeerd tot QA het vrijgeeft, picken volgens FEFO met een controle per retailer, lotnummers uit SAP ongewijzigd zodat een recall van Business Central naadloos doorloopt in het SAP-archief ([order tot levering](docs/03-processen/order-tot-levering.md), [recall](docs/03-processen/recall.md), [ADR-008](docs/adr/adr-008-lotnummers-behouden.md)).

## 5. De datamigratie en de 107 lots

Ik bouwde de controles aan de kant van Vaerdal als code ([`erpcase/`](erpcase/)): vijftien datakwaliteitsregels, elk met een eigenaar in de business, een mapping naar Business Central, een afstemming van voorraad, posten en saldi, en een mock recall. Vier proefmigraties ([datamigratie](docs/05-datamigratie/README.md)).

| | Blokkerende fouten | Voorraadverschil | Recall |
|---|---:|---:|---:|
| Proefmigratie 1 (W18) | <!--n:mock1.blocking-->417<!--/n--> | <!--n:mock1.stockDiffPct-->17,656%<!--/n--> | <!--n:mock1.recall-->76,5%<!--/n--> |
| Proefmigratie 2 (W21) | <!--n:mock2.blocking-->146<!--/n--> | <!--n:mock2.stockDiffPct-->4,783%<!--/n--> | <!--n:mock2.recall-->95,3%<!--/n--> |
| Proefmigratie 3, generale repetitie (W24) | <!--n:mock3.blocking-->107<!--/n--> | <!--n:mock3.stockDiffPct-->2,131%<!--/n--> | <!--n:mock3.recall-->96,7%<!--/n--> |

De laatste <!--n:mock3.DQ-10-->107<!--/n--> fouten waren allemaal lots halffabricaat uit Hal 2 zonder vervaldatum. Bij proefmigratie 2 waren het er <!--n:mock2.DQ-10-->104<!--/n-->, en QA had ze verbeterd. Maar de vergelijking per sleutel toonde dat alle <!--n:mock3.DQ-10-->107<!--/n--> nieuw waren: de eigen SAP-transactie uit workshop 3 sloeg het veld over, elke productiedag opnieuw. Opschonen zonder de bron te herstellen is dweilen met de kraan open.

Wat ik daarvan leerde: tel niet alleen fouten, kijk welke. Die vergelijking zit nu in de rapportering.

## 6. De go/no-go

In week 16 had de stuurgroep twaalf criteria vastgelegd: acht hard, vier zacht. In week 25 faalden er drie harde, allemaal door dezelfde lots: geen volledige recall, blokkerende fouten, een voorraadverschil van <!--n:mock3.stockDiffPct-->2,131%<!--/n-->. Volgens de regels: <!--n:gng1.decision-->NO-GO<!--/n--> ([metingen](docs/08-go-live/go-no-go-resultaten.md)).

Ik bracht de stuurgroep één pagina met vier opties: toch live en de lots met de hand bijwerken, live zonder halffabricaten, vier weken uitstel, of uitstel tot september. Mijn advies was uitstel tot 1 april, met eerst de bron hersteld, voor <!--n:budget.delay-->€55.700<!--/n--> uit de reserve. Die vier weken losten ook de opleiding van de laatste eindgebruikers en de EDI-certificering van één retailer op. Ze losten niet op dat de hypercare nu in de start van het BBQ-seizoen viel, dus daar kwamen maatregelen bij ([voorstel](docs/08-go-live/go-no-go.md)).

De stuurgroep koos uitstel. In week 29: recall <!--n:mock4.recall-->100,0%<!--/n-->, nul blokkerende fouten, voorraadverschil <!--n:mock4.stockDiffPct-->0,011%<!--/n-->, verklaard en afgetekend. <!--n:gng2.decision-->GO<!--/n-->.

## 7. Mensen

De moeilijkste gebruiker was de hoofdplanner, die al 22 jaar met hetzelfde planbord werkte. Ik probeerde haar niet te overtuigen. We liepen samen de formules door (elf regels, waarvan vier in de planningsparameters konden), ze plande een echte soepweek met het planningsvoorstel, en ik liet een Power BI-overzicht van de capaciteit per lijn bouwen omdat dat haar gemis was. Het grafische planbord als extensie bleef afgewezen, met de belofte het na één seizoen opnieuw te bekijken met data. Zij werd key user planning ([verandering](docs/07-verandering/README.md)).

Key users schreven hun eigen UAT-scenario's en trainden hun collega's ([testen](docs/06-testen/README.md)).

## 8. Na de go-live

Zes weken hypercare, <!--n:hc.total-->75<!--/n--> tickets, waarvan <!--n:hc.bug-->5<!--/n--> bugs. De grootste groep was opleiding ([hypercare](docs/08-go-live/hypercare.md)). Na drie maanden was één van zes KPI-doelen gehaald: de recall, van <!--n:kpi.K2.baseline-->220<!--/n--> naar <!--n:kpi.K2.measured-->42<!--/n--> minuten. De andere vijf zijn op weg, met een eigenaar en een actie ([batenreview](docs/09-baten/README.md)). Het budget eindigde op <!--n:budget.eac-->€842.400<!--/n-->. Met de IT Manager maakte ik een roadmap voor de volgende vier kwartalen en een voorstel voor een interne application owner ([roadmap](docs/10-it-roadmap/README.md)).

## 9. Wat dit over mijn manier van werken zegt

- Ik werk vanuit de business: proceseigenaars beslissen, data-eigenaars schonen op, key users testen hun eigen werk.
- Ik stuur een partner met afspraken die vooraf vastliggen: criteria, acceptatie, change, reserve.
- Ik maak slecht nieuws concreet: oorzaak, opties, kost, en wie beslist.

## 10. Wat de case niet is

Er draait niets in een echte Business Central-omgeving. De SAP-data is gegenereerd, met bewust ingebouwde fouten. Partners, budget, defects en resultaten zijn illustratief. Ik heb geen ERP-migratie in een bedrijf geleid. Wat de case wel toont: hoe ik het zou aanpakken, tot in de data en de beslissingen, met elk getal uit één model en getest in CI.
