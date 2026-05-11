#!/usr/bin/env python3
"""Gate for PD-OAP v2.0 definition hardening artifacts."""

import argparse
import json
from pathlib import Path
import re
import sys


CONCEPTS = [
    "public-data operation",
    "operation-accountability statement",
    "structural inspectability",
    "reviewability",
    "semantic failure surface",
    "controlled fixture benchmark",
]

REQUIRED_CORE_HEADINGS = [
    "One-sentence definition",
    "Longer definition",
    "Scope",
    "What this is not",
    "Example",
    "Non-example",
    "Artifact fields or components",
    "Validation consequence",
    "Software engineering role",
    "Safe manuscript wording",
    "Unsafe wording to avoid",
]

REQUIRED_FILES = [
    "README.md",
    "CORE_DEFINITIONS_V2_0.md",
    "DEFINITION_TEMPLATE_V2_0.md",
    "DEFINITIONS_TO_ARTIFACT_TRACEABILITY_V2_0.md",
    "DEFINITION_TO_EVALUATION_REQUIREMENTS_V2_0.md",
    "SE_PROBLEM_STATEMENT_V2_0.md",
    "CONCEPT_AMBIGUITY_AUDIT_V2_0.md",
    "CONTROLLED_FIXTURE_BENCHMARK_CONTRACT_V2_0.md",
    "EDITORIAL_REASON_1_RESPONSE_V2_0.md",
]

UNSAFE_CLAIMS = [
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

THESIS = (
    "PD-OAP studies how to specify, instantiate, validate, and evaluate "
    "operation-accountability artifacts for public-data workflows."
)


def read_text(path):
    return path.read_text(encoding="utf-8")


def extract_section(text, concept):
    pattern = re.compile(
        rf"^# {re.escape(concept)}\s*$([\s\S]*?)(?=^# (?!#)|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def markdown_list(items):
    if not items:
        return "- none\n"
    return "".join(f"- {item}\n" for item in items)


def write_markdown(path, report):
    lines = [
        "# Definition Hardening Gate v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- required_files_present: {report['required_files_present']}",
        f"- placeholder_found: {report['placeholder_found']}",
        "",
        "## Concepts Found",
        "",
        markdown_list(report["concepts_found"]),
        "## Missing Concepts",
        "",
        markdown_list(report["missing_concepts"]),
        "## Missing Headings",
        "",
    ]
    if report["missing_headings"]:
        for concept, headings in report["missing_headings"].items():
            lines.append(f"### {concept}")
            lines.append("")
            lines.append(markdown_list(headings))
    else:
        lines.append("- none\n")
    lines.extend([
        "## Unsafe Claims Found",
        "",
        markdown_list(report["unsafe_claims_found"]),
        "## Next Step",
        "",
    ])
    if report["overall_passed"]:
        lines.append(
            "Definition hardening passed. The next phase can plan fixture expansion, "
            "but existing fixtures and checker logic should remain unchanged until that phase begins."
        )
    else:
        lines.append("Resolve missing concepts, headings, unsafe claims, or placeholders before fixture expansion.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report(root):
    required_paths = [root / name for name in REQUIRED_FILES]
    missing_files = [str(path.relative_to(root)) for path in required_paths if not path.exists()]
    required_files_present = not missing_files

    all_text_parts = []
    for path in required_paths:
        if path.exists():
            all_text_parts.append(read_text(path))
    combined = "\n".join(all_text_parts)

    core_path = root / "CORE_DEFINITIONS_V2_0.md"
    core = read_text(core_path) if core_path.exists() else ""

    concepts_found = [concept for concept in CONCEPTS if concept in core]
    missing_concepts = [concept for concept in CONCEPTS if concept not in concepts_found]

    missing_headings = {}
    for concept in CONCEPTS:
        section = extract_section(core, concept)
        if not section:
            missing_headings[concept] = REQUIRED_CORE_HEADINGS[:]
            continue
        missing = [heading for heading in REQUIRED_CORE_HEADINGS if f"## {heading}" not in section]
        if missing:
            missing_headings[concept] = missing

    se_path = root / "SE_PROBLEM_STATEMENT_V2_0.md"
    se_text = read_text(se_path) if se_path.exists() else ""
    thesis_found = THESIS in se_text

    contract_path = root / "CONTROLLED_FIXTURE_BENCHMARK_CONTRACT_V2_0.md"
    contract_text = read_text(contract_path) if contract_path.exists() else ""
    contract_required = [
        "about 45 fixtures",
        "at least 12 failure classes",
        "mutation evaluation",
        "raw-count reporting",
    ]
    missing_contract_terms = [term for term in contract_required if term not in contract_text]

    unsafe_claims_found = [claim for claim in UNSAFE_CLAIMS if claim in combined]
    placeholder_found = any(pattern in combined for pattern in PLACEHOLDER_PATTERNS)

    overall = (
        required_files_present
        and not missing_concepts
        and not missing_headings
        and thesis_found
        and not missing_contract_terms
        and not unsafe_claims_found
        and not placeholder_found
    )

    return {
        "definition_hardening_gate": {
            "name": "pd-oap-v2-definition-hardening-gate",
            "version": "2.0",
        },
        "overall_passed": overall,
        "required_files_present": required_files_present,
        "missing_required_files": missing_files,
        "concepts_found": concepts_found,
        "missing_concepts": missing_concepts,
        "missing_headings": missing_headings,
        "thesis_found": thesis_found,
        "missing_contract_terms": missing_contract_terms,
        "unsafe_claims_found": unsafe_claims_found,
        "placeholder_found": placeholder_found,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--write-report", required=True)
    parser.add_argument("--write-markdown", required=True)
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(f"definition hardening root not found: {root}", file=sys.stderr)
        return 2

    report = build_report(root)

    report_path = Path(args.write_report)
    markdown_path = Path(args.write_markdown)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(markdown_path, report)

    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
