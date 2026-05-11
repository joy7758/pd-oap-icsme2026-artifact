# Simulation Decision

## Decision

Use strict deterministic simulated reviewability evaluation instead of a human reviewability dry run.

## Rationale

- No participants are available now.
- A deterministic simulation is reproducible from local fixtures and mutation cases.
- The simulation avoids ethics and recruitment delay.
- The simulation directly tests representation information availability across logs_only, policy_only, provenance_only, and full_pd_oap conditions.

## Tradeoff

The simulation does not provide human-subject evidence and cannot claim actual reviewer performance. It evaluates a rule-based reviewer model, not human cognition.

## Complementary role

The simulation complements the 45 fixture evaluation and the 72 mutation evaluation. It adds representation-ablation evidence over the same source specimens without replacing the semantic checker matrix or mutation detection results.
