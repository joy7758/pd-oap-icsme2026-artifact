# Simulated Reviewability Design

## Objective

The objective is to compare how much review-relevant information is preserved by four representation conditions: logs_only, policy_only, provenance_only, and full_pd_oap.

## Source specimens

The simulation uses 117 source specimens:

- 45 base fixtures
- 72 mutation fixtures
- total 117

The fixed v2.0 background is that the base fixture semantic checker matrix matched 45/45 and the mutation evaluation detected and classified 72/72 mutation cases with unexpected_count 0.

## Representation expansion

Each source specimen is expanded into four deterministic task views. The total simulated task count is:

117 source specimens x 4 representation conditions = 468 simulated review tasks.

## Scoring dimensions

The simulated reviewer scores six dimensions:

1. operation_reconstruction
2. policy_basis_assessment
3. evidence_completeness_assessment
4. reference_closure_assessment
5. failure_detection_assessment
6. claim_boundary_assessment

Each dimension is scored as true, partial, or false. The score is deterministic.

## Interpretation

The simulation evaluates representation-level information availability. It does not claim human-study results and does not measure actual reviewer behavior. It can support a bounded claim that full PD-OAP preserves more review-relevant information under the defined scoring model.
