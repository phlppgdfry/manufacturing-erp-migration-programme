"""SAP → Business Central mapping, reconciliation and the mock recall."""
import unittest

from erpcase import rules, transform

from .helpers import extract, summary


class Mapping(unittest.TestCase):
    def setUp(self):
        self.t = extract("mock-4")
        self.bc = transform.transform(self.t, rules.run(self.t))

    def test_posting_groups_follow_country(self):
        self.assertEqual(transform.posting_group("BE"), "BINNENL")
        self.assertEqual(transform.posting_group("FR"), "EU")
        self.assertEqual(transform.posting_group("GB"), "EXPORT")

    def test_lot_numbers_are_kept(self):  # ADR-008
        sap = {r["CHARG"] for r in self.t["MCHB"]}
        bc = {line["Lot No."] for line in self.bc["Item Journal (lots)"]}
        self.assertEqual(bc, sap)

    def test_every_migrated_lot_has_an_expiration_date(self):
        self.assertTrue(all(line["Expiration Date"] for line in self.bc["Item Journal (lots)"]))

    def test_expired_lots_migrate_blocked(self):  # DQ-12
        expired = {h["key"] for h in rules.run(self.t)["DQ-12"]}
        blocked = {line["Lot No."] for line in self.bc["Item Journal (lots)"] if line["Lot Blocked"]}
        self.assertTrue(expired)
        self.assertLessEqual(expired, blocked)

    def test_items_get_tracking_and_expiration_formula(self):
        items = {i["No."]: i for i in self.bc["Item"]}
        fg = next(i for k, i in items.items() if k.startswith("FG"))
        self.assertEqual(fg["Item Tracking Code"], "LOTVERV")
        self.assertRegex(fg["Expiration Calculation"], r"^\d+D$")
        pk = next(i for k, i in items.items() if k.startswith("PK"))
        self.assertEqual(pk["Item Tracking Code"], "")

    def test_deleted_items_do_not_migrate(self):
        deleted = {m["MATNR"] for m in self.t["MARA"] if m["LVORM"]}
        self.assertFalse(deleted & {i["No."] for i in self.bc["Item"]})


class Reconciliation(unittest.TestCase):
    def test_stock_difference_is_fully_explained(self):
        for mock in ("mock-1", "mock-2", "mock-3", "mock-4"):
            rec = summary(mock)["reconciliation"]["stock"]
            explained = rec["explained"]["excludedLots"] + rec["explained"]["averagePriceFallback"]
            with self.subTest(mock=mock):
                self.assertAlmostEqual(rec["diff"], explained, delta=1.0)

    def test_open_items_close_from_mock3(self):
        for mock in ("mock-3", "mock-4"):
            rec = summary(mock)["reconciliation"]
            self.assertEqual(rec["ar"]["diff"], 0)
            self.assertEqual(rec["ap"]["diff"], 0)
            self.assertTrue(rec["glBalanced"])

    def test_mock1_open_items_do_not_close(self):
        self.assertNotEqual(summary("mock-1")["reconciliation"]["ar"]["diff"], 0)


class Recall(unittest.TestCase):
    def test_incomplete_while_lots_miss_expiry(self):
        self.assertLess(summary("mock-3")["recall"]["pct"], 100)

    def test_complete_after_fix(self):
        r = summary("mock-4")["recall"]
        self.assertEqual(r["pct"], 100.0)
        self.assertEqual(r["found"], r["derived"])

    def test_descendants_follow_genealogy(self):
        t = extract("mock-4")
        link = t["CHVW"][0]
        self.assertIn(link["CHARG_PARENT"], transform.descendants(t, link["CHARG_COMP"]))

    def test_example_tree_shows_missing_lots_in_mock3(self):
        tree = summary("mock-3")["recall"]["example"]

        def statuses(node):
            yield node["status"]
            for child in node["children"]:
                yield from statuses(child)

        self.assertIn("ontbreekt in BC", set(statuses(tree)))


if __name__ == "__main__":
    unittest.main()
