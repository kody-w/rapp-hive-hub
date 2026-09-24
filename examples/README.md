# Generic non-RAPP example

The `generic/` documents describe the fictional Firefly Mesh protocol. They
contain no RAPP or GitHub integration and demonstrate that the core is
protocol-neutral.

## Where this fits

The RAPP/1 organism reads bottom to top: 0 RAPP/1 · 1 Estate · 2 Organization
(canonical `rapp-work/1`, specified) · 3 Hive (`rapp-hive/1` Private Hive in
force; the Hive folder convention experimental) · 4 your device · 5 Brainstem ·
6 you. This hub is RAPP Work starters plus discovery and join across Hives, and
this example sits outside that stack on purpose: the same core dials a Hive of
any declared protocol. Transport carries; signatures decide. See the
[README](../README.md#where-this-fits).

Regenerate deterministic documents from the typed API:

```bash
PYTHONPATH=src python examples/build_generic.py
```

Then run the lifecycle shown in the repository README. The human and AI cards
target the same public record; the AI card also carries an inert fetch plan.
No example contains a credential or QR factor.
