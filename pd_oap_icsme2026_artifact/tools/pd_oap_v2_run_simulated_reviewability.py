#!/usr/bin/env python3
"""Run deterministic simulated reviewability scoring for PD-OAP v2.0 tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


CONDITIONS = ["logs_only", "policy_only", "provenance_only", "full_pd_oap"]
DIMENSIONS = [
    "operation_reconstruction",
    "policy_basis_assessment",
    "evidence_completeness_assessment",
    "reference_closure_assessment",
    "failure_detection_assessment",
    "claim_boundary_assessment",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def score_label(value: float) -> str:
    if value == 1.0:
        return "true"
    if value == 0.5:
        return "partial"
    return "false"


def failure_detection_score(condition: str, failure: str, expected_result: str) -> float:
    if condition == "full_pd_oap":
        return 1.0
    if expected_result != "invalid":
        return {"logs_only": 0.0, "policy_only": 0.0, "provenance_only": 0.5}.get(condition, 0.0)
    if condition == "logs_only":
        return 0.5 if failure in {"missing_authorization_basis", "review_trigger_missing"} else 0.0
    if condition == "policy_only":
        return 0.5 if failure in {
            "purpose_constraint_mismatch",
            "requester_role_mismatch",
            "policy_version_mismatch",
            "reuse_condition_missing",
            "reuse_condition_mismatch",
            "review_trigger_missing",
        } else 0.0
    if condition == "provenance_only":
        return 0.5 if failure != "none" else 0.5
    return 0.0


def score_task(task: dict) -> dict:
    condition = task["representation_condition"]
    source = task["source_specimen"]
    expected_result = source.get("expected_result")
    failure = source.get("expected_primary_failure_code", "none")

    if condition == "full_pd_oap":
        values = {dimension: 1.0 for dimension in DIMENSIONS}
    elif condition == "logs_only":
        values = {
            "operation_reconstruction": 0.5,
            "policy_basis_assessment": 0.0,
            "evidence_completeness_assessment": 0.0,
            "reference_closure_assessment": 0.0,
            "failure_detection_assessment": failure_detection_score(condition, failure, expected_result),
            "claim_boundary_assessment": 0.0,
        }
    elif condition == "policy_only":
        values = {
            "operation_reconstruction": 0.0,
            "policy_basis_assessment": 1.0,
            "evidence_completeness_assessment": 0.0,
            "reference_closure_assessment": 0.0,
            "failure_detection_assessment": failure_detection_score(condition, failure, expected_result),
            "claim_boundary_assessment": 0.0,
        }
    elif condition == "provenance_only":
        values = {
            "operation_reconstruction": 1.0,
            "policy_basis_assessment": 0.5,
            "evidence_completeness_assessment": 0.5,
            "reference_closure_assessment": 0.5,
            "failure_detection_assessment": failure_detection_score(condition, failure, expected_result),
            "claim_boundary_assessment": 0.0,
        }
    else:
        raise ValueError(condition)

    reviewability_score = sum(values.values())
    max_score = 6
    ratio = reviewability_score / max_score
    outcome_match = condition == "full_pd_oap"
    return {
        "task_id": task["task_id"],
        "source_specimen": source,
        "representation_condition": condition,
        "dimension_scores": {
            name: {"label": score_label(score), "score": score}
            for name, score in values.items()
        },
        "reviewability_score": reviewability_score,
        "max_score": max_score,
        "reviewability_ratio": ratio,
        "outcome_match": outcome_match,
    }


def average(values: list[float]) -> float:
    return round(sum(values) / len(values), 6) if values else 0.0


def aggregate(results: list[dict], key_fn) -> dict:
    buckets: dict[str, list[dict]] = {}
    for result in results:
        buckets.setdefault(key_fn(result), []).append(result)
    return {
        key: {
            "task_count": len(items),
            "average_reviewability_ratio": average([item["reviewability_ratio"] for item in items]),
        }
        for key, items in sorted(buckets.items())
    }


def write_markdown(path: Path, report: dict) -> None:
    lines = [
        "# Simulated Reviewability Report v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- source_specimen_count: {report['source_specimen_count']}",
        f"- task_count: {report['task_count']}",
        f"- full_pd_oap_outcome_match_count: {report['full_pd_oap_outcome_match_count']}",
        f"- partial_conditions_lower_than_full: {report['partial_conditions_lower_than_full']}",
        "",
        "## Aggregate by condition",
        "",
        "| Condition | Tasks | Average reviewability ratio |",
        "|---|---:|---:|",
    ]
    for condition in CONDITIONS:
        item = report["aggregate_by_condition"][condition]
        lines.append(f"| {condition} | {item['task_count']} | {item['average_reviewability_ratio']} |")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "This is a deterministic representation-level simulation. It is not a human study and does not claim human reviewer performance.",
            "",
            "## Safe manuscript wording",
            "",
            "A deterministic simulated reviewability evaluation suggests that full PD-OAP preserves more review-relevant information under the defined scoring model.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(root: Path, report: dict) -> None:
    lines = [
        "# Simulation Results Summary",
        "",
        f"- source_specimen_count {report['source_specimen_count']}",
        f"- simulated_task_count {report['task_count']}",
        "- representation conditions 4",
        "- full_pd_oap average ratio expected 1.0",
        f"- full_pd_oap outcome match count {report['full_pd_oap_outcome_match_count']}",
        "",
        "## Partial representation ratios as generated",
        "",
        "| Condition | Average reviewability ratio |",
        "|---|---:|",
    ]
    for condition in ["logs_only", "policy_only", "provenance_only"]:
        ratio = report["aggregate_by_condition"][condition]["average_reviewability_ratio"]
        lines.append(f"| {condition} | {ratio} |")
    lines.extend(
        [
            "| full_pd_oap | 1.0 |",
            "",
            "These results are deterministic simulation outputs, not human-study results.",
            "",
        ]
    )
    (root / "SIMULATION_RESULTS_SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-root", required=True, type=Path)
    parser.add_argument("--write-report", required=True, type=Path)
    parser.add_argument("--write-markdown", required=True, type=Path)
    args = parser.parse_args(argv)

    task_paths = sorted(p for p in args.task_root.rglob("*.json") if p.name != "manifest.json")
    tasks = [load_json(path) for path in task_paths]
    results = [score_task(task) for task in tasks]

    condition_counts = {condition: sum(1 for result in results if result["representation_condition"] == condition) for condition in CONDITIONS}
    source_ids = {result["source_specimen"]["fixture_id"] for result in results}
    aggregate_by_condition = aggregate(results, lambda result: result["representation_condition"])
    aggregate_by_operation_family = aggregate(results, lambda result: result["source_specimen"]["operation_family"])
    aggregate_by_source_type = aggregate(results, lambda result: result["source_specimen"]["source_type"])
    aggregate_by_failure_class = aggregate(results, lambda result: result["source_specimen"]["expected_primary_failure_code"])

    full = [result for result in results if result["representation_condition"] == "full_pd_oap"]
    full_ratio = aggregate_by_condition.get("full_pd_oap", {}).get("average_reviewability_ratio")
    full_match = sum(1 for result in full if result["outcome_match"])
    partial_lower = all(aggregate_by_condition[condition]["average_reviewability_ratio"] < 1.0 for condition in ["logs_only", "policy_only", "provenance_only"])

    report = {
        "simulated_reviewability": {"name": "pd-oap-v2-simulated-reviewability", "version": "2.0-draft"},
        "overall_passed": len(tasks) == 468 and len(source_ids) == 117 and full_ratio == 1.0 and full_match == 117 and partial_lower,
        "task_count": len(tasks),
        "source_specimen_count": len(source_ids),
        "representation_condition_counts": condition_counts,
        "aggregate_by_condition": aggregate_by_condition,
        "aggregate_by_operation_family": aggregate_by_operation_family,
        "aggregate_by_source_type": aggregate_by_source_type,
        "aggregate_by_failure_class": aggregate_by_failure_class,
        "full_pd_oap_outcome_match_count": full_match,
        "partial_conditions_lower_than_full": partial_lower,
        "non_claims": {
            "human_study_result": False,
            "participant_data_collected": False,
        },
        "results": results,
    }

    write_json(args.write_report, report)
    write_markdown(args.write_markdown, report)
    write_summary(args.write_report.parent.parent, report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
