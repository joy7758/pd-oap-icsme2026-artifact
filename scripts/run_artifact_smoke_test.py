#!/usr/bin/env python3
"""Smoke test for the PD-OAP artifact repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED = {
    "fixture_count": 45,
    "failure_class_count": 12,
    "checker_matched_count": 45,
    "mutation_count": 72,
    "mutation_expected_failure_match_count": 72,
}


def find_one(root: Path, name: str) -> Path | None:
    matches = sorted(root.rglob(name))
    return matches[0] if matches else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_equal(label: str, actual: object, expected: object, failures: list[str]) -> None:
    print(f"{label}: {actual} expected {expected}")
    if actual != expected:
        failures.append(f"{label} expected {expected}, got {actual}")


def main() -> int:
    root = Path.cwd()
    failures: list[str] = []

    fixture_report = find_one(root, "fixture_expansion_gate_v2_0.json")
    checker_report = find_one(root, "semantic_checker_matrix_v2_0.json")
    mutation_report = find_one(root, "mutation_evaluation_report_v2_0.json")
    dashboard_report = find_one(root, "v2_0_evaluation_dashboard.json")

    for label, path in [
        ("fixture report", fixture_report),
        ("semantic checker report", checker_report),
        ("mutation report", mutation_report),
        ("evaluation dashboard", dashboard_report),
    ]:
        print(f"{label}: {path if path else 'missing'}")
        if path is None:
            failures.append(f"{label} missing")

    if fixture_report:
        data = load_json(fixture_report)
        fixture_count = data.get("fixture_count") or data.get("total_fixture_count")
        failure_count = data.get("failure_class_count")
        if failure_count is None and isinstance(data.get("failure_class_counts"), dict):
            failure_count = len(data["failure_class_counts"])
        check_equal("fixture_count", fixture_count, EXPECTED["fixture_count"], failures)
        check_equal("failure_class_count", failure_count, EXPECTED["failure_class_count"], failures)

    if checker_report:
        data = load_json(checker_report)
        matched_count = data.get("matched_count") or data.get("checker_matched_count")
        unexpected_count = data.get("unexpected_count") or data.get("checker_unexpected_count", 0)
        check_equal("semantic_checker_matched_count", matched_count, EXPECTED["checker_matched_count"], failures)
        check_equal("semantic_checker_unexpected_count", unexpected_count, 0, failures)

    if mutation_report:
        data = load_json(mutation_report)
        mutation_count = data.get("mutation_count")
        expected_failure_match_count = data.get("expected_failure_match_count") or data.get(
            "mutation_expected_failure_match_count"
        )
        unexpected_count = data.get("unexpected_count") or data.get("mutation_unexpected_count", 0)
        check_equal("mutation_count", mutation_count, EXPECTED["mutation_count"], failures)
        check_equal(
            "mutation_expected_failure_match_count",
            expected_failure_match_count,
            EXPECTED["mutation_expected_failure_match_count"],
            failures,
        )
        check_equal("mutation_unexpected_count", unexpected_count, 0, failures)

    if dashboard_report:
        data = load_json(dashboard_report)
        if "fixture_count" in data:
            check_equal("dashboard_fixture_count", data.get("fixture_count"), EXPECTED["fixture_count"], failures)
        if "mutation_count" in data:
            check_equal("dashboard_mutation_count", data.get("mutation_count"), EXPECTED["mutation_count"], failures)

    if failures:
        print("artifact_smoke_test_failed")
        for failure in failures:
            print(f"failure: {failure}")
        return 1

    print("artifact_smoke_test_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
