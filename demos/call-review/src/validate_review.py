"""Validate structured review output from a hypothetical AI scoring stage."""

import json
import sys
from pathlib import Path

ALLOWED_CRITERIA = {"greeting", "needs_discovery", "next_step"}


def validate_review(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    transcript = payload.get("transcript")
    evaluation = payload.get("evaluation")
    if not isinstance(transcript, str) or not transcript:
        raise ValueError("transcript must be non-empty text")
    if not isinstance(evaluation, dict):
        raise ValueError("evaluation must be an object")
    criteria = evaluation.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != len(ALLOWED_CRITERIA):
        raise ValueError("all rubric criteria must be present")
    seen = set()
    total = maximum = 0
    for item in criteria:
        if not isinstance(item, dict) or item.get("name") not in ALLOWED_CRITERIA:
            raise ValueError("unrecognized rubric criterion")
        name = item["name"]
        if name in seen:
            raise ValueError("duplicate rubric criterion")
        seen.add(name)
        score, max_score = item.get("score"), item.get("max_score")
        if type(score) is not int or type(max_score) is not int or max_score != 2 or not 0 <= score <= max_score:
            raise ValueError("invalid score")
        evidence = item.get("evidence")
        if not isinstance(evidence, str) or not evidence or evidence not in transcript:
            raise ValueError("quoted evidence is absent from the transcript")
        total += score
        maximum += max_score
    if seen != ALLOWED_CRITERIA:
        raise ValueError("incomplete rubric")
    if not isinstance(evaluation.get("coaching_note"), str):
        raise ValueError("coaching note is missing")
    return {"score": total, "max_score": maximum, "percentage": round(100 * total / maximum, 1)}


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/example_review.json")
    print(json.dumps(validate_review(json.loads(path.read_text(encoding="utf-8"))), indent=2))
