"""Data-quality rules that run on every SAP extract before anything is loaded into Business Central.

Each rule has an owner in the business (not in IT): the person who decides how a record is
corrected. Blocking rules stop the record from being migrated; warnings migrate with a note.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Callable

from .sap_extract import EU, be_vat_valid, iban_valid

VAT_FORMAT = {
    "NL": re.compile(r"^NL\d{9}B\d{2}$"),
    "FR": re.compile(r"^FR[0-9A-Z]{2}\d{9}$"),
    "DE": re.compile(r"^DE\d{9}$"),
}


@dataclass(frozen=True)
class Rule:
    id: str
    object: str
    title: str
    severity: str  # "blokkerend" | "waarschuwing" | "info"
    owner: str
    why: str
    check: Callable[[dict], list[dict]] = field(repr=False, compare=False)


def vat_valid(country: str, vat: str) -> bool:
    if country == "BE":
        return be_vat_valid(vat)
    pattern = VAT_FORMAT.get(country)
    return bool(pattern and pattern.match(vat))


def _stock_date(t: dict) -> date:
    return date.fromisoformat(t["_META"][0]["STOCK_DATE"])


def _in_stock(t: dict) -> set[str]:
    return {r["CHARG"] for r in t["MCHB"]}


def _active_items(t: dict) -> dict[str, dict]:
    return {m["MATNR"]: m for m in t["MARA"] if not m["LVORM"]}


def dq01(t):
    seen: dict[str, list[dict]] = {}
    for c in t["KNA1"]:
        if c["STCEG"]:
            seen.setdefault(c["STCEG"], []).append(c)
    return [{"key": c["KUNNR"], "detail": f"{c['NAME1']} · btw {c['STCEG']}"} for group in seen.values() if len(group) > 1 for c in group]


def dq02(t):
    return [{"key": c["KUNNR"], "detail": f"{c['NAME1']} ({c['LAND1']}) · btw '{c['STCEG']}'"} for c in t["KNA1"] if c["LAND1"] in EU and not vat_valid(c["LAND1"], c["STCEG"])]


def dq03(t):
    return [{"key": v["LIFNR"], "detail": f"{v['NAME1']} · IBAN {v['IBAN']}"} for v in t["LFA1"] if not iban_valid(v["IBAN"])]


def dq04(t):
    conv = {(m["MATNR"], m["MEINH"]) for m in t["MARM"]}
    return [{"key": m["MATNR"], "detail": f"verkoopeenheid {m['ZZSALES_UNIT']} zonder omrekening naar {m['MEINS']}"} for m in _active_items(t).values() if m.get("ZZSALES_UNIT") and (m["MATNR"], m["ZZSALES_UNIT"]) not in conv]


def dq05(t):
    return [{"key": m["MATNR"], "detail": "eindproduct zonder allergeneninformatie"} for m in _active_items(t).values() if m["MTART"] == "FERT" and m["ZZALLERGENS"] == ""]


def dq06(t):
    return [{"key": m["MATNR"], "detail": f"{m['MTART']} gemarkeerd voor verwijdering"} for m in t["MARA"] if m["LVORM"]]


def dq07(t):
    active = _active_items(t)
    header = {h["STLNR"]: h["MATNR"] for h in t["STKO"]}
    return [{"key": f"{header[r['STLNR']]}/{r['POSNR']}", "detail": f"component {r['IDNRK']} is niet actief"} for r in t["STPO"] if r["IDNRK"] not in active]


def bom_yield(t) -> dict[str, float]:
    """Kilograms in (components in KG) divided by kilograms out, per BOM."""
    ntgew = {m["MATNR"]: float(m["NTGEW"]) for m in t["MARA"]}
    kg_in: dict[str, float] = {}
    for r in t["STPO"]:
        if r["MEINS"] == "KG":
            kg_in[r["STLNR"]] = kg_in.get(r["STLNR"], 0.0) + float(r["MENGE"])
    result = {}
    for h in t["STKO"]:
        out = float(h["BMENG"]) if h["BMEIN"] == "KG" else float(h["BMENG"]) * ntgew[h["MATNR"]]
        result[h["STLNR"]] = kg_in.get(h["STLNR"], 0.0) / out
    return result


def dq08(t):
    header = {h["STLNR"]: h["MATNR"] for h in t["STKO"]}
    return [{"key": header[stl], "detail": f"input/output {ratio:.0%}"} for stl, ratio in bom_yield(t).items() if not 0.95 <= ratio <= 1.15]


def dq09(t):
    centers = {w["ARBPL"] for w in t["CRHD"]}
    return [{"key": f"{r['PLNNR']}/{r['VORNR']}", "detail": f"werkplek {r['ARBPL']} bestaat niet"} for r in t["PLPO"] if r["ARBPL"] not in centers]


def _lot_detail(r):
    return f"{r['MATNR']} · {r['WERKS']} · gemaakt {r['HSDAT']} · vervalt {r['VFDAT'] or '—'}"


def dq10(t):
    stock = _in_stock(t)
    return [{"key": r["CHARG"], "detail": _lot_detail(r), "mtart": {"R": "ROH", "S": "HALB", "F": "FERT"}[r["CHARG"][0]], "werks": r["WERKS"]} for r in t["MCH1"] if r["CHARG"] in stock and not r["VFDAT"]]


def dq11(t):
    stock = _in_stock(t)
    return [{"key": r["CHARG"], "detail": _lot_detail(r)} for r in t["MCH1"] if r["CHARG"] in stock and r["VFDAT"] and r["VFDAT"] < r["HSDAT"]]


def dq12(t):
    unrestricted = {r["CHARG"] for r in t["MCHB"] if float(r["CSPEM"]) == 0}
    day = _stock_date(t).isoformat()
    return [{"key": r["CHARG"], "detail": _lot_detail(r)} for r in t["MCH1"] if r["CHARG"] in unrestricted and r["VFDAT"] and r["HSDAT"] <= r["VFDAT"] < day]


def dq13(t):
    known = {c["KUNNR"] for c in t["KNA1"]}
    return [{"key": r["BELNR"], "detail": f"klant {r['KUNNR']} · €{float(r['DMBTR']):,.2f}"} for r in t["BSID"] if r["KUNNR"] not in known]


def dq14(t):
    stocked = {r["MATNR"] for r in t["MCHB"]}
    return [{"key": m["MATNR"], "detail": f"standaardprijs 0 · gemiddelde prijs €{float(m['VERPR']):.2f}"} for m in t["MBEW"] if m["MATNR"] in stocked and float(m["STPRS"]) == 0]


def dq15(t):
    return [{"key": m["SAP_ACCOUNT"], "detail": "geen rekening in het Belgische rekeningstelsel"} for m in t["GLMAP"] if not m["BC_ACCOUNT"]]


RULES = [
    Rule("DQ-01", "Klant", "Dubbel btw-nummer", "blokkerend", "Credit controller", "Twee klantfiches voor één klant splitsen kredietlimiet en omzet.", dq01),
    Rule("DQ-02", "Klant", "EU-klant zonder geldig btw-nummer", "blokkerend", "Boekhouding", "Zonder geldig btw-nummer geen intracommunautaire levering zonder btw en geen Peppol-factuur.", dq02),
    Rule("DQ-03", "Leverancier", "Ongeldige IBAN (controlegetal)", "blokkerend", "Boekhouding", "Een SEPA-betaling naar een ongeldige IBAN wordt geweigerd of komt bij de verkeerde rekening.", dq03),
    Rule("DQ-04", "Artikel", "Verkoopeenheid zonder omrekening naar de basiseenheid", "blokkerend", "Stamgegevensbeheer", "EDI-orders in dozen worden dan niet omgezet naar stuks.", dq04),
    Rule("DQ-05", "Artikel", "Eindproduct zonder allergeneninformatie", "blokkerend", "QA-manager", "Allergenen zijn wettelijk verplichte productinformatie.", dq05),
    Rule("DQ-06", "Artikel", "Artikel gemarkeerd voor verwijdering (niet migreren)", "info", "Stamgegevensbeheer", "Wat niet meer gebruikt wordt, gaat niet mee: minder data, minder fouten.", dq06),
    Rule("DQ-07", "Stuklijst", "Component is niet actief", "blokkerend", "Technoloog", "Een receptuur met een verwijderde grondstof kan niet gepland of geproduceerd worden.", dq07),
    Rule("DQ-08", "Stuklijst", "Receptuur: input/output buiten 95–115%", "waarschuwing", "Technoloog", "Te hoge of te lage hoeveelheden vertekenen kostprijs en planning.", dq08),
    Rule("DQ-09", "Routing", "Bewerking op een onbestaande werkplek", "blokkerend", "Plantmanager", "Zonder werkplek geen capaciteitsplanning en geen kostprijs.", dq09),
    Rule("DQ-10", "Lot", "Lot in voorraad zonder vervaldatum", "blokkerend", "QA-manager", "Zonder vervaldatum geen FEFO, geen controle op resterende houdbaarheid en geen volledige recall.", dq10),
    Rule("DQ-11", "Lot", "Vervaldatum vóór productiedatum", "blokkerend", "QA-manager", "Onmogelijke datum: het lot zou meteen geblokkeerd of fout gepickt worden.", dq11),
    Rule("DQ-12", "Lot", "Vervallen lot niet geblokkeerd", "waarschuwing", "QA-manager", "Wordt geblokkeerd gemigreerd; QA beslist over vernietiging.", dq12),
    Rule("DQ-13", "Openstaande post", "Klantpost zonder klant in de migratiescope", "blokkerend", "Boekhouding", "De post kan niet worden ingelezen; het saldo zou niet aansluiten.", dq13),
    Rule("DQ-14", "Waardering", "Artikel in voorraad zonder standaardprijs", "waarschuwing", "Controller", "Business Central waardeert tegen de gemiddelde prijs; het verschil met SAP wordt verklaard in de afstemming.", dq14),
    Rule("DQ-15", "Grootboek", "Rekening zonder mapping naar het Belgische rekeningstelsel", "blokkerend", "Controller", "Een saldo zonder doelrekening kan niet worden overgezet.", dq15),
]
RULE_BY_ID = {r.id: r for r in RULES}


def run(tables: dict) -> dict[str, list[dict]]:
    """Run every rule. Returns rule id → flagged records."""
    return {rule.id: rule.check(tables) for rule in RULES}


def blocked_keys(results: dict[str, list[dict]]) -> dict[str, set[str]]:
    """Per object type, the keys that may not be migrated (blocking rules and the info filter)."""
    out: dict[str, set[str]] = {}
    for rule in RULES:
        if rule.severity in ("blokkerend", "info"):
            out.setdefault(rule.object, set()).update(r["key"] for r in results[rule.id])
    return out
