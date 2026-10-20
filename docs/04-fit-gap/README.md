# Fit-gap: standaard eerst, met een beslisser per regel

> **Wat dit is:** hoe de eisen uit de workshops naast Business Central gelegd werden, met welke klassen en beslisregels. **Voor wie:** proceseigenaars, stuurgroep, partner. **Vorige:** [processen](../03-processen/README.md) · **Volgende:** [datamigratie](../05-datamigratie/README.md). **Het register:** [fit-gap.md](fit-gap.md) ([CSV](fit-gap.csv)).

## Klassen, in volgorde van voorkeur

| Klasse | Betekenis | Wie beslist |
|---|---|---|
| **Standaard** | Business Central doet het zonder meer | proceseigenaar bevestigt |
| **Configuratie** | instellingen, workflows, rapporten, Power BI | proceseigenaar |
| **ISV-app** | een app van een derde partij uit AppSource | IT Manager (licentie, leverancier, updates) |
| **Procesaanpassing** | Vaerdal past de werkwijze aan de standaard aan | proceseigenaar, met de COO of CFO als het meerdere afdelingen raakt |
| **Extensie** | eigen AL-code bovenop Business Central | **stuurgroep**, altijd ([ADR-001](../adr/adr-001-standaard-eerst.md)) |
| **Buiten scope** | niet in deze go-live; fase 2 of een andere oplossing | stuurgroep (via het charter) |

Een extensie moet drie vragen overleven: is het wettelijk of contractueel nodig? Lost een app of een procesaanpassing het niet op? Wie onderhoudt het na de go-live, bij elke halfjaarlijkse update van Business Central?

## Resultaat

<!--n:fg.total-->41<!--/n--> eisen, waarvan <!--n:fg.inScope-->35<!--/n--> in scope. Van die 35 zijn er <!--n:fg.stdConf-->26<!--/n--> (<!--n:fg.stdConfPct-->74%<!--/n-->) standaard of configuratie. Twee extensies:

| Extensie | Waarom geen standaard, app of procesaanpassing | Dagen |
|---|---|---:|
| **VK-05** Minimale resterende houdbaarheid per klant | contractuele eis van de retailers; de standaard kiest lots op FEFO maar kent geen minimum per klant; een food-app zou het kunnen, maar die brengt 40 functies mee waarvan we er één nodig hebben | 5 |
| **KW-03** Allergenen doorrekenen uit de stuklijst | wettelijk verplichte productinformatie; handmatig bijhouden bij elke receptwijziging is precies het soort fout dat in een audit gevonden wordt | 4 |

De grootste wens die het niet haalde: een grafisch planbord als extensie (CR-03, <!--n:budget.crRejected-->€48.700<!--/n--> aan afgewezen CR's in totaal). Het planningsvoorstel plus een Power BI-overzicht van de capaciteit per lijn doet 80% van het werk; na één BBQ-seizoen wordt een app opnieuw bekeken ([roadmap](../10-it-roadmap/README.md)).

## Hoe je het register leest

Elke regel heeft een ID, het domein, de eis in de woorden van de business, MoSCoW, de klasse, de oplossing, de bouwdagen van de partner, de eigenaar die beslist en het UAT-scenario dat het bewijst. De test [`tests/test_programme.py`](../../tests/test_programme.py) controleert dat elke eis in scope een scenario heeft en dat er niet meer dan drie extensies zijn.

De dagen zijn alleen het bouwwerk per eis (<!--n:fg.days-->96<!--/n--> dagen samen). Projectleiding, ontwerp, test, opleiding en migratie zitten in de vaste prijs van de partner, niet in deze kolom.
