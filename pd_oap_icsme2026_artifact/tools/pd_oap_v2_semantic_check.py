#!/usr/bin/env python3
"""PD-OAP v2.0 semantic checker for controlled fixtures and mutations."""

import argparse
import json
from pathlib import Path
import re
import sys


CHECKER = {
    "name": "pd-oap-v2-semantic-checker",
    "version": "2.0-draft",
}

EXCLUDED_JSON_NAMES = {"manifest.json", "expected_results.json"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_get(data, path, default=None):
    current = data
    for part in path:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    return current


def normalize_token(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")


def issue(failure_code, rule_surface, path, message):
    return {
        "failure_code": failure_code,
        "rule_surface": rule_surface,
        "path": path,
        "message": message,
    }


def collect_refs(data):
    evidence = data.get("evidence", {})
    evidence_ids = set(evidence.get("evidence_ids", []))
    for obj in evidence.get("evidence_objects", []):
        evidence_id = obj.get("evidence_id")
        if evidence_id:
            evidence_ids.add(evidence_id)
    return {
        "dataset_refs": set(data.get("catalog", {}).get("dataset_refs", [])),
        "policy_refs": set(data.get("catalog", {}).get("policy_refs", [])),
        "source_refs": set(data.get("provenance", {}).get("source_refs", [])),
        "handoff_refs": set(data.get("provenance", {}).get("handoff_refs", [])),
        "evidence_ids": evidence_ids,
    }


def evidence_kinds(data):
    kinds = set()
    purposes = set()
    for obj in data.get("evidence", {}).get("evidence_objects", []):
        kinds.add(normalize_token(obj.get("type")))
        purposes.add(normalize_token(obj.get("purpose")))
    return kinds | purposes


def condition_codes(data):
    codes = set()
    for cond in data.get("conditions", []):
        cond_type = normalize_token(cond.get("type"))
        value = normalize_token(cond.get("value"))
        if cond_type == "onward_transfer" and value == "forbidden":
            codes.add("onward_transfer_forbidden")
        elif cond_type == "onward_transfer" and value:
            codes.add(f"onward_transfer_{value}")
        elif cond_type:
            codes.add(cond_type)
    return codes


def has_condition_type(data, condition_type):
    target = normalize_token(condition_type)
    return any(normalize_token(cond.get("type")) == target for cond in data.get("conditions", []))


def policy_allowed_roles(data):
    return set(data.get("policy", {}).get("allowed_requester_roles", []))


def policy_required_conditions(data):
    return set(data.get("policy", {}).get("required_reuse_conditions", []))


def declared_policy_version(data):
    return (
        safe_get(data, ["operation", "policy_version"]),
        safe_get(data, ["policy", "policy_version"]),
    )


def declared_digest_values(data):
    return (
        safe_get(data, ["provenance", "integrity_digest"]),
        safe_get(data, ["evidence", "integrity_digest"]),
    )


def compute_simple_digest_if_possible(data):
    # Fixtures already declare synthetic digests. This hook is reserved for
    # future material-based digest checks when source material is packaged.
    return None


def validate_semantics(data):
    issues = []
    operation_family = safe_get(data, ["operation", "operation_family"])

    policy = data.get("policy", {})
    operation = data.get("operation", {})
    policy_id = policy.get("policy_id")
    operation_policy_id = operation.get("policy_id")
    policy_version = policy.get("policy_version")
    authorization_basis = policy.get("authorization_basis")
    if not policy or not policy_id or not policy_version or not authorization_basis or operation_policy_id != policy_id:
        issues.append(issue(
            "missing_authorization_basis",
            "policy basis completeness",
            "policy.authorization_basis",
            "Policy basis, policy id, policy version, or operation policy reference is missing or unresolved.",
        ))
        return issues

    refs = collect_refs(data)
    op_dataset = operation.get("data_object_id")
    subject_dataset = safe_get(data, ["subject", "data_object_id"])
    if not op_dataset or op_dataset != subject_dataset or op_dataset not in refs["dataset_refs"]:
        issues.append(issue(
            "unresolved_dataset_ref",
            "dataset reference closure",
            "operation.data_object_id",
            "Operation data object reference does not resolve to subject and catalog dataset refs.",
        ))
        return issues

    op_catalog = operation.get("catalog_id")
    catalog_id = safe_get(data, ["catalog", "catalog_id"])
    if not op_catalog or op_catalog != catalog_id:
        issues.append(issue(
            "unresolved_catalog_ref",
            "catalog reference closure",
            "operation.catalog_id",
            "Operation catalog reference does not match packaged catalog metadata.",
        ))
        return issues

    requester_role = safe_get(data, ["requester", "role"])
    if requester_role not in policy_allowed_roles(data):
        issues.append(issue(
            "requester_role_mismatch",
            "requester-role policy constraint",
            "requester.role",
            "Requester role is not allowed by the declared policy.",
        ))
        return issues

    declared_purpose = safe_get(data, ["purpose", "declared_purpose"])
    allowed_purposes = set(policy.get("allowed_purposes", []))
    if declared_purpose not in allowed_purposes or safe_get(data, ["purpose", "allowed_by_policy"]) is False:
        issues.append(issue(
            "purpose_constraint_mismatch",
            "purpose constraint matching",
            "purpose.declared_purpose",
            "Declared purpose is not allowed by the policy.",
        ))
        return issues

    if operation_family == "reuse_authorization":
        required = policy_required_conditions(data)
        codes = condition_codes(data)
        missing_required = [code for code in required if code == "attribution" and code not in codes]
        onward_required = "onward_transfer_forbidden" in required
        onward_present = has_condition_type(data, "onward_transfer")
        if missing_required or (onward_required and not onward_present):
            issues.append(issue(
                "reuse_condition_missing",
                "condition completeness",
                "conditions",
                "Required reuse conditions are missing.",
            ))
            return issues
        if onward_required and "onward_transfer_forbidden" not in codes:
            issues.append(issue(
                "reuse_condition_mismatch",
                "condition consistency",
                "conditions",
                "Declared reuse condition conflicts with policy-required onward-transfer boundary.",
            ))
            return issues
        if refs["handoff_refs"] and not refs["handoff_refs"].issubset(refs["evidence_ids"]):
            issues.append(issue(
                "handoff_ref_unresolved",
                "handoff reference closure",
                "provenance.handoff_refs",
                "One or more handoff references do not resolve to packaged evidence.",
            ))
            return issues

    if operation_family == "review_decision":
        if not policy.get("review_triggers"):
            issues.append(issue(
                "review_trigger_missing",
                "review trigger completeness",
                "policy.review_triggers",
                "Review operation lacks a declared review trigger.",
            ))
            return issues
        if "review_record" not in evidence_kinds(data):
            issues.append(issue(
                "review_evidence_missing",
                "review evidence completeness",
                "evidence.evidence_objects",
                "Review operation lacks review-record evidence.",
            ))
            return issues
        operation_version, policy_block_version = declared_policy_version(data)
        if operation_version != policy_block_version:
            issues.append(issue(
                "policy_version_mismatch",
                "policy version consistency",
                "operation.policy_version",
                "Operation policy version does not match packaged policy version.",
            ))
            return issues
        provenance_digest, evidence_digest = declared_digest_values(data)
        if provenance_digest != evidence_digest:
            issues.append(issue(
                "integrity_digest_mismatch",
                "integrity digest consistency",
                "provenance.integrity_digest",
                "Provenance integrity digest does not match evidence integrity digest.",
            ))
            return issues

    return issues


def check_expectation(data, observed_result, primary_failure_code):
    expected_result = safe_get(data, ["validation", "expected_result"])
    expected_primary = safe_get(data, ["validation", "expected_primary_failure_code"])
    return expected_result == observed_result and expected_primary == primary_failure_code


def check_fixture(path):
    data = load_json(path)
    issues = validate_semantics(data)
    observed_result = "invalid" if issues else "valid"
    primary = issues[0]["failure_code"] if issues else "none"
    return {
        "checker": CHECKER,
        "fixture_path": str(path),
        "fixture_id": data.get("fixture_id"),
        "operation_family": safe_get(data, ["fixture_metadata", "operation_family"]) or safe_get(data, ["operation", "operation_family"]),
        "expected_result": safe_get(data, ["validation", "expected_result"]),
        "expected_primary_failure_code": safe_get(data, ["validation", "expected_primary_failure_code"]),
        "observed_result": observed_result,
        "primary_failure_code": primary,
        "matched_expectation": check_expectation(data, observed_result, primary),
        "issues": issues,
    }


def find_fixture_json(root):
    files = []
    for path in sorted(Path(root).rglob("*.json")):
        if path.name in EXCLUDED_JSON_NAMES:
            continue
        if "reports" in path.parts:
            continue
        files.append(path)
    return files


def run_matrix(root):
    files = find_fixture_json(root)
    results = [check_fixture(path) for path in files]
    operation_counts = {}
    failure_counts = {}
    valid_expected_count = 0
    invalid_expected_count = 0
    matched_count = 0
    for result in results:
        family = result["operation_family"]
        operation_counts[family] = operation_counts.get(family, 0) + 1
        expected = result["expected_result"]
        if expected == "valid":
            valid_expected_count += 1
        elif expected == "invalid":
            invalid_expected_count += 1
            failure = result["expected_primary_failure_code"]
            failure_counts[failure] = failure_counts.get(failure, 0) + 1
        if result["matched_expectation"]:
            matched_count += 1
    return {
        "checker": CHECKER,
        "fixture_root": str(root),
        "fixture_count": len(results),
        "valid_expected_count": valid_expected_count,
        "invalid_expected_count": invalid_expected_count,
        "matched_count": matched_count,
        "unexpected_count": len(results) - matched_count,
        "operation_family_counts": operation_counts,
        "failure_class_counts": failure_counts,
        "results": results,
    }


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_matrix_markdown(report_path, matrix):
    md_path = Path(report_path).with_suffix(".md")
    lines = [
        "# Semantic Checker Matrix v2.0",
        "",
        f"- fixture_count: {matrix['fixture_count']}",
        f"- valid_expected_count: {matrix['valid_expected_count']}",
        f"- invalid_expected_count: {matrix['invalid_expected_count']}",
        f"- matched_count: {matrix['matched_count']}",
        f"- unexpected_count: {matrix['unexpected_count']}",
        "",
        "## Operation Family Counts",
        "",
    ]
    for key, value in sorted(matrix["operation_family_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Failure Class Counts", ""])
    for key, value in sorted(matrix["failure_class_counts"].items()):
        lines.append(f"- {key}: {value}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", nargs="?")
    parser.add_argument("--expect-declared", action="store_true")
    parser.add_argument("--matrix")
    parser.add_argument("--write-report")
    args = parser.parse_args(argv)

    if args.matrix:
        matrix = run_matrix(Path(args.matrix))
        if args.write_report:
            write_json(args.write_report, matrix)
            write_matrix_markdown(args.write_report, matrix)
        else:
            print(json.dumps(matrix, indent=2, sort_keys=True))
        return 0 if matrix["unexpected_count"] == 0 else 1

    if not args.fixture:
        parser.error("provide a fixture path or --matrix root")

    report = check_fixture(Path(args.fixture))
    if args.write_report:
        write_json(args.write_report, report)
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    if args.expect_declared:
        return 0 if report["matched_expectation"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
