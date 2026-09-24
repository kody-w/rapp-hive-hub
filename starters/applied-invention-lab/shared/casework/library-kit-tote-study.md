---
id: library-kit-tote-study
title: "Library Kit Tote Study: does a two-capacity heuristic actually reduce modeled bins?"
---

# Library Kit Tote Study: does a two-capacity heuristic actually reduce modeled bins?

A fictional library kit service wants a more explainable way to group harmless paper, cloth, foam, and counting materials into reusable totes. All items, capacities, shapes, and operating assumptions are SYNTHETIC. Eleven item-type rows expand into 29 instances across four scenarios. The offline reference compares input-order, dominant-load, and volume-first greedy packing, verifies every assignment, and optionally proves small scalar-model optima. It does not certify three-dimensional fit, lifting safety, physical performance, or commercial demand.

## Inputs

- `docs/problem-brief.md`: [[problem-brief]]
- `docs/data-dictionary.md`: [[data-dictionary]]
- `data/items.csv`: [[items.csv]]
- `data/capacity.json`: [[capacity.json]]
- `data/experiment-plan.json`: [[experiment-plan.json]]
- `reference/expected-baseline.json`: [[expected-baseline.json]]

## Success criteria

- Every item instance appears exactly once and every modeled tote respects both integer capacity constraints.
- The authored baseline reproduces all four expected scenario counts, including a case where the dominant heuristic is worse than input order.
- Seeded permutation experiments preserve all trials and can be rerun with matching source hashes and results.
- Lower-bound proofs, bounded search, unproven results, and skipped search are clearly distinguished.
- Physical fit, operator usefulness, cost, novelty, and customer demand remain unmeasured until separately approved studies occur.

## Tasks

- [[research-assumptions]] Frame the practical question and model assumptions (`research`, ready)
- [[research-interpretation]] Interpret gains, regressions, and model gaps (`research`, blocked)
- [[lab-decision]] Record a conditional next-experiment decision (`research`, blocked)
- [[baseline-computation]] Run the packing baseline and invariant checks (`experiments`, blocked)
- [[variant-experiment]] Run the predeclared seeded comparison (`experiments`, blocked)
- [[packing-prototype]] Turn assignments into an operator-readable prototype (`prototyping`, blocked)
- [[physical-fit-protocol]] Prepare a harmless physical-fit observation protocol (`prototyping`, blocked)
- [[dataset-audit]] Audit the original synthetic dataset (`replication`, blocked)
- [[replication-run]] Replicate the computation independently (`replication`, blocked)
- [[application-hypothesis]] Assess a bounded application hypothesis (`commercialization`, blocked)

No reference artifact counts as completed work without review.
