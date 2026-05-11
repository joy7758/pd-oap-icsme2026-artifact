#!/usr/bin/env python3
"""Generate the PD-OAP v2.0 controlled fixture benchmark."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


PROFILE = {
    "name": "public-data-operation-accountability-profile",
    "version": "2.0-draft",
    "profile_id": "public-data-operation-accountability-profile@2.0-draft",
}

NON_CLAIMS = {
    "real_government_decision": False,
    "legal_sufficiency": False,
    "production_deployment": False,
    "complete_workflow_coverage": False,
    "privacy_compliance_claim": False,
    "statistical_population_claim": False,
}

OPERATION_CONFIG = {
    "access_decision": {
        "short": "access",
        "requester_role": "public_research_unit",
        "allowed_purpose": "public_service_planning",
        "requested_action": "restricted_access",
        "condition_type": "access_boundary",
        "evidence_type": "authorization_record",
    },
    "reuse_authorization": {
        "short": "reuse",
        "requester_role": "public_service_partner",
        "allowed_purpose": "service_improvement",
        "requested_action": "bounded_reuse",
        "condition_type": "reuse_condition",
        "evidence_type": "reuse_authorization_record",
    },
    "review_decision": {
        "short": "review",
        "requester_role": "review_board_member",
        "allowed_purpose": "accountability_review",
        "requested_action": "post_operation_review",
        "condition_type": "review_condition",
        "evidence_type": "review_record",
    },
}

FAILURE_CLASSES = [
    ("missing_authorization_basis", "access_decision", "policy basis completeness"),
    ("unresolved_dataset_ref", "access_decision", "dataset reference closure"),
    ("unresolved_catalog_ref", "access_decision", "catalog reference closure"),
    ("requester_role_mismatch", "access_decision", "requester-role policy constraint"),
    ("purpose_constraint_mismatch", "reuse_authorization", "purpose constraint matching"),
    ("reuse_condition_missing", "reuse_authorization", "condition completeness"),
    ("reuse_condition_mismatch", "reuse_authorization", "condition consistency"),
    ("handoff_ref_unresolved", "reuse_authorization", "handoff reference closure"),
    ("review_trigger_missing", "review_decision", "review trigger completeness"),
    ("review_evidence_missing", "review_decision", "review evidence completeness"),
    ("policy_version_mismatch", "review_decision", "policy version consistency"),
    ("integrity_digest_mismatch", "review_decision", "integrity digest consistency"),
]

REQUIRED_SURFACES_BY_FAMILY = {
    "access_decision": [
        "operation_boundary",
        "policy_basis_presence",
        "dataset_reference_closure",
        "catalog_reference_closure",
        "requester_role_policy_match",
    ],
    "reuse_authorization": [
        "operation_boundary",
        "purpose_policy_match",
        "reuse_condition_completeness",
        "reuse_condition_consistency",
        "handoff_reference_closure",
    ],
    "review_decision": [
        "operation_boundary",
        "review_trigger_presence",
        "review_evidence_presence",
        "policy_version_consistency",
        "integrity_digest_consistency",
    ],
}


def digest(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def condition(condition_id, condition_type, value):
    return {
        "condition_id": condition_id,
        "type": condition_type,
        "value": value,
        "source": "synthetic_policy",
    }


def evidence_object(evidence_id, evidence_type, linked_refs, purpose):
    return {
        "evidence_id": evidence_id,
        "type": evidence_type,
        "linked_refs": linked_refs,
        "purpose": purpose,
        "digest": digest(evidence_id),
        "synthetic": True,
    }


def base_fixture(fixture_id, operation_family, fixture_family, index, expected_result, failure_class="none"):
    config = OPERATION_CONFIG[operation_family]
    dataset_id = f"synthetic-dataset-{config['short']}-{index:03d}"
    catalog_id = f"synthetic-catalog-{config['short']}-001"
    policy_id = f"synthetic-policy-{config['short']}-001"
    requester_id = f"synthetic-requester-{config['short']}-{index:03d}"
    actor_id = f"synthetic-data-steward-{config['short']}-001"
    policy_version = "2026.1"
    handoff_id = f"synthetic-handoff-{fixture_id}"
    evidence_ids = [
        f"evidence-{fixture_id}-policy",
        f"evidence-{fixture_id}-dataset",
        f"evidence-{fixture_id}-decision",
    ]
    if operation_family == "review_decision":
        evidence_ids.append(f"evidence-{fixture_id}-review")
    if operation_family == "reuse_authorization":
        evidence_ids.append(handoff_id)

    conditions = [
        condition(
            f"condition-{fixture_id}-purpose",
            config["condition_type"],
            f"limited_to_{config['allowed_purpose']}",
        )
    ]
    if operation_family == "reuse_authorization":
        conditions.extend([
            condition(f"condition-{fixture_id}-attribution", "attribution", "required"),
            condition(f"condition-{fixture_id}-onward-transfer", "onward_transfer", "forbidden"),
        ])

    evidence_objects = [
        evidence_object(evidence_ids[0], "policy_record", [policy_id], "policy_basis"),
        evidence_object(evidence_ids[1], "dataset_record", [dataset_id], "dataset_reference"),
        evidence_object(evidence_ids[2], config["evidence_type"], [dataset_id, policy_id], "decision_record"),
    ]
    if operation_family == "review_decision":
        evidence_objects.append(
            evidence_object(evidence_ids[-1], "review_record", [dataset_id, policy_id], "review_record")
        )
    if operation_family == "reuse_authorization":
        evidence_objects.append(
            evidence_object(handoff_id, "handoff_record", [dataset_id, policy_id], "handoff_record")
        )

    expected_failure = failure_class if expected_result == "invalid" else "none"
    return {
        "profile": PROFILE,
        "fixture_id": fixture_id,
        "statement_id": f"statement-{fixture_id}",
        "operation": {
            "operation_id": f"operation-{fixture_id}",
            "operation_family": operation_family,
            "operation_type": operation_family,
            "data_object_id": dataset_id,
            "catalog_id": catalog_id,
            "policy_id": policy_id,
            "policy_version": policy_version,
            "requested_action": config["requested_action"],
            "decision_scope": "single_operation",
        },
        "actor": {
            "actor_id": actor_id,
            "actor_type": "synthetic_data_steward",
            "name": "Synthetic Data Steward Office",
        },
        "requester": {
            "requester_id": requester_id,
            "role": config["requester_role"],
            "declared_affiliation": "synthetic local research or service unit",
        },
        "subject": {
            "data_object_id": dataset_id,
            "object_type": "public_data_object",
            "title": f"Synthetic {config['short']} public-data object {index:03d}",
            "sensitivity": "bounded_public_sector_data",
        },
        "catalog": {
            "catalog_id": catalog_id,
            "catalog_label": f"Synthetic {config['short']} catalog",
            "dataset_refs": [dataset_id],
            "policy_refs": [policy_id],
        },
        "policy": {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "authorization_basis": f"synthetic_authorization_basis_{config['short']}",
            "allowed_requester_roles": [config["requester_role"]],
            "allowed_purposes": [config["allowed_purpose"]],
            "required_reuse_conditions": ["attribution", "onward_transfer_forbidden"]
            if operation_family == "reuse_authorization"
            else [],
            "review_triggers": ["scheduled_review", "evidence_completeness_check"]
            if operation_family == "review_decision"
            else [],
        },
        "purpose": {
            "purpose_id": f"purpose-{fixture_id}",
            "declared_purpose": config["allowed_purpose"],
            "allowed_by_policy": True,
        },
        "decision": {
            "decision_id": f"decision-{fixture_id}",
            "outcome": "allow",
            "decision_basis": f"synthetic_authorization_basis_{config['short']}",
            "rationale": "Synthetic fixture decision with internally consistent policy and evidence linkage.",
        },
        "conditions": conditions,
        "provenance": {
            "source_refs": [dataset_id, catalog_id, policy_id],
            "handoff_refs": [handoff_id] if operation_family == "reuse_authorization" else [],
            "integrity_digest": digest(f"integrity-{fixture_id}"),
        },
        "evidence": {
            "evidence_ids": evidence_ids,
            "evidence_objects": evidence_objects,
            "integrity_digest": digest(f"integrity-{fixture_id}"),
        },
        "validation": {
            "expected_result": expected_result,
            "expected_primary_failure_code": expected_failure,
            "expected_failure_class": expected_failure,
            "required_rule_surfaces": REQUIRED_SURFACES_BY_FAMILY[operation_family],
        },
        "non_claims": NON_CLAIMS,
        "fixture_metadata": {
            "benchmark_version": "2.0-draft",
            "fixture_family": fixture_family,
            "operation_family": operation_family,
            "synthetic": True,
            "controlled_fixture": True,
            "primary_purpose": "negative_control" if expected_result == "invalid" else "representation",
            "notes": "Synthetic controlled fixture for PD-OAP v2.0 evaluation design.",
        },
    }


def apply_defect(fixture, failure_class, surface):
    if failure_class == "missing_authorization_basis":
        fixture["policy"]["authorization_basis"] = ""
        fixture["decision"]["decision_basis"] = ""
        description = "Authorization basis is absent while the operation depends on a declared policy basis."
    elif failure_class == "unresolved_dataset_ref":
        fixture["operation"]["data_object_id"] = "synthetic-dataset-missing"
        description = "Operation data object reference does not resolve in the packaged catalog."
    elif failure_class == "unresolved_catalog_ref":
        fixture["operation"]["catalog_id"] = "synthetic-catalog-missing"
        description = "Operation catalog reference does not match the packaged catalog block."
    elif failure_class == "requester_role_mismatch":
        fixture["requester"]["role"] = "synthetic_commercial_broker"
        description = "Requester role is outside the policy allowed roles."
    elif failure_class == "purpose_constraint_mismatch":
        fixture["purpose"]["declared_purpose"] = "synthetic_commercial_resale"
        fixture["purpose"]["allowed_by_policy"] = False
        description = "Declared purpose conflicts with the policy allowed purpose."
    elif failure_class == "reuse_condition_missing":
        fixture["conditions"] = [
            item for item in fixture["conditions"] if item["type"] not in {"attribution", "onward_transfer"}
        ]
        description = "Required reuse conditions are missing from the statement."
    elif failure_class == "reuse_condition_mismatch":
        for item in fixture["conditions"]:
            if item["type"] == "onward_transfer":
                item["value"] = "permitted"
        description = "Declared reuse condition contradicts the policy-required transfer boundary."
    elif failure_class == "handoff_ref_unresolved":
        fixture["provenance"]["handoff_refs"] = ["synthetic-handoff-missing"]
        description = "Handoff reference is not backed by a packaged evidence object."
    elif failure_class == "review_trigger_missing":
        fixture["policy"]["review_triggers"] = []
        description = "Review decision lacks the policy trigger that initiated review."
    elif failure_class == "review_evidence_missing":
        fixture["evidence"]["evidence_objects"] = [
            item for item in fixture["evidence"]["evidence_objects"] if item["type"] != "review_record"
        ]
        fixture["evidence"]["evidence_ids"] = [
            item for item in fixture["evidence"]["evidence_ids"] if "review" not in item
        ]
        description = "Review evidence is absent from the packaged statement."
    elif failure_class == "policy_version_mismatch":
        fixture["operation"]["policy_version"] = "2026.0"
        description = "Operation policy version differs from the packaged policy version."
    elif failure_class == "integrity_digest_mismatch":
        fixture["provenance"]["integrity_digest"] = digest("mismatched-integrity-value")
        description = "Provenance integrity digest differs from the packaged evidence digest."
    else:
        raise ValueError(f"unknown failure class: {failure_class}")

    fixture["intentional_defect"] = {
        "failure_class": failure_class,
        "defect_description": description,
        "expected_detection_surface": surface,
    }
    fixture["fixture_metadata"]["primary_purpose"] = "negative_control"


def apply_edge(fixture, edge_reason):
    fixture["edge_case_reason"] = edge_reason
    fixture["fixture_metadata"]["fixture_family"] = "edge"
    fixture["fixture_metadata"]["primary_purpose"] = "edge_case"
    if "denied" in edge_reason:
        fixture["decision"]["outcome"] = "deny"
        fixture["decision"]["rationale"] = "Synthetic denial with complete policy and evidence linkage."
    if "closed_without_renewal" in edge_reason:
        fixture["decision"]["outcome"] = "closed_without_renewal"
        fixture["decision"]["rationale"] = "Synthetic review closure with complete evidence and no renewal condition."


def fixture_path(output_root, fixture):
    fixture_id = fixture["fixture_id"]
    family = fixture["fixture_metadata"]["fixture_family"]
    operation_family = fixture["fixture_metadata"]["operation_family"]
    short = OPERATION_CONFIG[operation_family]["short"]
    if family == "valid":
        return output_root / "valid" / short / f"{fixture_id}.json"
    if family == "invalid":
        return output_root / "invalid" / short / f"{fixture_id}.json"
    return output_root / "edge" / f"{fixture_id}.json"


def build_fixtures():
    fixtures = []
    for operation_family in ["access_decision", "reuse_authorization", "review_decision"]:
        short = OPERATION_CONFIG[operation_family]["short"]
        for index in range(1, 7):
            fixture_id = f"valid_{operation_family}_{index:03d}"
            fixtures.append(base_fixture(fixture_id, operation_family, "valid", index, "valid"))

    counters = {family: 1 for _, family, _ in FAILURE_CLASSES}
    for failure_class, operation_family, surface in FAILURE_CLASSES:
        short = OPERATION_CONFIG[operation_family]["short"]
        for index in range(1, 3):
            ordinal = counters[operation_family]
            fixture_id = f"invalid_{short}_{failure_class}_{index:03d}"
            fixture = base_fixture(fixture_id, operation_family, "invalid", ordinal, "invalid", failure_class)
            apply_defect(fixture, failure_class, surface)
            fixtures.append(fixture)
            counters[operation_family] += 1

    edge_specs = [
        ("edge_access_denied_with_complete_evidence_001", "access_decision", "denied_but_valid_complete_evidence"),
        ("edge_reuse_denied_due_to_scope_001", "reuse_authorization", "denied_but_valid_scope_boundary"),
        ("edge_review_closed_without_renewal_001", "review_decision", "closed_without_renewal_but_valid"),
    ]
    for index, (fixture_id, operation_family, reason) in enumerate(edge_specs, start=1):
        fixture = base_fixture(fixture_id, operation_family, "edge", index, "valid")
        apply_edge(fixture, reason)
        fixtures.append(fixture)
    return fixtures


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_readme(output_root):
    text = """# PD-OAP v2.0 Controlled Fixture Benchmark

This directory contains the generated v2.0 controlled fixture benchmark.

- Total fixtures: 45
- Valid fixtures: 18
- Invalid fixtures: 24
- Edge fixtures: 3
- Operation families: access_decision, reuse_authorization, review_decision
- Failure classes: 12, with exactly two invalid fixtures per class

The fixtures are synthetic, controlled, and bounded. They are not a population-scale empirical benchmark and do not claim legal sufficiency, production deployment, or real public-sector approval.
"""
    (output_root / "README.md").write_text(text, encoding="utf-8")


def build_manifest(output_root, fixtures):
    operation_counts = {"access_decision": 0, "reuse_authorization": 0, "review_decision": 0}
    failure_counts = {failure_class: 0 for failure_class, _, _ in FAILURE_CLASSES}
    records = []
    valid_count = invalid_count = edge_count = 0

    for fixture in fixtures:
        family = fixture["fixture_metadata"]["fixture_family"]
        operation_family = fixture["fixture_metadata"]["operation_family"]
        operation_counts[operation_family] += 1
        if family == "valid":
            valid_count += 1
        elif family == "invalid":
            invalid_count += 1
            failure_counts[fixture["validation"]["expected_failure_class"]] += 1
        elif family == "edge":
            edge_count += 1
        path = fixture_path(output_root, fixture).relative_to(output_root).as_posix()
        records.append({
            "fixture_id": fixture["fixture_id"],
            "path": path,
            "fixture_family": family,
            "operation_family": operation_family,
            "expected_result": fixture["validation"]["expected_result"],
            "expected_failure_class": fixture["validation"]["expected_failure_class"],
        })

    return {
        "benchmark_id": "pd-oap-controlled-fixture-benchmark@2.0-draft",
        "fixture_count": len(fixtures),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "edge_count": edge_count,
        "operation_family_counts": operation_counts,
        "failure_class_counts": failure_counts,
        "non_claims": NON_CLAIMS,
        "fixtures": sorted(records, key=lambda item: item["fixture_id"]),
    }


def build_expected_results(fixtures):
    return {
        "expected_results_id": "pd-oap-v2-expected-results@2.0-draft",
        "results": sorted(
            [
                {
                    "fixture_id": fixture["fixture_id"],
                    "fixture_family": fixture["fixture_metadata"]["fixture_family"],
                    "operation_family": fixture["fixture_metadata"]["operation_family"],
                    "expected_result": fixture["validation"]["expected_result"],
                    "expected_primary_failure_code": fixture["validation"]["expected_primary_failure_code"],
                    "expected_failure_class": fixture["validation"]["expected_failure_class"],
                }
                for fixture in fixtures
            ],
            key=lambda item: item["fixture_id"],
        ),
    }


def write_expected_results_md(output_root, expected_results):
    lines = [
        "# v2.0 Expected Results",
        "",
        "| Fixture | Family | Operation family | Expected result | Expected primary failure code |",
        "|---|---|---|---|---|",
    ]
    for item in expected_results["results"]:
        lines.append(
            f"| {item['fixture_id']} | {item['fixture_family']} | {item['operation_family']} | "
            f"{item['expected_result']} | {item['expected_primary_failure_code']} |"
        )
    (output_root / "expected_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_generated_json(output_root):
    for dirname in ["valid", "invalid", "edge"]:
        directory = output_root / dirname
        if directory.exists():
            for path in directory.rglob("*.json"):
                path.unlink()


def generate(output_root):
    output_root.mkdir(parents=True, exist_ok=True)
    clean_generated_json(output_root)
    fixtures = build_fixtures()
    for fixture in fixtures:
        write_json(fixture_path(output_root, fixture), fixture)

    manifest = build_manifest(output_root, fixtures)
    expected_results = build_expected_results(fixtures)
    write_json(output_root / "manifest.json", manifest)
    write_json(output_root / "expected_results.json", expected_results)
    write_expected_results_md(output_root, expected_results)
    write_readme(output_root)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args(argv)

    output_root = Path(args.output_root)
    try:
        generate(output_root)
    except Exception as exc:
        print(f"failed to generate fixtures: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
