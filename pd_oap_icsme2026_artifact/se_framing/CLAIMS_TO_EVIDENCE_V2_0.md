# Claims To Evidence v2.0

| Claim | Evidence artifact | Current result | Safe wording | Unsafe wording to avoid |
|---|---|---|---|---|
| PD-OAP defines operation-accountability statements. | `pd-oap/v2/definition_hardening/CORE_DEFINITIONS_V2_0.md` | Core definition present. | PD-OAP defines a checkable statement artifact for one public-data operation. | Do not call it a complete legal audit record. |
| PD-OAP covers three operation families in controlled fixtures. | `pd-oap/v2/fixtures/v2_0/manifest.json` | 3 operation families. | The controlled benchmark covers access, reuse, and review operation families. | Do not claim universal workflow coverage. |
| v2.0 benchmark includes 45 controlled fixtures. | `pd-oap/v2/fixture_expansion/reports/fixture_expansion_gate_v2_0.json` | 45 fixtures. | v2.0 evaluates a 45-fixture controlled benchmark. | Do not call it population-scale evidence. |
| v2.0 failure taxonomy includes 12 semantic failure classes. | `pd-oap/v2/fixture_expansion/V2_0_FAILURE_CLASS_CATALOG.md` | 12 semantic failure classes. | v2.0 tests 12 semantic failure classes. | Do not call it complete coverage of all governance failures. |
| semantic checker matches declared outcomes for 45/45 fixtures. | `pd-oap/v2/semantic_checker/reports/semantic_checker_matrix_v2_0.json` | 45/45. | The v2 semantic checker matched declared outcomes for 45/45 controlled fixtures. | Do not claim external validation. |
| mutation evaluation detects and classifies 72/72 generated mutations. | `pd-oap/v2/mutation_evaluation/reports/mutation_evaluation_report_v2_0.json` | 72/72. | The mutation evaluation detected and classified 72/72 generated mutations. | Do not claim field deployment robustness. |
| artifact pipeline is reproducible through deterministic scripts. | v2 tools and reports. | unexpected_count 0 in checker and mutation reports. | The local evaluation pipeline is reproducible from deterministic scripts and reports. | Do not claim independent reproduction by external teams yet. |
| PD-OAP supports structural inspectability, not legal compliance. | definitions, non-claims, checker reports. | non-claims retained; unexpected_count 0. | PD-OAP supports structural inspectability within a controlled artifact boundary. | Do not state that it establishes legal compliance. |
