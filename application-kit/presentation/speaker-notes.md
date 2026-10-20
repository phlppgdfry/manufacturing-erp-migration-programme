# Sprekersnotities bij het interviewdeck

> Bij [het deck](https://phlppgdfry.github.io/manufacturing-erp-migration-programme/deck/). Tien minuten, acht slides. Per slide: wat je zegt, en de vraag die je kunt verwachten.

| Slide | Wat je zegt | Verwachte vraag | Kort antwoord + waar het staat |
|---|---|---|---|
| Titel | "Een fictieve case: hoe ik een ERP-migratie aan de klantkant zou leiden." | "Waarom fictief?" | "Ik heb dit niet in een bedrijf gedaan; ik wil tonen hoe ik denk, zonder bedrijfsgegevens te gebruiken." |
| 1 Probleem | onderhoud stopt, seizoenen, papier | "Waarom niet S/4HANA?" | omvang en kost; [business case](../../docs/01-mobilisatie/business-case.md) |
| 2 Hoe ik begon | criteria vóór offertes, demoscript, workshops met echte documenten | "Waarom weegt prijs zo weinig?" | het verschil tussen offertes was kleiner dan één maand vertraging; [partnerselectie](../../docs/02-partnerselectie/README.md) |
| 3 Ontwerp | lots als ruggengraat, lotnummers ongewijzigd | "Waarom geen historiek migreren?" | archief, tien jaar; [ADR-003](../../docs/adr/adr-003-geen-historiek-wel-archief.md) |
| 4 Standaard eerst | 146 → 2 extensies; extensies naar de stuurgroep | "En als de planner zijn planbord wil?" | luisteren, eigen week laten plannen, Power BI, CR na één seizoen; [verandering](../../docs/07-verandering/README.md) |
| 5 Migratie | zelfde aantal, andere lots → bron | "Wie schoont data op, de partner?" | nee, de data-eigenaar; [contractafspraken](../../docs/02-partnerselectie/contractafspraken.md) |
| 6 Beslissing | criteria vooraf, vier opties, stuurgroep beslist | "Zou je niet toch live gaan met een workaround?" | een hard criterium dat je op de dag kwijtscheldt, is geen criterium; [go/no-go](../../docs/08-go-live/go-no-go.md) |
| 7 Over mij | business-kant, afspraken vooraf, slecht nieuws concreet | "Wat zou je anders doen?" | bij proefmigratie 2 niet alleen tellen maar ook kijken welke lots; [datamigratie](../../docs/05-datamigratie/README.md#het-verhaal-van-de-halffabricaatlots-dq-10) |
