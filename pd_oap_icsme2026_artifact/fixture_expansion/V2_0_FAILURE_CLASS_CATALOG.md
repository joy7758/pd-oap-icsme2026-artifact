# v2.0 Failure Class Catalog

## Access Failure Classes

### missing_authorization_basis

- Operation family: access_decision
- Definition: The operation lacks a declared policy or authorization basis for the access decision.
- Why it matters: Reviewers cannot inspect why access was allowed or denied.
- Example defect: `policy.authorization_basis` is empty while the decision depends on it.
- Non-example: A denied access decision with a declared policy basis and complete evidence.
- Expected checker surface: policy basis completeness.
- Planned fixture count: 2
- Relationship to v1.x: Extends the earlier missing-policy style negative fixture into a named semantic class.

### unresolved_dataset_ref

- Operation family: access_decision
- Definition: The operation references a dataset that is not present in the packaged catalog or evidence context.
- Why it matters: The data object under decision cannot be reconstructed.
- Example defect: `operation.data_object_id` does not appear in `catalog.dataset_refs`.
- Non-example: A restricted dataset reference that resolves within the package.
- Expected checker surface: dataset reference closure.
- Planned fixture count: 2
- Relationship to v1.x: Generalizes unresolved reference checks.

### unresolved_catalog_ref

- Operation family: access_decision
- Definition: The operation references a catalog that is absent or inconsistent with the packaged catalog metadata.
- Why it matters: The source catalog context cannot be inspected.
- Example defect: `operation.catalog_id` differs from `catalog.catalog_id`.
- Non-example: A catalog id that matches the packaged catalog block.
- Expected checker surface: catalog reference closure.
- Planned fixture count: 2
- Relationship to v1.x: Adds a separate catalog-level reference failure.

### requester_role_mismatch

- Operation family: access_decision
- Definition: The requester role conflicts with the roles allowed by the declared policy.
- Why it matters: The decision cannot be reviewed against the stated role constraints.
- Example defect: requester role is `commercial_broker` while policy allows `public_research_unit`.
- Non-example: requester role appears in `policy.allowed_requester_roles`.
- Expected checker surface: requester-role policy constraint.
- Planned fixture count: 2
- Relationship to v1.x: Adds role-consistency failure coverage.

## Reuse Failure Classes

### purpose_constraint_mismatch

- Operation family: reuse_authorization
- Definition: The declared reuse purpose conflicts with the policy's allowed purposes.
- Why it matters: Reuse cannot be inspected without purpose-policy consistency.
- Example defect: declared purpose is `commercial_resale` while policy permits only `public_service_planning`.
- Non-example: purpose is included in the policy allowed purposes list.
- Expected checker surface: purpose constraint matching.
- Planned fixture count: 2
- Relationship to v1.x: Expands purpose and policy consistency checks.

### reuse_condition_missing

- Operation family: reuse_authorization
- Definition: Required reuse conditions are absent from the statement.
- Why it matters: Reviewers cannot inspect the obligations attached to reuse.
- Example defect: conditions list omits an attribution or retention limit required by policy.
- Non-example: all required reuse conditions are present.
- Expected checker surface: condition completeness.
- Planned fixture count: 2
- Relationship to v1.x: Refines condition-completeness failures.

### reuse_condition_mismatch

- Operation family: reuse_authorization
- Definition: Declared reuse conditions conflict with policy-required conditions.
- Why it matters: The operation may appear conditioned while actually contradicting the declared policy.
- Example defect: condition permits redistribution while policy forbids onward transfer.
- Non-example: conditions match the policy's required constraints.
- Expected checker surface: condition consistency.
- Planned fixture count: 2
- Relationship to v1.x: Adds condition mismatch coverage beyond missing condition coverage.

### handoff_ref_unresolved

- Operation family: reuse_authorization
- Definition: A reuse handoff reference is missing or cannot be resolved inside the packaged provenance or evidence.
- Why it matters: Reviewers cannot inspect downstream transfer context.
- Example defect: `provenance.handoff_refs` contains an id that has no evidence object.
- Non-example: every handoff reference resolves to an evidence object.
- Expected checker surface: handoff reference closure.
- Planned fixture count: 2
- Relationship to v1.x: Adds reuse-specific reference closure.

## Review Failure Classes

### review_trigger_missing

- Operation family: review_decision
- Definition: A review decision lacks the trigger or reason that initiated review.
- Why it matters: Reviewers cannot reconstruct why the review occurred.
- Example defect: `policy.review_triggers` is empty for a review operation.
- Non-example: the statement declares a review trigger linked to the decision.
- Expected checker surface: review trigger completeness.
- Planned fixture count: 2
- Relationship to v1.x: Adds review-specific evidence requirements.

### review_evidence_missing

- Operation family: review_decision
- Definition: Required review evidence is absent or not linked to the review decision.
- Why it matters: The review outcome cannot be assessed from the package.
- Example defect: evidence list lacks an object with `purpose` equal to `review_record`.
- Non-example: review evidence is present and linked.
- Expected checker surface: review evidence completeness.
- Planned fixture count: 2
- Relationship to v1.x: Extends evidence completeness checks.

### policy_version_mismatch

- Operation family: review_decision
- Definition: The policy version used by the operation conflicts with the policy version in the packaged policy block.
- Why it matters: Reviewers cannot know which rule version governed the decision.
- Example defect: operation declares `policy_version` 2026.1 while the policy block declares 2026.2.
- Non-example: operation and policy versions match.
- Expected checker surface: policy version consistency.
- Planned fixture count: 2
- Relationship to v1.x: Adds version-consistency coverage.

### integrity_digest_mismatch

- Operation family: review_decision
- Definition: The declared integrity digest for the reviewed evidence does not match the packaged evidence digest.
- Why it matters: Reviewers cannot trust that the reviewed evidence is the same object described by the statement.
- Example defect: `provenance.integrity_digest` differs from `evidence.integrity_digest`.
- Non-example: evidence and provenance digest values match.
- Expected checker surface: integrity digest consistency.
- Planned fixture count: 2
- Relationship to v1.x: Adds integrity consistency as a semantic failure class.
