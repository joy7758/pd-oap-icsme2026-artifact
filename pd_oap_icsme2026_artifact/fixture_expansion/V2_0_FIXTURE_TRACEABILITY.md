# v2.0 Fixture Traceability

| Editorial criticism | v2.0 fixture response | Artifact file path | Count | Remaining limitation |
|---|---|---|---:|---|
| insufficient evaluation | Expand from a small v1.x sanity set to a 45-fixture controlled benchmark. | `pd-oap/v2/fixtures/v2_0/manifest.json` | 45 | Still synthetic and controlled, not population-scale. |
| too few fixtures | Use 15 fixtures per operation family across access, reuse, and review. | `pd-oap/v2/fixtures/v2_0/valid/`, `invalid/`, `edge/` | 45 | Does not yet include mutation-derived fixtures. |
| weak SE validation connection | Encode expected results, failure classes, and validation surfaces per fixture. | `pd-oap/v2/fixtures/v2_0/expected_results.json` | 45 expected outcomes | Full v2 checker is a later stage. |
| benchmark ambiguity | Define the suite as controlled, executable, and bounded. | `pd-oap/v2/fixture_expansion/V2_0_FIXTURE_GENERATION_CONTRACT.md` | 1 contract | Not a statistical benchmark. |
| synthetic-case limitation | Use synthetic local identifiers and explicit non-claims. | every fixture JSON file | 45 | Does not show real public-sector deployment. |
