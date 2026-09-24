---
file: data/expected-contract.json
sha256: bf733860bbf7bd53e8ad9fdfcb06ed29d1c5f97b0f25d8152f3ef20d7c7219d5
---

```
{
  "classification": "SYNTHETIC",
  "artifact_kind": "desired-contract-not-a-completed-repair",
  "cases": [
    {
      "id": "clean", "fixture": "events-clean.jsonl", "reference_passes": true,
      "expected": {"event_count": 3, "open_items": 1, "closed_items": 1, "items": [
        {"item_id": "item-a", "state": "closed", "event_count": 2, "last_minute": 20},
        {"item_id": "item-b", "state": "open", "event_count": 1, "last_minute": 15}
      ]}
    },
    {
      "id": "duplicate", "fixture": "events-duplicate.jsonl", "reference_passes": false,
      "expected": {"event_count": 3, "open_items": 1, "closed_items": 1, "items": [
        {"item_id": "item-a", "state": "closed", "event_count": 2, "last_minute": 20},
        {"item_id": "item-b", "state": "open", "event_count": 1, "last_minute": 15}
      ]}
    },
    {
      "id": "out-of-order", "fixture": "events-out-of-order.jsonl", "reference_passes": false,
      "expected": {"event_count": 3, "open_items": 1, "closed_items": 1, "items": [
        {"item_id": "item-a", "state": "closed", "event_count": 2, "last_minute": 20},
        {"item_id": "item-b", "state": "open", "event_count": 1, "last_minute": 15}
      ]}
    }
  ]
}
```
