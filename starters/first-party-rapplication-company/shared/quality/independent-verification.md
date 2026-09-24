---
id: independent-verification
title: Issue current-subject independent verification
status: blocked
depends_on:
  - review-projection
---

# Issue current-subject independent verification

Room `quality` (Independent quality and verification). Blocked until [[review-projection]] is done.

Have authorized verifiers distinct from all builders and CEO independently reproduce acceptance, inspect final findings, verify public safety and record real evidence through the existing trusted native mechanism. Filling the template is not issuing an authenticated record.

## Inputs

- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/final-dogfood.json`, from [[final-dogfood]]
- `deliverables/final-review.json`, from [[final-review]]
- `deliverables/final-punch-list.json`, from [[final-review]]
- `deliverables/privacy-report.json`, from [[review-projection]]
- `deliverables/license-review.json`, from [[review-projection]]
- `templates/independent-verification.json`: [[independent-verification.json]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/verification.json`

## Acceptance

- Distinct verifier identities and current grants are actually checked; duplicate labels do not increase the count.
- Verification binds all subject components, review and actual checks.
- A structural RAPP/1 pass is labeled separately from authenticated acceptance; failed verification cannot approve.
