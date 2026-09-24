---
id: packing-prototype
title: Turn assignments into an operator-readable prototype
status: blocked
depends_on:
  - baseline-computation
---

# Turn assignments into an operator-readable prototype

Room `prototyping` (Usable prototype and observation design). Blocked until [[baseline-computation]] is done.

Create a printable packing-instruction prototype from one baseline scenario. Show tote labels, exact item IDs, both scalar loads, remaining capacity, and a prominent model-only warning.

## Inputs

- `deliverables/baseline-results.json`, from [[baseline-computation]]
- `docs/prototype-brief.md`: [[prototype-brief]]
- `docs/operator-worksheet.csv`: [[operator-worksheet.csv]]
- `data/items.csv`: [[items.csv]]

## Outputs

- `deliverables/packing-instructions.html`

## Acceptance

- Every chosen scenario item appears once in the printable artifact.
- Both load dimensions and the model-only warning are visible without color dependence.
- No real tote was packed and no physical dimensions were verified merely by rendering the instructions.
