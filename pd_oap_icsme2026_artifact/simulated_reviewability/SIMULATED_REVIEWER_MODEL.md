# Simulated Reviewer Model

The simulated reviewer is rule-based, not human, not LLM, and not stochastic. It measures information availability under explicit rules.

## operation_reconstruction

- Input signals: operation family, operation id, actor, requester, subject, and decision.
- Scoring rule: true when the representation exposes the operation family and enough party and decision fields; partial when only sparse operation clues are visible; false when no concrete operation can be reconstructed.
- Limitation: This measures visible fields, not human understanding.

## policy_basis_assessment

- Input signals: policy id, policy version, authorization basis, allowed roles, allowed purposes, and required conditions.
- Scoring rule: true when policy basis and version are visible; partial when only a policy reference is visible; false when no policy signal is visible.
- Limitation: It does not evaluate legal sufficiency.

## evidence_completeness_assessment

- Input signals: evidence object list, evidence refs, missing evidence markers, and validation evidence expectations.
- Scoring rule: true when evidence details are visible; partial when only evidence refs are visible; false when evidence is hidden.
- Limitation: It cannot establish real evidence quality.

## reference_closure_assessment

- Input signals: dataset, catalog, policy, purpose, decision, provenance, and handoff references.
- Scoring rule: true when complete refs are visible; partial when only some links are visible; false when refs are absent.
- Limitation: It measures inspectability of visible references only.

## failure_detection_assessment

- Input signals: expected result, expected primary failure code, validation fields, intentional defect metadata, and visible failure-relevant fields.
- Scoring rule: true when the representation exposes the expected failure class for invalid source specimens; partial when the representation gives a weak signal; false when the failure is not visible.
- Limitation: It is not a human error-detection measure.

## claim_boundary_assessment

- Input signals: non-claims such as legal_sufficiency false and production_deployment false.
- Scoring rule: true when non-claims are visible; false otherwise.
- Limitation: It does not prevent misuse outside the simulation.

This model measures information availability, not human cognition.
