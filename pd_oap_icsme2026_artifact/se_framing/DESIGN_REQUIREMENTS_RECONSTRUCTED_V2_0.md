# Reconstructed Design Requirements v2.0

| DR | Rationale | Design response | Evaluation evidence | Rejection concern addressed |
|---|---|---|---|---|
| DR1: Operation-level boundedness | Reviewability requires a bounded operation unit. | Define public-data operation as one access, reuse, or review decision. | 45 fixtures over 3 operation families. | Clarifies core concepts and SE scope. |
| DR2: Sector-specific field explicitness | A profile must make domain fields checkable. | Use explicit operation, requester, actor, subject, policy, purpose, decision, evidence, validation, and non-claim fields. | Fixture generation contract and top-level shape. | Moves beyond a loose technical report. |
| DR3: Reference closure and evidence linkage | Reviewers need resolvable references. | Encode dataset, catalog, handoff, policy, and evidence references. | semantic checker detects unresolved dataset, catalog, and handoff refs. | Establishes validation logic. |
| DR4: Semantic failure diagnosability | Schema shape is not enough. | Define 12 semantic failure classes and deterministic rule order. | semantic checker matrix matched 45/45. | Responds to evaluation insufficiency. |
| DR5: Checker-exercisable representation | The representation must be executable by tools. | Generate controlled fixtures with expected outcomes. | 45 fixtures checked. | Establishes software artifact evaluation. |
| DR6: Mutation-testable validation surface | Robustness needs negative-control stress tests. | Generate mutations from valid fixtures. | 72/72 mutations detected and matched. | Expands empirical/artifact evaluation. |
| DR7: Reproducible artifact packaging | Results must be regenerable. | Use deterministic scripts and JSON/Markdown reports. | evaluation dashboard overall_passed true. | Supports reproducibility as SE contribution. |
| DR8: Claim-boundary explicitness | Reviewers need safe claim limits. | Include non-claims in fixtures and contribution wording. | non-claims preserved in fixture and mutation manifests. | Avoids legal, deployment, and external adoption overclaims. |
