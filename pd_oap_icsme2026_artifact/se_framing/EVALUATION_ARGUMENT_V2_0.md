# Evaluation Argument v2.0

## Why v1.x evaluation was insufficient

The v1.x evaluation showed that a small artifact package could run, but 8 fixtures were too few for a journal-scale evaluation argument. The evaluation did not yet establish operation-family breadth, semantic failure-class coverage, or systematic negative-control behavior.

## How v2.0 expands evaluation

v2.0 expands the evaluation substrate to 45 fixtures, 21 expected-valid fixtures including edge cases, 24 expected-invalid fixtures, 12 semantic failure classes, 72 mutations, a semantic checker matrix, and a mutation evaluation report.

## Why 45 fixtures matter

The 45 fixtures provide balanced coverage over three operation families: access_decision, reuse_authorization, and review_decision. This supports RQ1 representation coverage and prevents the artifact from reading as a few examples.

## Why 12 failure classes matter

The 12 semantic failure classes make the validation surface explicit. They show that PD-OAP is evaluating semantic failure surfaces beyond JSON shape.

## Why mutation evaluation matters

Mutation evaluation stress-tests valid fixtures by injecting controlled defects. The v2.0 mutation suite has 72 mutations and detects 72/72, with expected failure-class matching and unexpected_count 0.

## Why checker matrix matters

The semantic checker matrix evaluates all 45 fixtures and matched 45/45 declared outcomes. This provides executable evidence for valid, invalid, and edge-case behavior.

## What this does not prove

This does not prove legal sufficiency, production deployment readiness, real public-sector approval, population-scale performance, or external adoption.

## How this supports a journal-scale evaluation section

The v2.0 evaluation substrate can support an RQ-driven evaluation section with representation coverage, failure detectability, mutation robustness, and reproducibility evidence. It changes the manuscript from a short artifact summary into a structured software engineering evaluation argument.
