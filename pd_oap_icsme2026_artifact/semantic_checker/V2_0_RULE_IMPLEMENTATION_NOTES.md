# v2.0 Rule Implementation Notes

| Failure code | Rule surface | Operation family | Detection logic | Limitation |
|---|---|---|---|---|
| missing_authorization_basis | policy basis completeness | access_decision | Detect empty policy id, missing policy version, empty authorization basis, or unresolved operation policy id. | Does not assess whether the policy is legally correct. |
| unresolved_dataset_ref | dataset reference closure | access_decision | Detect operation data object references not matching subject or catalog dataset references. | Synthetic references only. |
| unresolved_catalog_ref | catalog reference closure | access_decision | Detect operation catalog id that does not match the packaged catalog id. | Does not query external catalogs. |
| requester_role_mismatch | requester-role policy constraint | access_decision | Detect requester role not listed in policy allowed requester roles. | Uses declared role fields only. |
| purpose_constraint_mismatch | purpose constraint matching | reuse_authorization | Detect declared purpose outside policy allowed purposes or marked not allowed by policy. | Does not interpret free-text policy documents. |
| reuse_condition_missing | condition completeness | reuse_authorization | Detect missing attribution or missing onward-transfer condition when policy requires reuse conditions. | Limited to generated fixture condition codes. |
| reuse_condition_mismatch | condition consistency | reuse_authorization | Detect onward-transfer condition that conflicts with the policy-required forbidden transfer boundary. | Does not model all possible reuse contracts. |
| handoff_ref_unresolved | handoff reference closure | reuse_authorization | Detect handoff references absent from evidence ids or evidence objects. | Synthetic handoff refs only. |
| review_trigger_missing | review trigger completeness | review_decision | Detect review operation with no declared policy review trigger. | Does not evaluate trigger sufficiency outside the fixture. |
| review_evidence_missing | review evidence completeness | review_decision | Detect review operation with no review-record evidence object. | Does not validate external review documents. |
| policy_version_mismatch | policy version consistency | review_decision | Detect mismatch between operation policy version and policy block version. | Only compares declared versions. |
| integrity_digest_mismatch | integrity digest consistency | review_decision | Detect mismatch between provenance and evidence integrity digests, including explicit mutated digest fields. | Does not perform cryptographic attestation. |
