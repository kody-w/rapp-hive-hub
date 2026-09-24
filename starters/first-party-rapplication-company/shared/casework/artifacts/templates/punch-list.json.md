---
file: templates/punch-list.json
sha256: 0f6e27ca961e8df59b7d23459d4030ed9fe4b3067e3ef9609ae6fc57b90d1499
---

```
{
  "template_kind": "craftsmanship-review",
  "status": "unreviewed",
  "candidate_manifest_sha256": null,
  "previous_review_reference": null,
  "reviewer_role_reference": null,
  "recommendation": null,
  "focus": null,
  "dimension_scores": [],
  "items": [],
  "item_template": {
    "id": null,
    "first_seen_candidate": null,
    "locus": null,
    "observed": null,
    "expected": null,
    "severity": null,
    "owner_team": null,
    "verification_method": null,
    "disposition": "open",
    "reason": null,
    "evidence_references": []
  },
  "severity_values": ["blocker", "major", "minor", "screw"],
  "allowed_recommendations": ["ship", "iterate", "stop"],
  "approval": false,
  "instructions": "Preserve earlier findings. Blocker/major items must be resolved with current evidence; ship is only a recommendation."
}
```
