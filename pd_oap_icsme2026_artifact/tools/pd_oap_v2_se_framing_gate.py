#!/usr/bin/env python3
"""Gate for PD-OAP v2.0 software-engineering framing artifacts."""

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_FILES = [
    "README.md",
    "SOFTWARE_ENGINEERING_CONTRIBUTION_V2_0.md",
    "METHOD_CLAIM_RECONSTRUCTION_V2_0.md",
    "SE_PROBLEM_TO_ARTIFACT_PIPELINE_V2_0.md",
    "DESIGN_REQUIREMENTS_RECONSTRUCTED_V2_0.md",
    "RQ_RECONSTRUCTION_V2_0.md",
    "CLAIMS_TO_EVIDENCE_V2_0.md",
    "EVALUATION_ARGUMENT_V2_0.md",
    "RELATED_WORK_POSITIONING_V2_0.md",
    "EDITORIAL_REASON_3_RESPONSE_V2_0.md",
    "TECHNICAL_REPORT_TO_RESEARCH_ARTICLE_DELTA_V2_0.md",
]

METHOD_CLAIM = (
    "PD-OAP provides a profile-and-checker method for constructing and evaluating "
    "operation-accountability artifacts in public-data workflows."
)

THESIS = (
    "a software-engineering method for specifying, validating, and evaluating "
    "operation-accountability artifacts for public-data workflows"
)

UNSAFE_PATTERNS = [
    "proves legal compliance",
    "production-ready",
    "real government deployment",
    "full data-space interoperability",
    "third-party implementation proof",
]

PLACEHOLDER_PATTERNS = [
    "TODO",
    "citation-needed",
]

REQUIRED_NUMBERS = [
    "45 fixtures",
    "3 operation families",
    "12 semantic failure classes",
    "45/45",
    "72/72",
    "unexpected_count 0",
]

EVAL_ARGUMENT_NUMBERS = [
    "21 expected-valid fixtures",
    "24 expected-invalid fixtures",
    "72 mutations",
]

DELTA_TERMS = [
    "method claim",
    "formal definitions",
    "mutation evaluation",
    "RQ-driven evaluation",
]


def read_text(path):
    return path.read_text(encoding="utf-8")


def markdown_list(items):
    if not items:
        return "- none\n"
    return "".join(f"- {item}\n" for item in items)


def collect_text(root):
    parts = []
    for name in REQUIRED_FILES:
        path = root / name
        if path.exists():
            parts.append(read_text(path))
    return "\n".join(parts)


def find_markers(text, prefix, count):
    found = []
    for index in range(1, count + 1):
        token = f"{prefix}{index}"
        if re.search(rf"\b{re.escape(token)}\b", text):
            found.append(token)
    return found


def scan_unsafe(text):
    hits = []
    for pattern in UNSAFE_PATTERNS:
        if pattern in text:
            hits.append(pattern)
    return hits


def build_report(root, evaluation_report_path):
    required_paths = [root / name for name in REQUIRED_FILES]
    missing_files = [str(path.relative_to(root)) for path in required_paths if not path.exists()]
    combined = collect_text(root)
    claims_text = read_text(root / "CLAIMS_TO_EVIDENCE_V2_0.md") if (root / "CLAIMS_TO_EVIDENCE_V2_0.md").exists() else ""
    eval_text = read_text(root / "EVALUATION_ARGUMENT_V2_0.md") if (root / "EVALUATION_ARGUMENT_V2_0.md").exists() else ""
    delta_text = read_text(root / "TECHNICAL_REPORT_TO_RESEARCH_ARTICLE_DELTA_V2_0.md") if (root / "TECHNICAL_REPORT_TO_RESEARCH_ARTICLE_DELTA_V2_0.md").exists() else ""

    evaluation_dashboard_passed = False
    evaluation_report_exists = evaluation_report_path.exists()
    if evaluation_report_exists:
        try:
            evaluation_dashboard_passed = json.loads(read_text(evaluation_report_path)).get("overall_passed") is True
        except json.JSONDecodeError:
            evaluation_dashboard_passed = False

    rq_found = find_markers(combined, "RQ", 4)
    dr_found = find_markers(combined, "DR", 8)
    evaluation_numbers_found = all(token in claims_text for token in REQUIRED_NUMBERS)
    eval_argument_numbers_found = all(token in eval_text for token in EVAL_ARGUMENT_NUMBERS)
    delta_terms_found = all(term in delta_text for term in DELTA_TERMS)
    placeholder_found = any(pattern in combined for pattern in PLACEHOLDER_PATTERNS)

    report = {
        "se_framing_gate": {
            "name": "pd-oap-v2-se-framing-gate",
            "version": "2.0",
        },
        "overall_passed": False,
        "required_files_present": not missing_files,
        "missing_files": missing_files,
        "method_claim_found": METHOD_CLAIM in combined,
        "thesis_found": THESIS in combined,
        "rq_found": rq_found,
        "dr_found": dr_found,
        "evaluation_numbers_found": evaluation_numbers_found,
        "eval_argument_numbers_found": eval_argument_numbers_found,
        "delta_terms_found": delta_terms_found,
        "evaluation_report_exists": evaluation_report_exists,
        "evaluation_dashboard_passed": evaluation_dashboard_passed,
        "unsafe_claims_found": scan_unsafe(combined),
        "placeholder_found": placeholder_found,
    }
    report["overall_passed"] = (
        report["required_files_present"]
        and report["method_claim_found"]
        and report["thesis_found"]
        and len(rq_found) >= 4
        and len(dr_found) >= 8
        and evaluation_numbers_found
        and eval_argument_numbers_found
        and delta_terms_found
        and evaluation_report_exists
        and evaluation_dashboard_passed
        and not report["unsafe_claims_found"]
        and not placeholder_found
    )
    return report


def write_markdown(path, report):
    lines = [
        "# SE Framing Gate v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- required_files_present: {report['required_files_present']}",
        f"- method_claim_found: {report['method_claim_found']}",
        f"- thesis_found: {report['thesis_found']}",
        f"- evaluation_numbers_found: {report['evaluation_numbers_found']}",
        f"- evaluation_dashboard_passed: {report['evaluation_dashboard_passed']}",
        f"- placeholder_found: {report['placeholder_found']}",
        "",
        "## RQ Coverage",
        "",
        markdown_list(report["rq_found"]),
        "## DR Coverage",
        "",
        markdown_list(report["dr_found"]),
        "## Unsafe Claims",
        "",
        markdown_list(report["unsafe_claims_found"]),
        "## Next Step",
        "",
    ]
    if report["overall_passed"]:
        lines.append("Create v2.0 manuscript outline and rewritten evaluation section.")
    else:
        lines.append("Resolve missing SE framing requirements before drafting the manuscript outline.")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--evaluation-report", required=True)
    parser.add_argument("--write-report", required=True)
    parser.add_argument("--write-markdown", required=True)
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(f"SE framing root not found: {root}", file=sys.stderr)
        return 2

    report = build_report(root, Path(args.evaluation_report))
    report_path = Path(args.write_report)
    markdown_path = Path(args.write_markdown)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(markdown_path, report)
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
