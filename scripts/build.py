#!/usr/bin/env python3
"""Build everything from the two sources: data/programme.json and the generated SAP extracts.

    python3 scripts/build.py          # regenerate extracts, site data, generated docs, BPMN, numbers
    python3 scripts/build.py --check  # fail if anything on disk differs from what the model says (CI)

Numbers in Markdown and HTML are written as <!--n:key-->value<!--/n-->. The build fills in the
value from the model; --check fails when a document shows a number the model does not.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from erpcase import bpmn, programme as pg, rules, sap_extract, transform  # noqa: E402
from erpcase.fmt import eur, num, pct  # noqa: E402

CHECK = "--check" in sys.argv
GENERATED = "> Gegenereerd door `scripts/build.py` uit `data/programme.json` en de SAP-extracten. Niet met de hand aanpassen.\n"
NUMBER = re.compile(r"<!--n:([a-zA-Z0-9_.-]+)-->(.*?)<!--/n-->", re.S)
problems: list[str] = []


def write(path: Path, content: str) -> None:
    if CHECK:
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            problems.append(f"verouderd: {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- model

def build_model() -> tuple[dict, dict]:
    p = json.loads((ROOT / "data/programme.json").read_text(encoding="utf-8"))
    migrations, extracts = {}, {}
    previous = None
    for mock in sap_extract.MOCKS:
        tables = sap_extract.generate(mock)
        extracts[mock] = tables
        migrations[mock] = transform.migration_summary(tables)
        transform.compare_keys(previous, migrations[mock])
        previous = migrations[mock]
    for summary in migrations.values():
        for r in summary["rules"]:
            r.pop("keys")
    model = {
        "meta": p["meta"], "org": p["org"], "role": p["role"], "stakeholders": p["stakeholders"],
        "partners": {**p["partners"], "scores": pg.partner_scores(p), "sensitivity": pg.sensitivity(p)},
        "requirements": p["requirements"], "fitGap": pg.fit_gap(p),
        "budget": pg.budget(p), "changeRequests": p["changeRequests"], "costOfDelay": p["costOfDelay"],
        "milestones": pg.milestones(p), "goLiveDates": p["goLiveDates"],
        "mocks": [{**m, **migrations[m["id"]]} for m in p["mocks"]],
        "testing": p["testing"], "training": p["training"],
        "goNoGo": {"principle": p["goNoGo"]["principle"], "softRule": p["goNoGo"]["softRule"], "moments": pg.go_no_go(p, migrations)},
        "cutover": p["cutover"], "raid": p["raid"], "raidSummary": pg.raid(p), "decisions": p["decisions"],
        "hypercare": {**p["hypercare"], **pg.hypercare(p)}, "kpis": pg.kpis(p), "roadmap": p["roadmap"],
        "processes": [{"id": pr["id"], "name": pr["name"], "kind": pr["kind"], "notes": pr["notes"]}
                      for pr in json.loads((ROOT / "data/processes.json").read_text(encoding="utf-8"))["processes"]],
        "dqRules": [{"id": r.id, "object": r.object, "title": r.title, "severity": r.severity, "owner": r.owner, "why": r.why} for r in rules.RULES],
    }
    return model, extracts


def numbers(m: dict) -> dict[str, str]:
    b, fg = m["budget"], m["fitGap"]
    n = {
        "org.employees": num(m["org"]["employees"]), "org.erpUsers": num(m["org"]["erpUsers"]), "org.revenue": f"€{m['org']['revenueM']} miljoen",
        "budget.subtotal": eur(b["subtotal"]), "budget.contingency": eur(b["contingency"]), "budget.total": eur(b["total"]),
        "budget.overrun": eur(b["overrun"]), "budget.cr": eur(b["crApproved"]), "budget.crRejected": eur(b["crRejected"]), "budget.delay": eur(b["delay"]),
        "budget.used": eur(b["contingencyUsed"]), "budget.left": eur(b["contingencyLeft"]), "budget.eac": eur(b["eac"]),
        "budget.threshold": eur(b["threshold"]), "budget.spentW18": eur(b["spentAtW18"]),
        "fg.total": num(fg["total"]), "fg.inScope": num(fg["inScope"]), "fg.stdConfPct": f"{fg['stdConfPct']}%", "fg.stdConf": num(fg["stdConf"]),
        "fg.extensions": num(fg["extensions"]), "fg.days": num(fg["days"]), "fg.must": num(fg["must"]),
        "raid.openRisks": num(m["raidSummary"]["openRisks"]),
        "hc.total": num(m["hypercare"]["total"]), "hc.bug": num(m["hypercare"]["totals"]["bug"]), "hc.training": num(m["hypercare"]["totals"]["training"]),
        "hc.bugShare": f"{m['hypercare']['bugShare']}%",
        "uat.scenarios": num(len(m["testing"]["scenarios"])), "dq.rules": num(len(m["dqRules"])),
        "delay.weeks": num(m["costOfDelay"]["weeks"]),
    }
    for cid, rule in m["fitGap"]["byClass"].items():
        n[f"fg.class.{cid}"] = num(rule)
    for cand in m["partners"]["candidates"]:
        key = cand["id"][-1]
        n[f"partner.{key}.score"] = num(m["partners"]["scores"][cand["id"]], 2)
        n[f"partner.{key}.offer"] = eur(cand["offerImplementation"])
        n[f"partner.{key}.tco"] = eur(cand["tco3y"])
    for s in m["partners"]["sensitivity"]:
        n[f"sens.{s['id']}.to"] = f"{s['to']}%"
    for mock in m["mocks"]:
        k = mock["id"].replace("-", "")
        rec = mock["reconciliation"]
        n[f"{k}.blocking"] = num(mock["blocking"])
        n[f"{k}.warnings"] = num(mock["warnings"])
        n[f"{k}.recall"] = pct(mock["recall"]["pct"])
        n[f"{k}.recallFound"] = num(mock["recall"]["found"])
        n[f"{k}.recallDerived"] = num(mock["recall"]["derived"])
        n[f"{k}.recallMissing"] = num(mock["recall"]["derived"] - mock["recall"]["found"])
        n[f"{k}.stockSap"] = eur(rec["stock"]["sap"])
        n[f"{k}.stockBc"] = eur(rec["stock"]["bc"])
        n[f"{k}.stockDiff"] = eur(rec["stock"]["diff"])
        n[f"{k}.stockDiffPct"] = pct(rec["stock"]["diffPct"], 3)
        n[f"{k}.excluded"] = eur(-rec["stock"]["explained"]["excludedLots"])
        n[f"{k}.fallback"] = eur(rec["stock"]["explained"]["averagePriceFallback"])
        n[f"{k}.ar"] = eur(rec["ar"]["sap"], 2)
        n[f"{k}.arDiff"] = eur(rec["ar"]["diff"], 2)
        n[f"{k}.ap"] = eur(rec["ap"]["sap"], 2)
        for r in mock["rules"]:
            n[f"{k}.{r['id']}"] = num(r["count"])
            if r["new"] is not None:
                n[f"{k}.{r['id']}.new"] = num(r["new"])
                n[f"{k}.{r['id']}.carried"] = num(r["carried"])
        lots = next(o for o in mock["objects"] if o["bc"] == "Item Journal (lots)")
        n[f"{k}.lots"] = num(lots["source"])
        n[f"{k}.lotsMigrated"] = num(lots["migrated"])
    for g in m["goNoGo"]["moments"]:
        k = g["id"].lower().replace("-", "")
        n[f"{k}.decision"] = g["decision"]
        n[f"{k}.hardFail"] = ", ".join(g["hardFail"]) or "geen"
        n[f"{k}.softFail"] = ", ".join(g["softFail"]) or "geen"
    for k in m["kpis"]:
        n[f"kpi.{k['id']}.baseline"] = num(k["baseline"], 1 if isinstance(k["baseline"], float) else 0)
        n[f"kpi.{k['id']}.target"] = num(k["target"], 1 if isinstance(k["target"], float) else 0)
        n[f"kpi.{k['id']}.measured"] = num(k["measured"], 1 if isinstance(k["measured"], float) else 0)
    return n


# ---------------------------------------------------------------- generated documents

def doc_fit_gap(m: dict) -> str:
    fg = m["fitGap"]
    rows = [[r["id"], r["domain"], r["text"], r["moscow"], f"**{r['class']}**", r["solution"], num(r["days"], 1) if r["days"] % 1 else num(r["days"]), r["owner"], ", ".join(r["tests"]) or "—"] for r in m["requirements"]]
    summary = table(["Klasse", "Aantal", "Partnerdagen bouw"], [[k, v, num(fg["daysByClass"][k], 1) if fg["daysByClass"][k] % 1 else num(fg["daysByClass"][k])] for k, v in fg["byClass"].items()])
    return (f"# Fit-gap-register\n\n{GENERATED}\nTerug naar [de methode](README.md). Elke regel: wat de business nodig heeft, hoe Business Central het oplost, hoeveel bouwwerk de partner rekent, wie beslist en welk UAT-scenario het bewijst.\n\n"
            f"## Samenvatting\n\n{summary}\n{fg['inScope']} van de {fg['total']} eisen zitten in scope; {fg['stdConf']} daarvan ({fg['stdConfPct']}%) lossen we op met standaard of configuratie. Twee extensies, beide met een wettelijke of contractuele reden.\n\n"
            f"## Register\n\n" + table(["ID", "Domein", "Eis", "MoSCoW", "Klasse", "Oplossing", "Dagen", "Beslist door", "Test"], rows))


def csv_fit_gap(m: dict) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n")
    w.writerow(["id", "domein", "eis", "moscow", "klasse", "oplossing", "dagen", "eigenaar", "testen"])
    for r in m["requirements"]:
        w.writerow([r["id"], r["domain"], r["text"], r["moscow"], r["class"], r["solution"], r["days"], r["owner"], " ".join(r["tests"])])
    return buf.getvalue()


def doc_data_quality(m: dict) -> str:
    header = ["Regel", "Object", "Controle", "Ernst", "Eigenaar"] + [mk["name"].replace(" (generale repetitie)", "") for mk in m["mocks"]]
    rows = []
    for i, r in enumerate(m["dqRules"]):
        rows.append([r["id"], r["object"], r["title"], r["severity"], r["owner"]] + [num(mk["rules"][i]["count"]) for mk in m["mocks"]])
    rows.append(["", "", "**Blokkerend totaal**", "", ""] + [f"**{num(mk['blocking'])}**" for mk in m["mocks"]])
    new_rows = [[r["id"], r["title"]] + [("—" if mk["rules"][i]["new"] is None else f"{num(mk['rules'][i]['new'])} nieuw / {num(mk['rules'][i]['carried'])} bekend") for mk in m["mocks"]]
                for i, r in enumerate(m["dqRules"]) if any(mk["rules"][i]["count"] for mk in m["mocks"][1:]) and r["severity"] != "info"]
    dq10 = next(r for r in m["mocks"][2]["rules"] if r["id"] == "DQ-10")
    breakdown = ", ".join(f"{k}: {v}" for k, v in dq10.get("breakdown", {}).items())
    samples = "\n".join(f"- `{s['key']}` — {s['detail']}" for s in dq10["sample"])
    why = "\n".join(f"- **{r['id']} {r['title']}** — {r['why']}" for r in m["dqRules"])
    return (f"# Datakwaliteit per proefmigratie\n\n{GENERATED}\nTerug naar [het migratieplan](README.md). De regels zelf staan in [`erpcase/rules.py`](../../erpcase/rules.py); de testen controleren dat elke regel precies de fouten vindt die in de extracten zitten.\n\n"
            + table(header, rows)
            + "\n## Zelfde fouten of nieuwe fouten?\n\nPer regel: hoeveel gemelde records al in de vorige proefmigratie gemeld waren (bekend) en hoeveel nieuw zijn. Een gelijk aantal met nieuwe sleutels betekent dat de bron nog fouten maakt.\n\n"
            + table(["Regel", "Controle"] + [mk["name"].replace(" (generale repetitie)", "") for mk in m["mocks"]], new_rows)
            + f"\n## Waarom DQ-10 in proefmigratie 3 nog niet op nul stond\n\nVerdeling van de {dq10['count']} lots zonder vervaldatum in proefmigratie 3 (artikeltype · fabriek): **{breakdown}**. Alle fouten zitten in halffabricaten uit Hal 2, en **{dq10['new']} van de {dq10['count']} lots waren nieuw** ten opzichte van proefmigratie 2 (al eerder gemeld: {dq10['carried']}). Na proefmigratie 2 had QA de bestaande lots in SAP verbeterd, maar een eigen SAP-transactie voor de ontvangst van halffabricaten bleef nieuwe lots zonder vervaldatum maken. Opschonen zonder de bron te herstellen is dweilen met de kraan open. Zie [I-03 in de RAID-log](../governance/raid.md) en [het go/no-go-besluit](../08-go-live/go-no-go.md).\n\nVoorbeelden uit het extract:\n\n{samples}\n\n## Waarom elke regel bestaat\n\n{why}\n")


def doc_raid(m: dict) -> str:
    rows = []
    for r in m["raid"]:
        score = r["prob"] * r["impact"] if r["type"] == "Risico" else ""
        rows.append([r["id"], r["type"], r["title"], r["prob"] or "", r["impact"] or "", score, r["owner"], r["mitigation"], r["status"]])
    return (f"# RAID-log\n\n{GENERATED}\nRisico's (kans × impact, 1–5), aannames, issues en afhankelijkheden, met eigenaar. Stand bij de batenreview. Terug naar [governance](README.md).\n\n"
            + table(["ID", "Type", "Omschrijving", "Kans", "Impact", "Score", "Eigenaar", "Maatregel", "Status"], rows))


def doc_decisions(m: dict) -> str:
    rows = []
    for d in m["decisions"]:
        ref = d["ref"] if d["ref"].startswith("../") else f"../{d['ref']}"
        rows.append([d["id"], f"W{d['week']}", d["decision"], d["by"], f"[bron]({ref})"])
    return f"# Beslissingenlog\n\n{GENERATED}\nWie besliste wat en wanneer. Terug naar [governance](README.md).\n\n" + table(["ID", "Week", "Beslissing", "Door", "Onderbouwing"], rows)


def doc_change_requests(m: dict) -> str:
    rows = [[c["id"], c["title"], c["requestedBy"], num(c["impactDays"]), eur(c["cost"]), c["decision"], c["by"], c["reason"]] for c in m["changeRequests"]]
    b = m["budget"]
    return (f"# Change requests\n\n{GENERATED}\nTerug naar [governance](README.md). Regel: niets wordt gebouwd zonder getekende CR. Boven {eur(b['threshold'])} beslist de stuurgroep, daaronder de IT Manager.\n\n"
            + table(["CR", "Wijziging", "Gevraagd door", "Dagen", "Kost", "Besluit", "Door", "Reden"], rows)
            + f"\nGoedgekeurd: {eur(b['crApproved'])}, uit de reserve. Afgewezen: {eur(b['crRejected'])}.\n")


def doc_reconciliation(m: dict) -> str:
    rows = []
    for mk in m["mocks"]:
        rec = mk["reconciliation"]
        rows.append([mk["name"], eur(rec["stock"]["sap"]), eur(rec["stock"]["bc"]), eur(rec["stock"]["diff"]), pct(rec["stock"]["diffPct"], 3),
                     eur(-rec["stock"]["explained"]["excludedLots"]), eur(rec["stock"]["explained"]["averagePriceFallback"]),
                     eur(rec["ar"]["diff"], 2), eur(rec["ap"]["diff"], 2), "ja" if rec["glBalanced"] else "nee"])
    objects = []
    for mk in m["mocks"]:
        for o in mk["objects"]:
            objects.append([mk["name"].split(" (")[0], o["sap"], o["bc"], num(o["source"]), num(o["migrated"]), num(o["excluded"])])
    return (f"# Afstemming per proefmigratie\n\n{GENERATED}\nTerug naar [het migratieplan](README.md). Elk verschil heeft een verklaring of het is een fout. Het voorraadverschil = waarde van lots die niet mochten mee (blokkerende fouten) + artikels die in SAP op nul stonden en in Business Central de gemiddelde prijs krijgen (DQ-14, beslissing van de controller).\n\n"
            + table(["Proefmigratie", "Voorraad SAP", "Voorraad BC", "Verschil", "%", "Niet gemigreerde lots", "Gemiddelde prijs i.p.v. 0", "Klantposten", "Leveranciersposten", "Grootboek sluit"], rows)
            + "\n## Aantallen per object\n\n" + table(["Proefmigratie", "SAP", "Business Central", "Bron", "Gemigreerd", "Niet gemigreerd"], objects))


def doc_cutover(m: dict) -> str:
    c = m["cutover"]
    rows = [[f"`{s['t']}`", s["what"], s["who"]] for s in c["steps"]]
    return (f"# Cutover-draaiboek\n\n{GENERATED}\nTerug naar [het migratieplan](README.md). Venster: {c['window']}. In de generale repetitie (proefmigratie 3) liep het draaiboek in 37 uur; in proefmigratie 4 in 34 uur.\n\n"
            + table(["Moment", "Stap", "Wie"], rows)
            + f"\n## Terugvalplan\n\n{c['rollback']}\n\nWaarom geen terugval meer na D1 20:00: vanaf dan komen er orders, leveringen en productie in Business Central binnen. Teruggaan zou betekenen dat al die transacties dubbel moeten worden ingegeven in SAP. Het risico van voorwaarts herstellen is kleiner dan dat van terugdraaien.\n")


def doc_uat(m: dict) -> str:
    by_test: dict[str, list[str]] = {}
    for r in m["requirements"]:
        for t in r["tests"]:
            by_test.setdefault(t, []).append(r["id"])
    rows = [[s["id"], s["name"], s["owner"], ", ".join(by_test.get(s["id"], [])) or "—"] for s in m["testing"]["scenarios"]]
    defects = [[d["id"], d["sev"], d["area"], d["title"], d["status"], d["workaround"] or "—"] for d in m["testing"]["defects"]]
    out_of_scope = [r["id"] for r in m["requirements"] if r["class"] == "Buiten scope"]
    u = m["testing"]["uatResult"]
    return (f"# UAT-scenario's en traceerbaarheid\n\n{GENERATED}\nTerug naar [de teststrategie](README.md). Elke eis in scope heeft minstens één scenario; de test `tests/test_programme.py` faalt als dat niet zo is. Buiten scope en dus zonder test: {', '.join(out_of_scope)}.\n\n"
            + table(["Scenario", "Wat de key user doet", "Eigenaar", "Bewijst eisen"], rows)
            + f"\nResultaat UAT (W23): {u['executed']} scenario's uitgevoerd, {u['passed']} geslaagd, {u['passedWithDefect']} geslaagd met een open defect, {u['failed']} gefaald.\n\n## Defects\n\nErnst 1 = blokkeert een kernproces zonder omweg · 2 = kernproces met omweg · 3 = hinderlijk, geen impact op levering of boekhouding.\n\n"
            + table(["Defect", "Ernst", "Domein", "Omschrijving", "Status (W25)", "Workaround"], defects))


def doc_gng(m: dict) -> str:
    out = [f"# Go/no-go: resultaten per criterium\n\n{GENERATED}\nTerug naar [het besluit](go-no-go.md). {m['goNoGo']['principle']} {m['goNoGo']['softRule']}\n"]
    for g in m["goNoGo"]["moments"]:
        rows = [[c["id"], c["name"], {"hard": "hard", "soft": "zacht"}[c["type"]], c["threshold"], c["value"], "✓" if c["pass"] else "✗"] for c in g["criteria"]]
        out.append(f"\n## {g['id']} — week {g['week']}, voor go-live op {g['forGoLive']} ({g['mock']})\n\n**Uitkomst: {g['decision']}** · harde criteria gefaald: {', '.join(g['hardFail']) or 'geen'} · zachte criteria gefaald: {', '.join(g['softFail']) or 'geen'}\n\n" + table(["", "Criterium", "Soort", "Drempel", "Gemeten", ""], rows))
    return "".join(out)


# ---------------------------------------------------------------- numbers in documents

def fill_numbers(values: dict[str, str]) -> None:
    files = [p for p in ROOT.rglob("*") if p.suffix in (".md", ".html") and p.is_file()
             and not any(part in {".git", "node_modules", "dist"} for part in p.parts)]
    for path in files:
        text = path.read_text(encoding="utf-8")
        if "<!--n:" not in text:
            continue

        def repl(match: re.Match) -> str:
            key = match.group(1)
            if key not in values:
                problems.append(f"onbekend getal '{key}' in {path.relative_to(ROOT)}")
                return match.group(0)
            return f"<!--n:{key}-->{values[key]}<!--/n-->"

        new = NUMBER.sub(repl, text)
        if new != text:
            if CHECK:
                problems.append(f"getal wijkt af van het model in {path.relative_to(ROOT)}")
            else:
                path.write_text(new, encoding="utf-8")


def main() -> int:
    model, extracts = build_model()
    # One mock is kept in the repository as a readable sample; the others are regenerated on demand.
    if not CHECK:
        sap_extract.write_csv(extracts["mock-3"], ROOT / "data/sap-extract/mock-3")
    write(ROOT / "site/data/model.json", json.dumps(model, ensure_ascii=False, separators=(",", ":")) + "\n")
    write(ROOT / "docs/04-fit-gap/fit-gap.md", doc_fit_gap(model))
    write(ROOT / "docs/04-fit-gap/fit-gap.csv", csv_fit_gap(model))
    write(ROOT / "docs/05-datamigratie/datakwaliteit.md", doc_data_quality(model))
    write(ROOT / "docs/05-datamigratie/afstemming.md", doc_reconciliation(model))
    write(ROOT / "docs/governance/raid.md", doc_raid(model))
    write(ROOT / "docs/governance/decision-log.md", doc_decisions(model))
    write(ROOT / "docs/governance/change-requests.md", doc_change_requests(model))
    write(ROOT / "docs/05-datamigratie/cutover.md", doc_cutover(model))
    write(ROOT / "docs/06-testen/uat-scenarios.md", doc_uat(model))
    write(ROOT / "docs/08-go-live/go-no-go-resultaten.md", doc_gng(model))
    processes = json.loads((ROOT / "data/processes.json").read_text(encoding="utf-8"))["processes"]
    for proc in processes:
        svg = bpmn.to_svg(proc)
        write(ROOT / f"docs/03-processen/bpmn/{proc['id']}.bpmn", bpmn.to_bpmn(proc))
        write(ROOT / f"docs/03-processen/bpmn/{proc['id']}.svg", svg)
        write(ROOT / f"site/assets/bpmn/{proc['id']}.svg", svg)
    fill_numbers(numbers(model))
    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} probleem/problemen. Draai `python3 scripts/build.py` en commit het resultaat.")
        return 1
    print("check ok" if CHECK else "build ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
