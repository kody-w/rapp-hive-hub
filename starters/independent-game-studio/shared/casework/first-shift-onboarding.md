---
id: first-shift-onboarding
title: "Mosslight Courier: make the first bridge legible"
---

# Mosslight Courier: make the first bridge legible

SYNTHETIC production case: eight authored first-session records suggest confusion about four-beat bridge timing and undo. The starter game already works. Improve onboarding and readability without adding accounts, a backend, new mechanics, or an invented playtest result.

## Inputs

- `case/production.json`: [[production.json]]
- `data/playtests.csv`: [[playtests.csv]]
- `design/rules.md`: [[rules]]
- `quality/acceptance.csv`: [[acceptance.csv]]

## Success criteria

- All three original boards are solvable by the deterministic engine and are playable with arrows or WASD, Space, U, and R.
- A release candidate opens directly from disk with no fetches, CDN, trackers, storage, server, or dependency install.
- Bridge and carrying state are conveyed by text/symbol as well as color; generated audio is off by default.
- The synthetic baseline remains five completions out of eight, with five bridge stalls; no real improvement is claimed without new observation.
- A producer records pass, rework, or hold against every supplied acceptance case before any separately approved publication.

## Tasks

- [[lock-first-shift]] Freeze a two-day first-shift revision (`production`, ready)
- [[make-release-decision]] Record a conditional release decision (`production`, blocked)
- [[revise-bridge-onboarding]] Specify bridge and carrying onboarding (`design`, blocked)
- [[implement-onboarding]] Build the bounded onboarding revision (`engineering`, blocked)
- [[prepare-readable-art]] Produce a symbol-complete mini atlas (`art`, blocked)
- [[specify-local-cues]] Map optional synthesized cues (`audio`, blocked)
- [[verify-game-regressions]] Execute rule and input acceptance cases (`quality`, blocked)
- [[audit-offline-release]] Audit file-only release and accessibility (`quality`, blocked)
- [[read-synthetic-feedback]] Reproduce the authored feedback baseline (`player-research`, blocked)
- [[plan-observed-playtest]] Prepare the next real first-session test (`player-research`, blocked)

No reference artifact counts as completed work without review.
