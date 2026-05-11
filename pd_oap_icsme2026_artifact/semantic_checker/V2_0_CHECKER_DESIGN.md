# v2.0 Checker Design

## Purpose

The v2.0 semantic checker evaluates whether each controlled fixture is semantically valid or invalid under the PD-OAP v2.0 fixture contract.

## Architecture

The checker loads a fixture JSON file, applies deterministic semantic rules in a fixed order, reports all issues it detects, and uses the first detected issue as the primary failure code.

## Rule Order

1. missing_authorization_basis
2. unresolved_dataset_ref
3. unresolved_catalog_ref
4. requester_role_mismatch
5. purpose_constraint_mismatch
6. reuse_condition_missing
7. reuse_condition_mismatch
8. handoff_ref_unresolved
9. review_trigger_missing
10. review_evidence_missing
11. policy_version_mismatch
12. integrity_digest_mismatch
13. valid semantic closure

## Schema Versus Semantic Checking

The v2.0 fixtures share a required top-level shape. Semantic checking starts after that shape exists. A fixture may be structurally present but still fail because references are unresolved, policy constraints are inconsistent, reuse conditions are missing, review evidence is absent, or integrity metadata conflicts.

## Semantic Invalids

The invalid fixtures are intentionally schema-shaped. They test profile-specific failure surfaces rather than malformed JSON.
