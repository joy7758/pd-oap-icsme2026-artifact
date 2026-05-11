#!/usr/bin/env python3
"""Generate deterministic simulated reviewability tasks for PD-OAP v2.0."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys


CONDITIONS = ["logs_only", "policy_only", "provenance_only", "full_pd_oap"]
PROFILE = {"name": "pd-oap-simulated-reviewability", "version": "2.0-draft"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def json_files(root: Path, excluded: set[str]) -> list[Path]:
    return sorted(p for p in root.rglob("*.json") if p.name not in excluded)


def safe_get(obj: dict, key: str, default=None):
    cur = obj
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def source_type(obj: dict) -> str:
    family = safe_get(obj, "fixture_metadata.fixture_family", "")
    if family == "valid":
        return "base_valid"
    if family == "invalid":
        return "base_invalid"
    if family == "edge":
        return "edge"
    if family == "mutation":
        return "mutation"
    return "unknown"


def operation_family(obj: dict) -> str:
    return (
        safe_get(obj, "fixture_metadata.operation_family")
        or safe_get(obj, "operation.operation_family")
        or safe_get(obj, "operation.operation_type")
        or "unknown"
    )


def specimen_record(path: Path, obj: dict, specimen_kind: str) -> dict:
    return {
        "path": str(path),
        "fixture_id": obj.get("fixture_id", path.stem),
        "source_kind": specimen_kind,
        "source_type": source_type(obj),
        "operation_family": operation_family(obj),
        "expected_result": safe_get(obj, "validation.expected_result", "unknown"),
        "expected_primary_failure_code": safe_get(obj, "validation.expected_primary_failure_code", "none"),
        "expected_failure_class": safe_get(obj, "validation.expected_failure_class", "none"),
        "object": obj,
    }


def synthetic_event_time(fixture_id: str) -> str:
    digits = sum(ord(ch) for ch in fixture_id) % 86400
    hour = digits // 3600
    minute = (digits % 3600) // 60
    second = digits % 60
    return f"2026-01-01T{hour:02d}:{minute:02d}:{second:02d}Z"


def refs_summary(obj: dict) -> dict:
    return {
        "operation_id": safe_get(obj, "operation.operation_id"),
        "operation_family": operation_family(obj),
        "actor_id": safe_get(obj, "actor.actor_id"),
        "requester_id": safe_get(obj, "requester.requester_id"),
        "requester_role": safe_get(obj, "requester.requester_role"),
        "subject_id": safe_get(obj, "subject.dataset_id") or safe_get(obj, "operation.data_object_id"),
        "catalog_id": safe_get(obj, "catalog.catalog_record_id") or safe_get(obj, "operation.catalog_id"),
        "policy_id": safe_get(obj, "policy.policy_id") or safe_get(obj, "operation.policy_id"),
        "policy_version": safe_get(obj, "policy.policy_version") or safe_get(obj, "operation.policy_version"),
        "purpose": safe_get(obj, "purpose.declared_purpose"),
        "decision_status": safe_get(obj, "decision.status"),
    }


def visible_material(condition: str, obj: dict) -> dict:
    refs = refs_summary(obj)
    if condition == "logs_only":
        return {
            "event_type": "operation_event",
            "event_time": synthetic_event_time(obj.get("fixture_id", "unknown")),
            "operation_id": refs["operation_id"],
            "operation_family": refs["operation_family"],
            "actor_id": refs["actor_id"],
            "subject_ref": refs["subject_id"],
            "decision_status": refs["decision_status"],
        }
    if condition == "policy_only":
        policy = copy.deepcopy(obj.get("policy", {}))
        return {
            "policy": policy,
            "purpose_constraints": copy.deepcopy(obj.get("purpose", {})),
            "condition_codes": copy.deepcopy(obj.get("conditions", [])),
        }
    if condition == "provenance_only":
        return {
            "refs": refs,
            "provenance": copy.deepcopy(obj.get("provenance", {})),
            "reference_links": {
                "actor_id": refs["actor_id"],
                "requester_id": refs["requester_id"],
                "subject_id": refs["subject_id"],
                "catalog_id": refs["catalog_id"],
                "policy_id": refs["policy_id"],
                "purpose": refs["purpose"],
                "decision_status": refs["decision_status"],
            },
        }
    if condition == "full_pd_oap":
        return copy.deepcopy(obj)
    raise ValueError(condition)


def hidden_summary(condition: str) -> dict:
    if condition == "logs_only":
        return {
            "excluded": [
                "explicit_policy_basis_details",
                "evidence_package",
                "validation_expectations",
                "full_provenance_links",
                "non_claims",
            ]
        }
    if condition == "policy_only":
        return {
            "excluded": [
                "concrete_operation_execution",
                "evidence_package",
                "actual_provenance_closure",
                "actual_decision_record",
            ]
        }
    if condition == "provenance_only":
        return {
            "excluded": [
                "semantic_validation_expectations",
                "full_evidence_completeness",
                "non_claims",
                "explicit_checker_result",
            ]
        }
    return {"excluded": ["external_real_world_evidence_beyond_source_specimen"]}


def expected_review_target(specimen: dict) -> dict:
    expected_result = specimen["expected_result"]
    failure = specimen["expected_primary_failure_code"]
    if expected_result == "invalid":
        failure_expected = f"detect {failure}"
    else:
        failure_expected = "no semantic failure expected"
    return {
        "operation_reconstruction_expected": specimen["operation_family"],
        "failure_detection_expected": failure_expected,
        "policy_basis_expected": "identify policy id and policy version when visible",
        "evidence_completeness_expected": "judge whether evidence refs and validation fields are visible",
    }


def make_task(specimen: dict, condition: str) -> dict:
    fixture_id = specimen["fixture_id"]
    task_id = f"task_{fixture_id}_{condition}"
    return {
        "simulation_profile": PROFILE,
        "task_id": task_id,
        "source_specimen": {
            "fixture_id": fixture_id,
            "source_type": specimen["source_type"],
            "operation_family": specimen["operation_family"],
            "expected_result": specimen["expected_result"],
            "expected_primary_failure_code": specimen["expected_primary_failure_code"],
        },
        "representation_condition": condition,
        "visible_material": visible_material(condition, specimen["object"]),
        "hidden_material_summary": hidden_summary(condition),
        "expected_review_target": expected_review_target(specimen),
        "scoring_expectation": {},
        "non_claims": {
            "human_participant_data": False,
            "human_study_result": False,
            "legal_sufficiency": False,
            "production_deployment": False,
        },
    }


def safe_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def write_generation_markdown(path: Path, report: dict) -> None:
    lines = [
        "# Simulated Task Generation Report v2.0",
        "",
        f"- source_specimen_count: {report['source_specimen_count']}",
        f"- base_fixture_count: {report['base_fixture_count']}",
        f"- mutation_fixture_count: {report['mutation_fixture_count']}",
        f"- simulated_task_count: {report['simulated_task_count']}",
        f"- tasks_by_condition: {report['tasks_by_condition']}",
        "",
        "No participant data was collected.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-fixture-root", required=True, type=Path)
    parser.add_argument("--mutation-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args(argv)

    base_paths = json_files(args.base_fixture_root, {"manifest.json", "expected_results.json"})
    mutation_paths = json_files(args.mutation_root, {"manifest.json"})
    base = [specimen_record(p, load_json(p), "base") for p in base_paths]
    mutations = [specimen_record(p, load_json(p), "mutation") for p in mutation_paths]
    specimens = base + mutations

    for condition in CONDITIONS:
        (args.output_root / condition).mkdir(parents=True, exist_ok=True)

    tasks = []
    for specimen in specimens:
        for condition in CONDITIONS:
            task = make_task(specimen, condition)
            task_path = args.output_root / condition / f"{safe_filename(task['task_id'])}.json"
            write_json(task_path, task)
            tasks.append({"task_id": task["task_id"], "condition": condition, "path": str(task_path.relative_to(args.output_root))})

    tasks_by_condition = {condition: sum(1 for task in tasks if task["condition"] == condition) for condition in CONDITIONS}
    manifest = {
        "simulation_task_pack_id": "pd-oap-simulated-reviewability@2.0-draft",
        "source_specimen_count": len(specimens),
        "base_fixture_count": len(base),
        "mutation_fixture_count": len(mutations),
        "representation_conditions": CONDITIONS,
        "simulated_task_count": len(tasks),
        "tasks_by_condition": tasks_by_condition,
        "non_claims": {
            "human_participant_data": False,
            "human_study_result": False,
            "legal_sufficiency": False,
            "production_deployment": False,
        },
        "tasks": tasks,
    }
    write_json(args.output_root / "manifest.json", manifest)

    root = args.output_root.parent.parent
    report = {
        "simulated_task_generation": {"name": "pd-oap-v2-simulated-task-generation", "version": "2.0-draft"},
        **{key: manifest[key] for key in ["source_specimen_count", "base_fixture_count", "mutation_fixture_count", "simulated_task_count", "tasks_by_condition"]},
        "overall_passed": len(specimens) == 117 and len(tasks) == 468 and all(count == 117 for count in tasks_by_condition.values()),
        "non_claims": manifest["non_claims"],
    }
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    write_json(reports / "simulated_task_generation_report_v2_0.json", report)
    write_generation_markdown(reports / "simulated_task_generation_report_v2_0.md", report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
