---
id: portfolio-decision
title: Record the reviewable portfolio decision proposal
status: blocked
depends_on:
  - allocation-proposal
  - portfolio-messaging
---

# Record the reviewable portfolio decision proposal

Room `executive-office` (Portfolio owner). Blocked until [[allocation-proposal]], [[portfolio-messaging]] are done.

Use the decision example as a structural guide, not a prior approval. Name active and parked units, experiment exit rules, capacity totals, risks, and the exact human decision still needed.

## Inputs

- `deliverables/allocation-proposal.csv`, from [[allocation-proposal]]
- `deliverables/portfolio-messages.md`, from [[portfolio-messaging]]
- `docs/decision-template.json`: [[decision-template.json]]
- `docs/charter.md`: [[charter]]

## Outputs

- `deliverables/portfolio-decision.json`

## Acceptance

- Every unit is either active, parked, or rejected with a reason.
- The decision distinguishes recommendation from owner authorization.
- There are no claimed sales, real customers, or fabricated completed experiments.
