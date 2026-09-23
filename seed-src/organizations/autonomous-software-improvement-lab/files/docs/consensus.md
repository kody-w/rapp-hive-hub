# Consensus: how a tally is decided

Eight strategists looked at the same software through eight different
lenses. When several of them independently arrive at the same required fix,
that is strong evidence it matters. The tally turns eight reports into one
decision.

## Inputs

Each report ends with two machine-readable parts (see `templates/report.md`):

- **Top 3 features**: the three things the strategist would build next,
  ranked, each starting with a key such as `storage:non-atomic-save`;
- **Candidate ledger**: five to ten rows of
  `key | problem | proposed solution | impact 1-5 | confidence 1-5 | implemented`.

A key is kebab-case `area:problem`. Strategists choose keys independently, so
the same problem can arrive under different keys. That is expected.

## The rules

1. **Support** of a cluster is the number of *distinct* strategists whose Top 3
   or ledger names it. One strategist counts once, however often it repeats
   itself.
2. **Cluster by what the solution requires, not by wording.** Two keys belong
   together when one change delivers both. Two keys stay apart when they need
   different changes, even if they sound alike. The orchestrator records merges
   in `gG/aliases.json` (`{"other:key": "canonical:key"}`) and re-runs
   `tally`; the merged keys stay visible in the tally.
3. **Majority** means support of at least ceil((N+1)/2): 5 of 8, 4 of 7, 3 of
   5.
4. **Ranking**: by support, then by the mean of impact x confidence over the
   ledger rows that scored it, then by how many strategists put it in their
   Top 3, then by key.
5. **Continuous mode takes the top 3 clusters.** Each pick is labeled
   *majority* or *majority-like* (below the threshold).
6. **When nothing reaches a majority**, take the broadest coherent cluster as
   majority-like, and say so explicitly in the tally and the review.
7. **Minority findings are carried forward.** Every cluster that was not
   selected goes into the recurring-problems table, which accumulates across
   generations. A problem found again and again rises there and is a good
   candidate for a future focus.
8. **Minority branches are kept.** Their work was verified by the strategist
   who made it. The kit never deletes a branch.
9. **Interrupted work is never counted.** Tally only a complete set of reports.
   If strategists died, re-run the generation (`resume --apply`); `--allow-missing`
   exists for diagnosis and marks the tally incomplete.

## Worked example

**This is an illustrative example, not a result.** It uses the practice
target and the eight sample reports embedded in `reference/test_improver.py`
(labeled as fixtures there), so you can reproduce every number with the kit.
Strategists are S1 to S8.

The kit's first draft, clustered by key:

| Key | Named by | Support | Impact x confidence per row | Mean |
|---|---|---|---|---|
| `storage:non-atomic-save` | S1 S2 S3 S6 S8 | 5/8 | 25 20 20 16 16 | 19.4 |
| `errors:catch-all-hides-cause` | S1 S2 S4 S5 S7 | 5/8 | 16 16 20 9 12 | 14.6 |
| `cli:remove-silent-noop` | S2 S4 S5 S7 | 4/8 | 20 16 12 16 | 16.0 |
| `tests:write-real-home` | S1 S4 S8 | 3/8 | 15 12 20 | 15.7 |
| `cli:json-output` | S3 S6 S7 | 3/8 | 6 6 12 | 8.0 |
| `import:quadratic-save` | S1 S6 | 2/8 | 12 15 | 13.5 |
| `import:duplicate-default-contradiction` | S3 S8 | 2/8 | 12 9 | 10.5 |
| `storage:lost-update` | S5 | 1/8 | 25 | 25.0 |

Then the orchestrator reads the proposed solutions:

- S5's `storage:lost-update` proposes "serialize writers with a lock file and
  re-read under it". The `storage:non-atomic-save` proposals already require
  exactly that (atomic replace, plus a lock and a re-read). One change
  delivers both, so the orchestrator writes
  `{"storage:lost-update": "storage:non-atomic-save"}` to `aliases.json`.
  Support becomes **6/8**.
- `import:quadratic-save` sounds related to saving, but its fix (validate every
  row, then save once) is a different change. It stays separate.
- `errors:catch-all-hides-cause` and `cli:remove-silent-noop` are both about
  telling the truth, but one needs error reporting and the other needs id
  validation in `remove`. Different changes: they stay separate. Merging them
  would have freed a slot, which is exactly why the rule is about the required
  solution and not about the theme.

Decision after re-running the tally:

1. `storage:non-atomic-save`, 6/8, **majority**;
2. `errors:catch-all-hides-cause`, 5/8, **majority**;
3. `cli:remove-silent-noop`, 4/8, **majority-like**, and the tally says so.

The other clusters go to the recurring-problems table. Suppose, again as an
illustration, that generation 2 also finds `tests:write-real-home` with three
strategists: the table then shows it in g1 and g2 with total support 6, and
the owner might make hermetic tests the focus of generation 3.

**When nothing reaches a majority**, for example if the largest cluster has 4
of 8, the tally reads: "No cluster reached a majority (5 of 8). The broadest
cluster, with 4 of 8, is taken as majority-like: confirm it is one coherent
solution before integrating." The orchestrator confirms that the cluster
really requires one solution, or splits it and takes the broadest coherent
part.

## What the kit drafts, and what stays human

`tally` parses the reports, counts support, ranks clusters, applies
`aliases.json`, checks each claimed commit against the strategist's branch,
lists same-area keys worth a second look, and drafts `TALLY.md`,
`tally.json` and the integrator brief. Deciding which keys require the same
solution, confirming that a majority-like cluster is coherent, and writing
the reconciliation for the integrator are judgment calls: the orchestrator
makes them and writes them down before integrating.
