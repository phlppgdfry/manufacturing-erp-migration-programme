# Mapping SAP ECC → Business Central

> **Wat dit is:** per object welke SAP-tabellen de bron zijn, welke velden waar terechtkomen en welke regels gelden. **Voor wie:** partner (bouwt het), data-eigenaars (begrijpen het), controller en QA (tekenen af). **Terug naar:** [datamigratie](README.md). **Code:** [`erpcase/transform.py`](../../erpcase/transform.py).

De SAP-tabellen zijn de gangbare ECC-tabellen; in deze case vereenvoudigd tot de velden die de migratie nodig heeft. De doelvelden zijn de Business Central-veldnamen die een configuratiepakket of de API gebruikt.

## Klanten (KNA1 → Customer)

| SAP | Business Central | Regel |
|---|---|---|
| KNA1-KUNNR | No. | ongewijzigd: de EDI-provider en de retailers kennen dit nummer |
| KNA1-NAME1 | Name | |
| KNA1-LAND1 | Country/Region Code | |
| KNA1-STCEG | VAT Registration No. | DQ-01 (dubbel), DQ-02 (geldig voor EU) |
| afgeleid van LAND1 | Gen. Bus. Posting Group, VAT Bus. Posting Group | BE → BINNENL · NL/FR/DE → EU · overige → EXPORT |
| afgeleid van LAND1 | Customer Posting Group | BE → BINNEN · anders BUITEN |

## Leveranciers (LFA1 + LFBK → Vendor)

| SAP | Business Central | Regel |
|---|---|---|
| LFA1-LIFNR | No. | ongewijzigd |
| LFA1-NAME1, LAND1, STCEG | Name, Country/Region Code, VAT Registration No. | |
| LFBK (IBAN) | Vendor Bank Account → IBAN | DQ-03: controlegetal mod 97 (ISO 13616) |

## Artikels (MARA, MAKT, MARM, MBEW → Item)

| SAP | Business Central | Regel |
|---|---|---|
| MARA-MATNR | No. | ongewijzigd |
| MAKT-MAKTX | Description | |
| MARA-MEINS | Base Unit of Measure | ST → STUK · KG → KG |
| MARM (KAR) | Item Unit of Measure DOOS | DQ-04: verkoopeenheid zonder omrekening blokkeert |
| MARA-MTART | Inventory Posting Group | FERT → GEREED · HALB → HALFFABR · ROH → GRONDST · VERP → VERPAK |
| MARA-MTART | Replenishment System | FERT, HALB → Prod. Order · ROH, VERP → Purchase |
| MARA-MTART | Item Tracking Code | LOTVERV (lot + verplichte vervaldatum) voor alles behalve verpakking |
| MARA-MHDHB (totale houdbaarheid) | Expiration Calculation | `<dagen>D` |
| MARA-MHDRZ (min. resterende houdbaarheid) | veld van extensie VK-05 | per artikel; per klant overschrijfbaar |
| MARA-ZZALLERGENS (eigen veld) | artikelkenmerk Allergenen | DQ-05: verplicht voor eindproducten |
| MBEW-STPRS / PEINH | Unit Cost (Costing Method Standard) | DQ-14: als STPRS = 0, de gemiddelde prijs MBEW-VERPR |
| MARA-LVORM | — | DQ-06: gemarkeerd voor verwijdering = niet migreren |

## Recepturen en routings (STKO/STPO, PLKO/PLPO/CRHD → Production BOM, Routing)

| SAP | Business Central | Regel |
|---|---|---|
| STKO-MATNR | Production BOM Header No. = `P` + artikelnummer, Status Certified | |
| STPO-IDNRK | Production BOM Line No. | DQ-07: component moet actief zijn |
| STPO-MENGE / STKO-BMENG | Quantity per | basishoeveelheid 100 → per eenheid |
| STPO-AUSCH | Scrap % | |
| — | — | DQ-08: kg in / kg uit tussen 95 en 115% (waarschuwing) |
| PLKO-PLNNR | Routing No. | |
| PLPO-ARBPL | Routing Line → Work Center / Machine Center | DQ-09: werkplek moet bestaan in CRHD |

## Lots in voorraad (MCH1 + MCHB → Item Journal met artikeltracering)

| SAP | Business Central | Regel |
|---|---|---|
| MCHB-CHARG | Lot No. | **ongewijzigd** ([ADR-008](../adr/adr-008-lotnummers-behouden.md)) |
| MCH1-VFDAT | Expiration Date | DQ-10 (leeg blokkeert), DQ-11 (vóór productiedatum blokkeert) |
| MCHB-CLABS | Quantity | |
| MCHB-LGORT | Location Code | GRST, EIND → MAG · KOEL → KOEL · BULK → HAL1 of HAL2 volgens fabriek |
| MCHB-CSPEM > 0, of vervallen | Lot No. Information → Blocked | DQ-12: vervallen en niet geblokkeerd → geblokkeerd migreren |
| MCH1-LICHA | Lot No. Information → leverancierslot | nodig om een melding van de leverancier te vertalen naar een intern lot |
| CHVW (genealogie) | — | blijft in het archief; wordt gebruikt voor de mock recall |

## Openstaande posten en grootboek

| SAP | Business Central | Regel |
|---|---|---|
| BSID per document | Sales journal tegen overgangsrekening, per document | DQ-13: klant moet in de migratiescope zitten |
| BSIK per document | Purchase journal tegen overgangsrekening | |
| FAGLFLEXT-saldi | General journal opening per rekening, + saldi per maand lopend boekjaar | DQ-15: mapping naar het Belgische rekeningstelsel verplicht |

De overgangsrekening moet na het laden van posten en saldi op nul staan. Dat is de eerste afstemming die de controller aftekent ([afstemming](afstemming.md)).
