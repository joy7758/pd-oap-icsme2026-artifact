# Representation Ablation Conditions

The conditions are an ablation of operation-accountability information.

## logs_only

- Included fields: operation id, operation kind, event time, actor reference, subject reference, and decision status.
- Excluded fields: explicit policy basis details, evidence package, validation expectations, full provenance links, and non-claims.
- Expected strengths: partial operation reconstruction.
- Expected limitations: weak policy assessment, weak evidence assessment, weak failure detection, and no claim-boundary visibility.

## policy_only

- Included fields: policy id, policy version, policy clause, allowed requester roles, allowed purposes, and required conditions if available.
- Excluded fields: concrete operation execution, evidence package, actual provenance closure, and actual decision record.
- Expected strengths: policy understanding.
- Expected limitations: weak operation reconstruction and weak evidence assessment.

## provenance_only

- Included fields: actor, requester, subject, catalog, policy, purpose, decision refs, and provenance links.
- Excluded fields: semantic validation expectations, full evidence completeness, non-claims, and explicit checker result.
- Expected strengths: stronger reconstruction than logs or policy alone.
- Expected limitations: partial failure detection and no claim-boundary visibility.

## full_pd_oap

- Included fields: complete operation-accountability statement, policy, purpose, decision, conditions, provenance, evidence, validation expected result, non-claims, and intentional defect metadata if the source specimen already includes it.
- Excluded fields: no external real-world evidence beyond the synthetic source specimen.
- Expected strengths: full deterministic reviewability under the simulated reviewer model.
- Expected limitations: synthetic and deterministic, not human validation.
