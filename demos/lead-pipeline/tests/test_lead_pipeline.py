"""Regression scenarios for synthetic data ingestion."""

import json
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lead_pipeline import SCHEMA, ingest, normalize_us_phone, report  # noqa: E402


class LeadPipelineTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.executescript(SCHEMA)
        self.sample = json.loads((ROOT / "data" / "sample_leads.json").read_text())

    def tearDown(self):
        self.db.close()

    def test_phone_normalization(self):
        self.assertEqual(normalize_us_phone("(512) 555-0101"), "+15125550101")
        self.assertEqual(normalize_us_phone("+1 512 555 0101"), "+15125550101")
        with self.assertRaises(ValueError):
            normalize_us_phone("555")

    def test_retries_do_not_duplicate_events(self):
        result = ingest(self.db, self.sample)
        self.assertEqual(result, {"inserted_events": 3, "duplicate_events": 1, "invalid_events": 0})
        again = ingest(self.db, self.sample)
        self.assertEqual(again["inserted_events"], 0)
        self.assertEqual(again["duplicate_events"], 4)

    def test_same_contact_preserves_distinct_inquiries(self):
        ingest(self.db, self.sample)
        self.assertEqual(report(self.db)["unique_contacts"], 2)
        self.assertEqual(report(self.db)["unique_events"], 3)
        self.assertEqual(report(self.db)["events_by_source"], {
            "google_ads": 1, "local_services_ads": 1, "whatconverts": 1,
        })

    def test_invalid_events_logged(self):
        result = ingest(self.db, [{"source": "google_ads", "external_id": "bad"}])
        self.assertEqual(result["invalid_events"], 1)
        self.assertEqual(report(self.db)["invalid_event_attempts"], 1)
        self.assertEqual(report(self.db)["unique_events"], 0)

    def test_source_scoped_event_ids(self):
        a = dict(self.sample[0])
        b = dict(self.sample[0], source="whatconverts")
        self.assertEqual(ingest(self.db, [a, b])["inserted_events"], 2)
        self.assertEqual(report(self.db)["unique_contacts"], 1)


if __name__ == "__main__":
    unittest.main()
