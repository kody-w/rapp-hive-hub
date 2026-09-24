---
file: templates/candidate-manifest.json
sha256: 24ff71091182ad23e9533734da80ff5b8bf54927a17fdfb20f60d8b34e174766
---

```
{
  "template_kind": "candidate-manifest",
  "status": "unbound",
  "product": "session-checklist",
  "track": "first-party",
  "generation": null,
  "predecessor_candidate": null,
  "subject_sha256": {
    "source_inventory": null,
    "candidate_inventory": null,
    "dependency_lock": null,
    "support_inventory": null,
    "qualification_suite": null,
    "public_projection_inventory": null
  },
  "inventory": [],
  "evidence_references": [],
  "unresolved_gates": ["build", "internal-release", "dogfood", "feedback", "ship-decision", "promote"],
  "rapp1_structural_check": "not-run",
  "authenticated_acceptance": false,
  "external_effects_authorized": false,
  "instructions": "Compute exact raw hashes from reviewed relative-path inventories. This form is neither an application manifest nor a RAPP/1 frame."
}
```
