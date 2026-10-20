"""Programme control: budget and contingency, partner scoring, fit-gap, RAID, go/no-go.

Everything is computed from data/programme.json plus the migration results, so a number on the
site, in a document or in a status report always comes from one place.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from .fmt import eur, num, pct

CLASS_ORDER = ["Standaard", "Configuratie", "ISV-app", "Procesaanpassing", "Extensie", "Buiten scope"]


# ---------- budget ----------

def budget(p: dict) -> dict:
    b = p["budget"]
    approved = {line["id"]: line for line in b["approved"]}
    subtotal = sum(line["amount"] for line in b["approved"])
    contingency = round(subtotal * b["contingencyPct"] / 100)
    lines = []
    overrun = 0
    for f in b["forecastAtW18"]:
        a = approved[f["id"]]["amount"]
        delta = f["forecast"] - a
        overrun += max(0, delta)
        lines.append({"id": f["id"], "line": approved[f["id"]]["line"], "approved": a, "forecast": f["forecast"], "spent": f["spent"], "delta": delta, "note": f.get("note", "")})
    crs = [c for c in p["changeRequests"] if c["decision"] == "goedgekeurd"]
    cr_total = sum(c["cost"] for c in crs)
    delay_total = sum(i["amount"] for i in p["costOfDelay"]["items"])
    used = overrun + cr_total + delay_total
    return {
        "subtotal": subtotal, "contingency": contingency, "total": subtotal + contingency, "threshold": b["steercoThreshold"],
        "lines": lines, "overrun": overrun, "crApproved": cr_total, "crRejected": sum(c["cost"] for c in p["changeRequests"] if c["decision"] == "afgewezen"),
        "delay": delay_total, "contingencyUsed": used, "contingencyLeft": contingency - used,
        "eac": subtotal + used, "spentAtW18": sum(line["spent"] for line in lines),
        "steps": [
            {"label": "Overschrijding lijnen (W18)", "amount": overrun},
            {"label": "Goedgekeurde change requests", "amount": cr_total},
            {"label": "Uitstel go-live (4 weken)", "amount": delay_total},
        ],
    }


# ---------- partner selection ----------

def partner_scores(p: dict, weights: dict[str, float] | None = None) -> dict[str, float]:
    crit = p["partners"]["criteria"]
    w = weights or {c["id"]: c["weight"] for c in crit}
    total = sum(w.values())
    return {cand["id"]: round(sum(cand["scores"][cid] * w[cid] for cid in w) / total, 3) for cand in p["partners"]["candidates"]}


def reweight(p: dict, cid: str, new_weight: float) -> dict[str, float]:
    """Set one criterion to new_weight and scale the others so the total stays 100."""
    base = {c["id"]: c["weight"] for c in p["partners"]["criteria"]}
    rest = 100 - base[cid]
    out = {k: (v * (100 - new_weight) / rest if rest else 0) for k, v in base.items() if k != cid}
    out[cid] = new_weight
    return out


def sensitivity(p: dict) -> list[dict]:
    """Per criterion: the weight range (0–100) in which the chosen partner stays first, and who wins outside it."""
    chosen = p["partners"]["chosen"]
    rows = []
    for c in p["partners"]["criteria"]:
        winners = []
        for w in range(0, 101):
            s = partner_scores(p, reweight(p, c["id"], w))
            winners.append(max(s, key=lambda k: (s[k], k == chosen)))
        keep = [w for w, win in enumerate(winners) if win == chosen]
        others = sorted({win for win in winners if win != chosen})
        flips = [w for w in range(1, 101) if winners[w] != winners[w - 1]]
        rows.append({"id": c["id"], "name": c["name"], "weight": c["weight"], "from": min(keep) if keep else None, "to": max(keep) if keep else None,
                     "flipsAt": flips, "otherWinners": others})
    return rows


# ---------- fit-gap ----------

def fit_gap(p: dict) -> dict:
    reqs = p["requirements"]
    by_class = Counter(r["class"] for r in reqs)
    days = defaultdict(float)
    for r in reqs:
        days[r["class"]] += r["days"]
    in_scope = [r for r in reqs if r["class"] != "Buiten scope"]
    std_conf = by_class["Standaard"] + by_class["Configuratie"]
    must = [r for r in reqs if r["moscow"] == "Must"]
    must_in_scope = [r for r in must if r["class"] != "Buiten scope"]
    untested = [r["id"] for r in in_scope if not r["tests"]]
    domains = Counter(r["domain"] for r in reqs)
    return {
        "total": len(reqs), "inScope": len(in_scope), "byClass": {k: by_class.get(k, 0) for k in CLASS_ORDER},
        "daysByClass": {k: days.get(k, 0) for k in CLASS_ORDER}, "days": sum(days.values()),
        "stdConf": std_conf, "stdConfPct": round(std_conf / len(in_scope) * 100), "extensions": by_class["Extensie"],
        "must": len(must), "mustInScope": len(must_in_scope), "untested": untested, "domains": dict(domains),
    }


# ---------- RAID ----------

def raid(p: dict) -> dict:
    risks = [r for r in p["raid"] if r["type"] == "Risico"]
    for r in risks:
        r["score"] = r["prob"] * r["impact"]
    open_risks = [r for r in risks if r["status"] in ("open", "beheerst")]
    return {"counts": dict(Counter(r["type"] for r in p["raid"])), "openRisks": len(open_risks),
            "top": sorted(open_risks, key=lambda r: -r["score"])[:5], "highOpen": sum(1 for r in open_risks if r["score"] >= 12)}


# ---------- go / no-go ----------

def _open_defects(p: dict, moment: dict) -> list[dict]:
    fixed = set(moment.get("fixedDefects", []))
    return [d for d in p["testing"]["defects"] if d["status"] == "open" and d["id"] not in fixed]


def criterion_result(p: dict, crit: dict, moment: dict, mig: dict) -> dict:
    src = crit["source"]
    rec = mig["reconciliation"]
    defects = _open_defects(p, moment)
    train = p["training"]
    if src == "migration.recall":
        value, ok = f"{pct(mig['recall']['pct'])} ({num(mig['recall']['found'])} van {num(mig['recall']['derived'])})", mig["recall"]["pct"] == 100
    elif src == "migration.blocking":
        value, ok = num(mig["blocking"]), mig["blocking"] == 0
    elif src == "migration.stockDiff":
        value, ok = pct(rec["stock"]["diffPct"], 3), rec["stock"]["diffPct"] <= 0.1
    elif src == "migration.openItems":
        value, ok = eur(rec["ar"]["diff"] + rec["ap"]["diff"], 2), rec["ar"]["diff"] == 0 and rec["ap"]["diff"] == 0
    elif src == "testing.sev1":
        n = sum(1 for d in defects if d["sev"] == 1)
        value, ok = str(n), n == 0
    elif src == "testing.sev2":
        sev2 = [d for d in defects if d["sev"] == 2]
        value, ok = str(len(sev2)), len(sev2) <= 2 and all(d["workaround"] for d in sev2)
    elif src == "training.keyUsers":
        k = train["keyUsers"]
        value, ok = f"{k['trained']}/{k['planned']}", k["trained"] == k["planned"]
    elif src == "training.endUsers":
        e = train["endUsers"]
        n = e[moment["training"]]
        share = n / e["planned"] * 100
        value, ok = f"{n}/{e['planned']} ({share:.0f}%)", share >= 90
    elif src == "integration.edi":
        value, ok = f"{moment['edi']['tested']} / {moment['edi']['total']}", moment["edi"]["tested"] == moment["edi"]["total"]
    elif src == "cutover.hours":
        value, ok = f"{moment['cutoverHours']} u", moment["cutoverHours"] <= 40
    elif src == "cutover.rollback":
        value, ok = "ja" if moment["rollback"] else "nee", moment["rollback"]
    elif src == "support.ready":
        value, ok = "ja" if moment["support"] else "nee", moment["support"]
    else:
        raise ValueError(src)
    return {"id": crit["id"], "name": crit["name"], "type": crit["type"], "threshold": crit["threshold"], "value": value, "pass": bool(ok)}


def decide(results: list[dict]) -> dict:
    """All hard criteria pass and at most two soft criteria fail → GO. A hard criterion is never waived."""
    hard_fail = [r["id"] for r in results if r["type"] == "hard" and not r["pass"]]
    soft_fail = [r["id"] for r in results if r["type"] == "soft" and not r["pass"]]
    go = not hard_fail and len(soft_fail) <= 2
    return {"decision": "GO" if go else "NO-GO", "hardFail": hard_fail, "softFail": soft_fail}


def go_no_go(p: dict, migrations: dict[str, dict]) -> list[dict]:
    out = []
    for moment in p["goNoGo"]["moments"]:
        results = [criterion_result(p, c, moment, migrations[moment["mock"]]) for c in p["goNoGo"]["criteria"]]
        out.append({"id": moment["id"], "week": moment["week"], "mock": moment["mock"], "forGoLive": moment["forGoLive"],
                    "criteria": results, **decide(results), "openDefects": _open_defects(p, moment)})
    return out


# ---------- KPIs, hypercare, milestones ----------

def kpis(p: dict) -> list[dict]:
    out = []
    for k in p["kpis"]:
        gap = k["baseline"] - k["target"]
        progress = (k["baseline"] - k["measured"]) / gap if gap else 1
        met = k["measured"] <= k["target"] if k["betterIs"] == "lower" else k["measured"] >= k["target"]
        out.append({**k, "progress": round(progress * 100), "met": met})
    return out


def hypercare(p: dict) -> dict:
    cats = ["data", "setup", "training", "bug", "integration"]
    totals = {c: sum(w[c] for w in p["hypercare"]["tickets"]) for c in cats}
    per_week = [sum(w[c] for c in cats) for w in p["hypercare"]["tickets"]]
    return {"totals": totals, "total": sum(totals.values()), "perWeek": per_week, "bugShare": round(totals["bug"] / sum(totals.values()) * 100)}


def milestones(p: dict) -> list[dict]:
    out = []
    for m in p["milestones"]:
        slip = (m["actualWeek"] - m["plannedWeek"]) if m["plannedWeek"] and m["actualWeek"] else None
        out.append({**m, "slip": slip})
    return out
