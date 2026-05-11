# Reviewer Quickstart

This is the shortest reviewer path.

## 1. Inspect the Fixture Manifest

Open:

- `pd_oap_icsme2026_artifact/fixtures/v2_0/manifest.json`
- `pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json`

Expected key numbers:

- 45 controlled fixtures.
- 3 operation families.
- 21 expected-valid fixtures.
- 24 expected-invalid fixtures.
- 12 semantic failure classes.

## 2. Run or Inspect the Checker Matrix

Run the semantic checker matrix command in `REPRODUCIBILITY.md`, or inspect:

- `pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json`

Expected key number: 45/45 declared fixture outcomes matched.

## 3. Inspect Mutation Evaluation

Open:

- `pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json`

Expected key numbers:

- 72 mutation cases.
- 72/72 mutation detection/classification.
- mutation unexpected_count 0.

## 4. Inspect the Dashboard

Open:

- `pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.json`

Expected summary: fixture, checker, mutation, operation-family, and failure-class evidence.

## 5. Optional Secondary Material

The simulated reviewability material contains 468 deterministic tasks. It is secondary artifact material, not human-subject evidence.
