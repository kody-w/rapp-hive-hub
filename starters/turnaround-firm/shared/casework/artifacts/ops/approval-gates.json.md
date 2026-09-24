---
file: ops/approval-gates.json
sha256: 6e2e89930421dc3b1ab4b0a2b8fb80f8bb31e79e249fd77504ecbaaa6ea69fdf
---

```
{
  "classification":"SYNTHETIC",
  "default":"planning-only",
  "gates":[
    {"effect":"production-deployment","required":["candidate regression evidence","rollback/hold procedure","explicit owner approval"],"approved":false},
    {"effect":"support-work-against-accounts","required":["reviewed ticket scope","capacity and data-access review","explicit owner approval"],"approved":false},
    {"effect":"customer-message-or-refund-promise","required":["truthful draft","financial commitment review","explicit owner approval"],"approved":false},
    {"effect":"contractor-or-hosting-cost-change","required":["service continuity review","contract/cost evidence","explicit owner approval"],"approved":false},
    {"effect":"payment-trade-or-financing","required":["separate qualified review","explicit owner authority"],"approved":false}
  ],
  "reference_utility_effects":[],
  "warning":"A simulation or passing local test is not a financial instruction, completed support action, or approval."
}
```
