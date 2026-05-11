# Reviewer Quickstart

Run from repository root:

```bash
python scripts/run_artifact_smoke_test.py
```

Then inspect:

- `pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.json`
- `docs/COMPARATOR_RESULTS_SUMMARY.md`
- `docs/NON_CLAIMS.md`

Expected numbers:

- 45 controlled fixtures.
- 3 operation families.
- 21 expected-valid fixtures.
- 24 expected-invalid fixtures.
- 12 semantic failure classes.
- 45/45 semantic checker match.
- 72 mutation cases.
- 72/72 mutation detection/classification.
- 468 simulated reviewability tasks as secondary deterministic material.
