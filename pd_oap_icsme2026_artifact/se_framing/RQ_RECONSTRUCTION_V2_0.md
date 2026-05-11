# Research Question Reconstruction v2.0

## RQ1 Representation coverage

Can PD-OAP represent access, reuse, and review operation-accountability statements across controlled fixtures?

- Motivation: Show that the artifact class is not a single example.
- Method: Generate controlled fixtures over access_decision, reuse_authorization, and review_decision.
- Evidence: 45 fixtures across 3 operation families.
- Current v2.0 result: 15 fixtures per operation family.
- Limitation: Controlled synthetic fixtures.
- TOSEM criticism addressed: insufficient evaluation and weak SE framing.

## RQ2 Failure detectability

Can the semantic checker detect controlled semantic failure classes across operation families?

- Motivation: Show that validation goes beyond JSON shape.
- Method: Apply semantic checker to valid, invalid, and edge fixtures.
- Evidence: 12 semantic failure classes and semantic checker matrix.
- Current v2.0 result: 45/45 checker matched, unexpected_count 0.
- Limitation: Local reference checker.
- TOSEM criticism addressed: insufficient evaluation.

## RQ3 Mutation robustness

Can the checker detect and classify mutation-injected failures generated from valid fixtures?

- Motivation: Stress-test rule surfaces through controlled negative controls.
- Method: Generate 72 mutations from valid fixtures.
- Evidence: mutation generation and evaluation reports.
- Current v2.0 result: 72/72 mutations detected and matched, unexpected_count 0.
- Limitation: Synthetic mutations and no human reviewer task yet.
- TOSEM criticism addressed: insufficient empirical/artifact validation.

## RQ4 Reproducibility

Can the evaluation artifacts be regenerated and checked through deterministic scripts and reports?

- Motivation: Make the evaluation auditable as software artifact work.
- Method: Use deterministic generators, semantic checker, mutation gate, and dashboard reports.
- Evidence: fixture, checker, mutation, and dashboard scripts and reports.
- Current v2.0 result: dashboard overall_passed true with 45 fixtures, 12 failure classes, and 72 mutations.
- Limitation: Local scripts require future packaging for submission.
- TOSEM criticism addressed: weak software engineering connection.

## Optional RQ5 Comparative reviewability

How does full PD-OAP compare with logs-only, policy-only, and provenance-only representations?

- Motivation: Position PD-OAP against partial evidence representations.
- Method: Reuse and extend same-case comparison with raw counts.
- Evidence: v1.x ratios provide a baseline: logs_only 0.2679, policy_only 0.1964, provenance_only 0.4196, full_pd_oap 1.0.
- Current v2.0 result: not yet expanded in this phase.
- Limitation: Requires raw-count reconstruction before manuscript use.
- TOSEM criticism addressed: weak SE framing and evaluation clarity.
