# Definition To Evaluation Requirements v2.0

| Concept | What must be evaluated | Minimum v2.0 evidence | Expected metric or report | How this addresses TOSEM rejection |
|---|---|---|---|---|
| public-data operation | Whether access, reuse, and review operation families are represented with clear decision boundaries. | Operation family coverage across about 45 fixtures. | Fixture inventory by operation family and valid/invalid label. | Clarifies the unit of study and avoids a technical-report-only presentation. |
| operation-accountability statement | Whether statements include operation, policy, purpose, decision, evidence, validation expectations, and non-claims. | Fixture completeness checks and reference closure checks. | Completeness report; reference-closure report; checker/auditor outcome table. | Shows the research artifact is a checkable accountability object, not merely an implementation detail. |
| structural inspectability | Whether required structure, link closure, evidence linkage, and non-claims can be inspected offline. | Schema/checker/auditor coverage over valid, invalid, and mutated fixtures. | Schema pass counts; checker match counts; auditor match counts; agreement matrix. | Converts vague validation into explicit inspectability evidence. |
| reviewability | Whether a reviewer can reconstruct one operation from the packaged statement. | Same-case comparison with raw counts and possibly a small reviewer-task study. | Coverage score, total criteria, ratio, missing criteria, reviewer-task completion if added. | Strengthens the software engineering contribution around traceability and artifact review. |
| semantic failure surface | Whether profile-specific failures are detected beyond schema validity. | Expanded failure taxonomy and mutation evaluation. | Failure-class coverage; mutation generated/detected counts; expected failure-code match counts. | Responds to insufficient evaluation by testing negative controls and diagnostic behavior. |
| controlled fixture benchmark | Whether the fixture suite is bounded, executable, reproducible, and diagnostic. | Expanded fixture suite and failure injection. | Fixture count, failure-class count, mutation count, raw-count reporting, checker/auditor agreement. | Replaces a short artifact summary with an evaluation instrument that can support RQs. |

## Required Evaluation Consequences

- public-data operation -> operation family coverage
- operation-accountability statement -> fixture completeness and reference closure
- structural inspectability -> schema/checker/auditor coverage
- reviewability -> same-case comparison and possibly reviewer-task study
- semantic failure surface -> expanded failure taxonomy and mutation evaluation
- controlled fixture benchmark -> expanded fixture suite and failure injection
