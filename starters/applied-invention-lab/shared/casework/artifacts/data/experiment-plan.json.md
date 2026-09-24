---
file: data/experiment-plan.json
sha256: e6091595c336e502e329ec8b8cd2a9ca216cc9b8c7b782017eeca51f7874d340
---

```
{
  "classification": "SYNTHETIC",
  "plan_id": "paired-permutation-study",
  "random_seed": 1729,
  "repetitions": 20,
  "algorithms": ["input-first-fit", "dominant-first-fit", "volume-first-fit"],
  "pairing": "One shuffled item order per scenario and trial is shared across all algorithms.",
  "exclusions": "None; an invalid input stops the run.",
  "reporting": "Retain every trial and descriptive min/max/mean. Do not generalize to a real population."
}
```
