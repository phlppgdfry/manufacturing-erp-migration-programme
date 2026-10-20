# RAID-log

> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.

Risico's (kans × impact, 1–5), aannames, issues en afhankelijkheden, met eigenaar. Stand bij de batenreview. Terug naar [governance](README.md).

| ID | Type | Omschrijving | Kans | Impact | Score | Eigenaar | Maatregel | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Risico | Key users niet vrij tijdens het soepseizoen (ontwerp en test vallen in oktober – februari) | 4 | 4 | 16 | COO | Interim-vervanging van vier key users gebudgetteerd (B7); testweken vooraf in de productieplanning gezet | beheerst |
| R-02 | Risico | SAP-kennis verdwijnt: de ABAP-freelancer stopt eind december | 3 | 4 | 12 | IT Manager | Extractieprogramma's vóór december laten documenteren en testen; contract verlengd tot na de go-live op afroep | beheerst |
| R-03 | Risico | Partner vervangt de lead consultant | 2 | 4 | 8 | Projectmanager | Naam in het contract, vervanging alleen met akkoord, overlap van twee weken | open |
| R-04 | Risico | Lotgegevens in SAP onvolledig (houdbaarheid, vervaldatum) | 3 | 5 | 15 | QA-manager | Datakwaliteitsregels DQ-10 tot DQ-12 vanaf proefmigratie 1; QA tekent af | werkelijkheid geworden → I-03 |
| R-05 | Risico | Certificering EDI-berichten per retailer duurt vier tot zes weken | 4 | 3 | 12 | Teamleider klantendienst | Certificering gestart in W14, parallel aan de bouw; terugval via webportaal per retailer | open |
| R-06 | Risico | BRCGS-audit in mei valt kort na de go-live | 3 | 5 | 15 | QA-manager | Mock recall als hard go/no-go-criterium; auditor vooraf informeren over de systeemwissel | open |
| R-07 | Risico | Hoofd planning blijft het Excel-planbord gebruiken naast Business Central | 4 | 3 | 12 | COO | Planner test het planningsvoorstel op een echte week; Power BI-capaciteitsoverzicht als vervanging van het visuele bord; CR-03 in fase 2 opnieuw | open |
| R-08 | Risico | Licenties: Essentials en Premium kunnen niet gemengd worden | 5 | 2 | 10 | IT Manager | Alle volledige gebruikers op Premium begroot; licht gebruik via Team Members | gesloten |
| R-09 | Risico | Scope creep: ‘dat konden we in SAP ook’ voor 146 Z-objecten | 4 | 4 | 16 | Projectmanager | Elk Z-object kreeg in het ontwerp een beslissing (standaard, app, extensie, procesaanpassing, stoppen); nieuwe wensen alleen via CR | beheerst |
| R-10 | Risico | Hypercare valt samen met de voorraadopbouw voor het BBQ-seizoen | 3 | 4 | 12 | COO | Key users twee weken vrijgesteld na de go-live; partner on site in week 1–2 | open |
| A-01 | Aanname | De EDI-provider kan inkomende orders 40 uur bufferen tijdens de cutover |  |  |  | Teamleider klantendienst | Bevestigd in de SIT (W20) | bevestigd |
| A-02 | Aanname | Retailers aanvaarden een nieuw ordernummerformaat op leverberichten |  |  |  | Teamleider klantendienst | Brief aan retailers in W19; vijf van zes bevestigd | open |
| I-01 | Issue | Partnerkeuze één week later dan gepland: referentiebezoek Partner B verschoven |  |  |  | Projectmanager | Ontwerpfase ingekort door twee workshops samen te voegen | gesloten |
| I-02 | Issue | Retailer R4 weigert DESADV (SSCC-segment) |  |  |  | Teamleider klantendienst | DEF-11; terugval via webportaal | open |
| I-03 | Issue | Halffabricaatlots zonder vervaldatum: een eigen SAP-transactie voor ontvangst van halffabricaten slaat het veld over |  |  |  | QA-manager | Vervaldatum herberekenen uit productiedatum + houdbaarheid, QA controleert steekproef, proefmigratie 4 | opgelost in W29 |
| D-01 | Afhankelijkheid | Peppol-access point actief vóór de go-live |  |  |  | CFO | Aangevraagd in W10, getest in de SIT | afgerond |
| D-02 | Afhankelijkheid | Labelsoftware-leverancier levert de nieuwe koppeling |  |  |  | Magazijnverantwoordelijke | Opgenomen in de SIT; leverancier in de cutoverbezetting | afgerond |
| D-03 | Afhankelijkheid | Koelhuis (3PL) levert dagelijks een voorraadbestand in het nieuwe formaat |  |  |  | Magazijnverantwoordelijke | Formaat afgesproken in W12, getest in de SIT | afgerond |
