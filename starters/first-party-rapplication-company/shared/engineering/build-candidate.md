---
id: build-candidate
title: Build and freeze a complete candidate
status: blocked
depends_on:
  - reference-baseline
  - prepare-support
---

# Build and freeze a complete candidate

Room `engineering` (Rapplication engineering). Blocked until [[reference-baseline]], [[prepare-support]] are done.

Implement the approved host integration using existing native interfaces only if authorized capabilities exist. Bind source, candidate, dependencies, support, suite and proposed public distribution with exact relative-path inventories and hashes. Run local checks and list every unproven gate.

## Inputs

- `deliverables/reference-evidence.json`, from [[reference-baseline]]
- `deliverables/support-kit.md`, from [[prepare-support]]
- `deliverables/chat-design.md`, from [[design-chat]]
- `deliverables/product-spec.md`, from [[specify-product]]
- `templates/candidate-manifest.json`: [[candidate-manifest.json]]
- `docs/pipeline.md`: [[pipeline]]
- `data/pipeline-gates.json`: [[pipeline-gates.json]]

## Outputs

- `deliverables/candidate-manifest.json`
- `deliverables/build-evidence.json`

## Acceptance

- All six subject components are bound, including an explicit dependency lock even when empty.
- The selected chat adapter is implemented and tested or the task stays blocked.
- Canonical record checks use pinned native tools; structural success is not authenticated acceptance.
