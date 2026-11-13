import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from validate_review import validate_review  # noqa: E402


class CallReviewTests(unittest.TestCase):
    def setUp(self):
        self.valid = json.loads((ROOT / "data" / "example_review.json").read_text())

    def test_valid_mocked_ai_output(self):
        self.assertEqual(validate_review(self.valid), {"score": 6, "max_score": 6, "percentage": 100.0})

    def test_rejects_hallucinated_quote(self):
        broken = copy.deepcopy(self.valid)
        broken["evaluation"]["criteria"][0]["evidence"] = "We promise a discount"
        with self.assertRaisesRegex(ValueError, "absent"):
            validate_review(broken)

    def test_rejects_invalid_numeric_score(self):
        broken = copy.deepcopy(self.valid)
        broken["evaluation"]["criteria"][0]["score"] = 25
        with self.assertRaisesRegex(ValueError, "invalid score"):
            validate_review(broken)


if __name__ == "__main__":
    unittest.main()
