---
id: plan-iteration
title: Plan only evidence-earned iteration
status: blocked
depends_on:
  - review-craftsmanship
---

# Plan only evidence-earned iteration

Room `product` (Product scope and acceptance). Blocked until [[review-craftsmanship]] is done.

Prioritize the review's one focus and required repairs. Plan bounded changes with acceptance and disjoint ownership. If no change is justified, record no-change explicitly; do not invent a defect or pretend that an iteration happened.

## Inputs

- `deliverables/review.json`, from [[review-craftsmanship]]
- `deliverables/punch-list.json`, from [[review-craftsmanship]]
- `deliverables/product-spec.md`, from [[specify-product]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/iteration-plan.md`

## Acceptance

- Every proposed repair links to an observed finding and verification method.
- Blocker/major findings cannot be deferred through shipment.
- A changed subject requires new internal release, dogfood, review and verification.
