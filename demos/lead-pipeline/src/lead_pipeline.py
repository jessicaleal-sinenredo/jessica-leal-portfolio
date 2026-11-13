"""Dependency-free, fictional marketing lead ingestion demonstration.

This is not production-ready ingestion and does not access provider APIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    phone TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS lead_events (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id),
    source TEXT NOT NULL,
    external_id TEXT NOT NULL,
    submitted_at TEXT NOT NULL,
    campaign TEXT NOT NULL,
    message TEXT NOT NULL,
    UNIQUE(source, external_id)
);
CREATE TABLE IF NOT EXISTS ingestion_errors (
    id INTEGER PRIMARY KEY,
    source_payload TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

REQUIRED = ("source", "external_id", "submitted_at", "name", "phone")


def normalize_us_phone(raw: str) -> str:
    """Normalize illustrative US numbers; intentionally limited in scope."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
    if len(digits) != 10:
        raise ValueError("phone must have ten US digits")
    return "+1" + digits


def validate(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("lead is not a JSON object")
    missing = [key for key in REQUIRED if not isinstance(payload.get(key), str) or not payload[key].strip()]
    if missing:
        raise ValueError(f"required fields missing/empty: {', '.join(missing)}")
    cleaned = {key: payload[key].strip() for key in REQUIRED}
    cleaned["phone"] = normalize_us_phone(cleaned["phone"])
    cleaned["campaign"] = str(payload.get("campaign") or "unknown").strip()
    cleaned["message"] = str(payload.get("message") or "").strip()
    return cleaned


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.executescript(SCHEMA)
    return connection


def ingest(connection: sqlite3.Connection, payloads: list[Any]) -> dict[str, int]:
    stats = {"inserted_events": 0, "duplicate_events": 0, "invalid_events": 0}
    for payload in payloads:
        try:
            lead = validate(payload)
        except ValueError as exc:
            with connection:
                connection.execute(
                    "INSERT INTO ingestion_errors(source_payload, reason) VALUES(?, ?)",
                    (json.dumps(payload, ensure_ascii=False), str(exc)),
                )
            stats["invalid_events"] += 1
            continue

        # Transaction ensures the contact and event are persisted together.
        with connection:
            existing = connection.execute(
                "SELECT id FROM lead_events WHERE source = ? AND external_id = ?",
                (lead["source"], lead["external_id"]),
            ).fetchone()
            if existing is not None:
                stats["duplicate_events"] += 1
                continue
            connection.execute(
                "INSERT OR IGNORE INTO contacts(phone, name) VALUES(?, ?)",
                (lead["phone"], lead["name"]),
            )
            contact_id = connection.execute(
                "SELECT id FROM contacts WHERE phone = ?", (lead["phone"],)
            ).fetchone()[0]
            connection.execute(
                """INSERT INTO lead_events(
                    contact_id, source, external_id, submitted_at, campaign, message
                ) VALUES(?, ?, ?, ?, ?, ?)""",
                (
                    contact_id, lead["source"], lead["external_id"],
                    lead["submitted_at"], lead["campaign"], lead["message"],
                ),
            )
        stats["inserted_events"] += 1
    return stats


def report(connection: sqlite3.Connection) -> dict[str, Any]:
    contacts = connection.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    events = connection.execute("SELECT COUNT(*) FROM lead_events").fetchone()[0]
    errors = connection.execute("SELECT COUNT(*) FROM ingestion_errors").fetchone()[0]
    by_source = dict(connection.execute(
        "SELECT source, COUNT(*) FROM lead_events GROUP BY source ORDER BY source"
    ).fetchall())
    return {"unique_contacts": contacts, "unique_events": events,
            "invalid_event_attempts": errors, "events_by_source": by_source}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("leads.sqlite"))
    commands = parser.add_subparsers(dest="command", required=True)
    ingest_command = commands.add_parser("ingest")
    ingest_command.add_argument("--file", type=Path, required=True)
    commands.add_parser("report")
    args = parser.parse_args()
    with connect(args.db) as connection:
        if args.command == "ingest":
            payloads = json.loads(args.file.read_text(encoding="utf-8"))
            if not isinstance(payloads, list):
                parser.error("input JSON must contain a list of leads")
            print(json.dumps(ingest(connection, payloads), indent=2))
        else:
            print(json.dumps(report(connection), indent=2))


if __name__ == "__main__":
    main()
