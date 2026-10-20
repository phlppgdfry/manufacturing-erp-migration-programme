# Afstemming per proefmigratie

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Terug naar [het migratieplan](README.md). Elk verschil heeft een verklaring of het is een fout. Het voorraadverschil = waarde van lots die niet mochten mee (blokkerende fouten) + artikels die in SAP op nul stonden en in Business Central de gemiddelde prijs krijgen (DQ-14, beslissing van de controller).

| Proefmigratie | Voorraad SAP | Voorraad BC | Verschil | % | Niet gemigreerde lots | Gemiddelde prijs i.p.v. 0 | Klantposten | Leveranciersposten | Grootboek sluit |
|---|---|---|---|---|---|---|---|---|---|
| Proefmigratie 1 | €4.986.969 | €4.106.452 | -€880.517 | 17,656% | €887.518 | €7.001 | -€1.120.121,90 | €133.168,43 | nee |
| Proefmigratie 2 | €5.010.349 | €4.770.687 | -€239.661 | 4,783% | €242.588 | €2.927 | -€383.573,12 | €54.966,59 | nee |
| Proefmigratie 3 (generale repetitie) | €4.951.012 | €4.845.503 | -€105.508 | 2,131% | €106.717 | €1.209 | €0,00 | €0,00 | ja |
| Proefmigratie 4 | €4.899.433 | €4.899.984 | €551 | 0,011% | €0 | €551 | €0,00 | €0,00 | ja |

## Aantallen per object

| Proefmigratie | SAP | Business Central | Bron | Gemigreerd | Niet gemigreerd |
|---|---|---|---|---|---|
| Proefmigratie 1 | KNA1 | Customer | 412 | 375 | 37 |
| Proefmigratie 1 | LFA1 (+LFBK) | Vendor | 286 | 277 | 9 |
| Proefmigratie 1 | MARA/MAKT/MARM/MBEW | Item | 2.186 | 1.769 | 417 |
| Proefmigratie 1 | STKO/STPO | Production BOM Header | 856 | 736 | 120 |
| Proefmigratie 1 | PLKO/PLPO/CRHD | Routing Header | 38 | 32 | 6 |
| Proefmigratie 1 | MCH1/MCHB | Item Journal (lots) | 3.960 | 3.348 | 612 |
| Proefmigratie 1 | BSID | Cust. Ledger (open) | 1.320 | 1.188 | 132 |
| Proefmigratie 1 | BSIK | Vend. Ledger (open) | 690 | 673 | 17 |
| Proefmigratie 1 | FAGLFLEXT (saldi) | G/L Opening | 118 | 113 | 5 |
| Proefmigratie 2 | KNA1 | Customer | 412 | 402 | 10 |
| Proefmigratie 2 | LFA1 (+LFBK) | Vendor | 286 | 284 | 2 |
| Proefmigratie 2 | MARA/MAKT/MARM/MBEW | Item | 2.186 | 1.853 | 333 |
| Proefmigratie 2 | STKO/STPO | Production BOM Header | 856 | 832 | 24 |
| Proefmigratie 2 | PLKO/PLPO/CRHD | Routing Header | 38 | 38 | 0 |
| Proefmigratie 2 | MCH1/MCHB | Item Journal (lots) | 3.960 | 3.780 | 180 |
| Proefmigratie 2 | BSID | Cust. Ledger (open) | 1.320 | 1.284 | 36 |
| Proefmigratie 2 | BSIK | Vend. Ledger (open) | 690 | 683 | 7 |
| Proefmigratie 2 | FAGLFLEXT (saldi) | G/L Opening | 118 | 117 | 1 |
| Proefmigratie 3 | KNA1 | Customer | 412 | 412 | 0 |
| Proefmigratie 3 | LFA1 (+LFBK) | Vendor | 286 | 286 | 0 |
| Proefmigratie 3 | MARA/MAKT/MARM/MBEW | Item | 2.186 | 1.874 | 312 |
| Proefmigratie 3 | STKO/STPO | Production BOM Header | 856 | 856 | 0 |
| Proefmigratie 3 | PLKO/PLPO/CRHD | Routing Header | 38 | 38 | 0 |
| Proefmigratie 3 | MCH1/MCHB | Item Journal (lots) | 3.960 | 3.853 | 107 |
| Proefmigratie 3 | BSID | Cust. Ledger (open) | 1.320 | 1.320 | 0 |
| Proefmigratie 3 | BSIK | Vend. Ledger (open) | 690 | 690 | 0 |
| Proefmigratie 3 | FAGLFLEXT (saldi) | G/L Opening | 118 | 118 | 0 |
| Proefmigratie 4 | KNA1 | Customer | 412 | 412 | 0 |
| Proefmigratie 4 | LFA1 (+LFBK) | Vendor | 286 | 286 | 0 |
| Proefmigratie 4 | MARA/MAKT/MARM/MBEW | Item | 2.186 | 1.874 | 312 |
| Proefmigratie 4 | STKO/STPO | Production BOM Header | 856 | 856 | 0 |
| Proefmigratie 4 | PLKO/PLPO/CRHD | Routing Header | 38 | 38 | 0 |
| Proefmigratie 4 | MCH1/MCHB | Item Journal (lots) | 3.960 | 3.960 | 0 |
| Proefmigratie 4 | BSID | Cust. Ledger (open) | 1.320 | 1.320 | 0 |
| Proefmigratie 4 | BSIK | Vend. Ledger (open) | 690 | 690 | 0 |
| Proefmigratie 4 | FAGLFLEXT (saldi) | G/L Opening | 118 | 118 | 0 |
