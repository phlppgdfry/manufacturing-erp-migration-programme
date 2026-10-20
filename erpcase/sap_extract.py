"""Synthetic SAP ECC extracts for the four trial migrations (mock-1 … mock-4).

The data is generated, not exported from any real system. Table and field names follow
SAP ECC conventions (KNA1, LFA1, MARA, MCH1, MCHB, STKO/STPO, PLKO/PLPO, CHVW, BSID, BSIK)
in a simplified form: only the fields this migration needs, one CSV per table.

Data errors are injected on purpose, with an exact count per rule and per mock (DEFECTS).
The data-quality rules in rules.py must find exactly these counts; the tests check that.
"""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 1961

# Active master data per object (inactive items come on top, see INACTIVE_ITEMS).
SIZES = {"customers": 412, "vendors": 286, "FERT": 642, "HALB": 214, "ROH": 598, "VERP": 420, "gl": 118}
INACTIVE_ITEMS = 312
# Lots in stock at the moment of extraction.
LOTS_IN_STOCK = {"ROH": 1100, "HALB": 420, "FERT": 2440}
OPEN_AR = 1320
OPEN_AP = 690

# Stock date per mock: the day of the extraction.
STOCK_DATE = {
    "mock-1": date(2026, 1, 9),
    "mock-2": date(2026, 1, 30),
    "mock-3": date(2026, 2, 20),
    "mock-4": date(2026, 3, 20),
}

# Exact number of records each rule must flag, per mock.
DEFECTS = {
    "mock-1": {"DQ-01": 14, "DQ-02": 23, "DQ-03": 9, "DQ-04": 61, "DQ-05": 48, "DQ-07": 17, "DQ-08": 22, "DQ-09": 6, "DQ-10": 214, "DQ-11": 12, "DQ-12": 37, "DQ-13": 8, "DQ-14": 41, "DQ-15": 5},
    "mock-2": {"DQ-01": 4, "DQ-02": 6, "DQ-03": 2, "DQ-04": 12, "DQ-05": 9, "DQ-07": 3, "DQ-08": 9, "DQ-09": 0, "DQ-10": 104, "DQ-11": 3, "DQ-12": 18, "DQ-13": 2, "DQ-14": 15, "DQ-15": 1},
    "mock-3": {"DQ-01": 0, "DQ-02": 0, "DQ-03": 0, "DQ-04": 0, "DQ-05": 0, "DQ-07": 0, "DQ-08": 4, "DQ-09": 0, "DQ-10": 107, "DQ-11": 0, "DQ-12": 9, "DQ-13": 0, "DQ-14": 6, "DQ-15": 0},
    "mock-4": {"DQ-01": 0, "DQ-02": 0, "DQ-03": 0, "DQ-04": 0, "DQ-05": 0, "DQ-07": 0, "DQ-08": 4, "DQ-09": 0, "DQ-10": 0, "DQ-11": 0, "DQ-12": 3, "DQ-13": 0, "DQ-14": 2, "DQ-15": 0},
}
MOCKS = list(DEFECTS)

ALLERGENS = ["MOSTERD", "SELDERIJ", "EI", "MELK", "GLUTEN", "SOJA", "SESAM", "VIS", "SCHAALDIEREN", "NOTEN", "SULFIET"]
COUNTRIES = [("BE", 45), ("NL", 25), ("FR", 22), ("GB", 5), ("DE", 3)]
EU = {"BE", "NL", "FR", "DE"}
WORK_CENTERS = ["H1-KOOK1", "H1-KOOK2", "H1-VUL1", "H1-VUL2", "H1-PAK", "H2-MENG1", "H2-MENG2", "H2-EMUL", "H2-VUL1", "H2-VUL2", "H2-VUL3", "H2-PAK", "MAG-WEEG", "QA-LABO"]
PLACES = ["Westerdijk", "Ravelingen", "Oudemeers", "Kerselaar", "Lindhoven", "Brakveld", "Moerland", "Hazegras", "Vrijbos", "Zandhoeke", "Polderkant", "Wildeburg"]
NAME_A = ["Noord", "Zuid", "Groot", "Oost", "West", "Midden", "Kust", "Haven", "Markt", "Linde"]
NAME_B = ["Foodservice", "Groothandel", "Traiteur", "Catering", "Distributie", "Verswaren", "Horeca", "Delicatessen"]
RAW = ["Mosterdzaad", "Tomatenpuree", "Zonnebloemolie", "Azijn", "Eigeel", "Suiker", "Zout", "Ui", "Selder", "Wortel", "Room", "Bloem", "Sojasaus", "Sesamolie", "Peper", "Kerrie", "Paprika", "Knoflook", "Dragon", "Bouillon"]
FG_NAMES = ["Andalouse", "Bearnaise", "Cocktailsaus", "Tartaar", "Samurai", "Mosterdsaus", "Curry ketchup", "Tomatensoep", "Groentesoep", "Pompoensoep", "Champignonsoep", "Kervelsoep", "Honing-mosterddressing", "Yoghurtdressing", "Pepersaus"]
EPOCH = date(2026, 3, 31)


def _be_vat(rng: random.Random) -> str:
    first8 = f"0{rng.randint(2000000, 9999999)}"  # enterprise numbers start with 0 or 1
    check = 97 - int(first8) % 97
    return f"BE{first8}{check:02d}"


def be_vat_valid(vat: str) -> bool:
    """Belgian VAT/enterprise number: BE + 10 digits, last two = 97 - (first eight mod 97)."""
    if len(vat) != 12 or not vat.startswith("BE") or not vat[2:].isdigit():
        return False
    first8, check = int(vat[2:10]), int(vat[10:])
    return 97 - first8 % 97 == check


def _vat(rng: random.Random, country: str) -> str:
    if country == "BE":
        return _be_vat(rng)
    if country == "NL":
        return f"NL{rng.randint(100000000, 999999999)}B{rng.randint(1, 99):02d}"
    if country == "FR":
        return f"FR{rng.randint(10, 99)}{rng.randint(100000000, 999999999)}"
    if country == "DE":
        return f"DE{rng.randint(100000000, 999999999)}"
    return f"GB{rng.randint(100000000, 999999999)}"


def iban_valid(iban: str) -> bool:
    """ISO 13616 check: move the first four characters to the end, letters to numbers, mod 97 == 1."""
    s = iban.replace(" ", "").upper()
    if len(s) < 15 or not s[:2].isalpha() or not s[2:4].isdigit():
        return False
    moved = s[4:] + s[:4]
    digits = "".join(str(int(ch, 36)) for ch in moved)
    return int(digits) % 97 == 1


def _iban(rng: random.Random, country: str) -> str:
    if country == "BE":
        bank = f"{rng.randint(100, 999)}{rng.randint(1000000, 9999999)}"
        bban = bank + f"{int(bank) % 97 or 97:02d}"
    elif country == "NL":
        bban = "RABO" + f"{rng.randint(0, 9999999999):010d}"
    elif country == "FR":
        bban = f"{rng.randint(10**22, 10**23 - 1)}"
    else:
        bban = f"{rng.randint(10**17, 10**18 - 1)}"
    numeric = "".join(str(int(ch, 36)) for ch in bban + country + "00")
    check = 98 - int(numeric) % 97
    return f"{country}{check:02d}{bban}"


def _pick_country(rng: random.Random) -> str:
    return rng.choices([c for c, _ in COUNTRIES], weights=[w for _, w in COUNTRIES])[0]


def _master(rng: random.Random) -> dict[str, list[dict]]:
    """Master data that is the same for every mock before errors are injected."""
    customers = []
    for i in range(SIZES["customers"]):
        country = "BE" if i < 6 else _pick_country(rng)
        if i < 6:
            name = f"Retailer R{i + 1}"
        else:
            name = f"{rng.choice(NAME_A)}{rng.choice(['', ' '])}{rng.choice(NAME_B)} {rng.choice(PLACES)}"
        customers.append({"KUNNR": f"{100001 + i}", "NAME1": name, "LAND1": country, "STCEG": _vat(rng, country), "ORT01": rng.choice(PLACES)})
    vendors = []
    for i in range(SIZES["vendors"]):
        country = _pick_country(rng)
        vendors.append({"LIFNR": f"{200001 + i}", "NAME1": f"{rng.choice(RAW)} {rng.choice(['NV', 'BV', 'SAS', 'GmbH', 'Ltd'])} {rng.choice(PLACES)}", "LAND1": country, "STCEG": _vat(rng, country), "IBAN": _iban(rng, country)})

    mara, makt, marm, mbew = [], [], [], []
    prefixes = {"FERT": ("FG", 10001), "HALB": ("SF", 20001), "ROH": ("RM", 30001), "VERP": ("PK", 40001)}
    for mtart, (prefix, start) in prefixes.items():
        for i in range(SIZES[mtart] + (INACTIVE_ITEMS // 4 if mtart != "VERP" else INACTIVE_ITEMS - 3 * (INACTIVE_ITEMS // 4))):
            inactive = i >= SIZES[mtart]
            matnr = f"{prefix}-{start + i}"
            if mtart == "FERT":
                meins, shelf, desc = "ST", rng.randint(60, 240), f"{rng.choice(FG_NAMES)} {rng.choice([250, 300, 500, 1000])} ml {rng.choice(['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'eigen merk', 'FS'])}"
            elif mtart == "HALB":
                meins, shelf, desc = "KG", rng.randint(5, 21), f"Basis {rng.choice(FG_NAMES).lower()} (bulk)"
            elif mtart == "ROH":
                meins, shelf, desc = "KG", rng.randint(120, 720), f"{rng.choice(RAW)} {rng.choice(['bio', 'standaard', 'premium', ''])}".strip()
            else:
                meins, shelf, desc = "ST", 0, f"{rng.choice(['Pot', 'Fles', 'Deksel', 'Etiket', 'Doos', 'Folie'])} {rng.randint(100, 999)}"
            allergens = ""
            if mtart == "ROH":
                allergens = ",".join(sorted(rng.sample(ALLERGENS, rng.choice([0, 0, 0, 1, 1, 2])))) or "-"
            elif mtart in ("FERT", "HALB"):
                allergens = "?"  # filled from the BOM below
            row = {"MATNR": matnr, "MTART": mtart, "MEINS": meins, "NTGEW": round(rng.choice([0.25, 0.3, 0.5, 1.0]), 2) if mtart == "FERT" else 1.0, "MHDHB": shelf, "MHDRZ": round(shelf * 2 / 3) if mtart == "FERT" else 0, "ZZALLERGENS": allergens, "LVORM": "X" if inactive else ""}
            mara.append(row)
            makt.append({"MATNR": matnr, "SPRAS": "N", "MAKTX": desc})
            if mtart == "FERT":
                marm.append({"MATNR": matnr, "MEINH": "KAR", "UMREZ": rng.choice([6, 8, 12]), "UMREN": 1})
            price = {"FERT": rng.uniform(0.6, 3.2), "HALB": rng.uniform(1.2, 4.5), "ROH": rng.uniform(0.4, 9.0), "VERP": rng.uniform(0.02, 0.6)}[mtart]
            mbew.append({"MATNR": matnr, "BWKEY": "VAER", "VPRSV": "S", "STPRS": round(price, 2), "VERPR": round(price * rng.uniform(0.95, 1.08), 2), "PEINH": 1})
    return {"KNA1": customers, "LFA1": vendors, "MARA": mara, "MAKT": makt, "MARM": marm, "MBEW": mbew}


def _boms_and_routings(rng: random.Random, mara: list[dict]) -> dict[str, list[dict]]:
    by_type = {t: [m for m in mara if m["MTART"] == t and not m["LVORM"]] for t in ("FERT", "HALB", "ROH", "VERP")}
    stko, stpo, mapl = [], [], []
    stlnr = 1
    for sf in by_type["HALB"]:
        comps = rng.sample(by_type["ROH"], rng.randint(3, 6))
        shares = [rng.uniform(0.5, 1.5) for _ in comps]
        total = sum(shares)
        stko.append({"STLNR": f"{stlnr:08d}", "MATNR": sf["MATNR"], "BMENG": 100, "BMEIN": "KG"})
        for pos, (comp, share) in enumerate(zip(comps, shares), start=1):
            stpo.append({"STLNR": f"{stlnr:08d}", "POSNR": f"{pos * 10:04d}", "IDNRK": comp["MATNR"], "MENGE": round(100 * share / total * rng.uniform(1.0, 1.06), 3), "MEINS": "KG", "AUSCH": rng.choice([0, 0, 1, 2])})
        stlnr += 1
    for fg in by_type["FERT"]:
        kg_out = 100 * fg["NTGEW"]
        sfs = rng.sample(by_type["HALB"], rng.choice([1, 1, 2]))
        rms = rng.sample(by_type["ROH"], rng.randint(1, 2))
        kg_parts = [rng.uniform(0.7, 1.0)] + [rng.uniform(0.05, 0.2) for _ in range(len(sfs) - 1 + len(rms))]
        scale = kg_out * rng.uniform(1.0, 1.05) / sum(kg_parts)
        stko.append({"STLNR": f"{stlnr:08d}", "MATNR": fg["MATNR"], "BMENG": 100, "BMEIN": "ST"})
        pos = 1
        for comp, part in zip(sfs + rms, kg_parts):
            stpo.append({"STLNR": f"{stlnr:08d}", "POSNR": f"{pos * 10:04d}", "IDNRK": comp["MATNR"], "MENGE": round(part * scale, 3), "MEINS": "KG", "AUSCH": rng.choice([0, 1, 2])})
            pos += 1
        for comp in rng.sample(by_type["VERP"], rng.randint(2, 3)):
            stpo.append({"STLNR": f"{stlnr:08d}", "POSNR": f"{pos * 10:04d}", "IDNRK": comp["MATNR"], "MENGE": 100, "MEINS": "ST", "AUSCH": 1})
            pos += 1
        stlnr += 1
    # Allergens of semi-finished and finished goods follow from their components.
    allergens = {m["MATNR"]: m["ZZALLERGENS"] for m in mara}
    items_by_bom: dict[str, list[str]] = {}
    for row in stpo:
        items_by_bom.setdefault(row["STLNR"], []).append(row["IDNRK"])
    header = {h["STLNR"]: h["MATNR"] for h in stko}
    for mtart in ("HALB", "FERT"):
        for stl, comps in items_by_bom.items():
            matnr = header[stl]
            if not matnr.startswith("SF" if mtart == "HALB" else "FG"):
                continue
            found = set()
            for c in comps:
                value = allergens.get(c, "-")
                if value not in ("-", "", "?"):
                    found.update(value.split(","))
            allergens[matnr] = ",".join(sorted(found)) or "-"
    for m in mara:
        if m["ZZALLERGENS"] == "?":
            value = allergens.get(m["MATNR"], "-")
            m["ZZALLERGENS"] = "-" if value == "?" else value
    # Routings per product family: 38 task lists over the work centers.
    plko, plpo = [], []
    for n in range(38):
        hall = "H1" if n < 16 else "H2"
        plnnr = f"5{n + 1:07d}"
        plko.append({"PLNNR": plnnr, "KTEXT": f"Routing {'soep' if hall == 'H1' else 'saus'} familie {n + 1}", "WERKS": "HAL1" if hall == "H1" else "HAL2"})
        centers = [w for w in WORK_CENTERS if w.startswith(hall)]
        steps = [centers[0], rng.choice(centers[1:-1]), centers[-1]]
        for i, arbpl in enumerate(steps, start=1):
            plpo.append({"PLNNR": plnnr, "VORNR": f"{i * 10:04d}", "ARBPL": arbpl, "VGW01": rng.choice([15, 20, 30, 45]), "VGW02": round(rng.uniform(8, 40), 1)})
    for prod in by_type["FERT"] + by_type["HALB"]:
        is_soup = rng.random() < 0.4
        mapl.append({"MATNR": prod["MATNR"], "PLNNR": f"5{rng.randint(1, 16) if is_soup else rng.randint(17, 38):07d}"})
    crhd = [{"ARBPL": w, "WERKS": "HAL1" if w.startswith("H1") else ("HAL2" if w.startswith("H2") else "MAG")} for w in WORK_CENTERS]
    return {"STKO": stko, "STPO": stpo, "PLKO": plko, "PLPO": plpo, "MAPL": mapl, "CRHD": crhd}


def _lots(rng: random.Random, mara: list[dict], stpo: list[dict], stko: list[dict], vendors: list[dict], stock_date: date) -> dict[str, list[dict]]:
    active = {t: [m for m in mara if m["MTART"] == t and not m["LVORM"]] for t in ("FERT", "HALB", "ROH")}
    shelf = {m["MATNR"]: m["MHDHB"] for m in mara}
    bom_of = {h["MATNR"]: h["STLNR"] for h in stko}
    comps: dict[str, list[str]] = {}
    for row in stpo:
        comps.setdefault(row["STLNR"], []).append(row["IDNRK"])
    mch1, mchb, chvw = [], [], []
    lots_by_mat: dict[str, list[str]] = {}
    counter = {"ROH": 0, "HALB": 0, "FERT": 0}
    prefix = {"ROH": "R", "HALB": "S", "FERT": "F"}

    def new_lot(mtart: str, matnr: str, made: date, werks: str, lgort: str, qty: float, in_stock: bool, vendor: str = "") -> str:
        counter[mtart] += 1
        charg = f"{prefix[mtart]}{stock_date.toordinal() % 1000:03d}{counter[mtart]:05d}"
        vfdat = made + timedelta(days=shelf[matnr])
        mch1.append({"MATNR": matnr, "CHARG": charg, "HSDAT": made.isoformat(), "VFDAT": vfdat.isoformat(), "LIFNR": vendor, "LICHA": f"L{rng.randint(100000, 999999)}" if vendor else "", "WERKS": werks})
        if in_stock:
            mchb.append({"MATNR": matnr, "WERKS": werks, "LGORT": lgort, "CHARG": charg, "CLABS": round(qty, 3), "CSPEM": 0})
        lots_by_mat.setdefault(matnr, []).append(charg)
        return charg

    # Raw-material lots: in stock, plus a pool of consumed lots used by older production.
    rm_pool = []
    for _ in range(LOTS_IN_STOCK["ROH"]):
        m = rng.choice(active["ROH"])
        made = stock_date - timedelta(days=rng.randint(5, max(6, min(150, shelf[m["MATNR"]] - 10))))
        rm_pool.append(new_lot("ROH", m["MATNR"], made, "VAER", "GRST", rng.uniform(10, 380), True, rng.choice(vendors)["LIFNR"]))
    # Semi-finished lots in stock (bulk sauce/soup base, a few days old).
    sfg_in_stock = []
    for i in range(LOTS_IN_STOCK["HALB"]):
        m = rng.choice(active["HALB"])
        werks = "HAL2" if i < 260 else "HAL1"
        made = stock_date - timedelta(days=rng.randint(0, max(1, shelf[m["MATNR"]] - 2)))
        charg = new_lot("HALB", m["MATNR"], made, werks, "BULK", rng.uniform(60, 780), True)
        sfg_in_stock.append(charg)
        for _ in range(rng.randint(2, 4)):
            chvw.append({"CHARG_PARENT": charg, "CHARG_COMP": rng.choice(rm_pool)})
    # Finished-good lots in stock (own warehouse or the external cold store).
    for _ in range(LOTS_IN_STOCK["FERT"]):
        m = rng.choice(active["FERT"])
        made = stock_date - timedelta(days=rng.randint(1, max(2, shelf[m["MATNR"]] // 2)))
        lgort = rng.choice(["EIND", "KOEL", "KOEL"])
        charg = new_lot("FERT", m["MATNR"], made, "HAL1" if rng.random() < 0.4 else "HAL2", lgort, rng.uniform(36, 1440), True)
        for _ in range(rng.choice([1, 1, 2])):
            chvw.append({"CHARG_PARENT": charg, "CHARG_COMP": rng.choice(sfg_in_stock)})
        chvw.append({"CHARG_PARENT": charg, "CHARG_COMP": rng.choice(rm_pool)})
    return {"MCH1": mch1, "MCHB": mchb, "CHVW": chvw}


def _open_items(rng: random.Random, customers: list[dict], vendors: list[dict], stock_date: date) -> dict[str, list[dict]]:
    bsid = []
    for i in range(OPEN_AR):
        c = rng.choice(customers)
        amount = round(rng.uniform(80, 18000), 2)
        credit = rng.random() < 0.06
        bsid.append({"KUNNR": c["KUNNR"], "BELNR": f"90{i + 1:08d}", "BUDAT": (stock_date - timedelta(days=rng.randint(1, 75))).isoformat(), "SHKZG": "H" if credit else "S", "DMBTR": amount})
    bsik = []
    for i in range(OPEN_AP):
        v = rng.choice(vendors)
        bsik.append({"LIFNR": v["LIFNR"], "BELNR": f"51{i + 1:08d}", "BUDAT": (stock_date - timedelta(days=rng.randint(1, 60))).isoformat(), "SHKZG": "H", "DMBTR": round(rng.uniform(40, 14000), 2)})
    return {"BSID": bsid, "BSIK": bsik}


def _gl(rng: random.Random) -> dict[str, list[dict]]:
    rows, mapping = [], []
    for i in range(SIZES["gl"]):
        racct = f"{rng.choice(['1', '2', '3', '4', '5', '6', '7'])}{i:05d}"
        rows.append({"RACCT": racct, "BALANCE": round(rng.uniform(-250000, 250000), 2)})
        mapping.append({"SAP_ACCOUNT": racct, "BC_ACCOUNT": f"{racct[0]}{rng.randint(10, 99)}{rng.randint(0, 9)}00"})
    # Trial balance must be zero: the last account absorbs the difference.
    rows[-1]["BALANCE"] = round(-sum(r["BALANCE"] for r in rows[:-1]), 2)
    return {"GLBAL": rows, "GLMAP": mapping}


def _inject(rng: random.Random, t: dict[str, list[dict]], defects: dict[str, int], stock_date: date, mock: str) -> None:
    """Inject exactly the requested number of flagged records per rule. Targets never overlap.

    Master data is the same in every mock, and each rule walks its candidates in a fixed order.
    So the errors left in a later mock are a subset of the earlier ones: cleansing removes errors,
    it does not invent new ones. Lots and open items change between mocks, so their errors are new."""
    used: dict[str, set[str]] = {}
    rotating = {"MCH1", "BSID", "MBEW"}
    # Rules that change the same field may not hit the same record; other rules may overlap.
    group = {"DQ-01": "vat", "DQ-02": "vat", "DQ-10": "vfdat", "DQ-11": "vfdat", "DQ-12": "vfdat"}

    def take(rows: list[dict], key: str, n: int, where=lambda r: True, rule: str = "", table: str = "") -> list[dict]:
        order = random.Random(f"{SEED}-{rule}" + (f"-{mock}" if table in rotating else ""))
        pool = sorted((r for r in rows if where(r)), key=lambda r: r[key])
        order.shuffle(pool)
        taken = used.setdefault(group.get(rule, rule), set())
        chosen = [r for r in pool if r[key] not in taken][:n]
        if len(chosen) < n:
            raise ValueError(f"not enough candidates for {rule}")
        taken.update(r[key] for r in chosen)
        return chosen

    eu_customers = lambda r: r["LAND1"] in EU
    # DQ-01: duplicate VAT numbers — n records = n/2 pairs sharing one number.
    pairs = take(t["KNA1"], "KUNNR", defects["DQ-01"], eu_customers, "DQ-01", "KNA1")
    for a, b in zip(pairs[::2], pairs[1::2]):
        b["STCEG"], b["LAND1"] = a["STCEG"], a["LAND1"]
        b["NAME1"] = a["NAME1"].upper()
    # DQ-02: EU customer with empty or malformed VAT number.
    for r in take(t["KNA1"], "KUNNR", defects["DQ-02"], eu_customers, "DQ-02", "KNA1"):
        r["STCEG"] = rng.choice(["", r["STCEG"][:-3], r["STCEG"].replace(r["LAND1"], "", 1)])
    # DQ-03: invalid IBAN (one digit changed).
    for r in take(t["LFA1"], "LIFNR", defects["DQ-03"], rule="DQ-03", table="LFA1"):
        digits = list(r["IBAN"])
        pos = rng.choice([i for i in range(4, len(digits)) if digits[i].isdigit()])
        digits[pos] = str((int(digits[pos]) + 1) % 10)
        r["IBAN"] = "".join(digits)
    # DQ-04: finished good sold in cartons without a carton conversion.
    fert_with_kar = {m["MATNR"] for m in t["MARM"]}
    victims = take([m for m in t["MARA"] if m["MTART"] == "FERT" and not m["LVORM"] and m["MATNR"] in fert_with_kar], "MATNR", defects["DQ-04"], rule="DQ-04", table="MARA")
    drop = {m["MATNR"] for m in victims}
    t["MARM"] = [m for m in t["MARM"] if m["MATNR"] not in drop]
    for m in victims:
        m["ZZSALES_UNIT"] = "KAR"
    for m in t["MARA"]:
        m.setdefault("ZZSALES_UNIT", "KAR" if m["MTART"] == "FERT" else "")
    # DQ-05: finished good without allergen information.
    for m in take(t["MARA"], "MATNR", defects["DQ-05"], lambda r: r["MTART"] == "FERT" and not r["LVORM"], "DQ-05", "MARA"):
        m["ZZALLERGENS"] = ""
    # DQ-07: BOM line pointing at an inactive (deleted) component.
    inactive_rm = [m["MATNR"] for m in t["MARA"] if m["MTART"] == "ROH" and m["LVORM"]]
    for row in take(t["STPO"], "POSNR_KEY", defects["DQ-07"], lambda r: r["IDNRK"].startswith("RM"), "DQ-07", "STPO"):
        row["IDNRK"] = rng.choice(inactive_rm)
    # DQ-08: recipe yield outside 95–115% (warning).
    kg_out = {h["STLNR"]: (100 if h["BMEIN"] == "KG" else None) for h in t["STKO"]}
    ntgew = {m["MATNR"]: m["NTGEW"] for m in t["MARA"]}
    for h in t["STKO"]:
        if kg_out[h["STLNR"]] is None:
            kg_out[h["STLNR"]] = 100 * ntgew[h["MATNR"]]
    for h in take(t["STKO"], "STLNR", defects["DQ-08"], rule="DQ-08", table="STKO"):
        lines = [r for r in t["STPO"] if r["STLNR"] == h["STLNR"] and r["MEINS"] == "KG"]
        lines[0]["MENGE"] = round(lines[0]["MENGE"] + kg_out[h["STLNR"]] * 0.4, 3)
    # DQ-09: routing operation on a work center that does not exist.
    for row in take(t["PLPO"], "OP_KEY", defects["DQ-09"], rule="DQ-09", table="PLPO"):
        row["ARBPL"] = row["ARBPL"] + "X"
    # DQ-10..12 work on lots in stock.
    in_stock = {r["CHARG"] for r in t["MCHB"]}
    lots = [r for r in t["MCH1"] if r["CHARG"] in in_stock]
    if defects["DQ-10"]:
        # mock-1: finished and semi-finished goods; from mock-2 on only semi-finished goods made in Hal 2.
        if defects["DQ-10"] > 150:
            victims = take(lots, "CHARG", defects["DQ-10"], lambda r: r["CHARG"][0] in "FS", "DQ-10", "MCH1")
        else:
            victims = take(lots, "CHARG", defects["DQ-10"], lambda r: r["CHARG"][0] == "S" and r["WERKS"] == "HAL2", "DQ-10", "MCH1")
        for r in victims:
            r["VFDAT"] = ""
    for r in take(lots, "CHARG", defects["DQ-11"], lambda r: r["VFDAT"] != "", "DQ-11", "MCH1"):
        r["VFDAT"] = (date.fromisoformat(r["HSDAT"]) - timedelta(days=rng.randint(1, 30))).isoformat()
    old_enough = (stock_date - timedelta(days=21)).isoformat()
    for r in take(lots, "CHARG", defects["DQ-12"], lambda r: r["VFDAT"] != "" and r["CHARG"][0] in "RF" and r["HSDAT"] < old_enough, "DQ-12", "MCH1"):
        r["VFDAT"] = (stock_date - timedelta(days=rng.randint(1, 20))).isoformat()
    # DQ-13: open receivable for a customer that is not in the extract.
    for r in take(t["BSID"], "BELNR", defects["DQ-13"], rule="DQ-13", table="BSID"):
        r["KUNNR"] = f"{190001 + rng.randint(0, 900)}"
    # DQ-14: item in stock without a standard price (warning; Business Central falls back to the average price).
    # Victims are low-value raw materials: the kind of item nobody noticed was valued at zero.
    value: dict[str, float] = {}
    price = {m["MATNR"]: m["STPRS"] for m in t["MBEW"]}
    for r in t["MCHB"]:
        value[r["MATNR"]] = value.get(r["MATNR"], 0.0) + r["CLABS"] * price[r["MATNR"]]
    cheap = set(sorted((v, k) for k, v in value.items() if k.startswith("RM"))[i][1] for i in range(60))
    for m in take(t["MBEW"], "MATNR", defects["DQ-14"], lambda r: r["MATNR"] in cheap, "DQ-14", "MBEW"):
        m["STPRS"] = 0.0
    # DQ-15: GL account without a mapping to the Belgian chart of accounts.
    for m in take(t["GLMAP"], "SAP_ACCOUNT", defects["DQ-15"], rule="DQ-15", table="GLMAP"):
        m["BC_ACCOUNT"] = ""


def generate(mock: str) -> dict[str, list[dict]]:
    """Build all tables for one mock. Deterministic: same mock → same data."""
    if mock not in DEFECTS:
        raise ValueError(f"unknown mock {mock}")
    stock_date = STOCK_DATE[mock]
    rng = random.Random(SEED)
    tables = _master(rng)
    tables.update(_boms_and_routings(rng, tables["MARA"]))
    tables.update(_gl(rng))
    stock_rng = random.Random(f"{SEED}-{mock}")
    tables.update(_lots(stock_rng, tables["MARA"], tables["STPO"], tables["STKO"], tables["LFA1"], stock_date))
    tables.update(_open_items(stock_rng, tables["KNA1"], tables["LFA1"], stock_date))
    for row in tables["STPO"]:
        row["POSNR_KEY"] = f"{row['STLNR']}-{row['POSNR']}"
    for row in tables["PLPO"]:
        row["OP_KEY"] = f"{row['PLNNR']}-{row['VORNR']}"
    _inject(random.Random(f"{SEED}-{mock}-defects"), tables, DEFECTS[mock], stock_date, mock)
    for row in tables["STPO"]:
        row.pop("POSNR_KEY")
    for row in tables["PLPO"]:
        row.pop("OP_KEY")
    tables["_META"] = [{"MOCK": mock, "STOCK_DATE": stock_date.isoformat(), "SOURCE": "synthetic SAP ECC extract, generated by erpcase/sap_extract.py"}]
    return tables


def write_csv(tables: dict[str, list[dict]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        if not rows:
            continue
        fields = list(dict.fromkeys(k for r in rows for k in r))
        with open(outdir / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)


def read_csv(indir: Path) -> dict[str, list[dict]]:
    tables = {}
    for path in sorted(indir.glob("*.csv")):
        with open(path, encoding="utf-8") as fh:
            tables[path.stem] = list(csv.DictReader(fh, delimiter=";"))
    return tables
