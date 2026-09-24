---
id: issue-owner-decision-gate
title: Issue the investigation handoff and owner gate
status: blocked
depends_on:
  - challenge-decision-brief
---

# Issue the investigation handoff and owner gate

Room `briefing` (briefing-editor). Blocked until [[challenge-decision-brief]] is done.

Resolve or explicitly retain each challenge, and issue a final investigation handoff. Record what the corpus supports and what evidence/approval must exist before a real pilot or commercial decision.

## Inputs

- `deliverables/pilot-decision-brief.md`, from [[draft-decision-brief]]
- `deliverables/brief-challenge.md`, from [[challenge-decision-brief]]
- `deliverables/prospective-investigation.csv`, from [[plan-next-collection]]
- `case/question.json`: [[question.json]]

## Outputs

- `deliverables/investigation-handoff.json`

## Acceptance

- Includes as-of date, confidence limitations, unresolved inquiries, and exact review triggers.
- Authorizes no contact, procurement, deployment, identity lookup, private collection, or cross-organization access.
