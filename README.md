# Jessica Leal
### AI Automation Specialist · Full-Stack Developer · Business Systems

I turn operational problems into working software: API integrations, reliable data workflows, AI-assisted customer operations, and tools that reduce repetitive work.

My background bridges **economics and business operations** with hands-on product engineering. I have worked on business applications involving messaging, scheduling, customer records, reporting, and operational workflows.

**Core technologies:** TypeScript · React · JavaScript · PostgreSQL · Supabase · n8n · REST APIs · Webhooks · Vercel · OpenAI integrations

## Selected work

| Project | What it demonstrates | Evidence |
|---|---|---|
| **ARVI — Business AI Automation** | WhatsApp Cloud API integrations, conversational business context, human handoff, multi-system workflows | [Case study](cases/arvi.md) · [Interactive demo](https://arvi-portfolio-demo.vercel.app/) |
| **Service Business Scheduling** | Google Calendar integration, appointment workflows, automated reminders | [Case study](cases/service-scheduling.md) |
| **Hospitality & Business Software** | Product development for operational processes, administrative records and hospitality workflows | [Case study](cases/business-software.md) |
| **Lead Data Pipeline — Independent Demo** | Event idempotency, contact deduplication, source attribution, error handling, reproducible tests | [Runnable sample](demos/lead-pipeline/) |
| **Sales Call Review — Independent Demo** | Validating hypothetical AI output, enforcing a scoring rubric and verifying evidence against transcripts | [Runnable sample](demos/call-review/) |

## Code sample: lead data integration

The [Lead Data Pipeline](demos/lead-pipeline/) is a **self-contained example**, built with Python and SQLite using fictional data. It demonstrates the kind of defensive integration design useful for marketing operations: preserving each source event, preventing duplicate contact records, and making ingestion observable. This is not a customer deployment and does not connect to live advertising or CRM accounts.

```bash
cd demos/lead-pipeline
python3 -m unittest discover -s tests -v
python3 src/lead_pipeline.py --db /tmp/jessica-leads-demo.sqlite ingest --file data/sample_leads.json
python3 src/lead_pipeline.py --db /tmp/jessica-leads-demo.sqlite report
```

## How I work

1. Understand the business problem, its data sources and success criteria.
2. Define contracts, permissions, failure cases and a testable first milestone.
3. Implement the smallest reliable version and verify with representative scenarios.
4. Document ownership, handover, and ongoing operational risks.

## Engineering approach

- Prefer official APIs and clear authorization boundaries.
- Use idempotency and durable state for high-value workflows.
- Distinguish **demonstration data** from verified production functionality.
- Keep credentials and customer data out of source control.
- Make human review possible for consequential AI decisions.

## Collaboration and confidentiality

I contribute to both individual and collaborative products. Case studies describe my role at a high level; **private repositories are intentionally not shared** because they contain product IP or client-specific work. Public examples are original, isolated educational demonstrations using fictional data.

## Contact

- **Portfolio demo:** https://arvi-portfolio-demo.vercel.app/
- **GitHub:** https://github.com/rohigroup
- **Website:** https://www.sinenredo.co

_This repository is a curated portfolio, not the source of ARVI, Arribo, or client production deployments._
