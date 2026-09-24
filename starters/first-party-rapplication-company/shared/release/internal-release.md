---
id: internal-release
title: Distribute the exact candidate internally
status: blocked
depends_on:
  - build-candidate
---

# Distribute the exact candidate internally

Room `release` (Internal release and public promotion). Blocked until [[build-candidate]] is done.

Request and verify owner permission for a specific internal channel. Distribute only the bound candidate with support and recovery instructions using trusted native tooling. Record the actual result and whether the channel is signed; an unsigned channel requires explicit policy.

## Inputs

- `deliverables/candidate-manifest.json`, from [[build-candidate]]
- `deliverables/build-evidence.json`, from [[build-candidate]]
- `deliverables/support-kit.md`, from [[prepare-support]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/internal-release.json`

## Acceptance

- Actual internal artifact hashes match the complete candidate subject.
- Unsigned delivery is never labeled a signed Hive release.
- No public write, authority grant or channel access is inferred from the seed.
