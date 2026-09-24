---
file: docs/issue-register.csv
sha256: f3f5b5d48fb958b853d9a76a64f2698c09e4bdb0a74ecf1d61d7e3d08da4f6a4
---

```
classification,issue-id,title,fixture,expected,reference-actual,repair-boundary
SYNTHETIC,ll-duplicate,Repeated identical event is counted twice,data/events-duplicate.jsonl,3 global events and 2 for item-a,4 global events and 3 for item-a,Deduplicate identical IDs after conflict validation
SYNTHETIC,ll-order,Arrival order overrides later event minute,data/events-out-of-order.jsonl,item-a closed at minute 20,item-a open at minute 10,Sort unique events by minute then event ID before reduction
```
