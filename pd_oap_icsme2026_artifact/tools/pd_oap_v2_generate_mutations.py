#!/usr/bin/env python3
"""Generate PD-OAP v2.0 mutation fixtures from valid fixtures."""

import argparse
import copy
import json
from pathlib import Path
import sys


NON_CLAIMS = {
    "real_government_decision": False,
    "legal_sufficiency": False,
    "production_deployment": False,
    "complete_workflow_coverage": False,
    "privacy_compliance_claim": False,
    "statistical_population_claim": False,
}

OPERATORS = [
    ("mutate_access_remove_authorization_basis", "access_decision", "missing_authorization_basis"),
    ("mutate_access_break_dataset_ref", "access_decision", "unresolved_dataset_ref"),
    ("mutate_access_break_catalog_ref", "access_decision", "unresolved_catalog_ref"),
    ("mutate_access_requester_role_mismatch", "access_decision", "requester_role_mismatch"),
    ("mutate_reuse_purpose_constraint_mismatch", "reuse_authorization", "purpose_constraint_mismatch"),
    ("mutate_reuse_remove_reuse_conditions", "reuse_authorization", "reuse_condition_missing"),
    ("mutate_reuse_condition_mismatch", "reuse_authorization", "reuse_condition_mismatch"),
    ("mutate_reuse_break_handoff_ref", "reuse_authorization", "handoff_ref_unresolved"),
    ("mutate_review_remove_trigger", "review_decision", "review_trigger_missing"),
    ("mutate_review_remove_review_evidence", "review_decision", "review_evidence_missing"),
    ("mutate_review_policy_version_mismatch", "review_decision", "policy_version_mismatch"),
    ("mutate_review_integrity_digest_mismatch", "review_decision", "integrity_digest_mismatch"),
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def valid_fixtures(fixture_root):
    fixtures = []
    for path in sorted(Path(fixture_root).rglob("*.json")):
        if path.name in {"manifest.json", "expected_results.json"}:
            continue
        data = load_json(path)
        if data.get("fixture_metadata", {}).get("fixture_family") == "valid" and data.get("validation", {}).get("expected_result") == "valid":
            fixtures.append((path, data))
    return fixtures


def operator_short_name(operator):
    for prefix in ["mutate_access_", "mutate_reuse_", "mutate_review_"]:
        if operator.startswith(prefix):
            return operator[len(prefix):]
    return operator


def operation_dir(operation_family):
    return {
        "access_decision": "access",
        "reuse_authorization": "reuse",
        "review_decision": "review",
    }[operation_family]


def apply_operator(data, operator):
    if operator == "mutate_access_remove_authorization_basis":
        data["policy"]["authorization_basis"] = ""
        data["decision"]["decision_basis"] = ""
        return "Authorization basis removed."
    if operator == "mutate_access_break_dataset_ref":
        data["operation"]["data_object_id"] = "synthetic-dataset-mutation-missing"
        return "Operation dataset reference changed to an unresolved id."
    if operator == "mutate_access_break_catalog_ref":
        data["operation"]["catalog_id"] = "synthetic-catalog-mutation-missing"
        return "Operation catalog reference changed to an unresolved id."
    if operator == "mutate_access_requester_role_mismatch":
        data["requester"]["role"] = "synthetic_commercial_broker"
        return "Requester role changed outside the policy allowed roles."
    if operator == "mutate_reuse_purpose_constraint_mismatch":
        data["purpose"]["declared_purpose"] = "synthetic_commercial_resale"
        data["purpose"]["allowed_by_policy"] = False
        return "Purpose changed outside allowed purposes."
    if operator == "mutate_reuse_remove_reuse_conditions":
        data["conditions"] = [
            item for item in data.get("conditions", [])
            if item.get("type") not in {"attribution", "onward_transfer"}
        ]
        return "Required reuse attribution and onward-transfer conditions removed."
    if operator == "mutate_reuse_condition_mismatch":
        for item in data.get("conditions", []):
            if item.get("type") == "onward_transfer":
                item["value"] = "permitted"
        return "Onward transfer condition changed to conflict with policy boundary."
    if operator == "mutate_reuse_break_handoff_ref":
        data["provenance"]["handoff_refs"] = ["synthetic-handoff-mutation-missing"]
        return "Handoff reference changed to an unresolved id."
    if operator == "mutate_review_remove_trigger":
        data["policy"]["review_triggers"] = []
        return "Review triggers removed."
    if operator == "mutate_review_remove_review_evidence":
        data["evidence"]["evidence_objects"] = [
            item for item in data["evidence"].get("evidence_objects", [])
            if item.get("type") != "review_record"
        ]
        data["evidence"]["evidence_ids"] = [
            item for item in data["evidence"].get("evidence_ids", [])
            if "review" not in item
        ]
        return "Review-record evidence removed."
    if operator == "mutate_review_policy_version_mismatch":
        data["operation"]["policy_version"] = "2026.0"
        return "Operation policy version changed away from policy block version."
    if operator == "mutate_review_integrity_digest_mismatch":
        data["provenance"]["integrity_digest"] = "sha256:mutation-mismatched-integrity"
        return "Provenance integrity digest changed away from evidence digest."
    raise ValueError(f"unknown operator: {operator}")


def clean_output(output_root):
    for dirname in ["access", "reuse", "review"]:
        directory = output_root / dirname
        if directory.exists():
            for path in directory.rglob("*.json"):
                path.unlink()
    manifest = output_root / "manifest.json"
    if manifest.exists():
        manifest.unlink()


def generate(fixture_root, output_root):
    output_root.mkdir(parents=True, exist_ok=True)
    clean_output(output_root)
    source = valid_fixtures(fixture_root)
    mutations = []
    operator_counts = {}
    failure_counts = {}
    operation_counts = {"access_decision": 0, "reuse_authorization": 0, "review_decision": 0}

    for _, fixture in source:
        source_family = fixture["fixture_metadata"]["operation_family"]
        for operator, operation_family, failure_class in OPERATORS:
            if source_family != operation_family:
                continue
            mutated = copy.deepcopy(fixture)
            source_fixture_id = fixture["fixture_id"]
            short = operator_short_name(operator)
            mutation_id = f"mutation_{source_fixture_id}_{short}"
            mutation_description = apply_operator(mutated, operator)
            mutated["fixture_id"] = mutation_id
            mutated["statement_id"] = f"statement-{mutation_id}"
            mutated["validation"]["expected_result"] = "invalid"
            mutated["validation"]["expected_primary_failure_code"] = failure_class
            mutated["validation"]["expected_failure_class"] = failure_class
            mutated["fixture_metadata"]["fixture_family"] = "mutation"
            mutated["fixture_metadata"]["primary_purpose"] = "mutation_evaluation"
            mutated["fixture_metadata"]["notes"] = "Synthetic mutation generated from a valid v2.0 fixture."
            mutated["mutation_metadata"] = {
                "source_fixture_id": source_fixture_id,
                "mutation_operator": operator,
                "expected_failure_class": failure_class,
                "mutation_description": mutation_description,
            }
            mutated["non_claims"] = NON_CLAIMS
            out_path = output_root / operation_dir(operation_family) / f"{mutation_id}.json"
            write_json(out_path, mutated)
            mutations.append({
                "fixture_id": mutation_id,
                "path": out_path.relative_to(output_root).as_posix(),
                "source_fixture_id": source_fixture_id,
                "operation_family": operation_family,
                "mutation_operator": operator,
                "expected_failure_class": failure_class,
            })
            operation_counts[operation_family] += 1
            operator_counts[operator] = operator_counts.get(operator, 0) + 1
            failure_counts[failure_class] = failure_counts.get(failure_class, 0) + 1

    manifest = {
        "mutation_benchmark_id": "pd-oap-mutation-evaluation@2.0-draft",
        "source_valid_fixture_count": len(source),
        "mutation_count": len(mutations),
        "operation_family_counts": operation_counts,
        "mutation_operator_counts": operator_counts,
        "expected_failure_class_counts": failure_counts,
        "non_claims": NON_CLAIMS,
        "mutations": sorted(mutations, key=lambda item: item["fixture_id"]),
    }
    write_json(output_root / "manifest.json", manifest)
    write_generation_report(output_root, manifest)


def write_generation_report(output_root, manifest):
    report_dir = output_root.parents[1] / "reports"
    report = {
        "mutation_generation": {
            "name": "pd-oap-v2-mutation-generation",
            "version": "2.0-draft",
        },
        "overall_passed": manifest["mutation_count"] == 72,
        **manifest,
    }
    write_json(report_dir / "mutation_generation_report_v2_0.json", report)
    lines = [
        "# Mutation Generation Report v2.0",
        "",
        f"- source_valid_fixture_count: {manifest['source_valid_fixture_count']}",
        f"- mutation_count: {manifest['mutation_count']}",
        "",
        "## Operator Counts",
        "",
    ]
    for key, value in sorted(manifest["mutation_operator_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Expected Failure Class Counts", ""])
    for key, value in sorted(manifest["expected_failure_class_counts"].items()):
        lines.append(f"- {key}: {value}")
    (report_dir / "mutation_generation_report_v2_0.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args(argv)
    try:
        generate(Path(args.fixture_root), Path(args.output_root))
    except Exception as exc:
        print(f"mutation generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
