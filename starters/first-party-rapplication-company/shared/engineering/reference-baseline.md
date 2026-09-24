---
id: reference-baseline
title: Reproduce the bounded offline reference
status: blocked
depends_on:
  - design-chat
---

# Reproduce the bounded offline reference

Room `engineering` (Rapplication engineering). Blocked until [[design-chat]] is done.

After separate local execution approval, run the authored Python standard-library suite and command examples. Record exact commands, source hashes and observed results, including negative cases. This is source-level evidence, not live chat qualification.

## Inputs

- `deliverables/product-spec.md`, from [[specify-product]]
- `deliverables/chat-design.md`, from [[design-chat]]
- `README.md`: [[README]]
- `reference/checklist.py`: [[checklist.py]]
- `reference/test_checklist.py`: [[test_checklist.py]]
- `data/acceptance-cases.json`: [[acceptance-cases.json]]

## Outputs

- `deliverables/reference-evidence.json`

## Acceptance

- Acceptance fixtures and mutation/refusal/determinism tests actually pass or retain their failures.
- Only process memory changes; no external runtime or publication is claimed.
- Blocked execution is reported honestly instead of inventing results.
