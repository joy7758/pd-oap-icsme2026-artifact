# Software Engineering Problem Statement v2.0

## 1. Problem in one sentence

Software teams lack a bounded method for specifying, packaging, validating, and evaluating accountability artifacts for individual public-data access, reuse, and review operations.

## 2. Why this is a software engineering problem

The problem concerns artifact design, specification boundaries, traceability, validation logic, failure diagnosis, reproducibility, and reviewer-facing evidence packaging. These are software engineering concerns because they determine whether an accountability artifact can be implemented, checked, tested, and maintained across tools.

## 3. Why logs alone are insufficient

Logs can record events, but they usually do not bind an operation to policy basis, purpose, conditions, evidence completeness, validation expectations, and explicit non-claims. A log can show that something happened without making the operation reviewable.

## 4. Why policy records alone are insufficient

Policy records can describe rules or authorizations, but they do not necessarily bind one executed operation to a requester, data object, purpose, evidence context, and validation result.

## 5. Why provenance alone is insufficient

Provenance can describe data flow and derivation, but a provenance graph does not by itself establish the policy basis, decision conditions, evidence completeness, validation expectations, or non-claims for one public-data operation.

## 6. Why a schema alone is insufficient

A schema can enforce JSON shape, but shape alone does not diagnose missing authorization basis, unresolved dataset references, purpose mismatches, missing review evidence, or other semantic failure surfaces.

## 7. Why a profile-and-checker method is needed

A profile-and-checker method specifies the fields and relationships expected in the statement, instantiates those expectations in fixtures, and evaluates whether checker and auditor logic can detect missing, inconsistent, or unreviewable operation records.

## 8. What v2.0 must prove

PD-OAP studies how to specify, instantiate, validate, and evaluate operation-accountability artifacts for public-data workflows.

v2.0 must show that the method supports clear operation boundaries, checkable statement completeness, structural inspectability, reviewer-facing reconstruction, semantic failure diagnosis, and reproducible evaluation through a controlled fixture benchmark.
