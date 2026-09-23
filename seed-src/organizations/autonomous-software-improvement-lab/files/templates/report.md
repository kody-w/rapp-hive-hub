# G{GEN} - {STRATEGY_NAME} - {STRATEGY_SLUG}

## Verdict
(One or two sentences: the most important problem, and your fix.)

## Evidence
(What your strategy found: file:line references, commands, measurements,
observations.)

## Why this target
(Why it beats the other problems your strategy surfaced.)

## Solution
(Design, files changed, behavior before and after.)

## Verification
(Every verify command with its result. Anything that could not run, and why.)

## Commits
(Full or short sha and subject for each commit on branch {BRANCH}. Confirm that
`git status` is clean.)

## Risks
(What could go wrong, and what is left to do.)

## Top 3 features
(The three features you would have the orchestrator build next, ranked,
whether you implemented them or not. One line each, starting with the key in
backticks, then a one-line spec, then why it matters. Replace the angle
brackets.)
1. `<area>:<problem>` - one-line spec - why it matters
2. `<area>:<problem>` - one-line spec - why it matters
3. `<area>:<problem>` - one-line spec - why it matters

## Candidate ledger
(Five to ten rows: the most important problems you found, implemented or not.
Use the same keys as your Top 3. Impact and confidence are integers from 1 to
5. Implemented is yes, partial or no. Never put a `|` inside a cell.)

| key | problem | proposed solution | impact 1-5 | confidence 1-5 | implemented |
|---|---|---|---|---|---|
| <area>:<problem> | one line | one line | 4 | 3 | no |
