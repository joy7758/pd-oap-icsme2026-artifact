#!/usr/bin/env python3
"""Evaluate PD-OAP v2.0 mutation detection using the semantic checker."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path, report):
    lines = [
        "# Mutation Evaluation Report v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- mutation_count: {report['mutation_count']}",
        f"- detected_invalid_count: {report['detected_invalid_count']}",
        f"- expected_failure_match_count: {report['expected_failure_match_count']}",
        f"- unexpected_count: {report['unexpected_count']}",
        "",
        "## Operation Family Counts",
        "",
    ]
    for key, value in sorted(report["operation_family_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Failure Class Counts", ""])
    for key, value in sorted(report["failure_class_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Operator Counts", ""])
    for key, value in sorted(report["operator_counts"].items()):
        lines.append(f"- {key}: {value}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_checker(checker, mutation_root):
    completed = subprocess.run(
        [sys.executable, str(checker), "--matrix", str(mutation_root)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"checker failed: {completed.stderr}")
    return json.loads(completed.stdout)


def evaluate(mutation_root, checker):
    manifest = load_json(mutation_root / "manifest.json")
    matrix = run_checker(checker, mutation_root)
    results = matrix.get("results", [])
    detected_invalid = sum(1 for item in results if item.get("observed_result") == "invalid")
    expected_failure_match = sum(1 for item in results if item.get("matched_expectation") is True)
    unexpected = len(results) - expected_failure_match
    report = {
        "mutation_evaluation": {
            "name": "pd-oap-v2-mutation-evaluation",
            "version": "2.0-draft",
        },
        "mutation_count": manifest.get("mutation_count"),
        "detected_invalid_count": detected_invalid,
        "expected_failure_match_count": expected_failure_match,
        "unexpected_count": unexpected,
        "operation_family_counts": manifest.get("operation_family_counts", {}),
        "failure_class_counts": manifest.get("expected_failure_class_counts", {}),
        "operator_counts": manifest.get("mutation_operator_counts", {}),
        "overall_passed": False,
        "checker_matrix": matrix,
    }
    report["overall_passed"] = (
        report["mutation_count"] == 72
        and detected_invalid == 72
        and expected_failure_match == 72
        and unexpected == 0
        and all(count == 6 for count in report["failure_class_counts"].values())
        and all(count == 6 for count in report["operator_counts"].values())
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation-root", required=True)
    parser.add_argument("--checker", required=True)
    parser.add_argument("--write-report", required=True)
    parser.add_argument("--write-markdown", required=True)
    args = parser.parse_args(argv)

    try:
        report = evaluate(Path(args.mutation_root), Path(args.checker))
    except Exception as exc:
        print(f"mutation evaluation failed: {exc}", file=sys.stderr)
        return 1

    write_json(args.write_report, report)
    write_markdown(args.write_markdown, report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
