# v2.0 Mutation Operator Catalog

| Operator | Operation family | Expected failure class | Mutation action | Why it matters |
|---|---|---|---|---|
| mutate_access_remove_authorization_basis | access_decision | missing_authorization_basis | Clear the declared authorization basis and decision basis. | Tests whether access needs explicit policy basis. |
| mutate_access_break_dataset_ref | access_decision | unresolved_dataset_ref | Change the operation data object reference to an unresolved id. | Tests dataset reference closure. |
| mutate_access_break_catalog_ref | access_decision | unresolved_catalog_ref | Change the operation catalog id to an unresolved id. | Tests catalog reference closure. |
| mutate_access_requester_role_mismatch | access_decision | requester_role_mismatch | Change requester role outside policy allowed roles. | Tests role-policy consistency. |
| mutate_reuse_purpose_constraint_mismatch | reuse_authorization | purpose_constraint_mismatch | Change declared purpose outside policy allowed purposes. | Tests purpose-policy matching. |
| mutate_reuse_remove_reuse_conditions | reuse_authorization | reuse_condition_missing | Remove required attribution and onward-transfer conditions. | Tests reuse condition completeness. |
| mutate_reuse_condition_mismatch | reuse_authorization | reuse_condition_mismatch | Permit onward transfer where policy expects forbidden onward transfer. | Tests condition consistency. |
| mutate_reuse_break_handoff_ref | reuse_authorization | handoff_ref_unresolved | Replace handoff reference with unresolved id. | Tests handoff reference closure. |
| mutate_review_remove_trigger | review_decision | review_trigger_missing | Remove review triggers from policy. | Tests review trigger presence. |
| mutate_review_remove_review_evidence | review_decision | review_evidence_missing | Remove review-record evidence. | Tests review evidence completeness. |
| mutate_review_policy_version_mismatch | review_decision | policy_version_mismatch | Change operation policy version away from policy block version. | Tests version consistency. |
| mutate_review_integrity_digest_mismatch | review_decision | integrity_digest_mismatch | Change provenance digest away from evidence digest. | Tests integrity consistency. |
