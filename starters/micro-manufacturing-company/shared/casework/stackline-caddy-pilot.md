---
id: stackline-caddy-pilot
title: "Stackline desk caddy: a 20-kit planning exercise"
---

# Stackline desk caddy: a 20-kit planning exercise

SYNTHETIC case: a fictional micro-business is considering twenty desktop organizers consisting of a tray and removable ladder insert. A request to widen the tray from 180 to 196 mm must be evaluated against a fixed packing envelope. No object has been manufactured, sourced, purchased, inspected, or shipped.

## Inputs

- `case/brief.json`: [[brief.json]]
- `design/parameters.json`: [[parameters.json]]
- `data/bom.csv`: [[bom.csv]]
- `ops/change-request.json`: [[change-request.json]]

## Success criteria

- The original SCAD source and offline planner describe the same two-part nominal geometry and 1.5 mm side clearance.
- All dollar amounts are hypothetical and reproducible from the included cost table and solid-volume model.
- The baseline synthetic inspection exercise identifies exactly three conforming and two nonconforming rows.
- The proposed 196 mm width is held because it exceeds the supplied packing envelope, even if other calculations pass.
- A pilot recommendation distinguishes design review from real fabrication, material certification, inspection, spending, and shipment approvals.

## Tasks

- [[freeze-desk-use]] Freeze the noncritical desk-use envelope (`industrial-design`, ready)
- [[decide-pilot-hold]] Issue the bounded design review decision (`industrial-design`, blocked)
- [[verify-parametric-fit]] Verify the tray and lift-out insert model (`engineering`, blocked)
- [[trace-width-change]] Trace the 196 mm width request through dependencies (`engineering`, blocked)
- [[bound-material-assumptions]] Review the inert BOM and assumed cost inputs (`sourcing`, blocked)
- [[plan-dry-assembly]] Plan fit checks and a reversible pilot sequence (`production-planning`, blocked)
- [[define-inspection-gates]] Derive a dimensional inspection sheet (`quality`, blocked)
- [[replay-inspection-samples]] Classify the synthetic gauge exercise (`quality`, blocked)
- [[check-pack-envelope]] Check the baseline packing envelope (`logistics`, blocked)
- [[calculate-pilot-economics]] Reproduce a hypothetical 20-kit cost baseline (`finance`, blocked)

No reference artifact counts as completed work without review.
