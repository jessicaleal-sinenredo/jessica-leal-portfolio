# Sales Call Review — AI Output Validation Demo

This is an **independent, offline portfolio example**, not a production AI scoring service.

The sample accepts **simulated AI-generated JSON** for a fictional sales call, validates its score/rubric structure, and ensures each cited piece of evidence actually appears in the provided transcript. It does **not** call an LLM or score calls autonomously.

The purpose is to demonstrate how to place deterministic business rules around probabilistic AI output before storing customer-facing performance evaluations.

```bash
python3 -m unittest discover -s tests -v
python3 src/validate_review.py data/example_review.json
```

A production implementation would require authorized transcription sources, consent/privacy controls, calibrated rubrics, sampling and human review, model monitoring, and a securely deployed scoring service.
