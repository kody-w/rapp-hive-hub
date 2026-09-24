---
id: exception-routing
title: Design accountable exception handoffs
status: blocked
depends_on:
  - acceptance-review
---

# Design accountable exception handoffs

Room `architecture` (Solution architecture). Blocked until [[acceptance-review]] is done.

Turn the observed reason codes into a proposed routing table with role, minimum evidence, proposed response window, and re-evaluation trigger. Do not auto-approve any exception.

## Inputs

- `deliverables/acceptance-matrix.csv`, from [[acceptance-review]]
- `docs/handoff-contracts.md`: [[handoff-contracts]]
- `docs/process-facts.md`: [[process-facts]]

## Outputs

- `deliverables/exception-routing.md`

## Acceptance

- Each observed reason code has a proposed owner and return path.
- Commercial policy and missing-data routes remain separate.
- All response times are targets to validate, not measured service levels.
