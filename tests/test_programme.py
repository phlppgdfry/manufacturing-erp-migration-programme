"""Programme rules: budget, partner choice, fit-gap traceability, go/no-go."""
import unittest

from erpcase import programme as pg

from .helpers import migrations, programme


class Budget(unittest.TestCase):
    def test_contingency_covers_everything_that_was_drawn(self):
        b = pg.budget(programme())
        self.assertGreaterEqual(b["contingencyLeft"], 0)
        self.assertLessEqual(b["eac"], b["total"])

    def test_steering_committee_decided_everything_above_threshold(self):
        p = programme()
        threshold = p["budget"]["steercoThreshold"]
        for cr in p["changeRequests"]:
            if cr["cost"] > threshold:
                self.assertEqual(cr["by"], "Stuurgroep", cr["id"])
        self.assertGreater(pg.budget(p)["delay"], threshold)

    def test_spend_never_exceeds_forecast(self):
        for line in pg.budget(programme())["lines"]:
            self.assertLessEqual(line["spent"], line["forecast"], line["id"])


class Partners(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(c["weight"] for c in programme()["partners"]["criteria"]), 100)

    def test_chosen_partner_scores_highest(self):
        p = programme()
        scores = pg.partner_scores(p)
        self.assertEqual(max(scores, key=scores.get), p["partners"]["chosen"])

    def test_price_must_weigh_more_than_40_percent_to_change_the_choice(self):
        c6 = next(s for s in pg.sensitivity(programme()) if s["id"] == "C6")
        self.assertEqual(c6["to"], 40)
        self.assertEqual(c6["otherWinners"], ["P-C"])


class FitGap(unittest.TestCase):
    def test_every_requirement_in_scope_has_a_uat_scenario(self):
        self.assertEqual(pg.fit_gap(programme())["untested"], [])

    def test_tests_referenced_exist(self):
        p = programme()
        scenarios = {s["id"] for s in p["testing"]["scenarios"]}
        for r in p["requirements"]:
            for t in r["tests"]:
                self.assertIn(t, scenarios, r["id"])

    def test_every_scenario_proves_at_least_one_requirement(self):
        p = programme()
        used = {t for r in p["requirements"] for t in r["tests"]}
        self.assertEqual({s["id"] for s in p["testing"]["scenarios"]} - used, set())

    def test_at_most_three_extensions(self):  # ADR-001
        self.assertLessEqual(pg.fit_gap(programme())["extensions"], 3)

    def test_ids_are_unique(self):
        ids = [r["id"] for r in programme()["requirements"]]
        self.assertEqual(len(ids), len(set(ids)))


class GoNoGo(unittest.TestCase):
    def setUp(self):
        self.moments = {g["id"]: g for g in pg.go_no_go(programme(), migrations())}

    def test_first_moment_is_no_go_on_the_lot_data(self):
        g = self.moments["GNG-1"]
        self.assertEqual(g["decision"], "NO-GO")
        self.assertEqual(g["hardFail"], ["G1", "G2", "G3"])

    def test_second_moment_is_go(self):
        g = self.moments["GNG-2"]
        self.assertEqual(g["decision"], "GO")
        self.assertEqual(g["hardFail"] + g["softFail"], [])

    def test_a_hard_criterion_cannot_be_waived(self):
        results = [{"id": "G1", "type": "hard", "pass": False}] + [{"id": f"S{i}", "type": "soft", "pass": True} for i in range(4)]
        self.assertEqual(pg.decide(results)["decision"], "NO-GO")

    def test_three_soft_failures_is_no_go(self):
        results = [{"id": "H", "type": "hard", "pass": True}] + [{"id": f"S{i}", "type": "soft", "pass": False} for i in range(3)]
        self.assertEqual(pg.decide(results)["decision"], "NO-GO")

    def test_two_soft_failures_is_go(self):
        results = [{"id": "H", "type": "hard", "pass": True}] + [{"id": f"S{i}", "type": "soft", "pass": i > 1} for i in range(4)]
        self.assertEqual(pg.decide(results)["decision"], "GO")


class Raid(unittest.TestCase):
    def test_every_entry_has_an_owner(self):
        for r in programme()["raid"]:
            self.assertTrue(r["owner"], r["id"])

    def test_risk_scores_are_on_a_1_to_5_scale(self):
        for r in programme()["raid"]:
            if r["type"] == "Risico":
                self.assertTrue(1 <= r["prob"] <= 5 and 1 <= r["impact"] <= 5, r["id"])


if __name__ == "__main__":
    unittest.main()
