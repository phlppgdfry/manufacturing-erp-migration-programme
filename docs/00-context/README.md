# Context: Vaerdal Foods en waarom het programma bestaat

> **Wat dit is:** de fictieve organisatie, het probleem, mijn rol, de aannames, de data en de beperkingen van deze case. **Voor wie:** iedereen die de rest wil plaatsen. **Volgende stap:** [programmacharter](../01-mobilisatie/project-charter.md).

*Onafhankelijke portfoliocase over een fictieve organisatie. Geen vertrouwelijke informatie van een echte werkgever, klant of leverancier. Alle cijfers zijn illustratieve aannames.*

## De organisatie

**Vaerdal Foods NV** is een familiebedrijf uit 1961 in de West-Vlaamse kuststreek. <!--n:org.employees-->185<!--/n--> medewerkers, ongeveer <!--n:org.revenue-->€74 miljoen<!--/n--> omzet, <!--n:org.erpUsers-->58<!--/n--> ERP-gebruikers. Het maakt gekoelde sauzen, dressings en soepen, grotendeels als huismerk voor supermarkten in België, Nederland en Frankrijk.

| Plek | Wat er gebeurt |
|---|---|
| Hal 1 | soepen, hot-fill, drie lijnen |
| Hal 2 | sauzen en dressings, cold-fill, vier lijnen |
| Magazijn | grondstoffen en verpakking |
| Extern koelhuis (3PL) | eindproducten, levert aan de distributiecentra van de retailers |

Twee seizoenen bepalen alles: **soep van oktober tot februari** (Hal 1 op volle kracht) en **BBQ- en saladesauzen van april tot augustus** (Hal 2 bouwt vanaf april voorraad op). Zes retailers zijn samen goed voor ongeveer twee derde van de omzet. Ze bestellen via EDI, eisen een minimale resterende houdbaarheid bij levering en controleren traceerbaarheid tijdens audits.

## Het systeemlandschap vandaag

| Systeem | Gebruik | Probleem |
|---|---|---|
| SAP ECC 6.0 (sinds 2009) | financiën, verkoop, aankoop, voorraad, kostprijs; productieorders alleen voor terugmelding | 146 eigen Z-objecten; één ABAP-freelancer, één dag per week; hosting bij een externe partij |
| Excel-planbord | weekplanning van zeven lijnen | één persoon kent de formules; MRP in SAP wordt niet gebruikt |
| Papieren batchrecords | CCP-registraties, lotkoppeling grondstof → eindproduct | traceren betekent dossiers doorbladeren |
| EDI-provider | orders, leverberichten en facturen van zes retailers | 7,5% van de orders wordt manueel gecorrigeerd |
| Labelsoftware | GS1-128-paletlabels | gekoppeld via een nachtelijk bestand |
| Labo-Excel | QA-resultaten per lot | geen koppeling met lotblokkering |
| Power BI | 14 rapporten op SAP-extracten | extracten handmatig ververst |

## Waarom nu

Het standaardonderhoud van SAP ECC 6.0 loopt eind 2027 af; verlengd onderhoud tot 2030 kost extra en bevriest de functionaliteit ([SAP-onderhoudsstrategie, secundaire bronnen in de bronnenlijst](#data-en-bronnen)). Het hostingcontract loopt in hetzelfde jaar af en de enige ABAP-kracht stopt. Een offerte voor S/4HANA lag ver boven wat een bedrijf van deze omvang wil uitgeven. De raad van bestuur koos in het voorjaar voor **Microsoft Dynamics 365 Business Central** en keurde een programmabudget goed ([business case](../01-mobilisatie/business-case.md)). Daarna werd een IT-projectmanager aangeworven om het programma te leiden.

## Mijn rol in deze case

**IT-projectmanager / business analist aan de kant van Vaerdal**, rapporteert aan de IT Manager. Ik:

- kies mee de implementatiepartner en onderhandel de contractvorm ([partnerselectie](../02-partnerselectie/README.md));
- leid de procesworkshops en vertaal processen naar eisen en een fit-gap ([processen](../03-processen/README.md), [fit-gap](../04-fit-gap/README.md));
- bewaak planning, budget en kwaliteit van partner en leveranciers ([governance](../governance/README.md));
- organiseer de datamigratie aan Vaerdal-kant: data-eigenaars, kwaliteitsregels, afstemming ([datamigratie](../05-datamigratie/README.md));
- organiseer testen en opleiding met finance en productie ([testen](../06-testen/README.md), [verandering](../07-verandering/README.md));
- bereid de go/no-go voor; de stuurgroep beslist ([go/no-go](../08-go-live/go-no-go.md));
- schets de IT-roadmap na de go-live met de IT Manager ([IT-roadmap](../10-it-roadmap/README.md)).

**Niet mijn rol:** configureren en bouwen (de partner), beslissen over budget, scope en go-live (de stuurgroep), procesbeslissingen (de proceseigenaars).

## Aannames

- Alle cijfers (omzet, aantallen, budget, defects, KPI's) zijn illustratief, gekozen om realistisch te zijn voor een producent van deze omvang.
- De keuze voor Business Central was al gemaakt bij de start; deze case gaat over het uitvoeren, niet over de pakketkeuze.
- Manufacturing in Business Central (productiestuklijsten, routings, productieorders, planning) vereist de Premium-licentie ([Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/business-central/production-manage-manufacturing)). Essentials en Premium kunnen niet gemengd worden in één omgeving; daarom zijn alle volledige gebruikers op Premium begroot (R-08). Controleer licentievoorwaarden altijd in de actuele Microsoft-licentiegids.
- Partners A, B en C zijn fictief. Geen enkele beschrijving verwijst naar een bestaand bedrijf.
- Weken tellen vanaf de programmastart (W1 = eerste week van september). Er staan geen jaartallen in de documenten; de gegenereerde data gebruikt wel datums omdat houdbaarheid daarop rekent.

## Data en bronnen

| Wat | Herkomst | Licentie |
|---|---|---|
| SAP-extracten (klanten, leveranciers, artikels, stuklijsten, routings, lots, genealogie, openstaande posten, saldi) | **gegenereerd** door [`erpcase/sap_extract.py`](../../erpcase/sap_extract.py), vaste seed; tabel- en veldnamen volgen SAP ECC-conventies in vereenvoudigde vorm | CC BY 4.0 (deze repo) |
| Datafouten in de extracten | bewust ingebouwd, met een exact aantal per regel en per proefmigratie; de testen controleren dat de regels precies die fouten vinden | idem |
| Programmagegevens (budget, partners, eisen, RAID, defects, KPI's) | [`data/programme.json`](../../data/programme.json), zelf opgesteld | idem |
| Processen | [`data/processes.json`](../../data/processes.json) → BPMN 2.0 en SVG via [`erpcase/bpmn.py`](../../erpcase/bpmn.py) | idem |
| Business Central-functionaliteit | [Microsoft Learn: Business Central](https://learn.microsoft.com/en-us/dynamics365/business-central/), o.a. [artikeltracering](https://learn.microsoft.com/en-us/dynamics365/business-central/inventory-how-work-item-tracking), [productie](https://learn.microsoft.com/en-us/dynamics365/business-central/production-manage-manufacturing), [datamigratie](https://learn.microsoft.com/en-us/dynamics365/business-central/admin-migrate-data) | bron, niet gekopieerd |
| Implementatiemethode | [Dynamics 365 Implementation Guide / Success by Design](https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/success-by-design) | bron |
| SAP-onderhoudstermijnen | secundaire bronnen, o.a. [endoflife.ai](https://endoflife.ai/sap-ecc), [ERP Research](https://erpresearch.com/en-gb/sap-ecc-6-erp); de officiële SAP-roadmap blijft de referentie | bron |
| Belgische e-facturatie (Peppol B2B vanaf 1 januari 2026) | [FOD Financiën — e-facturatie](https://financien.belgium.be/nl/ondernemingen/btw/e-facturatie) | bron |
| Traceerbaarheid en recall | [Verordening (EG) 178/2002, art. 18–19](https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32002R0178) (één stap voor, één stap na; terugroepen) en de [FAVV-meldingsplicht](https://favv-afsca.be/nl/professionelen/meldingsplicht) | bron |
| IBAN- en btw-controles | [ISO 13616](https://www.iso.org/standard/81090.html) (mod 97), Belgisch ondernemingsnummer (mod 97 op de eerste acht cijfers) | bron |

Code: MIT. Documentatie, diagrammen en data: CC BY 4.0. Zie [LICENSE](../../LICENSE).

## Beperkingen

- **Niets draait in een echte Business Central-omgeving.** De migratie zet SAP-extracten om naar records met Business Central-veldnamen (wat een configuratiepakket of de API zou laden), stemt af en traceert, maar laadt niets.
- **De SAP-data is gegenereerd.** Ze lijkt op een echte extractie, maar heeft de rommel van een echte SAP-installatie (tekstvelden, vrije notities, half gebruikte velden) niet.
- **Resultaten na de go-live zijn gesimuleerd:** hypercare-tickets en KPI-metingen zijn illustratief, geen meetresultaat.
- **Geen echte partner, geen echt contract.** De onderhandelde afspraken zijn hoe ik het zou aanpakken, geen juridisch advies.
- **Wat de case niet toont:** het configureren van Business Central zelf (zie daarvoor een aparte case over de partnerkant: [business-central-implementation-case](https://github.com/phlppgdfry/business-central-implementation-case)), loonadministratie, HR, CRM.
