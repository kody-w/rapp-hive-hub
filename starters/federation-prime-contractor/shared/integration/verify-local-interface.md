---
id: verify-local-interface
title: Validate local fixture and dependency contracts
status: blocked
depends_on:
  - freeze-prime-engagement
---

# Validate local fixture and dependency contracts

Room `integration` (integration-lead). Blocked until [[freeze-prime-engagement]] is done.

Run the authored utility tests and inspect the explicit deliverable/dependency/matrix inputs. Validate only local inert JSON; do not import code, contact a partner, or add a workspace pointer.

## Inputs

- `interfaces/pilot.json`: [[pilot.json]]
- `data/deliverables.csv`: [[deliverables.csv]]
- `data/dependencies.csv`: [[dependencies.csv]]
- `data/acceptance-matrix.csv`: [[acceptance-matrix.csv]]
- `fixtures/submissions.json`: [[submissions.json]]
- `fixtures/rework-submissions.json`: [[rework-submissions.json]]
- `tools/acceptance.py`: [[acceptance.py]]
- `tests/test_acceptance.py`: [[test_acceptance.py]]
- `deliverables/prime-scope.json`, from [[freeze-prime-engagement]]

## Outputs

- `deliverables/interface-validation.json`

## Acceptance

- Rejects unknown rules, duplicate artifacts, cycles, unknown candidates, and unexpected artifact fields.
- Confirms an acyclic dependency chain from prototype to operating model and pilot kit to the prime's derived report.
- Describes offline behavior flags as content declarations, not dynamic proof that a partner application works.
