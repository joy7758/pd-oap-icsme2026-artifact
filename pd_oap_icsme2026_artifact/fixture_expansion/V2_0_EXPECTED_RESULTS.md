# v2.0 Expected Results

## Fixture Family Summary

| Fixture family | Operation family | Count | Expected result | Expected primary failure code pattern |
|---|---|---:|---|---|
| valid | access_decision | 6 | valid | none |
| valid | reuse_authorization | 6 | valid | none |
| valid | review_decision | 6 | valid | none |
| invalid | access_decision | 8 | invalid | one of four access failure classes |
| invalid | reuse_authorization | 8 | invalid | one of four reuse failure classes |
| invalid | review_decision | 8 | invalid | one of four review failure classes |
| edge | access_decision | 1 | valid | none |
| edge | reuse_authorization | 1 | valid | none |
| edge | review_decision | 1 | valid | none |

## Failure-Class Coverage

| Failure class | Operation family | Expected invalid fixture count |
|---|---|---:|
| missing_authorization_basis | access_decision | 2 |
| unresolved_dataset_ref | access_decision | 2 |
| unresolved_catalog_ref | access_decision | 2 |
| requester_role_mismatch | access_decision | 2 |
| purpose_constraint_mismatch | reuse_authorization | 2 |
| reuse_condition_missing | reuse_authorization | 2 |
| reuse_condition_mismatch | reuse_authorization | 2 |
| handoff_ref_unresolved | reuse_authorization | 2 |
| review_trigger_missing | review_decision | 2 |
| review_evidence_missing | review_decision | 2 |
| policy_version_mismatch | review_decision | 2 |
| integrity_digest_mismatch | review_decision | 2 |
