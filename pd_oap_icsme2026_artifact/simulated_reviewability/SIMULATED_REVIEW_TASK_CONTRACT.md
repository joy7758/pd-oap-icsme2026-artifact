# Simulated Review Task Contract

Every generated task is synthetic and deterministic. No participant data is included.

## Required task JSON shape

```json
{
  "simulation_profile": {},
  "task_id": "",
  "source_specimen": {},
  "representation_condition": "",
  "visible_material": {},
  "hidden_material_summary": {},
  "expected_review_target": {},
  "scoring_expectation": {},
  "non_claims": {}
}
```

## Required top-level keys

- simulation_profile
- task_id
- source_specimen
- representation_condition
- visible_material
- hidden_material_summary
- expected_review_target
- scoring_expectation
- non_claims

## Non-claims

Every task must state:

- human_participant_data: false
- human_study_result: false
- legal_sufficiency: false
- production_deployment: false
