---
file: reference/check_acceptance.py
sha256: c0e6320a0862eb2b2e06b0c19f74cf5b6394546339f62639b715ff3e1b4f10ef
---

```
"""Strict desired-behavior checks; --characterize verifies known baseline failures."""

import argparse
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
SPEC = importlib.util.spec_from_file_location("line_ledger_acceptance", HERE / "line_ledger.py")
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


def check():
    fixtures = json.loads((DATA / "expected-contract.json").read_text(encoding="utf-8"))["cases"]
    observations = []
    for fixture in fixtures:
        if not re.fullmatch(r"[a-z0-9-]+\.jsonl", fixture["fixture"]):
            raise ValueError("fixture must be a local JSONL basename")
        actual = ledger.reduce_events(ledger.load_events(DATA / fixture["fixture"]))
        passed = actual == fixture["expected"]
        observations.append({
            "id": fixture["id"], "passed": passed,
            "reference_passes": fixture["reference_passes"],
            "matches_reference_characterization": passed == fixture["reference_passes"],
            "expected": fixture["expected"], "actual": actual,
        })
    return {
        "classification": "SYNTHETIC",
        "artifact_kind": "reference-contract-check",
        "release_eligible": bool(observations) and all(row["passed"] for row in observations),
        "passing_cases": sum(row["passed"] for row in observations),
        "failing_cases": sum(not row["passed"] for row in observations),
        "observations": observations,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--characterize", action="store_true", help="succeed only when the supplied known-failure pattern is reproduced")
    args = parser.parse_args()
    result = check()
    result["mode"] = "reference-characterization" if args.characterize else "strict-acceptance"
    if args.characterize:
        result["warning"] = "Matching known failures is not a release pass."
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.characterize:
        return 0 if all(row["matches_reference_characterization"] for row in result["observations"]) else 1
    return 0 if result["release_eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```
