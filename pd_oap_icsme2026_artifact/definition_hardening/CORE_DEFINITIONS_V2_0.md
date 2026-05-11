# Core Definitions for PD-OAP v2.0

These definitions harden the conceptual layer for the v2.0 manuscript. They are intended to be used before artifact details, fixture counts, and evaluation results are introduced.

# public-data operation

## One-sentence definition

A public-data operation is one bounded access, reuse, or review decision involving a public-data object, requester, actor, policy basis, decision, and evidence context.

## Longer definition

In PD-OAP, a public-data operation is the unit of accountability that the profile packages for inspection. It is smaller than a data program and more structured than a casual data-sharing event. The operation has a decision boundary: a particular requester or actor seeks access, reuse, handoff, or review of a public-data object under a stated policy basis and purpose, with evidence that supports later inspection.

## Scope

The concept includes access decisions, reuse authorizations, and review decisions over public-sector data objects. It includes the operation subject, acting party, requester role, policy basis, purpose, decision outcome, conditions, references, and evidence context needed to inspect that one operation.

## What this is not

It is not a full public-data platform, not an entire open-data portal, not a city data strategy, not a general governance program, and not generic data sharing without an inspectable decision boundary.

## Example

One restricted mobility-data access decision in which a named municipal analytics unit requests access to a specific dataset under a stated public-interest basis and receives an allow or deny decision with recorded conditions.

## Non-example

An entire city open-data portal with many datasets, policies, users, and access patterns but no single packaged operation decision.

## Artifact fields or components

The operation is represented through fields or components such as operation identifier, operation type, data object reference, requester, actor, policy basis, purpose, decision, conditions, evidence references, provenance references, and validation expectations.

## Validation consequence

A valid statement must allow the checker and auditor to determine which operation is being inspected, which data object is involved, which policy basis is declared, which actor made the decision, and which evidence supports the operation boundary.

## Software engineering role

This concept defines the unit under test. It lets the profile, checker, fixtures, and evaluation operate over repeatable artifacts rather than vague governance narratives.

## Relationship to other PD-OAP concepts

The public-data operation is packaged by an operation-accountability statement, inspected through structural inspectability, assessed through reviewability, challenged through semantic failure surfaces, and exercised through the controlled fixture benchmark.

## Safe manuscript wording

PD-OAP treats one bounded public-data access, reuse, or review decision as the operation unit to be packaged and inspected.

## Unsafe wording to avoid

Do not describe PD-OAP as evaluating an entire public-data platform, certifying a public-sector data program, or modeling all public-data governance activity.

# operation-accountability statement

## One-sentence definition

An operation-accountability statement is a portable reviewer-facing object that binds an operation, actor, requester, subject, policy, purpose, decision, conditions, provenance, evidence, validation expectations, and explicit non-claims.

## Longer definition

The operation-accountability statement is the central packaged artifact in PD-OAP. It is designed so that a third party can inspect the structure and declared basis of one public-data operation outside the original runtime. It combines operation context with policy and evidence linkage, validation expectations, and boundaries on what the statement does not establish.

## Scope

The statement includes operation identity, parties, public-data object references, declared policy basis, purpose, decision outcome, conditions, evidence references, provenance references where available, checker expectations, auditor expectations, and non-claim fields.

## What this is not

It is not merely a log entry, not merely a policy record, not merely a provenance graph, not a legal certificate, and not a deployment assurance artifact.

## Example

A JSON statement that records a reuse authorization for a public transport dataset, the requester role, policy basis, allowed purpose, reuse conditions, dataset reference, evidence references, validation expectations, and explicit statement that it does not establish legal sufficiency.

## Non-example

A timestamped log line saying that a user downloaded a dataset, with no policy basis, decision context, evidence links, validation expectations, or non-claims.

## Artifact fields or components

Relevant fields or components include operation metadata, actor and requester blocks, data object references, policy basis, purpose, decision, conditions, provenance links, evidence links, validation block, non-claims block, checker report, auditor report, and fixture metadata.

## Validation consequence

The checker and auditor must be able to test completeness, reference closure, required policy and evidence linkage, consistency of declared conditions, and presence of non-claims. A structurally shaped JSON file can still fail if these semantic expectations are not met.

## Software engineering role

The statement is the software artifact under specification and validation. It turns accountability into a structured artifact that can be versioned, checked, tested, and reproduced.

## Relationship to other PD-OAP concepts

The statement packages the public-data operation. Structural inspectability describes what can be checked in the statement. Reviewability describes what a reviewer can reconstruct from it. Semantic failure surfaces describe ways it can fail. The controlled fixture benchmark exercises valid and invalid statements.

## Safe manuscript wording

An operation-accountability statement packages one operation as a portable artifact with declared policy, evidence, validation expectations, and non-claims.

## Unsafe wording to avoid

Do not call the statement a complete audit record, a legal proof, a full provenance system, or a substitute for institutional review.

# structural inspectability

## One-sentence definition

Structural inspectability is the ability to inspect whether an operation-accountability statement has required structure, reference closure, declared policy and evidence linkage, validation expectations, and explicit non-claims.

## Longer definition

Structural inspectability is an offline artifact property. It asks whether a packaged statement can be inspected for the presence, consistency, and closure of the fields needed to understand one operation. It does not decide whether the underlying policy is correct or whether the decision should have been made.

## Scope

The concept covers required fields, typed components, references to public-data objects, policy and evidence linkage, validation metadata, checker-readable expectations, auditor-readable expectations, and explicit non-claims.

## What this is not

It is not legal sufficiency, not correctness of the policy, not proof that the operation was fair, not runtime monitoring, and not deployment assurance.

## Example

A checker confirms that a statement contains a dataset reference, policy basis, requester, purpose, decision, evidence references, validation expectations, and non-claims, and that referenced identifiers resolve within the packaged artifact.

## Non-example

A legal office decides that the operation satisfies a statute after reviewing external evidence that is not represented in the statement.

## Artifact fields or components

Relevant fields include schema-required fields, reference identifiers, policy basis, evidence list, provenance links, validation expectations, fixture expected outcome, checker report, independent auditor report, and non-claims.

## Validation consequence

The checker and auditor must be able to report missing structure, unresolved references, missing policy linkage, missing evidence linkage, missing validation expectations, and absent non-claims.

## Software engineering role

Structural inspectability provides a validation target for a profile-and-checker method. It supports reproducible testing, failure diagnosis, and artifact review.

## Relationship to other PD-OAP concepts

Structural inspectability is a property of operation-accountability statements. It supports reviewability but is narrower than reviewability. Semantic failure surfaces identify inspectability failures that go beyond raw JSON shape.

## Safe manuscript wording

PD-OAP evaluates whether a packaged operation is structurally inspectable through schema, checker, and auditor checks.

## Unsafe wording to avoid

Do not equate structural inspectability with legal compliance, policy correctness, institutional approval, or operational readiness.

# reviewability

## One-sentence definition

Reviewability is the ability of a reviewer to reconstruct and assess one operation after execution using the packaged operation-accountability statement.

## Longer definition

Reviewability describes what the statement enables for a third-party reader or tool-assisted reviewer. A reviewable statement makes it possible to identify the operation, data object, requester, actor, policy basis, purpose, decision, conditions, evidence, and validation status well enough to inspect why the operation is represented as allowed, denied, reused, handed off, or reviewed.

## Scope

The concept covers reconstruction of one operation, comparison of available evidence and policy linkage, evaluation of completeness, and diagnosis of missing or inconsistent information. It is evaluated through same-case comparison and may later be evaluated through reviewer-task studies.

## What this is not

It is not model explainability alone, not human approval, not legal audit completion, not a guarantee that a reviewer agrees with the decision, and not a claim that every relevant context is captured.

## Example

A reviewer receives a statement for one reuse authorization and can identify the requester role, dataset reference, permitted purpose, reuse condition, evidence links, and validation result without accessing the original runtime.

## Non-example

A dashboard says a request was approved but omits the policy basis, dataset reference, purpose, reuse condition, and evidence links needed to reconstruct the operation.

## Artifact fields or components

Reviewability depends on operation metadata, requester and actor blocks, data references, policy basis, purpose, decision, conditions, evidence references, provenance references, validation report, same-case comparison criteria, and reviewer-facing summaries.

## Validation consequence

Evaluation must show whether the representation gives enough information to reconstruct the case, compare representations, identify missing elements, and diagnose failures. Same-case comparison should report raw counts rather than only ratios.

## Software engineering role

Reviewability connects traceability, evidence packaging, and validation into a reviewer-facing artifact property. It is the user-visible consequence of the profile-and-checker method.

## Relationship to other PD-OAP concepts

Reviewability builds on public-data operations, operation-accountability statements, and structural inspectability. Semantic failure surfaces identify ways reviewability can fail, and the controlled fixture benchmark exercises those failures.

## Safe manuscript wording

PD-OAP studies whether a reviewer can reconstruct and inspect one public-data operation from a packaged statement.

## Unsafe wording to avoid

Do not claim that reviewability means the operation was legally approved, morally correct, fully explained by a model, or accepted by a real public authority.

# semantic failure surface

## One-sentence definition

A semantic failure surface is a profile-specific failure condition that can make an operation-accountability statement incomplete, inconsistent, or unreviewable even when its JSON shape is valid.

## Longer definition

Semantic failure surfaces capture the gap between syntactic validity and meaningful reviewability. A statement can satisfy a JSON Schema while still failing because a policy basis is missing, a dataset reference is unresolved, a purpose contradicts a condition, or evidence needed for review is absent.

## Scope

The concept includes profile-specific failures such as `missing_authorization_basis`, `unresolved_dataset_ref`, `purpose_constraint_mismatch`, `reuse_condition_missing`, and `review_evidence_missing`. v2.0 will expand the taxonomy beyond the v1.x failure classes.

## What this is not

It is not the same as a schema violation, not a runtime exception, not a performance failure, and not a complete classification of all governance failures.

## Example

A statement has all required JSON fields, but the declared dataset reference does not resolve to a packaged dataset object, making the operation impossible to inspect fully.

## Non-example

A JSON file fails schema validation because a required top-level field is absent.

## Artifact fields or components

Relevant components include expected failure codes, fixture metadata, checker rules, auditor rules, reference closure checks, policy basis checks, purpose and condition checks, evidence completeness checks, mutation operators, and evaluation reports.

## Validation consequence

The checker and auditor must diagnose profile-specific semantic failures, and the evaluation must report whether expected failures are detected and whether checker and auditor agree.

## Software engineering role

Semantic failure surfaces make failure diagnosis explicit. They support negative-control testing, mutation evaluation, and traceable validation design.

## Relationship to other PD-OAP concepts

Semantic failures occur in operation-accountability statements for public-data operations. They reduce structural inspectability and reviewability. The controlled fixture benchmark exercises these failures systematically.

## Safe manuscript wording

PD-OAP distinguishes schema validity from semantic failure surfaces that affect reviewability.

## Unsafe wording to avoid

Do not describe semantic failure detection as proving the operation is correct, legally sufficient, or complete in every possible context.

# controlled fixture benchmark

## One-sentence definition

A controlled fixture benchmark is a small, executable, deliberately bounded suite of valid and invalid fixtures used to test representation boundaries and diagnostic behavior.

## Longer definition

The controlled fixture benchmark is an evaluation instrument for PD-OAP. It is designed to make artifact behavior reproducible across valid cases, invalid cases, failure classes, checker outputs, auditor outputs, and same-case comparison. It is controlled because cases are intentionally constructed; it is a benchmark only in the limited sense of repeatable fixture-based evaluation.

## Scope

The concept includes valid fixtures, invalid fixtures, expected outcomes, failure classes, mutation-derived cases, checker reports, auditor reports, agreement reports, and raw-count comparison tables.

## What this is not

It is not a population-scale empirical benchmark, not a performance benchmark, not a deployment evaluation, not evidence of real-world adoption, and not a claim that the fixture distribution represents all public-data operations.

## Example

A v2.0 fixture suite with about 45 synthetic access, reuse, and review operations, at least 12 failure classes, mutation-derived negative controls, and checker/auditor agreement reports.

## Non-example

A large collection of unrelated public-data portal records with no expected outcomes, no failure labels, and no deterministic checker/auditor reports.

## Artifact fields or components

Relevant components include fixture files, fixture inventory, valid/invalid labels, operation family, expected failure code, mutation metadata, checker report, auditor report, cross-checker comparison, same-case comparison, and aggregate evaluation summary.

## Validation consequence

The benchmark must support deterministic reruns, raw-count reporting, failure-class coverage, mutation evaluation, and agreement analysis. The v1.x package used 8 fixtures for a small artifact sanity check; v2.0 should expand toward about 45 fixtures to support a stronger evaluation argument.

## Software engineering role

The benchmark turns the profile-and-checker method into an executable evaluation object. It supports reproducibility, regression testing, negative-control design, and failure-diagnosis claims.

## Relationship to other PD-OAP concepts

The benchmark instantiates public-data operations as operation-accountability statements, tests structural inspectability and reviewability, and exercises semantic failure surfaces.

## Safe manuscript wording

The controlled fixture benchmark is a bounded executable suite for testing representation and diagnostic boundaries.

## Unsafe wording to avoid

Do not present the controlled fixture benchmark as a population study, a statistical benchmark, a deployment evaluation, or evidence that the profile covers all public-data operations.
