---
id: build-provenance-index
title: Build the offline evidence index
status: blocked
depends_on:
  - freeze-local-corpus
---

# Build the offline evidence index

Room `collection` (collection-editor). Blocked until [[freeze-local-corpus]] is done.

Run the authored index and audit utility and its tests. Save a reviewable index with exact citations and content hashes; do not fetch sources or execute any source content.

## Inputs

- `tools/evidence.py`: [[evidence.py]]
- `tests/test_evidence.py`: [[test_evidence.py]]
- `analysis/claims.csv`: [[claims.csv]]
- `analysis/contradictions.csv`: [[contradictions.csv]]
- `analysis/hypotheses.json`: [[hypotheses.json]]
- `ops/investigation-board.csv`: [[investigation-board.csv]]
- `deliverables/corpus-inventory.json`, from [[freeze-local-corpus]]

## Outputs

- `deliverables/evidence-index.json`
- `deliverables/citation-audit.json`

## Acceptance

- Every source citation resolves to a declared file and physical CSV row, header counted as row 1.
- Every coded claim and conflict reference resolves; duplicate IDs and future-dated evidence are rejected.
