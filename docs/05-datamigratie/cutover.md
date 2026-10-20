# Cutover-draaiboek

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Terug naar [het migratieplan](README.md). Venster: vrijdag 14:00 tot zondag 06:00 (40 uur), productie stil van vrijdag 22:00 tot zondag 06:00. In de generale repetitie (proefmigratie 3) liep het draaiboek in 37 uur; in proefmigratie 4 in 34 uur.

| Moment | Stap | Wie |
|---|---|---|
| `D-10` | Bevriezing stamgegevens in SAP (geen nieuwe artikelen, klanten, recepturen) | Data-eigenaars |
| `D-3` | Laatste aankooporders in SAP; leveranciers geïnformeerd over nieuw ordernummerformaat | Aankoop |
| `D-1 12:00` | Laatste productieorders in SAP afgewerkt; geen halffabricaat in bewerking | Planning |
| `D0 14:00` | SAP op alleen-lezen voor voorraad en verkoop; EDI-provider buffert inkomende orders | IT + EDI-provider |
| `D0 16:00` | Fysieke telling per lot in Hal 1, Hal 2 en magazijn; koelhuis levert lotlijst | Magazijn + koelhuis |
| `D0 22:00` | Extractie SAP (stamgegevens, lots, openstaande orders en posten, saldi) | Partner |
| `D1 02:00` | Datakwaliteitscontrole; blokkerende fouten = stop en escaleren | Projectmanager |
| `D1 04:00` | Inladen in productie-omgeving Business Central | Partner |
| `D1 12:00` | Afstemming voorraadwaarde, openstaande posten, grootboeksaldi; aftekening door de controller | Controller + CFO |
| `D1 16:00` | Mock recall op productie-data, aftekening QA | QA-manager |
| `D1 20:00` | Go/no-go-call: laatste beslissing, anders terugval | Stuurgroep |
| `D2 04:00` | EDI-buffer vrijgegeven naar Business Central; eerste orders gecontroleerd | Klantendienst |
| `D2 06:00` | Eerste ploeg start op Business Central; key users op de vloer | Productie + key users |

## Terugvalplan

Tot de go/no-go-call op D1 20:00 kan SAP volledig terug in gebruik: EDI-buffer terug naar SAP, telling in SAP geboekt. Daarna geen terugval meer maar voorwaarts herstellen.

Waarom geen terugval meer na D1 20:00: vanaf dan komen er orders, leveringen en productie in Business Central binnen. Teruggaan zou betekenen dat al die transacties dubbel moeten worden ingegeven in SAP. Het risico van voorwaarts herstellen is kleiner dan dat van terugdraaien.
