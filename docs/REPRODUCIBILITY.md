# Reproducibility

## Smoke Test

```bash
python scripts/run_artifact_smoke_test.py
```

The smoke test searches recursively for expected report JSON files and checks key counts.

## Detailed Reports

Expected report filenames:

- `fixture_expansion_gate_v2_0.json`
- `semantic_checker_matrix_v2_0.json`
- `mutation_evaluation_report_v2_0.json`
- `v2_0_evaluation_dashboard.json`

Expected counts:

- 45 controlled fixtures.
- 12 semantic failure classes.
- semantic checker 45/45.
- 72 mutation cases.
- 72/72 mutation detection/classification.

The smoke test is repository consistency checking. It is not external validation.
