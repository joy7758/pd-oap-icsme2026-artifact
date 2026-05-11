# PD-OAP ICSME 2026 Artifact

This repository contains the PD-OAP artifact package: executable operation-accountability materials for reviewable public-data operations.

Repository: https://github.com/joy7758/pd-oap-icsme2026-artifact

## Contents

- 45 controlled fixtures across 3 operation families.
- 21 expected-valid fixtures.
- 24 expected-invalid fixtures.
- 12 semantic failure classes.
- Semantic checker with 45/45 declared fixture outcomes matched.
- 72 mutation cases.
- Mutation detection/classification 72/72.
- Evaluation dashboard and generated reports.
- 468 simulated reviewability tasks as secondary deterministic artifact material.

## Quickstart

Run the smoke test:

```bash
python scripts/run_artifact_smoke_test.py
```

Expected checks:

- fixture manifest or report contains 45 controlled fixtures;
- semantic checker report contains 45/45 match;
- mutation report contains 72 mutation cases and 72/72 expected failure matches;
- evaluation dashboard report exists.

See:

- `docs/REVIEWER_QUICKSTART.md`
- `docs/REPRODUCIBILITY.md`
- `docs/EXPECTED_OUTPUTS.md`
- `docs/NON_CLAIMS.md`

## Comparator Summary

The journal-only comparator study is internal deterministic evidence. Condition ratios:

- full_pd_oap 1.000
- policy_as_code_bundle 0.583
- policy_bundle 0.500
- provenance_graph 0.333
- logs_only 0.250
- schema_only_validation 0.167

This is not external validation and not human-study evidence.

## Non-Claims

This repository makes no legal compliance claim, no production deployment claim, no human-study result claim, no external validation claim, and no independent rerun claim.
