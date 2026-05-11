# Fixture Expansion Gate v2.0

- overall_passed: True
- fixture_count: 45
- valid_count: 18
- invalid_count: 24
- edge_count: 3

## Operation Family Distribution

- access_decision: 15
- reuse_authorization: 15
- review_decision: 15

## Failure Class Coverage

- handoff_ref_unresolved: 2
- integrity_digest_mismatch: 2
- missing_authorization_basis: 2
- policy_version_mismatch: 2
- purpose_constraint_mismatch: 2
- requester_role_mismatch: 2
- reuse_condition_mismatch: 2
- reuse_condition_missing: 2
- review_evidence_missing: 2
- review_trigger_missing: 2
- unresolved_catalog_ref: 2
- unresolved_dataset_ref: 2

## Limitations

- The benchmark is controlled and synthetic.
- It is not a population-scale empirical benchmark.
- It prepares checker and mutation evaluation but does not implement them.

## Next Step Recommendation

Implement v2.0 checker and mutation evaluation.
