# Governance, overlegritme en RACI

> **Wat dit is:** wie beslist wat, wanneer we elkaar zien en hoe iets escaleert. **Voor wie:** iedereen in het programma, en de partner. **Vorige:** [business case](business-case.md) · **Volgende:** [planning](planning.md).

## Structuur

```text
Stuurgroep (elke 4 weken, 60 min)
  CEO (voorzitter) · CFO (sponsor) · COO · IT Manager · engagement manager partner
  beslist: budget uit de reserve > €25.000, scope, go/no-go, partnerkwesties
        │
Projectteam (wekelijks, 60 min)
  projectmanager (voorzitter) · lead consultant partner · migratieconsultant · key users per domein
  beslist: planning binnen een fase, defects, CR's < €25.000 (via IT Manager)
        │
Ontwerpautoriteit (op afroep, 30 min)
  projectmanager · lead consultant · IT Manager · betrokken proceseigenaar
  beslist: elke afwijking van de standaard (extensie, app, procesaanpassing) vóór ze in de fit-gap komt
        │
Werkstromen: financiën · verkoop & EDI · productie & planning · kwaliteit & voorraad · data · test · verandering
```

Waarom een aparte ontwerpautoriteit: in een SAP-bedrijf met 146 Z-objecten wordt elke workshop een vraag om maatwerk. Door elke afwijking in een korte vaste ronde te leggen met de proceseigenaar erbij, blijft de discussie bij de business en niet tussen projectmanager en partner.

## Beslisrechten

| Beslissing | Wie | Drempel |
|---|---|---|
| Budget uit de reserve | IT Manager | tot <!--n:budget.threshold-->€25.000<!--/n--> per beslissing |
| Budget uit de reserve | Stuurgroep | boven <!--n:budget.threshold-->€25.000<!--/n--> |
| Extensie (AL-maatwerk) | Stuurgroep | altijd, ongeacht bedrag ([ADR-001](../adr/adr-001-standaard-eerst.md)) |
| Procesaanpassing | Proceseigenaar | binnen het eigen domein |
| Go/no-go | Stuurgroep | op voorstel van de projectmanager |
| Aftekening mijlpaal partner | IT Manager | na aftekening van de acceptatiecriteria door de key users |

## RACI

R = voert uit · A = eindverantwoordelijk · C = geraadpleegd · I = geïnformeerd

| Activiteit | Stuurgroep | IT Manager | Projectmanager | Proceseigenaar | Key user | Partner |
|---|---|---|---|---|---|---|
| Programmacharter | A | C | R | C | I | I |
| Partnerselectie | A | R | R | C | C | — |
| Procesworkshops | I | I | R | A | C | C |
| Fit-gap en oplossingsontwerp | I | C | R | A | C | R |
| Configuratie en extensies | — | I | C | I | C | A/R |
| Datakwaliteit opschonen | I | I | C | A | R | C |
| Extractie, transformatie en laden | — | I | C | I | I | A/R |
| Afstemming na migratie | I | C | R | A (controller/QA) | R | C |
| Testscenario's schrijven | — | I | R | A | R | C |
| UAT uitvoeren en aftekenen | I | I | C | A | R | C |
| Opleiding eindgebruikers | I | I | A | C | R | C |
| Go/no-go-voorstel | I | C | A/R | C | C | C |
| Go/no-go-besluit | A/R | C | C | C | I | I |
| Cutover | I | A | R | C | R | R |
| Hypercare | I | A | R | C | C | R |

Waar ik (projectmanager) **niet** A ben: de inhoud van een proces (de proceseigenaar), de configuratie (de partner), het go/no-go-besluit (de stuurgroep).

## Rapportering

- **Wekelijks:** RAID-log en defectlijst bijgewerkt, partnerverbruik in regie (migratie).
- **Elke vier weken:** statusrapport van één pagina voor de stuurgroep ([voorbeeld W18](../governance/statusrapport-w18.md)).
- **Escalatie:** risico met score ≥ 12 binnen een week naar de stuurgroep; een blokkerende datakwaliteitsfout die de eigenaar niet binnen twee weken oplost, naar de COO of CFO.

## Contractoverleg met de partner

Maandelijks, apart van het projectoverleg: verbruik in regie, openstaande CR's, mijlpaalfacturen en ingehouden bedrag, bezetting van het benoemde team ([contractafspraken](../02-partnerselectie/contractafspraken.md)). Zo blijft het wekelijkse overleg over inhoud gaan.
