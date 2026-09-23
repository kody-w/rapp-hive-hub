# Practice Shelf answer key

**Spoiler. Keep this file out of the practice repository.** Open it only after
the generation-1 tally is drafted. It lists the flaws that were put into
Practice Shelf on purpose, so the owner desk can measure what the loop found.
Strategists may also find genuine problems that are not listed here; those
count when their reports carry evidence.

Every flaw below was reproduced against the shipped files before publication.

| # | Flaw | Where | Lenses likely to find it |
|---|---|---|---|
| 1 | The tests write into the real home directory | `CommandLineTests` in `test_shelf.py` uses the default data directory | hermetic test audit, empirical sweep, trust boundary |
| 2 | `remove` silently does nothing on an unknown or malformed id, and still says `removed` with exit code 0, although its help promises to fail | `parse_id`, `Shelf.remove`, `main` | error paths, promise audit, outcome semantics, copy review |
| 3 | Contradictory defaults: `add` refuses a duplicate link, but `import` accepts duplicates by default, so importing the same export twice doubles the shelf | `Shelf.add` vs `Shelf.import_file` | defaults audit, invariants, artifact conformance, configuration matrix |
| 4 | Non-atomic, unlocked writes: `save` truncates the file in place, and every command does load → change → save, so two concurrent writers lose updates and reuse ids, and an interrupted write leaves an unreadable shelf | `Shelf.save`, `Shelf.__init__` | concurrency and races, data durability, seeded invariants, lifecycle, soak |
| 5 | The catch-all error handler hides every cause: `error: operation failed` even for the carefully written `ShelfError` messages, a corrupt file, or a missing import file | `main` | error paths, first contact, diagnostics, copy review |
| 6 | `import` rewrites the whole file after every row, so large imports are quadratic (about 27 s for 2,000 links on the reference machine) and multiply flaw 4's crash window | `Shelf.import_file` calling `add` | performance budget, soak, synthetic-input driver |

## How each one reproduces

1. Run the suite with a throwaway home and list it afterwards:
   `.practice-shelf/shelf.json` appears. The kit's baseline reports it as
   `home_writes`.
2. `python3 shelf.py remove abc` and `python3 shelf.py remove 999` both print
   `removed` and exit 0.
3. Export a one-link shelf, import the export twice: three links.
4. Open two `Shelf()` objects on the same file, add a different link through
   each: only the second survives, and both used the same next id. Write a
   truncated `shelf.json`: every command now fails.
5. Add the same link twice from the command line: the second attempt prints
   `error: operation failed` instead of `already on the shelf`.
6. Import a generated export with 2,000 links and time it.

## What a complete fix includes (for judging the integration)

- 1: a preload the test module imports first, giving the whole test process a
  throwaway home and clearing `PRACTICE_SHELF_*`; a check that the real home is
  untouched.
- 2: unknown or malformed ids fail with a clear message and a non-zero exit;
  a test for each case.
- 3: one documented duplicate policy shared by `add` and `import`, with an
  explicit flag to change it; an idempotent re-import test.
- 4: write to a temporary file in the same directory, flush and `fsync`, then
  atomically replace; serialize writers (a lock file) and re-read under the
  lock; tests for the lost update and the truncated file.
- 5: user-facing errors print their cause and the next step; unexpected
  errors name the operation and the file; tests assert the messages.
- 6: import validates everything first and saves once; a scaled test with a
  time budget generous enough not to flake.

The strongest consensus usually forms around 4 (with 3 or 6 as part of the
same "safe writes" solution) and around 2 + 5 ("tell the truth about
outcomes"). That is an expectation from the design of this target, not a
recorded result: your strategists decide.
