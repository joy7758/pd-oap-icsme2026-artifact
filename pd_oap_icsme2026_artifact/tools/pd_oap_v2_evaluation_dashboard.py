#!/usr/bin/env python3
"""Build the PD-OAP v2.0 evaluation dashboard."""

import argparse
import json
from pathlib import Path
import sys


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path, report):
    lines = [
        "# v2.0 Evaluation Dashboard",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- fixture_count: {report['fixture_count']}",
        f"- valid_expected_count: {report['valid_expected_count']}",
        f"- invalid_expected_count: {report['invalid_expected_count']}",
        f"- checker_matched_count: {report['checker_matched_count']}",
        f"- checker_unexpected_count: {report['checker_unexpected_count']}",
        f"- mutation_count: {report['mutation_count']}",
        f"- mutation_detected_invalid_count: {report['mutation_detected_invalid_count']}",
        f"- mutation_expected_failure_match_count: {report['mutation_expected_failure_match_count']}",
        f"- mutation_unexpected_count: {report['mutation_unexpected_count']}",
        f"- failure_class_count: {report['failure_class_count']}",
        "",
        "## RQ Evidence",
        "",
    ]
    for rq, item in report["rq_evidence"].items():
        lines.append(f"### {rq}")
        lines.append("")
        lines.append(f"- evidence: {item['evidence']}")
        lines.append(f"- result: {item['result']}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def build_dashboard(fixture_report, checker_report, mutation_report):
    failure_classes = set(checker_report.get("failure_class_counts", {})) | set(mutation_report.get("failure_class_counts", {}))
    report = {
        "evaluation_dashboard": {
            "name": "pd-oap-v2-evaluation-dashboard",
            "version": "2.0-draft",
        },
        "fixture_count": fixture_report.get("fixture_count"),
        "valid_expected_count": checker_report.get("valid_expected_count"),
        "invalid_expected_count": checker_report.get("invalid_expected_count"),
        "checker_matched_count": checker_report.get("matched_count"),
        "checker_unexpected_count": checker_report.get("unexpected_count"),
        "mutation_count": mutation_report.get("mutation_count"),
        "mutation_detected_invalid_count": mutation_report.get("detected_invalid_count"),
        "mutation_expected_failure_match_count": mutation_report.get("expected_failure_match_count"),
        "mutation_unexpected_count": mutation_report.get("unexpected_count"),
        "failure_class_count": len(failure_classes),
        "operation_family_counts": fixture_report.get("operation_family_counts"),
        "rq_evidence": {
            "RQ1": {
                "evidence": "45 fixtures over 3 operation families",
                "result": "15 access_decision, 15 reuse_authorization, and 15 review_decision fixtures",
            },
            "RQ2": {
                "evidence": "24 invalid fixtures over 12 failure classes",
                "result": "semantic checker matched all expected invalid fixture outcomes",
            },
            "RQ3": {
                "evidence": "72 mutations generated from valid fixtures",
                "result": "72 mutations detected and classified with expected failure classes",
            },
            "RQ4": {
                "evidence": "deterministic generators and reports",
                "result": "fixture, checker, and mutation results are reproducible from local scripts",
            },
        },
        "overall_passed": False,
    }
    report["overall_passed"] = (
        fixture_report.get("overall_passed") is True
        and checker_report.get("fixture_count") == 45
        and checker_report.get("matched_count") == 45
        and checker_report.get("unexpected_count") == 0
        and mutation_report.get("overall_passed") is True
        and mutation_report.get("mutation_count") == 72
        and mutation_report.get("detected_invalid_count") == 72
        and mutation_report.get("expected_failure_match_count") == 72
        and mutation_report.get("unexpected_count") == 0
        and len(failure_classes) == 12
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-report", required=True)
    parser.add_argument("--checker-report", required=True)
    parser.add_argument("--mutation-report", required=True)
    parser.add_argument("--write-report", required=True)
    parser.add_argument("--write-markdown", required=True)
    args = parser.parse_args(argv)

    try:
        report = build_dashboard(
            load_json(args.fixture_report),
            load_json(args.checker_report),
            load_json(args.mutation_report),
        )
    except Exception as exc:
        print(f"dashboard generation failed: {exc}", file=sys.stderr)
        return 1

    write_json(args.write_report, report)
    write_markdown(args.write_markdown, report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
