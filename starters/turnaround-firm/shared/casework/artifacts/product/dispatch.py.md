---
file: product/dispatch.py
sha256: 273c16c64eb389baa1d867f4d94b12cbcb7eb3661c480d3b15fb150e14ef3c59
---

```
"""Original SYNTHETIC defective baseline, retained for the recovery exercise.

Known bug: alphabetical priority sorting chooses low before normal before
urgent. This file performs no work and must not be treated as a production
scheduler. The recovery utility contrasts it with a candidate policy.
"""


def next_batch(tickets, limit=4):
    if type(limit) is not int or limit < 0:
        raise ValueError("A nonnegative integer batch limit is required")
    eligible = [ticket for ticket in tickets if ticket["state"] == "open" and not ticket["blocked_by"]]
    return sorted(eligible, key=lambda ticket: (ticket["priority"], ticket["opened_on"], ticket["ticket_id"]))[:limit]
```
