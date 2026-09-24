---
id: script-lock
title: Lock the script against the claim ledger
status: ready
depends_on: []
---

# Lock the script against the claim ledger

Room `explainers` (explainer-producer). Ready to claim: it depends on nothing.

Fetch the pinned RFC 6455 text, confirm its sha256, confirm every claim anchor's snippet sits inside its line range, and confirm every factual script line maps to a verified claim. Record the script and ledger sha256.

## Inputs

- `source/script.md`: [[script]]
- `source/claims.json`: [[claims.json]]
- `source/corpus.json`: [[corpus.json]]

## Outputs

- `deliverables/script/script-lock.json`

## Acceptance

- The corpus sha256 matches source/corpus.json.
- Every anchor verifies and every factual line has a verified claim key.
- Records the sha256 of script.md and claims.json.
