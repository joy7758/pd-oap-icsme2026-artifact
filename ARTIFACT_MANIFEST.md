# Artifact Manifest

## Included Directories

- `pd_oap_icsme2026_artifact/definition_hardening/`
- `pd_oap_icsme2026_artifact/fixture_expansion/`
- `pd_oap_icsme2026_artifact/fixtures/v2_0/`
- `pd_oap_icsme2026_artifact/semantic_checker/`
- `pd_oap_icsme2026_artifact/mutation_evaluation/`
- `pd_oap_icsme2026_artifact/evaluation/`
- `pd_oap_icsme2026_artifact/se_framing/`
- `pd_oap_icsme2026_artifact/simulated_reviewability/`
- `pd_oap_icsme2026_artifact/tools/`
- `pd_oap_icsme2026_artifact/reports/`

## Expected Counts

- 45 controlled fixtures.
- 3 operation families.
- 21 expected-valid fixtures.
- 24 expected-invalid fixtures.
- 12 semantic failure classes.
- 45/45 semantic checker declared-outcome match.
- 72 mutation cases.
- 72/72 mutation detection/classification.
- 468 simulated reviewability tasks as secondary artifact material.

## Required Scripts

- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_fixture_expansion_gate.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_semantic_check.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_generate_mutations.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_mutation_evaluation_gate.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_generate_simulated_review_tasks.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_run_simulated_reviewability.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_simulated_reviewability_gate.py`
- `pd_oap_icsme2026_artifact/tools/pd_oap_v2_evaluation_dashboard.py`

## Required Reports

- `pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/simulated_reviewability_report_v2_0.json`
- `pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.json`
