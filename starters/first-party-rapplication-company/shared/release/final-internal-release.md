---
id: final-internal-release
title: Re-establish the final candidate's internal channel
status: blocked
depends_on:
  - revise-candidate
---

# Re-establish the final candidate's internal channel

Room `release` (Internal release and public promotion). Blocked until [[revise-candidate]] is done.

Repeat authorized internal distribution for changed bytes. Reference an earlier distribution only if every subject binding is unchanged and its authority remains current. Keep the signed/unsigned qualification visible.

## Inputs

- `deliverables/final-candidate.json`, from [[revise-candidate]]
- `deliverables/iteration-evidence.json`, from [[revise-candidate]]
- `deliverables/internal-release.json`, from [[internal-release]]
- `docs/pipeline.md`: [[pipeline]]

## Outputs

- `deliverables/final-internal-release.json`

## Acceptance

- Final internal artifact and full subject hashes match exactly.
- Any absent permission or failed delivery blocks dogfood.
- No public channel or fabricated signed receipt substitutes for internal evidence.
