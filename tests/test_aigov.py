import os
import unittest

from aigov import QUESTIONS, assess, load, severity
from aigov.cli import main

EX = os.path.join(os.path.dirname(__file__), "..", "examples", "use_cases.json")
NONE = {q: False for q in QUESTIONS}


def ans(**kw):
    return {**NONE, **kw}


class TierTests(unittest.TestCase):
    def test_all_no_is_low(self):
        r = assess("x", ans())
        self.assertEqual((r.tier, r.score), ("low", 0))

    def test_boundaries(self):
        self.assertEqual(assess("x", ans(personal_data=True, customer_facing=True)).tier, "low")      # 4
        self.assertEqual(assess("x", ans(personal_data=True, no_human_review=True)).tier, "medium")   # 5
        self.assertEqual(assess("x", ans(sensitive_data=True, no_human_review=True,
                                         irreversible_action=True, personal_data=True)).tier, "high")  # 11

    def test_higher_tier_includes_lower_controls(self):
        high = assess("x", ans(sensitive_data=True, no_human_review=True, irreversible_action=True, personal_data=True))
        self.assertIn("All medium-tier controls", high.controls)
        self.assertEqual(high.approver, "AI governance board")

    def test_blocker_regulated_automated_decision_on_people(self):
        r = assess("x", ans(regulated_domain=True, affects_individuals=True, no_human_review=True))
        self.assertEqual(r.tier, "blocked")
        self.assertIn("legal", r.approver.lower())
        self.assertIn("no human review", r.reasons[0])

    def test_adding_human_review_removes_the_block(self):
        r = assess("x", ans(regulated_domain=True, affects_individuals=True, no_human_review=False))
        self.assertNotEqual(r.tier, "blocked")

    def test_reasons_list_heavy_factors(self):
        r = assess("x", ans(sensitive_data=True, personal_data=True))
        self.assertEqual(r.reasons, ["sensitive_data"])


class ValidationTests(unittest.TestCase):
    def test_unknown_question(self):
        with self.assertRaises(ValueError):
            assess("x", {**NONE, "vibes": True})

    def test_missing_answer_is_an_error_not_a_default(self):
        partial = dict(NONE)
        del partial["personal_data"]
        with self.assertRaises(ValueError):
            assess("x", partial)

    def test_non_boolean(self):
        with self.assertRaises(ValueError):
            assess("x", {**NONE, "personal_data": "yes"})


class ExampleTests(unittest.TestCase):
    def test_example_use_cases(self):
        by = {r.name: r for r in load(EX)}
        self.assertEqual(by["Meeting notes summariser (internal)"].tier, "low")
        self.assertEqual(by["Onboarding knowledge assistant"].tier, "medium")
        self.assertEqual(by["Client reply drafting"].tier, "medium")
        self.assertEqual(by["Candidate shortlisting agent"].tier, "blocked")
        self.assertNotEqual(by["Candidate shortlisting with recruiter review"].tier, "blocked")

    def test_cli_assess_ok_and_error(self):
        self.assertEqual(main(["assess", EX]), 0)
        self.assertEqual(main(["assess", EX + ".missing"]), 2)


class IncidentTests(unittest.TestCase):
    def test_data_exposure_is_sev1(self):
        self.assertEqual(severity(False, True, False, True), "SEV1")

    def test_uncontained_harm_is_sev1(self):
        self.assertEqual(severity(True, False, False, False), "SEV1")

    def test_contained_harm_is_sev2(self):
        self.assertEqual(severity(True, False, False, True), "SEV2")

    def test_repeated_uncontained_is_sev2(self):
        self.assertEqual(severity(False, False, True, False), "SEV2")

    def test_repeated_contained_is_sev3(self):
        self.assertEqual(severity(False, False, True, True), "SEV3")

    def test_one_off_contained_is_sev4(self):
        self.assertEqual(severity(False, False, False, True), "SEV4")

    def test_cli_incident(self):
        self.assertEqual(main(["incident", "--exposed"]), 0)


if __name__ == "__main__":
    unittest.main()
