# Datakwaliteit per proefmigratie

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Terug naar [het migratieplan](README.md). De regels zelf staan in [`erpcase/rules.py`](../../erpcase/rules.py); de testen controleren dat elke regel precies de fouten vindt die in de extracten zitten.

| Regel | Object | Controle | Ernst | Eigenaar | Proefmigratie 1 | Proefmigratie 2 | Proefmigratie 3 | Proefmigratie 4 |
|---|---|---|---|---|---|---|---|---|
| DQ-01 | Klant | Dubbel btw-nummer | blokkerend | Credit controller | 14 | 4 | 0 | 0 |
| DQ-02 | Klant | EU-klant zonder geldig btw-nummer | blokkerend | Boekhouding | 23 | 6 | 0 | 0 |
| DQ-03 | Leverancier | Ongeldige IBAN (controlegetal) | blokkerend | Boekhouding | 9 | 2 | 0 | 0 |
| DQ-04 | Artikel | Verkoopeenheid zonder omrekening naar de basiseenheid | blokkerend | Stamgegevensbeheer | 61 | 12 | 0 | 0 |
| DQ-05 | Artikel | Eindproduct zonder allergeneninformatie | blokkerend | QA-manager | 48 | 9 | 0 | 0 |
| DQ-06 | Artikel | Artikel gemarkeerd voor verwijdering (niet migreren) | info | Stamgegevensbeheer | 312 | 312 | 312 | 312 |
| DQ-07 | Stuklijst | Component is niet actief | blokkerend | Technoloog | 17 | 3 | 0 | 0 |
| DQ-08 | Stuklijst | Receptuur: input/output buiten 95–115% | waarschuwing | Technoloog | 22 | 9 | 4 | 4 |
| DQ-09 | Routing | Bewerking op een onbestaande werkplek | blokkerend | Plantmanager | 6 | 0 | 0 | 0 |
| DQ-10 | Lot | Lot in voorraad zonder vervaldatum | blokkerend | QA-manager | 214 | 104 | 107 | 0 |
| DQ-11 | Lot | Vervaldatum vóór productiedatum | blokkerend | QA-manager | 12 | 3 | 0 | 0 |
| DQ-12 | Lot | Vervallen lot niet geblokkeerd | waarschuwing | QA-manager | 37 | 18 | 9 | 3 |
| DQ-13 | Openstaande post | Klantpost zonder klant in de migratiescope | blokkerend | Boekhouding | 8 | 2 | 0 | 0 |
| DQ-14 | Waardering | Artikel in voorraad zonder standaardprijs | waarschuwing | Controller | 41 | 15 | 6 | 2 |
| DQ-15 | Grootboek | Rekening zonder mapping naar het Belgische rekeningstelsel | blokkerend | Controller | 5 | 1 | 0 | 0 |
|  |  | **Blokkerend totaal** |  |  | **417** | **146** | **107** | **0** |

## Zelfde fouten of nieuwe fouten?

Per regel: hoeveel gemelde records al in de vorige proefmigratie gemeld waren (bekend) en hoeveel nieuw zijn. Een gelijk aantal met nieuwe sleutels betekent dat de bron nog fouten maakt.

| Regel | Controle | Proefmigratie 1 | Proefmigratie 2 | Proefmigratie 3 | Proefmigratie 4 |
|---|---|---|---|---|---|
| DQ-01 | Dubbel btw-nummer | — | 0 nieuw / 4 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-02 | EU-klant zonder geldig btw-nummer | — | 0 nieuw / 6 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-03 | Ongeldige IBAN (controlegetal) | — | 0 nieuw / 2 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-04 | Verkoopeenheid zonder omrekening naar de basiseenheid | — | 0 nieuw / 12 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-05 | Eindproduct zonder allergeneninformatie | — | 0 nieuw / 9 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-07 | Component is niet actief | — | 0 nieuw / 3 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-08 | Receptuur: input/output buiten 95–115% | — | 0 nieuw / 9 bekend | 0 nieuw / 4 bekend | 0 nieuw / 4 bekend |
| DQ-10 | Lot in voorraad zonder vervaldatum | — | 104 nieuw / 0 bekend | 107 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-11 | Vervaldatum vóór productiedatum | — | 3 nieuw / 0 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-12 | Vervallen lot niet geblokkeerd | — | 18 nieuw / 0 bekend | 9 nieuw / 0 bekend | 3 nieuw / 0 bekend |
| DQ-13 | Klantpost zonder klant in de migratiescope | — | 2 nieuw / 0 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |
| DQ-14 | Artikel in voorraad zonder standaardprijs | — | 9 nieuw / 6 bekend | 6 nieuw / 0 bekend | 2 nieuw / 0 bekend |
| DQ-15 | Rekening zonder mapping naar het Belgische rekeningstelsel | — | 0 nieuw / 1 bekend | 0 nieuw / 0 bekend | 0 nieuw / 0 bekend |

## Waarom DQ-10 in proefmigratie 3 nog niet op nul stond

Verdeling van de 107 lots zonder vervaldatum in proefmigratie 3 (artikeltype · fabriek): **HALB · HAL2: 107**. Alle fouten zitten in halffabricaten uit Hal 2, en **107 van de 107 lots waren nieuw** ten opzichte van proefmigratie 2 (al eerder gemeld: 0). Na proefmigratie 2 had QA de bestaande lots in SAP verbeterd, maar een eigen SAP-transactie voor de ontvangst van halffabricaten bleef nieuwe lots zonder vervaldatum maken. Opschonen zonder de bron te herstellen is dweilen met de kraan open. Zie [I-03 in de RAID-log](../governance/raid.md) en [het go/no-go-besluit](../08-go-live/go-no-go.md).

Voorbeelden uit het extract:

- `S66700009` — SF-20054 · HAL2 · gemaakt 2026-02-16 · vervalt —
- `S66700021` — SF-20027 · HAL2 · gemaakt 2026-02-18 · vervalt —
- `S66700123` — SF-20048 · HAL2 · gemaakt 2026-02-19 · vervalt —
- `S66700121` — SF-20002 · HAL2 · gemaakt 2026-02-19 · vervalt —
- `S66700016` — SF-20194 · HAL2 · gemaakt 2026-02-18 · vervalt —

## Waarom elke regel bestaat

- **DQ-01 Dubbel btw-nummer** — Twee klantfiches voor één klant splitsen kredietlimiet en omzet.
- **DQ-02 EU-klant zonder geldig btw-nummer** — Zonder geldig btw-nummer geen intracommunautaire levering zonder btw en geen Peppol-factuur.
- **DQ-03 Ongeldige IBAN (controlegetal)** — Een SEPA-betaling naar een ongeldige IBAN wordt geweigerd of komt bij de verkeerde rekening.
- **DQ-04 Verkoopeenheid zonder omrekening naar de basiseenheid** — EDI-orders in dozen worden dan niet omgezet naar stuks.
- **DQ-05 Eindproduct zonder allergeneninformatie** — Allergenen zijn wettelijk verplichte productinformatie.
- **DQ-06 Artikel gemarkeerd voor verwijdering (niet migreren)** — Wat niet meer gebruikt wordt, gaat niet mee: minder data, minder fouten.
- **DQ-07 Component is niet actief** — Een receptuur met een verwijderde grondstof kan niet gepland of geproduceerd worden.
- **DQ-08 Receptuur: input/output buiten 95–115%** — Te hoge of te lage hoeveelheden vertekenen kostprijs en planning.
- **DQ-09 Bewerking op een onbestaande werkplek** — Zonder werkplek geen capaciteitsplanning en geen kostprijs.
- **DQ-10 Lot in voorraad zonder vervaldatum** — Zonder vervaldatum geen FEFO, geen controle op resterende houdbaarheid en geen volledige recall.
- **DQ-11 Vervaldatum vóór productiedatum** — Onmogelijke datum: het lot zou meteen geblokkeerd of fout gepickt worden.
- **DQ-12 Vervallen lot niet geblokkeerd** — Wordt geblokkeerd gemigreerd; QA beslist over vernietiging.
- **DQ-13 Klantpost zonder klant in de migratiescope** — De post kan niet worden ingelezen; het saldo zou niet aansluiten.
- **DQ-14 Artikel in voorraad zonder standaardprijs** — Business Central waardeert tegen de gemiddelde prijs; het verschil met SAP wordt verklaard in de afstemming.
- **DQ-15 Rekening zonder mapping naar het Belgische rekeningstelsel** — Een saldo zonder doelrekening kan niet worden overgezet.
