# SE Problem To Artifact Pipeline v2.0

| Step | SE concern | PD-OAP artifact | Evaluation evidence | Limitation |
|---|---|---|---|---|
| Step 1: Define operation-level reviewability problem. | Scope the unit under test. | public-data operation definition. | 3 operation families represented. | Does not cover every public-data setting. |
| Step 2: Define operation-accountability statement. | Specify the artifact class. | operation-accountability statement definition. | fixture top-level shape and non-claims. | Statement completeness is local to profile scope. |
| Step 3: Define sector profile fields. | Make fields explicit and checkable. | profile fields for operation, policy, purpose, evidence, validation, and non-claims. | fixture generation contract. | The profile is a draft research artifact. |
| Step 4: Generate controlled fixtures. | Create executable evaluation inputs. | 45 controlled fixtures. | 15/15/15 operation-family distribution. | Controlled suite, not population evidence. |
| Step 5: Implement semantic checker. | Diagnose semantic failure surfaces. | v2 semantic checker. | checker matrix matched 45/45 fixtures. | Local reference checker. |
| Step 6: Generate mutations. | Stress-test validation behavior. | 72 mutation cases from valid fixtures. | 12 operators, each count 6. | Synthetic mutations. |
| Step 7: Evaluate checker and mutation outcomes. | Report repeatable validation evidence. | checker and mutation reports. | mutation detection 72/72 and unexpected_count 0. | No human reviewer study yet. |
| Step 8: Report RQ evidence. | Connect artifacts to research questions. | evaluation dashboard. | RQ-ready dashboard overall_passed true. | Manuscript rewrite still needed. |
