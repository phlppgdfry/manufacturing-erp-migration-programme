"""SAP → Business Central: mapping, reconciliation and the mock recall.

The output records use Business Central field names (No., Gen. Bus. Posting Group, Lot No.,
Expiration Date …). They are what a configuration package or the standard API would load;
nothing here talks to a real Business Central environment.
"""
from __future__ import annotations

import random
from collections import defaultdict
from datetime import date

from . import rules
from .sap_extract import EU

UOM = {"ST": "STUK", "KG": "KG", "KAR": "DOOS"}
INV_POSTING_GROUP = {"FERT": "GEREED", "HALB": "HALFFABR", "ROH": "GRONDST", "VERP": "VERPAK"}
LOCATION = {"GRST": "MAG", "BULK": None, "EIND": "MAG", "KOEL": "KOEL"}  # BULK → the hall that made it


def posting_group(country: str) -> str:
    """Gen./VAT Bus. Posting Group in the Belgian setup: domestic, EU, or export."""
    if country == "BE":
        return "BINNENL"
    return "EU" if country in EU else "EXPORT"


def unit_cost(mbew: dict) -> float:
    """Standard price per base unit; average price when the standard price is missing (DQ-14)."""
    std = float(mbew["STPRS"]) / float(mbew["PEINH"])
    return std if std > 0 else float(mbew["VERPR"]) / float(mbew["PEINH"])


def transform(t: dict, results: dict[str, list[dict]]) -> dict[str, list[dict]]:
    blocked = rules.blocked_keys(results)
    expired = {r["key"] for r in results["DQ-12"]}
    items = {m["MATNR"]: m for m in t["MARA"] if m["MATNR"] not in blocked.get("Artikel", set())}
    mbew = {m["MATNR"]: m for m in t["MBEW"]}

    customers = [
        {"No.": c["KUNNR"], "Name": c["NAME1"], "Country/Region Code": c["LAND1"], "VAT Registration No.": c["STCEG"],
         "Gen. Bus. Posting Group": posting_group(c["LAND1"]), "VAT Bus. Posting Group": posting_group(c["LAND1"]),
         "Customer Posting Group": "BINNEN" if c["LAND1"] == "BE" else "BUITEN"}
        for c in t["KNA1"] if c["KUNNR"] not in blocked.get("Klant", set())
    ]
    vendors = [
        {"No.": v["LIFNR"], "Name": v["NAME1"], "Country/Region Code": v["LAND1"], "VAT Registration No.": v["STCEG"],
         "Gen. Bus. Posting Group": posting_group(v["LAND1"]), "IBAN": v["IBAN"]}
        for v in t["LFA1"] if v["LIFNR"] not in blocked.get("Leverancier", set())
    ]
    bc_items = [
        {"No.": m["MATNR"], "Base Unit of Measure": UOM[m["MEINS"]], "Inventory Posting Group": INV_POSTING_GROUP[m["MTART"]],
         "Replenishment System": "Prod. Order" if m["MTART"] in ("FERT", "HALB") else "Purchase",
         "Item Tracking Code": "LOTVERV" if m["MTART"] != "VERP" else "",
         "Expiration Calculation": f"{m['MHDHB']}D" if m["MTART"] != "VERP" else "",
         "Costing Method": "Standard", "Unit Cost": round(unit_cost(mbew[m["MATNR"]]), 5),
         "Allergens": m["ZZALLERGENS"], "Min. Remaining Shelf Life (days)": m["MHDRZ"]}
        for m in items.values()
    ]
    bom_blocked = {k.split("/")[0] for k in blocked.get("Stuklijst", set())}
    header = {h["STLNR"]: h for h in t["STKO"]}
    boms, bom_lines = [], []
    for stl, h in header.items():
        if h["MATNR"] not in items or h["MATNR"] in bom_blocked:
            continue
        boms.append({"No.": f"P{h['MATNR']}", "Item No.": h["MATNR"], "Unit of Measure Code": UOM[h["BMEIN"]], "Status": "Certified", "Base Qty": h["BMENG"]})
    for r in t["STPO"]:
        h = header[r["STLNR"]]
        if h["MATNR"] in items and h["MATNR"] not in bom_blocked:
            bom_lines.append({"Production BOM No.": f"P{h['MATNR']}", "Line No.": int(r["POSNR"]) * 100, "No.": r["IDNRK"],
                              "Quantity per": round(float(r["MENGE"]) / float(h["BMENG"]), 5), "Unit of Measure Code": UOM[r["MEINS"]], "Scrap %": float(r["AUSCH"])})
    routing_blocked = {k.split("/")[0] for k in blocked.get("Routing", set())}
    routings = [{"No.": p["PLNNR"], "Description": p["KTEXT"], "Status": "Certified"} for p in t["PLKO"] if p["PLNNR"] not in routing_blocked]

    lot_master = {r["CHARG"]: r for r in t["MCH1"]}
    blocked_lots = blocked.get("Lot", set())
    lots, excluded_lots = [], []
    for s in t["MCHB"]:
        lot = lot_master[s["CHARG"]]
        location = LOCATION[s["LGORT"]] or ("HAL1" if s["WERKS"] == "HAL1" else "HAL2")
        line = {"Item No.": s["MATNR"], "Location Code": location, "Lot No.": s["CHARG"],  # ADR-008: lot numbers unchanged
                "Expiration Date": lot["VFDAT"], "Quantity": float(s["CLABS"]),
                "Unit Cost": round(unit_cost(mbew[s["MATNR"]]), 5),
                "Lot Blocked": s["CHARG"] in expired or float(s["CSPEM"]) > 0}
        if s["CHARG"] in blocked_lots or s["MATNR"] not in items:
            excluded_lots.append(line)
        else:
            lots.append(line)
    migrated_customers = {c["No."] for c in customers}
    migrated_vendors = {v["No."] for v in vendors}
    open_ar = [r for r in t["BSID"] if r["BELNR"] not in blocked.get("Openstaande post", set()) and r["KUNNR"] in migrated_customers]
    open_ap = [r for r in t["BSIK"] if r["LIFNR"] in migrated_vendors]
    gl = {m["SAP_ACCOUNT"]: m["BC_ACCOUNT"] for m in t["GLMAP"]}
    gl_lines = [{"G/L Account No.": gl[g["RACCT"]], "Amount": float(g["BALANCE"])} for g in t["GLBAL"] if gl.get(g["RACCT"])]
    return {"Customer": customers, "Vendor": vendors, "Item": bc_items, "Production BOM Header": boms, "Production BOM Line": bom_lines,
            "Routing Header": routings, "Item Journal (lots)": lots, "_excluded_lots": excluded_lots,
            "Cust. Ledger (open)": open_ar, "Vend. Ledger (open)": open_ap, "G/L Opening": gl_lines}


def _signed(r: dict) -> float:
    return float(r["DMBTR"]) * (-1 if r["SHKZG"] == "H" else 1)


def reconcile(t: dict, bc: dict) -> dict:
    """Totals in SAP vs what Business Central would contain after loading."""
    mbew = {m["MATNR"]: m for m in t["MBEW"]}
    sap_stock = sum(float(s["CLABS"]) * float(mbew[s["MATNR"]]["STPRS"]) / float(mbew[s["MATNR"]]["PEINH"]) for s in t["MCHB"])
    bc_stock = sum(line["Quantity"] * line["Unit Cost"] for line in bc["Item Journal (lots)"])
    excluded_value = sum(float(line["Quantity"]) * float(mbew[line["Item No."]]["STPRS"]) / float(mbew[line["Item No."]]["PEINH"]) for line in bc["_excluded_lots"])
    fallback_value = sum(line["Quantity"] * line["Unit Cost"] for line in bc["Item Journal (lots)"] if float(mbew[line["Item No."]]["STPRS"]) == 0)
    sap_ar = sum(_signed(r) for r in t["BSID"])
    bc_ar = sum(_signed(r) for r in bc["Cust. Ledger (open)"])
    sap_ap = sum(_signed(r) for r in t["BSIK"])
    bc_ap = sum(_signed(r) for r in bc["Vend. Ledger (open)"])
    gl_unmapped = sum(abs(float(g["BALANCE"])) for g in t["GLBAL"]) - sum(abs(line["Amount"]) for line in bc["G/L Opening"])
    by_group: dict[str, list[float]] = defaultdict(lambda: [0.0, 0.0])
    group_of = {m["MATNR"]: m["MTART"] for m in t["MARA"]}
    for s in t["MCHB"]:
        by_group[group_of[s["MATNR"]]][0] += float(s["CLABS"]) * float(mbew[s["MATNR"]]["STPRS"])
    for line in bc["Item Journal (lots)"]:
        by_group[group_of[line["Item No."]]][1] += line["Quantity"] * line["Unit Cost"]
    stock_diff = bc_stock - sap_stock
    return {
        "stock": {"sap": round(sap_stock, 2), "bc": round(bc_stock, 2), "diff": round(stock_diff, 2),
                  "diffPct": round(abs(stock_diff) / sap_stock * 100, 3),
                  "explained": {"excludedLots": round(-excluded_value, 2), "averagePriceFallback": round(fallback_value, 2)},
                  "byGroup": {k: {"sap": round(v[0], 2), "bc": round(v[1], 2)} for k, v in sorted(by_group.items())}},
        "ar": {"sap": round(sap_ar, 2), "bc": round(bc_ar, 2), "diff": round(bc_ar - sap_ar, 2)},
        "ap": {"sap": round(sap_ap, 2), "bc": round(bc_ap, 2), "diff": round(bc_ap - sap_ap, 2)},
        "glUnmappedAbs": round(gl_unmapped, 2),
        "glBalanced": round(sum(line["Amount"] for line in bc["G/L Opening"]), 2) == 0 and gl_unmapped == 0,
    }


def descendants(t: dict, lot: str) -> set[str]:
    """Every lot that (directly or indirectly) consumed this lot, according to the batch where-used list."""
    children: dict[str, list[str]] = defaultdict(list)
    for r in t["CHVW"]:
        children[r["CHARG_COMP"]].append(r["CHARG_PARENT"])
    found, todo = set(), [lot]
    while todo:
        for child in children.get(todo.pop(), []):
            if child not in found:
                found.add(child)
                todo.append(child)
    return found


def mock_recall(t: dict, bc: dict, sample: int = 25) -> dict:
    """Forward trace from raw-material lots: is every derived lot in stock present in Business Central
    with lot number and expiration date? Same sample in every mock: the 25 raw-material lots with the
    most derived lots in stock (worst case, the lots a real recall would hurt most)."""
    in_stock = {s["CHARG"] for s in t["MCHB"]}
    migrated = {line["Lot No."]: line for line in bc["Item Journal (lots)"] if line["Expiration Date"]}
    raw_lots = sorted({r["CHARG_COMP"] for r in t["CHVW"] if r["CHARG_COMP"].startswith("R")})
    scored = sorted(((len(descendants(t, lot) & in_stock), lot) for lot in raw_lots), reverse=True)[:sample]
    total = found = 0
    worst = None
    for _, lot in scored:
        derived = descendants(t, lot) & in_stock
        ok = {d for d in derived if d in migrated}
        total += len(derived)
        found += len(ok)
        missing = derived - ok
        if worst is None or len(missing) > len(worst["missing"]):
            worst = {"lot": lot, "derived": sorted(derived), "missing": sorted(missing)}
    example = _recall_tree(t, worst["lot"], migrated, in_stock) if worst else None
    return {"sample": len(scored), "derived": total, "found": found, "pct": round(found / total * 100, 1) if total else 100.0,
            "example": example}


def _recall_tree(t: dict, lot: str, migrated: dict, in_stock: set[str]) -> dict:
    lot_master = {r["CHARG"]: r for r in t["MCH1"]}
    children: dict[str, list[str]] = defaultdict(list)
    for r in t["CHVW"]:
        children[r["CHARG_COMP"]].append(r["CHARG_PARENT"])

    def node(charg: str, depth: int) -> dict:
        m = lot_master[charg]
        kids = sorted(set(children.get(charg, []))) if depth < 2 else []
        status = "in BC" if charg in migrated else ("ontbreekt in BC" if charg in in_stock else "verbruikt (archief)")
        return {"lot": charg, "item": m["MATNR"], "expires": m["VFDAT"] or None, "status": status,
                "children": [node(k, depth + 1) for k in kids if k in in_stock][:8]}

    root = node(lot, 0)
    root["supplierLot"] = lot_master[lot]["LICHA"]
    return root


def migration_summary(t: dict) -> dict:
    """Run rules, transform, reconcile and recall for one mock; everything the site and docs show."""
    results = rules.run(t)
    bc = transform(t, results)
    rec = reconcile(t, bc)
    recall = mock_recall(t, bc)
    rng = random.Random(7)
    rule_rows = []
    for rule in rules.RULES:
        hits = results[rule.id]
        row = {"id": rule.id, "object": rule.object, "title": rule.title, "severity": rule.severity, "owner": rule.owner,
               "why": rule.why, "count": len(hits), "sample": rng.sample(hits, min(5, len(hits))), "keys": sorted(h["key"] for h in hits)}
        if rule.id == "DQ-10" and hits:
            by = defaultdict(int)
            for h in hits:
                by[f"{h['mtart']} · {h['werks']}"] += 1
            row["breakdown"] = dict(sorted(by.items()))
        rule_rows.append(row)
    blocking = sum(r["count"] for r in rule_rows if r["severity"] == "blokkerend")
    sources = {"Customer": len(t["KNA1"]), "Vendor": len(t["LFA1"]), "Item": len(t["MARA"]), "Production BOM Header": len(t["STKO"]),
               "Routing Header": len(t["PLKO"]), "Item Journal (lots)": len(t["MCHB"]), "Cust. Ledger (open)": len(t["BSID"]),
               "Vend. Ledger (open)": len(t["BSIK"]), "G/L Opening": len(t["GLBAL"])}
    sap_names = {"Customer": "KNA1", "Vendor": "LFA1 (+LFBK)", "Item": "MARA/MAKT/MARM/MBEW", "Production BOM Header": "STKO/STPO",
                 "Routing Header": "PLKO/PLPO/CRHD", "Item Journal (lots)": "MCH1/MCHB", "Cust. Ledger (open)": "BSID",
                 "Vend. Ledger (open)": "BSIK", "G/L Opening": "FAGLFLEXT (saldi)"}
    objects = [{"bc": k, "sap": sap_names[k], "source": v, "migrated": len(bc[k]), "excluded": v - len(bc[k])} for k, v in sources.items()]
    return {"stockDate": t["_META"][0]["STOCK_DATE"], "rules": rule_rows, "blocking": blocking,
            "warnings": sum(r["count"] for r in rule_rows if r["severity"] == "waarschuwing"),
            "objects": objects, "reconciliation": rec, "recall": recall}


def compare_keys(previous: dict | None, current: dict) -> None:
    """Per rule: how many flagged records were already flagged in the previous mock, and how many are new.
    Same count with new keys means the source keeps producing errors (DQ-10 between mock 2 and 3)."""
    prev = {r["id"]: set(r["keys"]) for r in previous["rules"]} if previous else {}
    for r in current["rules"]:
        keys = set(r["keys"])
        carried = len(keys & prev[r["id"]]) if previous else None
        r["carried"] = carried
        r["new"] = len(keys) - carried if previous else None
