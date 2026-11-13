# Lead Data Pipeline — Reproducible Code Sample

**A synthetic portfolio project.** No Google Ads, Google Local Services Ads, WhatConverts, or Tekmetric account is connected. No private/customer data is included.

## What it shows

- Normalize basic US telephone numbers (demo rules; not an international phone parsing library).
- Preserve every distinct inbound lead event with its `source` and `external_id`.
- Use database-level unique constraints for **event idempotency** and **contact deduplication**.
- Allow one contact to have multiple genuine inquiries from different channels.
- Validate inputs and record errors for triage instead of silently dropping invalid leads.
- Produce a simple source summary suitable as a building block for a reporting layer.
- Provide deterministic tests without any dependencies beyond the Python standard library.

## Run locally

Requires Python 3.10+.

```bash
python3 -m unittest discover -s tests -v
python3 src/lead_pipeline.py --db leads.sqlite ingest --file data/sample_leads.json
python3 src/lead_pipeline.py --db leads.sqlite report
```

The demo reports 3 unique events, 2 unique contacts, 1 repeated delivery and no invalid events. Delete `leads.sqlite` to start over.

## Why the design matters

**Deduplicating contacts is not deduplicating submissions.** A customer may contact a business twice. An event retry should not create duplicate events, but two different inquiries from that same person should both be recorded.

A real production pipeline would additionally need authenticated ingestion, a durable queue/outbox, full observability, provider rate-limit handling, encryption/access policies, stronger international phone parsing, client-specific reconciliation rules, tests against official APIs, and appropriate data processing agreements.

## Architecture

```text
Sample JSON events
      |
      v
Validate + normalize
      |
      v
SQLite transaction
  +--> contacts (unique normalized phone)
  +--> lead_events (unique source + external_id)
  +--> ingestion_errors (invalid records)
      |
      v
CLI source report
```

**Authorship:** Independent demonstration prepared for Jessica Leal's public engineering portfolio. It is not represented as a commissioned client integration.
