---
title: The Micro-Manufacturing Company
---

# The Micro-Manufacturing Company

Take a small physical object from parameters to a reviewable pilot plan.

Coordinate industrial design, engineering, sourcing, production planning, quality, logistics, and finance around a non-safety-critical two-piece desk caddy. Trace dimensional changes through material, cost, fit, inspection, and packaging before any approved fabrication.

## Rooms

- `shared/industrial-design/`: industrial-designer. Own the desk-use requirements, compartment layout, and proposed width change.
- `shared/engineering/`: design-engineer. Maintain the parametric tray/insert geometry and nominal fit calculations.
- `shared/sourcing/`: sourcing-planner. Maintain clearly synthetic material and cost assumptions without quotations, orders, or supplier claims.
- `shared/production-planning/`: production-planner. Plan a bounded pilot and manual fit sequence, without executing fabrication or specifying hazardous machinery.
- `shared/quality/`: quality-engineer. Define measurements, evaluate synthetic sample rows, and hold nonconforming geometry.
- `shared/logistics/`: logistics-planner. Check modeled packing dimensions, mass, labeling, and approval boundaries.
- `shared/finance/`: cost-analyst. Reproduce material, handling, packaging, and overhead scenarios with explicit rounding and uncertainty.
- `shared/casework/`: the shared delivery case. Its intake is [[stackline-caddy-pilot]]; shared inputs sit in `artifacts/`; accepted deliverables land here too.

Related starters, for discovery only (never shared membership): `applied-invention-lab`.

All names, estimates and observations are synthetic public starter data.
