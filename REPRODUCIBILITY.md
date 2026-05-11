# Reproducibility

Run commands from the repository root.

## 1. Fixture Expansion Gate

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_fixture_expansion_gate.py \
  --fixture-root pd_oap_icsme2026_artifact/fixtures/v2_0 \
  --design-root pd_oap_icsme2026_artifact/fixture_expansion \
  --write-report pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.md
```

Expected report: 45 controlled fixtures over 3 operation families.

## 2. Semantic Checker Matrix

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_semantic_check.py \
  --matrix pd_oap_icsme2026_artifact/fixtures/v2_0 \
  --write-report pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json
```

Expected report: 45/45 declared outcomes matched and unexpected_count 0.

## 3. Mutation Evaluation

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_mutation_evaluation_gate.py \
  --mutation-root pd_oap_icsme2026_artifact/mutation_evaluation/mutations/v2_0 \
  --checker pd_oap_icsme2026_artifact/tools/pd_oap_v2_semantic_check.py \
  --write-report pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.md
```

Expected report: 72 mutation cases, 72/72 detection/classification, and mutation unexpected_count 0.

## 4. Simulated Reviewability Gate

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_simulated_reviewability_gate.py \
  --root pd_oap_icsme2026_artifact/simulated_reviewability \
  --write-report pd_oap_icsme2026_artifact/reports/simulated_reviewability_gate_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/simulated_reviewability_gate_v2_0.md
```

Expected report: 468 deterministic simulated reviewability tasks pass as secondary artifact material.

## 5. Evaluation Dashboard

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_evaluation_dashboard.py \
  --fixture-report pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json \
  --checker-report pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json \
  --mutation-report pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json \
  --write-report pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.md
```

Expected report: dashboard combines fixture, checker, and mutation evidence.
