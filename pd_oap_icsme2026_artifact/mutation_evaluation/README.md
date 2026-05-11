# v2.0 Mutation Evaluation

This package generates and evaluates 72 controlled mutations from the 18 valid v2.0 fixtures.

The mutation evaluation uses 12 operators, one per semantic failure class. Each operator is applied to the six valid fixtures in its operation family. The purpose is to test whether the semantic checker detects controlled negative controls with the expected failure classes.

This directly addresses the evaluation insufficiency criticism by adding systematic failure injection beyond the 45 base fixtures.
