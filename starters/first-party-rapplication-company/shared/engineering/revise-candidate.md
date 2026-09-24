---
id: revise-candidate
title: Prepare the reviewed successor or exact no-change candidate
status: blocked
depends_on:
  - plan-iteration
---

# Prepare the reviewed successor or exact no-change candidate

Room `engineering` (Rapplication engineering). Blocked until [[plan-iteration]] is done.

Apply approved repairs and rerun affected and regression checks. Freeze the new complete subject and link its predecessor without editing old evidence. For an approved no-change assessment, preserve every subject hash and explicitly record that no successor was built.

## Inputs

- `deliverables/iteration-plan.md`, from [[plan-iteration]]
- `deliverables/candidate-manifest.json`, from [[build-candidate]]
- `deliverables/build-evidence.json`, from [[build-candidate]]
- `deliverables/support-kit.md`, from [[prepare-support]]
- `templates/candidate-manifest.json`: [[candidate-manifest.json]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/final-candidate.json`
- `deliverables/iteration-evidence.json`

## Acceptance

- All changed bindings invalidate previous qualification; none is inherited by version label.
- Failed observations and predecessor artifacts remain available privately.
- The result is build evidence, not independent approval.
