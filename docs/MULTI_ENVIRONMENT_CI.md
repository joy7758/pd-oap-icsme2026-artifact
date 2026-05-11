# Multi-Environment CI

This repository patch adds an Artifact Smoke Test Matrix workflow.

The matrix runs:

- `ubuntu-latest`
- `macos-latest`
- `windows-latest`
- Python `3.10`
- Python `3.11`
- Python `3.12`

Command:

```bash
python scripts/run_artifact_smoke_test.py
```

Expected outputs:

- 45 controlled fixtures
- 12 semantic failure classes
- semantic checker matched 45/45 declared outcomes
- 72 mutation cases
- mutation detection/classification 72/72

Safe claim: the repository includes automated multi-environment smoke tests if this workflow is applied and passes.

Unsafe claim: CI establishes external validation or independent human rerun.
