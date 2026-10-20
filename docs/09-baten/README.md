# Batenreview: drie maanden na de go-live

> **Wat dit is:** wat het programma beloofde, wat er gemeten is, en wat er gebeurt waar het doel niet gehaald werd. **Voor wie:** stuurgroep, proceseigenaars. **Vorige:** [hypercare](../08-go-live/hypercare.md) · **Volgende:** [IT-roadmap](../10-it-roadmap/README.md).

*Metingen zijn gesimuleerd, niet gemeten bij een echt bedrijf.*

| KPI | Vóór | Doel | Gemeten (+3 maanden) | Gehaald | Eigenaar | Hoe gemeten |
|---|---:|---:|---:|---|---|---|
| Maandafsluiting (werkdagen) | <!--n:kpi.K1.baseline-->9<!--/n--> | <!--n:kpi.K1.target-->5<!--/n--> | <!--n:kpi.K1.measured-->6<!--/n--> | nee | CFO | dag waarop de controller de maandcijfers vrijgeeft |
| Mock recall grondstof → klant (minuten) | <!--n:kpi.K2.baseline-->220<!--/n--> | <!--n:kpi.K2.target-->60<!--/n--> | <!--n:kpi.K2.measured-->42<!--/n--> | ja | QA-manager | oefening per kwartaal, stopwatch |
| Weekplanning opstellen (uur) | <!--n:kpi.K3.baseline-->11<!--/n--> | <!--n:kpi.K3.target-->4<!--/n--> | <!--n:kpi.K3.measured-->5<!--/n--> | nee | COO | tijdregistratie planner, vier weken |
| Manueel gecorrigeerde EDI-orders (%) | <!--n:kpi.K4.baseline-->7,5<!--/n--> | <!--n:kpi.K4.target-->2<!--/n--> | <!--n:kpi.K4.measured-->2,4<!--/n--> | nee | Teamleider klantendienst | orders met manuele wijziging / alle EDI-orders |
| Voorraadnauwkeurigheid (%) | <!--n:kpi.K5.baseline-->94,1<!--/n--> | <!--n:kpi.K5.target-->98<!--/n--> | <!--n:kpi.K5.measured-->97,2<!--/n--> | nee | Magazijnverantwoordelijke | lots zonder telverschil / getelde lots |
| Jaarlijkse runkosten ERP (k€) | <!--n:kpi.K6.baseline-->286<!--/n--> | <!--n:kpi.K6.target-->168<!--/n--> | <!--n:kpi.K6.measured-->171<!--/n--> | nee | IT Manager | licenties + support + apps, op jaarbasis |

Eén van zes doelen gehaald, vijf op weg. Dat is geen mislukking maar wel iets om eerlijk te zeggen: drie maanden na een go-live in het begin van het hoogseizoen is te vroeg voor de meeste doelen. De recall, de reden waarom de go-live vier weken opschoof, is het enige doel dat ruim gehaald is.

## Waar het doel niet gehaald is

| KPI | Waarom nog niet | Actie | Eigenaar | Opnieuw meten |
|---|---|---|---|---|
| Maandafsluiting 6 i.p.v. 5 | afschrijvingen en voorzieningen nog in Excel | terugkerende dagboeken, afsluitkalender herzien | CFO | +6 maanden |
| Weekplanning 5 i.p.v. 4 uur | planner controleert het voorstel nog regel per regel tegen het oude planbord | na het BBQ-seizoen: welke controles kunnen weg? Planbord-app opnieuw bekijken | COO | na het seizoen |
| EDI 2,4% i.p.v. 2% | één retailer stuurt artikelcodes van een oude catalogus | kruistabel bij de EDI-provider; retailer gevraagd de catalogus bij te werken | Teamleider klantendienst | +3 maanden |
| Voorraad 97,2% i.p.v. 98% | koelhuis meldt per pallet, verschillen bij deelpallets | cyclische telling deelpallets wekelijks; afspraak met 3PL | Magazijnverantwoordelijke | +3 maanden |
| Runkosten €171k i.p.v. €168k | twee extra Team Members-licenties voor QA-technici | aanvaard; doel bijgesteld | IT Manager | jaarlijks |

## Wat niet in een KPI staat

- De BRCGS-audit in mei werd gehaald zonder tekortkoming op traceerbaarheid; de auditor deed de recall-oefening zelf in Business Central.
- Geen enkele retailer miste een levering door de systeemwissel.
- De ABAP-freelancer is gestopt; niemand heeft hem nog nodig gehad.
