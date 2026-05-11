# v2.0 Mutation Evaluation Design

## Design

Mutation evaluation starts from valid fixtures, injects one controlled semantic defect, and checks whether the v2 semantic checker reports the expected failure class.

## Why Valid Fixtures Are Mutated

Valid fixtures provide internally consistent starting points. A single mutation can therefore be attributed to a known semantic failure surface without mixing multiple defects.

## Operation-Family Distribution

- 6 valid access fixtures x 4 access operators = 24 mutations
- 6 valid reuse fixtures x 4 reuse operators = 24 mutations
- 6 valid review fixtures x 4 review operators = 24 mutations

Total: 72 mutations.

## Evaluation Target

The expected result is 72 detected invalid mutations, 72 expected failure-class matches, and 0 unexpected outcomes.
