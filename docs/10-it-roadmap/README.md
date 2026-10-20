# IT-roadmap na de go-live

> **Wat dit is:** het landschap na SAP, de principes waarmee we verder bouwen, het team dat nodig is en de eerste vier kwartalen. Opgesteld met de IT Manager. **Voor wie:** IT Manager, directie. **Vorige:** [batenreview](../09-baten/README.md).

## Landschap: voor en na

```text
VOOR                                           NA
SAP ECC (gehost, 146 Z-objecten)          →    Business Central (SaaS, 2 extensies, 5 apps)
Excel-planbord                            →    planningsvoorstel + Power BI capaciteit
Papieren lotkoppeling                     →    lots gescand bij verbruik, genealogie in BC
Labo-Excel + mail voor vrijgave           →    vrijgave in BC; labo-Excel blijft (fase 2)
EDI via IDocs                             →    EDI-connector-app + Peppol
Labels via nachtelijk bestand             →    label-app, rechtstreeks
Power BI op handmatige extracten          →    Power BI-connector op BC + archief
                                               SAP-archief (read-only, 10 jaar)
```

## Architectuurprincipes

1. **Standaard en SaaS eerst.** Een extensie alleen bij een wettelijke of contractuele eis, met een eigenaar die ze onderhoudt bij elke update.
2. **Elk stamgegeven heeft één bron en één eigenaar.** Artikel en receptuur: technoloog in Business Central. Klant: klantendienst. Lot: het systeem, niet een mens.
3. **Koppelingen via API, niet via bestanden.** Waar een leverancier alleen bestanden kan (het koelhuis), is er een dagelijkse afstemming met een eigenaar.
4. **Identiteit is de perimeter.** Business Central is SaaS; wie inlogt en vanaf welk toestel, is de belangrijkste beveiliging.
5. **Elke wijziging via change.** Ook na het project: een wens wordt een ticket, een ticket met impact wordt een change met een beslisser.

## Team

| Rol | Nu | Voorstel | Waarom |
|---|---|---|---|
| IT Manager | 1 | 1 | |
| Helpdesk en werkplek | 1 | 1 | |
| **Application owner Business Central** | — | 1 (intern) | de kennis zit nu bij de partner en de projectmanager; elke halfjaarlijkse update moet iemand intern testen |
| Data en rapportering | — | 0,5 (gedeeld met finance) | 14 Power BI-rapporten naar één model |
| Partner | project | supportcontract + dagen op afroep | tweede lijn, extensies, updates |
| SAP-freelancer | 1 dag/week | — | gestopt na de go-live |

## Roadmap

| Kwartaal | Wat | Waarom | Bron |
|---|---|---|---|
| Q+1 | Koppeling controleweegschalen → output in Business Central | manuele outputboeking kost 25 minuten per ploeg | PR-07, [ADR-007](../adr/adr-007-weegschalen-fase-2.md) |
| Q+1 | Application owner Business Central aanstellen | kennis intern brengen | team |
| Q+2 | Kwaliteitsapp: laboresultaten per lot, automatische vrijgave | QA-vrijgave is nog handwerk op basis van Excel | KW-05 |
| Q+2 | Planbord-app evalueren na één BBQ-seizoen | CR-03 opnieuw, met data in plaats van gewoonte | PR-04 |
| Q+3 | Elektronisch batchrecord op tablets | het papieren batchrecord is de laatste breuk in de traceerbaarheid | PR-08 |
| Q+3 | Beveiligingsbasis M365 en Entra ID: MFA, voorwaardelijke toegang, beheerde toestellen op de vloer | identiteit is de nieuwe perimeter | principe 4 |
| Q+4 | Eén Power BI-model op Business Central en het archief | 14 losse rapporten | IT-02 |
| Q+4 | Leveranciersbeoordeling | aankoop vraagt het al twee jaar | AK-04 |

Wat er bewust niet op staat: een eigen datawarehouse, een MES, AI-toepassingen. Eerst moet de basis een seizoen stabiel draaien; dan pas is er data om op te bouwen.
