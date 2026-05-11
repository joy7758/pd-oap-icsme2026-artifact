# Method Claim Reconstruction v2.0

## Central claim

PD-OAP provides a profile-and-checker method for constructing and evaluating operation-accountability artifacts in public-data workflows.

## What is the method?

The method defines a bounded public-data operation, packages it as an operation-accountability statement, instantiates controlled fixtures, applies semantic checking, generates mutation-based negative controls, and reports RQ-ready evaluation evidence.

## What inputs does it require?

- operation family
- requester/actor/subject/policy/purpose/decision/evidence context
- failure taxonomy

## What outputs does it produce?

- operation-accountability statement
- fixture set
- semantic checker matrix
- mutation evaluation report

## What can be validated?

- representation coverage
- failure detectability
- mutation detectability
- reproducibility

## What cannot be validated?

The method does not validate legal sufficiency, real-world institutional approval, production deployment readiness, all possible data-space integrations, model performance, or external implementation adoption.

## How the method is evaluated in v2.0

v2.0 evaluates the method through 45 controlled fixtures over 3 operation families, 12 semantic failure classes, a semantic checker matrix with 45/45 matched outcomes, and 72/72 mutation detections with unexpected_count 0.

## Why this is a research contribution rather than a technical report

The contribution is no longer only an artifact description. It defines a method, states the artifact class, derives evaluation obligations from definitions, exercises controlled fixtures, tests semantic failure diagnosis, and uses mutation evaluation to stress the validation surface.
