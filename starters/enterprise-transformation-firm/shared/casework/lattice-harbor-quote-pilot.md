---
id: lattice-harbor-quote-pilot
title: "Lattice Harbor Supply: quote readiness before any invoice is issued"
---

# Lattice Harbor Supply: quote readiness before any invoice is issued

Lattice Harbor Supply and every account, quote, policy, and process observation are SYNTHETIC. Eight office-supply quotes expose credit, discount, terms, inactive-account, missing-data, and rounding cases. The reference utility computes line-rounded amounts and returns needs-data, needs-review, or ready-for-human-approval. It never issues invoices, authorizes credit, or contacts an enterprise system.

## Inputs

- `docs/client-brief.md`: [[client-brief]]
- `docs/process-facts.md`: [[process-facts]]
- `docs/requirements.csv`: [[requirements.csv]]
- `data/accounts.csv`: [[accounts.csv]]
- `data/quotes.csv`: [[quotes.csv]]
- `data/quote-lines.csv`: [[quote-lines.csv]]
- `data/policy.json`: [[policy.json]]

## Success criteria

- All eight quote cases are traced from original inputs through requirements to explicit acceptance results.
- The prototype reproduces exact expected monetary totals using decimal half-up line and shipping-tax rounding.
- Missing data blocks readiness; policy exceptions require review; even a clean quote still requires human approval.
- Each exception has a proposed accountable role, handoff payload, and return path.
- The pilot case reports hypotheses and measurement plans, never fabricated savings or a completed deployment.

## Tasks

- [[engagement-boundary]] Bound the quote-readiness engagement (`account-strategy`, ready)
- [[pilot-value-case]] Prepare an honest pilot measurement case (`account-strategy`, blocked)
- [[source-reconciliation]] Reconcile quote and account source facts (`discovery`, blocked)
- [[requirements-trace]] Build field-to-requirement traceability (`discovery`, blocked)
- [[calculation-boundary]] Specify the replaceable calculation contract (`architecture`, blocked)
- [[exception-routing]] Design accountable exception handoffs (`architecture`, blocked)
- [[prototype-reproduction]] Reproduce the offline quote batch (`engineering`, blocked)
- [[correction-proposals]] Propose source corrections without fabricating authorization (`engineering`, blocked)
- [[acceptance-review]] Check arithmetic and exception acceptance (`quality`, blocked)
- [[pilot-quality-gate]] Assemble a conditional pilot gate (`quality`, blocked)
- [[adoption-workshop]] Prepare the role-based practice session (`adoption`, blocked)
- [[owner-handoff]] Deliver the reversible pilot owner pack (`adoption`, blocked)

No reference artifact counts as completed work without review.
