---
id: request-separate-decision
title: Obtain an external decision, never issue one for the CEO
status: blocked
depends_on:
  - independent-verification
---

# Obtain an external decision, never issue one for the CEO

Room `release` (Internal release and public promotion). Blocked until [[independent-verification]] is done.

Assemble a request for the owner-selected external decider. Obtain a separate actual decision after verification through the trusted native host. The decider is neither a builder nor the CEO; release merely retains the reference and cannot fill an approval on their behalf.

## Inputs

- `deliverables/verification.json`, from [[independent-verification]]
- `deliverables/final-review.json`, from [[final-review]]
- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/company-configuration.json`, from [[configure-company]]
- `templates/decision-receipt.json`: [[decision-receipt.json]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/decision-reference.json`

## Acceptance

- A real separate decision references the exact review, verification and subject, and follows them.
- No template, CEO statement or failed verification is accepted as approval.
- Absent or refused decisions leave promotion blocked.
