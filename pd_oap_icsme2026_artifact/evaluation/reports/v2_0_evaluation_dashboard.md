# v2.0 Evaluation Dashboard

- overall_passed: True
- fixture_count: 45
- valid_expected_count: 21
- invalid_expected_count: 24
- checker_matched_count: 45
- checker_unexpected_count: 0
- mutation_count: 72
- mutation_detected_invalid_count: 72
- mutation_expected_failure_match_count: 72
- mutation_unexpected_count: 0
- failure_class_count: 12

## RQ Evidence

### RQ1

- evidence: 45 fixtures over 3 operation families
- result: 15 access_decision, 15 reuse_authorization, and 15 review_decision fixtures

### RQ2

- evidence: 24 invalid fixtures over 12 failure classes
- result: semantic checker matched all expected invalid fixture outcomes

### RQ3

- evidence: 72 mutations generated from valid fixtures
- result: 72 mutations detected and classified with expected failure classes

### RQ4

- evidence: deterministic generators and reports
- result: fixture, checker, and mutation results are reproducible from local scripts
