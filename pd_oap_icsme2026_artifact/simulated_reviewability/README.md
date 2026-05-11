# PD-OAP v2.0 Simulated Reviewability

This package replaces the planned human dry run with a strict deterministic simulation. No participants were recruited and no human data was collected.

The simulation evaluates representation-level reviewability under deterministic reviewer models. It does not claim human validation.

The simulation uses 117 source specimens:

- 45 base fixtures
- 72 mutation fixtures

For each source specimen, the generator creates four representation conditions:

- logs_only
- policy_only
- provenance_only
- full_pd_oap

The result is 468 simulated review tasks. The simulation measures information availability for operation reconstruction, policy-basis assessment, evidence completeness, reference closure, failure detection, and claim-boundary visibility.

This package supports representation-level reviewability claims only. It does not support claims about actual human reviewer performance, legal compliance, deployment readiness, or production behavior.
