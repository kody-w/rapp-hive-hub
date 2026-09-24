---
id: freeze-local-corpus
title: Freeze the bounded synthetic corpus
status: ready
depends_on: []
---

# Freeze the bounded synthetic corpus

Room `collection` (collection-editor). Ready to claim: it depends on nothing.

Inventory the five source files and the question's as-of date. Record provenance, authored-source type, limitations, and exclusion of live collection.

## Inputs

- `case/question.json`: [[question.json]]
- `sources/announcements.csv`: [[announcements.csv]]
- `sources/release-notes.csv`: [[release-notes.csv]]
- `sources/lab-notes.csv`: [[lab-notes.csv]]
- `sources/support-notices.csv`: [[support-notices.csv]]
- `sources/benchmark-runs.csv`: [[benchmark-runs.csv]]

## Outputs

- `deliverables/corpus-inventory.json`

## Acceptance

- Lists five explicit files and eighteen uniquely identified records, all SYNTHETIC.
- Treats vendor-authored items as one origin group and the lab-style notes as another, without claiming statistical independence.
