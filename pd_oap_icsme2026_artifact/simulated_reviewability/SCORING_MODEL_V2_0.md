# Scoring Model v2.0

## Dimension scores

- true = 1.0
- partial = 0.5
- false = 0.0

## Task score

- reviewability_score = sum of six dimension scores
- max_score = 6
- reviewability_ratio = reviewability_score / 6

## Aggregate scores

Aggregates are reported by:

- representation condition
- operation family
- failure class
- source type: base_valid, base_invalid, edge, mutation

The ratios are descriptive deterministic simulation metrics, not statistical human performance. They should be interpreted as representation-level information availability under the defined simulated reviewer model.
