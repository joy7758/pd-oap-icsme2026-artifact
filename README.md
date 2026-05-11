# PD-OAP ICSME 2026 Artifact

This artifact supports the ICSME 2026 Data Showcase submission for PD-OAP: executable operation-accountability artifacts for reviewable public-data operations.

## What Is Included

- 45 controlled fixtures across 3 operation families.
- 21 expected-valid fixtures.
- 24 expected-invalid fixtures.
- 12 semantic failure classes.
- Semantic checker with 45/45 declared fixture outcomes matched.
- 72 mutation cases.
- Mutation detection/classification 72/72.
- Generated reports and an evaluation dashboard.
- 468 simulated reviewability tasks as secondary artifact material.

## Directory Layout

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

## Quickstart Commands

Run commands from the repository root.

### Fixture Expansion Gate

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_fixture_expansion_gate.py \
  --fixture-root pd_oap_icsme2026_artifact/fixtures/v2_0 \
  --design-root pd_oap_icsme2026_artifact/fixture_expansion \
  --write-report pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.md
```

Expected output: fixture gate passes for 45 controlled fixtures.

### Semantic Checker Matrix

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_semantic_check.py \
  --matrix pd_oap_icsme2026_artifact/fixtures/v2_0 \
  --write-report pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json
```

Expected output: semantic checker matched 45/45 declared outcomes with unexpected_count 0.

### Mutation Evaluation Gate

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_mutation_evaluation_gate.py \
  --mutation-root pd_oap_icsme2026_artifact/mutation_evaluation/mutations/v2_0 \
  --checker pd_oap_icsme2026_artifact/tools/pd_oap_v2_semantic_check.py \
  --write-report pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.md
```

Expected output: 72 mutation cases detected and classified with 72/72 expected failure matches and mutation unexpected_count 0.

### Simulated Reviewability Gate

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_simulated_reviewability_gate.py \
  --root pd_oap_icsme2026_artifact/simulated_reviewability \
  --write-report pd_oap_icsme2026_artifact/reports/simulated_reviewability_gate_v2_0.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/simulated_reviewability_gate_v2_0.md
```

Expected output: secondary deterministic simulated reviewability materials pass with 468 tasks.

### Evaluation Dashboard

```bash
python3 pd_oap_icsme2026_artifact/tools/pd_oap_v2_evaluation_dashboard.py \
  --fixture-report pd_oap_icsme2026_artifact/reports/fixture_expansion_gate_v2_0.json \
  --checker-report pd_oap_icsme2026_artifact/reports/semantic_checker_matrix_v2_0.json \
  --mutation-report pd_oap_icsme2026_artifact/reports/mutation_evaluation_report_v2_0.json \
  --write-report pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.json \
  --write-markdown pd_oap_icsme2026_artifact/reports/v2_0_evaluation_dashboard.md
```

Expected output: dashboard summarizes 45 fixtures, 12 semantic failure classes, checker 45/45, 72 mutation cases, and 72/72 mutation detection/classification.

## Non-Claims

This artifact makes no legal compliance claim, no production deployment claim, no human-study result claim, no real government approval claim, and no statistical population benchmark claim.

The fixtures are synthetic and contain no human participant data, no real public-sector decision data, and no confidential operational data.
