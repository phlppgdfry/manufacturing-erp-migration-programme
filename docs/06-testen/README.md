# Teststrategie

> **Wat dit is:** wat we testen, wie test, wanneer een testfase mag starten en wanneer ze klaar is. **Voor wie:** key users, partner, stuurgroep. **Vorige:** [datamigratie](../05-datamigratie/README.md) · **Volgende:** [verandering](../07-verandering/README.md). **Scenario's en defects:** [uat-scenarios.md](uat-scenarios.md).

## Wie test wat

| Fase | Week | Wie | Wat | Op welke data |
|---|---|---|---|---|
| Unit en configuratie | doorlopend | partner | elke instelling en extensie werkt zoals ontworpen | demodata |
| CRP1 | W14 | key users + partner | het standaardproces op onze artikelen: "zo zou het gaan" | eigen artikelen, handmatig |
| CRP2 | W17 | key users | het ingerichte proces met extensies en apps | eigen artikelen |
| SIT | W20 | partner + leveranciers | EDI, labels, koelhuis, Peppol, bank — met echte berichten | proefmigratie 1 |
| UAT | W23 | key users | <!--n:uat.scenarios-->17<!--/n--> end-to-end scenario's, ook uitzonderingen | proefmigratie 2 |
| Generale repetitie | W24 | iedereen | volledig cutover-draaiboek op tijd, afstemming, mock recall | proefmigratie 3 |

## Instap- en uitstapcriteria UAT

**Instap:** CRP2 afgetekend · SIT zonder open ernst 1 · proefmigratie 2 geladen en afgestemd · key users opgeleid · scenario's geschreven door de key users zelf en nagelezen door mij.

**Uitstap:** elk scenario uitgevoerd · geen open ernst 1 · ten hoogste twee open ernst 2, elk met een aanvaarde workaround · aftekening per domein door de proceseigenaar.

## Ernst van een defect

| Ernst | Betekenis | Voorbeeld |
|---|---|---|
| 1 | blokkeert een kernproces, geen omweg | btw-boekingsgroep ontbreekt bij Franse klanten: geen factuur mogelijk (DEF-02, opgelost) |
| 2 | kernproces met omweg | DESADV van retailer R4 geweigerd; omweg via het portaal van de retailer (DEF-11) |
| 3 | hinderlijk, geen impact op levering of boekhouding | datumformaat op het paletlabel (DEF-14) |

## Waarom de key users de scenario's zelf schrijven

Een scenario dat de partner schrijft, test wat de partner gebouwd heeft. Een scenario dat de planner schrijft, test of de planner er maandagochtend mee kan plannen. Ik lever het sjabloon (doel, startsituatie, stappen, verwacht resultaat, wat als het misgaat) en lees elk scenario na op twee dingen: zit er een uitzondering in, en is het verwachte resultaat controleerbaar?

Voorbeeld (UAT-04, picken met houdbaarheid):

```text
Gegeven  retailer R1 eist minstens 2/3 resterende houdbaarheid (160 van 240 dagen)
En       er liggen twee lots van FG-10132: lot A vervalt over 120 dagen, lot B over 200 dagen
Wanneer  het magazijn een order van R1 pickt met de scanner
Dan      stelt de scanner lot B voor (FEFO binnen wat voor R1 mag)
En       wordt een scan van lot A geweigerd met de reden "resterende houdbaarheid te kort voor R1"
```

## Resultaten

UAT: <!--n:uat.scenarios-->17<!--/n--> scenario's uitgevoerd, 15 geslaagd, 2 geslaagd met een open defect, 0 gefaald. Twee open defects van ernst 2 bij go/no-go 1 (DEF-07 uitval, DEF-11 R4), beide met workaround; opgelost vóór go/no-go 2. Overzicht en traceerbaarheid naar de eisen: [uat-scenarios.md](uat-scenarios.md).
