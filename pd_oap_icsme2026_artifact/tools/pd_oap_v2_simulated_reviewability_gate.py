#!/usr/bin/env python3
"""Gate for PD-OAP v2.0 simulated reviewability evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_DOCS = [
    "README.md",
    "SIMULATION_DECISION.md",
    "SIMULATED_REVIEWABILITY_DESIGN.md",
    "SIMULATED_REVIEWER_MODEL.md",
    "REPRESENTATION_ABLATION_CONDITIONS.md",
    "SIMULATED_REVIEW_TASK_CONTRACT.md",
    "SCORING_MODEL_V2_0.md",
    "SIMULATION_RESULTS_SUMMARY.md",
    "SIMULATION_LIMITATIONS.md",
    "SIMULATION_TO_RQ_MAPPING.md",
    "SIMULATION_TO_EDITORIAL_REASON_2_RESPONSE.md",
    "DO_NOT_CLAIM_HUMAN_RESULTS.md",
]

CONDITIONS = ["logs_only", "policy_only", "provenance_only", "full_pd_oap"]
UNSAFE_HUMAN_RESULT_PHRASES = [
    "participants confirmed",
    "human study validates",
    "reviewers performed better",
    "full pd-oap is better according to participants",
]
PLACEHOLDERS = ["TODO", "citation-needed"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def negative_context(line: str, start: int) -> bool:
    context = line[max(0, start - 90) : start].lower()
    return any(marker in context for marker in ["no ", "not ", "do not ", "does not ", "unsafe ", "avoid "])


def human_result_claims(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*.md"):
        if path.name == "DO_NOT_CLAIM_HUMAN_RESULTS.md":
            continue
        text = read_text(path).lower()
        for line in text.splitlines():
            for phrase in UNSAFE_HUMAN_RESULT_PHRASES:
                start = line.find(phrase)
                if start >= 0 and not negative_context(line, start):
                    hits.append(f"{path}:{phrase}")
    return sorted(set(hits))


def participant_data_files(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith("tasks/") or rel.startswith("reports/"):
            continue
        lowered = path.name.lower()
        if "participant" in lowered and path.name != "DO_NOT_CLAIM_HUMAN_RESULTS.md":
            hits.append(str(path))
        if path.suffix.lower() in {".csv", ".tsv", ".xlsx"}:
            hits.append(str(path))
    return sorted(set(hits))


def placeholder_found(root: Path) -> bool:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json"}:
            text = read_text(path)
            if any(token in text for token in PLACEHOLDERS):
                return True
    return False


def write_markdown(path: Path, report: dict) -> None:
    lines = [
        "# Simulated Reviewability Gate v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- task_count: {report['task_count']}",
        f"- source_specimen_count: {report['source_specimen_count']}",
        f"- condition_counts: {report['condition_counts']}",
        f"- full_pd_oap_average_ratio: {report['full_pd_oap_average_ratio']}",
        f"- partial_conditions_lower_than_full: {report['partial_conditions_lower_than_full']}",
        f"- human_result_claims_found: {report['human_result_claims_found']}",
        f"- participant_data_files_found: {report['participant_data_files_found']}",
        f"- placeholder_found: {report['placeholder_found']}",
        "",
        "This gate checks deterministic simulated reviewability only. It does not claim human validation.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run_gate(root: Path) -> dict:
    missing_docs = [str(root / rel) for rel in REQUIRED_DOCS if not (root / rel).exists()]
    task_root = root / "tasks" / "v2_0"
    manifest_path = task_root / "manifest.json"
    sim_report_path = root / "reports" / "simulated_reviewability_report_v2_0.json"

    manifest = load_json(manifest_path) if manifest_path.exists() else {}
    sim_report = load_json(sim_report_path) if sim_report_path.exists() else {}

    task_files = [p for p in task_root.rglob("*.json") if p.name != "manifest.json"]
    condition_counts = {condition: len(list((task_root / condition).glob("*.json"))) for condition in CONDITIONS}
    full_ratio = sim_report.get("aggregate_by_condition", {}).get("full_pd_oap", {}).get("average_reviewability_ratio")
    partial_lower = sim_report.get("partial_conditions_lower_than_full") is True
    full_match = sim_report.get("full_pd_oap_outcome_match_count")
    claims = human_result_claims(root)
    participant_files = participant_data_files(root)
    has_placeholder = placeholder_found(root)

    overall = all(
        [
            not missing_docs,
            manifest.get("source_specimen_count") == 117,
            manifest.get("simulated_task_count") == 468,
            len(task_files) == 468,
            all(condition_counts.get(condition) == 117 for condition in CONDITIONS),
            sim_report.get("overall_passed") is True,
            full_ratio == 1.0,
            partial_lower,
            full_match == 117,
            not claims,
            not participant_files,
            not has_placeholder,
        ]
    )
    return {
        "simulated_reviewability_gate": {"name": "pd-oap-v2-simulated-reviewability-gate", "version": "2.0"},
        "overall_passed": overall,
        "missing_docs": missing_docs,
        "task_count": len(task_files),
        "source_specimen_count": manifest.get("source_specimen_count"),
        "condition_counts": condition_counts,
        "full_pd_oap_average_ratio": full_ratio,
        "partial_conditions_lower_than_full": partial_lower,
        "full_pd_oap_outcome_match_count": full_match,
        "human_result_claims_found": claims,
        "participant_data_files_found": participant_files,
        "placeholder_found": has_placeholder,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--write-report", required=True, type=Path)
    parser.add_argument("--write-markdown", required=True, type=Path)
    args = parser.parse_args(argv)

    if not args.root.exists():
        print(f"root does not exist: {args.root}", file=sys.stderr)
        return 2
    report = run_gate(args.root)
    write_json(args.write_report, report)
    write_markdown(args.write_markdown, report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
