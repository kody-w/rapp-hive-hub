---
id: lab-decision
title: Record a conditional next-experiment decision
status: blocked
depends_on:
  - physical-fit-protocol
  - application-hypothesis
---

# Record a conditional next-experiment decision

Room `research` (Problem framing and interpretation). Blocked until [[physical-fit-protocol]], [[application-hypothesis]] are done.

Combine replication, interpretation, mock-fit protocol, and application hypothesis into a reviewable stop/continue recommendation. Distinguish a working computation from a proven invention and keep external action owner-gated.

## Inputs

- `deliverables/replication-report.json`, from [[replication-run]]
- `deliverables/research-interpretation.md`, from [[research-interpretation]]
- `deliverables/physical-fit-protocol.csv`, from [[physical-fit-protocol]]
- `deliverables/application-hypothesis.md`, from [[application-hypothesis]]
- `docs/commercialization-boundary.md`: [[commercialization-boundary]]

## Outputs

- `deliverables/lab-decision.json`

## Acceptance

- The recommendation states what the code established and what it could not establish.
- All four scenarios and unfavorable evidence inform the recommendation.
- No real study, commercialization, patent filing, purchase, or publication is represented as approved or completed.
