---
id: correction-proposals
title: Propose source corrections without fabricating authorization
status: blocked
depends_on:
  - exception-routing
---

# Propose source corrections without fabricating authorization

Room `engineering` (Prototype engineering). Blocked until [[exception-routing]] is done.

Create a correction-proposal ledger for q-105 and q-107. Record original values, why they block evaluation, what evidence is needed, and who may supply a replacement. Use proposed synthetic alternatives only as clearly labeled what-if examples.

## Inputs

- `deliverables/exception-routing.md`, from [[exception-routing]]
- `deliverables/acceptance-matrix.csv`, from [[acceptance-review]]
- `data/quotes.csv`: [[quotes.csv]]
- `data/quote-lines.csv`: [[quote-lines.csv]]

## Outputs

- `deliverables/correction-proposals.csv`

## Acceptance

- Original fixtures are preserved and all three data defects are addressed.
- Missing PO, tax code, and quantity are not guessed into approved source data.
- A reviewer can distinguish a hypothetical correction from an authorized one.
