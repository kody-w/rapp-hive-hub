---
id: pilot-quality-gate
title: Assemble a conditional pilot gate
status: blocked
depends_on:
  - adoption-workshop
  - pilot-value-case
---

# Assemble a conditional pilot gate

Room `quality` (Acceptance and quality). Blocked until [[adoption-workshop]], [[pilot-value-case]] are done.

Evaluate the acceptance matrix, unresolved data proposals, adoption plan, and measurement case. Record pass, fail, or not-observed for each gate; lack of real policy confirmation must remain visible.

## Inputs

- `deliverables/acceptance-matrix.csv`, from [[acceptance-review]]
- `deliverables/correction-proposals.csv`, from [[correction-proposals]]
- `deliverables/adoption-session.md`, from [[adoption-workshop]]
- `deliverables/pilot-value-case.md`, from [[pilot-value-case]]
- `docs/requirements.csv`: [[requirements.csv]]

## Outputs

- `deliverables/pilot-gate.json`

## Acceptance

- Every requirement has a gate disposition and linked evidence.
- The gate cannot authorize production connectivity, spending, or invoice issuance.
- Unobserved adoption and real-policy validation are explicitly not passed.
