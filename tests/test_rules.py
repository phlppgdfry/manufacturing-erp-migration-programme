"""Every data-quality rule finds exactly the errors that were put into the extract, no more, no less."""
import unittest

from erpcase import rules, sap_extract
from erpcase.sap_extract import be_vat_valid, iban_valid

from .helpers import extract


class RulesFindInjectedErrors(unittest.TestCase):
    def test_counts_per_mock(self):
        for mock, expected in sap_extract.DEFECTS.items():
            found = rules.run(extract(mock))
            for rule_id, count in expected.items():
                with self.subTest(mock=mock, rule=rule_id):
                    self.assertEqual(len(found[rule_id]), count)

    def test_deleted_items_are_filtered_not_failed(self):
        found = rules.run(extract("mock-4"))
        self.assertEqual(len(found["DQ-06"]), sap_extract.INACTIVE_ITEMS)
        self.assertEqual(rules.RULE_BY_ID["DQ-06"].severity, "info")

    def test_every_rule_has_an_owner_in_the_business(self):
        for rule in rules.RULES:
            with self.subTest(rule=rule.id):
                self.assertNotIn(rule.owner.lower(), {"it", "partner", "projectmanager"})
                self.assertTrue(rule.why)

    def test_mock3_lot_errors_are_all_semi_finished_from_hall_2(self):
        hits = rules.run(extract("mock-3"))["DQ-10"]
        self.assertEqual({(h["mtart"], h["werks"]) for h in hits}, {("HALB", "HAL2")})

    def test_generation_is_deterministic(self):
        a, b = sap_extract.generate("mock-2"), sap_extract.generate("mock-2")
        self.assertEqual(a["MCH1"][:50], b["MCH1"][:50])
        self.assertEqual(a["KNA1"], b["KNA1"])


class Checksums(unittest.TestCase):
    def test_iban(self):
        self.assertTrue(iban_valid("BE68539007547034"))  # the standard example IBAN
        self.assertTrue(iban_valid("NL91ABNA0417164300"))
        self.assertFalse(iban_valid("BE68539007547035"))
        self.assertFalse(iban_valid("BE6853900754"))

    def test_belgian_vat(self):
        self.assertTrue(be_vat_valid("BE0417497106"))
        self.assertFalse(be_vat_valid("BE0417497107"))
        self.assertFalse(be_vat_valid("BE041749710"))

    def test_generated_master_data_is_valid_before_injection(self):
        clean = sap_extract._master(__import__("random").Random(sap_extract.SEED))
        self.assertTrue(all(iban_valid(v["IBAN"]) for v in clean["LFA1"]))
        self.assertTrue(all(rules.vat_valid(c["LAND1"], c["STCEG"]) for c in clean["KNA1"] if c["LAND1"] in sap_extract.EU))


if __name__ == "__main__":
    unittest.main()
