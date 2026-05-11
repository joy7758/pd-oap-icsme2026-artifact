# Mutation Evaluation Report v2.0

- overall_passed: True
- mutation_count: 72
- detected_invalid_count: 72
- expected_failure_match_count: 72
- unexpected_count: 0

## Operation Family Counts

- access_decision: 24
- reuse_authorization: 24
- review_decision: 24

## Failure Class Counts

- handoff_ref_unresolved: 6
- integrity_digest_mismatch: 6
- missing_authorization_basis: 6
- policy_version_mismatch: 6
- purpose_constraint_mismatch: 6
- requester_role_mismatch: 6
- reuse_condition_mismatch: 6
- reuse_condition_missing: 6
- review_evidence_missing: 6
- review_trigger_missing: 6
- unresolved_catalog_ref: 6
- unresolved_dataset_ref: 6

## Operator Counts

- mutate_access_break_catalog_ref: 6
- mutate_access_break_dataset_ref: 6
- mutate_access_remove_authorization_basis: 6
- mutate_access_requester_role_mismatch: 6
- mutate_reuse_break_handoff_ref: 6
- mutate_reuse_condition_mismatch: 6
- mutate_reuse_purpose_constraint_mismatch: 6
- mutate_reuse_remove_reuse_conditions: 6
- mutate_review_integrity_digest_mismatch: 6
- mutate_review_policy_version_mismatch: 6
- mutate_review_remove_review_evidence: 6
- mutate_review_remove_trigger: 6
