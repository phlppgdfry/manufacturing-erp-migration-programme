# ADR-008 — Lotnummers uit SAP ongewijzigd overnemen

**Status:** aanvaard (W11, DEC-05) · **Beslist door:** QA-manager · **Terug naar:** [ADR's](README.md)

## Context

De partner stelde voor om lots bij de migratie een nieuw nummer te geven volgens de nummering van Business Central. Op de dag van de go-live liggen er bijna 4.000 lots in voorraad, met het SAP-lotnummer op het etiket, in het koelhuis en in de papieren batchrecords. De genealogie van die lots blijft in het SAP-archief ([ADR-003](adr-003-geen-historiek-wel-archief.md)).

## Opties

1. **Hernummeren, met een kruistabel oud → nieuw.** Elke recall over de go-live heen gaat via een kruistabel: één stap meer, onder tijdsdruk.
2. **Ongewijzigd overnemen.** Hetzelfde nummer op het etiket, in Business Central en in het archief. Nieuwe lots krijgen een eigen nummerreeks met een ander voorvoegsel.

## Besluit

Optie 2. Leverancierslots (MCH1-LICHA) gaan ook mee, zodat een melding van een leverancier meteen naar een intern lot leidt.

## Gevolgen

- De recall loopt naadloos van Business Central naar het archief ([recall](../03-processen/recall.md)).
- De mock recall in de migratie test precies dit: elk afgeleid lot in voorraad moet in Business Central staan met zijn originele nummer en een vervaldatum.
