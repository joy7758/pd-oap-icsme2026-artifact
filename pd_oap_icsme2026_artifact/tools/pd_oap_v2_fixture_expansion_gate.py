#!/usr/bin/env python3
"""Gate for the PD-OAP v2.0 expanded fixture benchmark."""

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_TOP_LEVEL_KEYS = [
    "profile",
    "fixture_id",
    "statement_id",
    "operation",
    "actor",
    "requester",
    "subject",
    "catalog",
    "policy",
    "purpose",
    "decision",
    "conditions",
    "provenance",
    "evidence",
    "validation",
    "non_claims",
    "fixture_metadata",
]

EXPECTED_OPERATION_COUNTS = {
    "access_decision": 15,
    "reuse_authorization": 15,
    "review_decision": 15,
}

FAILURE_CLASSES = [
    "missing_authorization_basis",
    "unresolved_dataset_ref",
    "unresolved_catalog_ref",
    "requester_role_mismatch",
    "purpose_constraint_mismatch",
    "reuse_condition_missing",
    "reuse_condition_mismatch",
    "handoff_ref_unresolved",
    "review_trigger_missing",
    "review_evidence_missing",
    "policy_version_mismatch",
    "integrity_digest_mismatch",
]

DESIGN_DOCS = [
    "README.md",
    "V2_0_FIXTURE_EXPANSION_DESIGN.md",
    "V2_0_OPERATION_FAMILY_MATRIX.md",
    "V2_0_FAILURE_CLASS_CATALOG.md",
    "V2_0_FIXTURE_GENERATION_CONTRACT.md",
    "V2_0_EXPECTED_RESULTS.md",
    "V2_0_FIXTURE_TRACEABILITY.md",
    "V2_0_EDITORIAL_REASON_2_RESPONSE.md",
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_files(fixture_root):
    files = []
    for dirname in ["valid", "invalid", "edge"]:
        directory = fixture_root / dirname
        if directory.exists():
            files.extend(sorted(directory.rglob("*.json")))
    return files


def count_by(items, key):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def scan_for_placeholders(paths):
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "TODO" in text or "citation-needed" in text:
            hits.append(str(path))
    return hits


def write_markdown(path, report):
    lines = [
        "# Fixture Expansion Gate v2.0",
        "",
        f"- overall_passed: {report['overall_passed']}",
        f"- fixture_count: {report['fixture_count']}",
        f"- valid_count: {report['valid_count']}",
        f"- invalid_count: {report['invalid_count']}",
        f"- edge_count: {report['edge_count']}",
        "",
        "## Operation Family Distribution",
        "",
    ]
    for family, count in sorted(report["operation_family_counts"].items()):
        lines.append(f"- {family}: {count}")
    lines.extend(["", "## Failure Class Coverage", ""])
    for failure_class, count in sorted(report["failure_class_counts"].items()):
        lines.append(f"- {failure_class}: {count}")
    lines.extend([
        "",
        "## Limitations",
        "",
        "- The benchmark is controlled and synthetic.",
        "- It is not a population-scale empirical benchmark.",
        "- It prepares checker and mutation evaluation but does not implement them.",
        "",
        "## Next Step Recommendation",
        "",
        "Implement v2.0 checker and mutation evaluation.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report(fixture_root, design_root):
    report = {
        "fixture_expansion_gate": {
            "name": "pd-oap-v2-fixture-expansion-gate",
            "version": "2.0",
        },
        "overall_passed": False,
        "fixture_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "edge_count": 0,
        "operation_family_counts": {},
        "failure_class_counts": {},
        "missing_top_level_keys": {},
        "unsafe_claims_found": [],
        "placeholder_found": False,
        "missing_design_docs": [],
        "missing_failure_classes_in_catalog": [],
        "missing_contract_terms": [],
        "errors": [],
    }

    if not fixture_root.exists():
        report["errors"].append("fixture root missing")
        return report

    manifest_path = fixture_root / "manifest.json"
    if not manifest_path.exists():
        report["errors"].append("manifest.json missing")
        return report

    files = fixture_files(fixture_root)
    report["fixture_count"] = len(files)
    fixtures = []
    for path in files:
        try:
            data = read_json(path)
        except Exception as exc:
            report["errors"].append(f"{path}: unreadable JSON: {exc}")
            continue
        fixtures.append((path, data))

    valid_count = invalid_count = edge_count = 0
    operation_families = []
    failure_classes = []
    missing_keys = {}
    unsafe = []
    paths_for_placeholder_scan = [path for path, _ in fixtures]

    for path, data in fixtures:
        missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in data]
        if missing:
            missing_keys[str(path)] = missing
        family = data.get("fixture_metadata", {}).get("fixture_family")
        if family == "valid":
            valid_count += 1
        elif family == "invalid":
            invalid_count += 1
        elif family == "edge":
            edge_count += 1
        operation_family = data.get("fixture_metadata", {}).get("operation_family")
        if operation_family:
            operation_families.append(operation_family)
        validation = data.get("validation", {})
        expected = validation.get("expected_result")
        primary = validation.get("expected_primary_failure_code")
        failure_class = validation.get("expected_failure_class")
        if family == "invalid":
            if not primary or primary == "none":
                unsafe.append(f"{path}: invalid fixture has no primary failure code")
            if failure_class:
                failure_classes.append(failure_class)
        elif family in {"valid", "edge"}:
            if primary != "none":
                unsafe.append(f"{path}: valid/edge fixture primary failure code is not none")
        if expected not in {"valid", "invalid"}:
            unsafe.append(f"{path}: missing or invalid validation.expected_result")
        non_claims = data.get("non_claims", {})
        for key in [
            "real_government_decision",
            "legal_sufficiency",
            "production_deployment",
            "statistical_population_claim",
        ]:
            if non_claims.get(key) is True:
                unsafe.append(f"{path}: {key} true")

    operation_counts = count_by(operation_families, None)
    failure_counts = count_by(failure_classes, None)
    report["valid_count"] = valid_count
    report["invalid_count"] = invalid_count
    report["edge_count"] = edge_count
    report["operation_family_counts"] = operation_counts
    report["failure_class_counts"] = failure_counts
    report["missing_top_level_keys"] = missing_keys
    report["unsafe_claims_found"] = unsafe

    placeholder_paths = scan_for_placeholders(paths_for_placeholder_scan)
    report["placeholder_found"] = bool(placeholder_paths)
    report["placeholder_paths"] = placeholder_paths

    manifest = read_json(manifest_path)
    for key, expected in [
        ("fixture_count", 45),
        ("valid_count", 18),
        ("invalid_count", 24),
        ("edge_count", 3),
    ]:
        if manifest.get(key) != expected:
            report["errors"].append(f"manifest {key} expected {expected}, found {manifest.get(key)}")

    missing_docs = [name for name in DESIGN_DOCS if not (design_root / name).exists()]
    report["missing_design_docs"] = missing_docs

    catalog_text = (design_root / "V2_0_FAILURE_CLASS_CATALOG.md").read_text(encoding="utf-8") if (design_root / "V2_0_FAILURE_CLASS_CATALOG.md").exists() else ""
    missing_catalog = [failure_class for failure_class in FAILURE_CLASSES if failure_class not in catalog_text]
    report["missing_failure_classes_in_catalog"] = missing_catalog

    contract_text = (design_root / "V2_0_FIXTURE_GENERATION_CONTRACT.md").read_text(encoding="utf-8") if (design_root / "V2_0_FIXTURE_GENERATION_CONTRACT.md").exists() else ""
    contract_terms = [
        "about 45 fixtures",
        "at least 12 failure classes",
        "mutation evaluation",
        "raw-count reporting",
    ]
    missing_contract_terms = [term for term in contract_terms if term not in contract_text]
    report["missing_contract_terms"] = missing_contract_terms

    if report["fixture_count"] != 45:
        report["errors"].append("fixture_count must be 45")
    if valid_count != 18:
        report["errors"].append("valid_count must be 18")
    if invalid_count != 24:
        report["errors"].append("invalid_count must be 24")
    if edge_count != 3:
        report["errors"].append("edge_count must be 3")
    if operation_counts != EXPECTED_OPERATION_COUNTS:
        report["errors"].append("operation family counts do not match expected 15/15/15")
    if set(failure_counts) != set(FAILURE_CLASSES):
        report["errors"].append("failure class set must contain exactly 12 required classes")
    for failure_class in FAILURE_CLASSES:
        if failure_counts.get(failure_class) != 2:
            report["errors"].append(f"failure class {failure_class} must have exactly 2 invalid fixtures")
    if missing_keys:
        report["errors"].append("some fixtures are missing required top-level keys")
    if missing_docs:
        report["errors"].append("design docs missing")
    if missing_catalog:
        report["errors"].append("failure class catalog missing classes")
    if missing_contract_terms:
        report["errors"].append("fixture generation contract missing required terms")

    report["overall_passed"] = not (
        report["errors"]
        or report["unsafe_claims_found"]
        or report["placeholder_found"]
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--design-root", required=True)
    parser.add_argument("--write-report", required=True)
    parser.add_argument("--write-markdown", required=True)
    args = parser.parse_args(argv)

    fixture_root = Path(args.fixture_root)
    design_root = Path(args.design_root)
    report = build_report(fixture_root, design_root)

    report_path = Path(args.write_report)
    markdown_path = Path(args.write_markdown)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(markdown_path, report)

    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
