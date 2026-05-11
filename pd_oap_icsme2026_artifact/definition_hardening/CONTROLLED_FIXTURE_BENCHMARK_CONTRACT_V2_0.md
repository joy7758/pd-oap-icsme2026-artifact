# Controlled Fixture Benchmark Contract v2.0

## Contract

The v2.0 fixture benchmark is controlled, executable, and bounded. It is an evaluation instrument for representation and diagnostic boundaries.

It is not statistical, population-scale, or deployment-based. It does not claim that the fixture distribution represents all public-data operations.

## Required Fixture Fields

Each fixture should declare:

- fixture id
- operation family
- operation type
- valid or invalid label
- data object reference
- requester role
- actor
- policy basis
- purpose
- decision
- conditions
- evidence references
- expected checker outcome
- expected auditor outcome
- expected failure code if invalid

## Valid Fixture Expectations

A valid fixture should include enough structure, references, policy linkage, evidence linkage, validation expectations, and non-claims for checker and auditor to accept it under the profile boundary.

## Invalid Fixture Expectations

An invalid fixture should be intentionally failing, deterministic, and mapped to an expected semantic failure class or structural failure. The expected failure must be documented before running checker and auditor reports.

## Failure-Class Coverage Expectations

v2.0 should cover at least 12 failure classes across access, reuse, and review operation families. Each class should have a definition, expected failure code, and representative fixtures where practical.

## Mutation Evaluation Expectations

v2.0 should add mutation evaluation over valid fixtures. Mutation operators should remove or alter policy basis, dataset reference, requester role, purpose, reuse condition, review evidence, handoff reference, or integrity digest where applicable.

## Checker/Auditor Agreement Expectations

Evaluation should report checker outcomes, auditor outcomes, expected failure-code matches, agreement counts, and disagreement counts. Disagreements should be analyzed rather than hidden.

## Planned v2.0 Target

- about 45 fixtures
- at least 12 failure classes
- mutation evaluation over valid fixtures
- raw-count reporting
- checker/auditor agreement matrix
