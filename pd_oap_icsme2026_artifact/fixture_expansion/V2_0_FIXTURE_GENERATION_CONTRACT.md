# v2.0 Fixture Generation Contract

## Generation Rules

- Fixture identifiers are deterministic.
- Fixtures use no real government data.
- Fixtures use synthetic local identifiers only.
- All fixtures use the same required top-level shape.
- Valid fixtures must be internally consistent.
- Invalid fixtures target one primary failure class.
- Edge fixtures are valid but non-happy-path.
- All fixture content must be reproducible from the generation script.

## Claim Boundaries

- no legal compliance claim
- no deployment claim
- no statistical population claim

## Controlled Benchmark Requirements

The generated suite is a controlled fixture benchmark with:

- about 45 fixtures
- at least 12 failure classes
- mutation evaluation prepared for a later stage
- raw-count reporting prepared through manifest and expected-results files

This generation contract does not implement the v2 semantic checker. It creates the executable fixture substrate that the checker and mutation stages can use later.
