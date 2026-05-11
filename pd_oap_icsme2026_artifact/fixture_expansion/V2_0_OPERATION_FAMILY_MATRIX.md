# v2.0 Operation Family Matrix

| Operation family | Valid fixtures | Invalid fixtures | Edge fixtures | Total | Reviewability concerns | Evaluation purpose |
|---|---:|---:|---:|---:|---|---|
| access_decision | 6 | 8 | 1 | 15 | requester role, authorization basis, dataset reference, catalog reference, access decision rationale | Test whether access operations are packaged with enough structure and evidence for offline inspection. |
| reuse_authorization | 6 | 8 | 1 | 15 | purpose constraint, reuse condition, handoff reference, scope denial | Test whether reuse operations bind purpose, conditions, and transfer context to an inspectable statement. |
| review_decision | 6 | 8 | 1 | 15 | review trigger, review evidence, policy version, integrity digest, closure without renewal | Test whether review operations preserve enough evidence and validation context for post-operation assessment. |

All operation families total 15 fixtures.
