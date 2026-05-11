# v2.0 Fixture Expansion Design

## Why v1.x Was Insufficient

The v1.x package had 8 fixtures: 3 valid and 5 invalid. That was enough to show that the artifact could run, but it was not enough to support a journal-scale evaluation argument. It did not cover enough operation families, failure classes, or negative-control variation to answer research questions about inspectability and reviewability.

## Why v2.0 Expands To 45 Fixtures

v2.0 expands the benchmark to 45 controlled fixtures so that evaluation can report operation-family coverage, valid/invalid behavior, edge cases, and failure-class coverage. The number is deliberately bounded but large enough to move beyond a small sanity set.

## Operation-Family Distribution

The benchmark uses a 15/15/15 distribution:

- 15 access_decision fixtures
- 15 reuse_authorization fixtures
- 15 review_decision fixtures

Each operation family contains 6 valid fixtures, 8 invalid fixtures, and 1 edge fixture.

## Fixture Categories

- Valid fixtures represent internally consistent operation-accountability statements.
- Invalid fixtures are semantic invalids, not malformed JSON.
- Edge fixtures are valid but non-happy-path cases, such as denied-but-complete decisions.

## Semantic Invalids

Invalid fixtures target one primary semantic failure class. They keep the required top-level structure so that later checker and auditor work can distinguish JSON shape from semantic failure surfaces.

## Later Stages

This expansion prepares later v2 semantic checker and mutation evaluation work. It does not implement the full v2 semantic checker and does not claim production or legal validation.
