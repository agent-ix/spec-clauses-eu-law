"""Acceptance tests for the EU GMP Annex 11 clause set."""

from __future__ import annotations

import copy
import json
import pathlib
import re
import shutil
import subprocess

import pytest
import yaml
from annex11_spec import (
    applicability_dimensions,
    binding_rows,
    clause_rows,
    crosswalk_rows,
    expected_metadata,
    limited_shared_outputs,
    official_url,
    risk_scaled_clauses,
    set_key,
    set_path,
    title_rows,
    tool_limit_sentences,
)
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    assert_crosswalk_targets_resolve,
    assert_output_catalog_consistent,
    assert_shared_producers_identical,
    clause_set_key,
    engine_tool,
    evaluate_clause_set,
    load_clause_sets,
    run,
)
from test_clause_sets import _installed_clause_sets, _spec_output_catalog

SET_KEY = set_key()
SET_PATH = set_path()
OFFICIAL_URL = official_url()
CORPUS_ROOT = PACKAGE_ROOT.parent / "tests" / "corpus"
AS_OF = "2026-11-15T00:00:00Z"
GMP = "gmp_regulated_use=yes"
CUSTOMER_SUPPLIED_KINDS = {
    "system-validation": "record",
    "access-control": "record",
    "system-access-control": "record",
    "written-procedure": "procedure",
    "training-record": "procedure",
    "supplier-agreement": "procedure",
    "supplier-assessment": "procedure",
    "system-inventory": "procedure",
    "backup-restore-record": "procedure",
    "periodic-evaluation-record": "procedure",
    "business-continuity-plan": "procedure",
    "archive-verification-record": "procedure",
    "batch-certification-record": "procedure",
}


def _annex() -> dict:
    return next(item for item in load_clause_sets() if clause_set_key(item) == SET_KEY)


def _all_yes_context() -> list[str]:
    return [GMP, *(f"{name}=yes" for name in applicability_dimensions())]


def _outcomes(context: list[str]) -> dict[str, str]:
    binding = evaluate_clause_set(PACKAGE_ROOT, SET_KEY, *context)
    return {item["clauseId"]: item["outcome"] for item in binding["clauses"]}


def _assert_clause_table(clause_set: dict) -> None:
    """Compare ids, force, text, outputs and dimensions with the spec table."""
    rows = clause_rows()
    clauses = clause_set["clauses"]
    assert [c["id"] for c in clauses] == [r["id"] for r in rows]
    for clause, row in zip(clauses, rows, strict=True):
        cid = clause["id"]
        assert clause["force"] == "recommended", f"{cid} force"
        assert clause["text"].strip(), f"{cid} text"
        assert clause["expectedOutputs"] == row["outputs"], f"{cid} outputs"
        terms = [{"op": "eq", "dimension": "gmp_regulated_use", "value": "yes"}]
        if row["dimension"]:
            terms.append({"op": "eq", "dimension": row["dimension"], "value": "yes"})
        expected = terms[0] if len(terms) == 1 else {"op": "all", "terms": terms}
        assert clause["applicability"] == expected, f"{cid} applicability"


def _expected_clause_text(row: dict) -> str:
    """Summary followed by each distinct tool-limit sentence its outputs need."""
    sentences = tool_limit_sentences()
    limited = limited_shared_outputs()
    tail: list[str] = []
    for output in row["outputs"]:
        if output in limited and sentences[output] not in tail:
            tail.append(sentences[output])
    return " ".join([row["summary"].rstrip(".") + ".", *tail])


def _assert_tool_limits(clause_set: dict) -> None:
    """Every clause text is its summary then exactly its tool-limit sentences."""
    rows = {row["id"]: row for row in clause_rows()}
    for clause in clause_set["clauses"]:
        assert clause["text"] == _expected_clause_text(
            rows[clause["id"]]
        ), f"clause {clause['id']} text differs from its summary and tool limits"


def _assert_titles_and_subjects(clause_set: dict) -> None:
    """Compare every clause title and subject list with the spec table."""
    titles = title_rows()
    assert set(titles) == {c["id"] for c in clause_set["clauses"]}
    for clause in clause_set["clauses"]:
        title, subjects = titles[clause["id"]]
        assert clause["title"] == title, f"{clause['id']} title"
        assert clause["subjects"] == subjects, f"{clause['id']} subjects"


def _assert_commands_exist(rows: list[dict]) -> None:
    """Every command in the producer-command column answers --help."""
    for row in rows:
        for command in row["commands"]:
            words = command.split()
            result = run(engine_tool(words[0]), *words[1:], "--help")
            assert (
                result.returncode == 0
            ), f"command `{command}` for {row['outputs']} is unavailable"


def _write_module(tmp_path: pathlib.Path, clause_set: dict) -> pathlib.Path:
    module = tmp_path / "module"
    (module / "clauses").mkdir(parents=True)
    (module / "clauses" / "annex.json").write_text(json.dumps(clause_set))
    (module / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "manifest_version": "1.0.0",
                "name": "annex11-fixture",
                "version": "0.0.1",
                "clause_sets": ["clauses/annex.json"],
            }
        )
    )
    return module


@pytest.mark.trace("FR-001-AC-1", "FR-023-AC-1")
def test_manifest_declares_the_annex_11_set_once():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"].count(SET_PATH) == 1
    assert [clause_set_key(item) for item in load_clause_sets()].count(SET_KEY) == 1


@pytest.mark.trace("FR-023-AC-2", "FR-026-AC-4")
def test_annex_11_module_passes_publish_check():
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("FR-023-AC-3", "NFR-004-AC-1")
def test_annex_11_source_and_rights_match_the_spec_by_field():
    clause_set = _annex()
    expected = expected_metadata()[SET_KEY]
    assert (
        clause_set["source"]["officialUrl"] == expected["officialUrl"] == OFFICIAL_URL
    )
    for field, value in expected["rights"].items():
        assert clause_set["rights"][field] == value, f"rights.{field}"
    assert clause_set["rights"]["licence"] == expected["licence"]
    assert clause_set["rights"]["attribution"] == expected["attribution"]
    assert "no licence statement of its own" in clause_set["rights"]["licence"]
    assert (clause_set["authority"], clause_set["id"], clause_set["version"]) == (
        "eu",
        "eu-gmp-annex-11",
        "2011-01",
    )


@pytest.mark.trace("FR-023-AC-4")
def test_annex_11_set_does_not_cite_the_2025_draft():
    text = json.dumps(_annex()).casefold()
    assert "draft" not in text
    assert "2025" not in text


@pytest.mark.trace("FR-024-AC-1", "FR-024-AC-2")
def test_annex_11_clause_table_matches_the_spec():
    clause_set = _annex()
    _assert_clause_table(clause_set)
    catalog = clause_set["outputCatalog"]
    assert all(
        output in catalog
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    )
    broken = copy.deepcopy(clause_set)
    broken["clauses"][4]["expectedOutputs"] = ["software-architecture"]
    with pytest.raises(AssertionError, match=r"\b4\.1\b|\b4\.4\b|outputs"):
        _assert_clause_table(broken)
    broken = copy.deepcopy(clause_set)
    broken["clauses"].pop()
    with pytest.raises(AssertionError):
        _assert_clause_table(broken)


@pytest.mark.trace("FR-024-AC-3")
def test_gmp_regulated_use_gates_every_clause():
    ids = [row["id"] for row in clause_rows()]
    assert set(_outcomes([])) == set(ids)
    assert set(_outcomes([]).values()) == {"unresolved"}
    assert set(_outcomes(["gmp_regulated_use=no"]).values()) == {"not_binding"}
    plain = {row["id"] for row in clause_rows() if row["dimension"] is None}
    bound = {cid for cid, outcome in _outcomes([GMP]).items() if outcome == "binding"}
    assert bound == plain


@pytest.mark.trace("FR-024-AC-4")
def test_each_second_dimension_gates_its_clauses():
    for dimension in applicability_dimensions():
        gated = {row["id"] for row in clause_rows() if row["dimension"] == dimension}
        assert gated
        yes = _outcomes([GMP, f"{dimension}=yes"])
        no = _outcomes([GMP, f"{dimension}=no"])
        unset = _outcomes([GMP])
        for cid in gated:
            assert yes[cid] == "binding", f"{cid} with {dimension}=yes"
            assert no[cid] == "not_binding", f"{cid} with {dimension}=no"
            assert unset[cid] == "unresolved", f"{cid} with {dimension} unset"


@pytest.mark.trace("FR-024-AC-6")
def test_titles_subjects_and_text_follow_the_spec():
    clause_set = _annex()
    _assert_titles_and_subjects(clause_set)
    _assert_tool_limits(clause_set)
    broken = copy.deepcopy(clause_set)
    broken["clauses"][0]["title"] = "changed"
    with pytest.raises(AssertionError, match="title"):
        _assert_titles_and_subjects(broken)
    broken = copy.deepcopy(clause_set)
    broken["clauses"][0]["subjects"] = ["changed"]
    with pytest.raises(AssertionError, match="subjects"):
        _assert_titles_and_subjects(broken)


@pytest.mark.trace("FR-024-AC-5")
def test_no_criticality_or_risk_class_dimension_exists():
    dimensions = set(_annex()["classificationDimensions"])
    assert dimensions == {"gmp_regulated_use", *applicability_dimensions()}
    for name in dimensions:
        assert not re.search(r"criticality|risk_class|risk_level|score", name)
    for dimension in dimensions:
        assert _annex()["classificationDimensions"][dimension] == {
            "values": ["yes", "no"]
        }


@pytest.mark.trace("FR-025-AC-1")
def test_annex_11_catalog_subset_equals_the_spec_catalog():
    clause_set = _annex()
    used = {o for c in clause_set["clauses"] for o in c["expectedOutputs"]}
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}


@pytest.mark.trace("FR-025-AC-2")
def test_shared_outputs_equal_the_us_health_law_catalog():
    us_sets = _installed_clause_sets("spec_clauses_us_health")
    us_catalog = {
        name: definition
        for item in us_sets
        for name, definition in item["outputCatalog"].items()
    }
    shared = set(_annex()["outputCatalog"]) & set(us_catalog)
    assert {
        "verification-records",
        "risk-management-records",
        "software-requirements",
        "software-architecture",
        "anomaly-list",
        "soup-list",
    } <= shared
    for name in shared:
        assert _annex()["outputCatalog"][name] == us_catalog[name], name
    assert_output_catalog_consistent([*load_clause_sets(), *us_sets])
    assert_shared_producers_identical([*load_clause_sets(), *us_sets])
    drifted = copy.deepcopy(_annex())
    drifted["outputCatalog"]["verification-records"]["description"] = "changed"
    with pytest.raises(AssertionError, match="verification-records"):
        assert_output_catalog_consistent([drifted, *us_sets])


@pytest.mark.trace("FR-025-AC-3")
def test_customer_supplied_outputs_name_no_producer():
    catalog = _annex()["outputCatalog"]
    rows = {
        name: row
        for row in binding_rows()
        if row["source"] == "Customer-supplied"
        for name in row["outputs"]
    }
    assert set(rows) == set(CUSTOMER_SUPPLIED_KINDS)
    assert all(not row["commands"] for row in rows.values())
    for name, kind in CUSTOMER_SUPPLIED_KINDS.items():
        assert catalog[name]["kind"] == kind, name
        assert rows[name]["source"] == "Customer-supplied", name
        assert not re.search(
            r"produced by `(quoin|quire|engineering-assurance)",
            catalog[name]["description"],
        ), name


@pytest.mark.trace("FR-025-AC-7")
def test_system_access_clauses_name_system_not_repository_access():
    by_id = {c["id"]: c["expectedOutputs"] for c in _annex()["clauses"]}
    for cid in ("12.1", "12.2"):
        assert "system-access-control" in by_id[cid], cid
        assert "access-control" not in by_id[cid], cid
    for cid in ("7.1", "12.3"):
        assert "access-control" in by_id[cid], cid
    description = _annex()["outputCatalog"]["system-access-control"]["description"]
    assert "repository" not in description


@pytest.mark.trace("FR-025-AC-4")
def test_every_named_producer_command_exists():
    rows = binding_rows()
    assert any(row["commands"] for row in rows)
    _assert_commands_exist(rows)
    with pytest.raises(AssertionError, match="software-requirements"):
        _assert_commands_exist(
            [
                {
                    "outputs": ["software-requirements"],
                    "commands": ["quire no-such-command"],
                }
            ]
        )


@pytest.mark.trace("FR-025-AC-6")
def test_tool_limits_reach_the_shipped_pack():
    clause_set = _annex()
    _assert_tool_limits(clause_set)
    assert set(tool_limit_sentences()) == limited_shared_outputs()
    assert limited_shared_outputs() >= {
        "audit-trail",
        "signed-record",
        "signer-registry",
    }
    sentences = tool_limit_sentences()
    broken = copy.deepcopy(clause_set)
    clause = next(c for c in broken["clauses"] if c["id"] == "14(c)")
    clause["text"] = clause["text"].replace(sentences["signed-record"], "")
    with pytest.raises(AssertionError, match=r"clause 14\(c\)"):
        _assert_tool_limits(broken)
    duplicated = copy.deepcopy(clause_set)
    clause = next(c for c in duplicated["clauses"] if c["id"] == "14(c)")
    clause["text"] += " " + sentences["signed-record"]
    with pytest.raises(AssertionError, match=r"clause 14\(c\)"):
        _assert_tool_limits(duplicated)
    moved = copy.deepcopy(clause_set)
    clause = next(c for c in moved["clauses"] if c["id"] == "14(c)")
    clause["text"] = sentences["signed-record"] + " " + clause_rows()[-4]["summary"]
    with pytest.raises(AssertionError, match=r"clause 14\(c\)"):
        _assert_tool_limits(moved)
    catalog = clause_set["outputCatalog"]
    for name, phrase in {
        "change-assurance-record": "does not establish authorisation",
        "baseline-record": "a person decides its contents",
        "record-export": "does not show a record's change history",
    }.items():
        assert phrase in catalog[name]["description"], name
    for name, kind in CUSTOMER_SUPPLIED_KINDS.items():
        if kind == "procedure" and name not in {"written-procedure", "training-record"}:
            assert "no quoin, quire or engineering-assurance command" in (
                catalog[name]["description"]
            ), name


@pytest.mark.trace("FR-026-AC-1", "FR-026-AC-3")
def test_part_11_crosswalks_match_the_policy():
    crosswalks = _annex()["crosswalks"]
    found = {
        (c["sourceClause"], c["target"]["clause"], c["relation"]) for c in crosswalks
    }
    assert found == crosswalk_rows()
    assert len(found) == len(crosswalks)
    for crosswalk in crosswalks:
        assert crosswalk["target"]["set"] == {
            "authority": "us-fda",
            "id": "21-cfr-11",
            "version": "2026-11-12",
        }
        assert crosswalk["relation"] in {"partial", "informative"}
        assert crosswalk["rationale"].strip()


@pytest.mark.trace("FR-026-AC-2")
def test_part_11_crosswalk_targets_resolve_and_a_missing_one_fails():
    clause_set = _annex()
    assert_crosswalk_targets_resolve([clause_set])
    broken = copy.deepcopy(clause_set)
    broken["crosswalks"][0]["target"]["clause"] = "11.999"
    with pytest.raises(AssertionError, match=r"11\.999"):
        assert_crosswalk_targets_resolve([broken])
    absent = copy.deepcopy(clause_set)
    absent["crosswalks"][0]["target"]["set"]["version"] = "1900-01-01"
    with pytest.raises(AssertionError, match="1900-01-01"):
        assert_crosswalk_targets_resolve([absent])


@pytest.mark.trace("NFR-004-AC-2")
def test_annex_11_text_passes_the_content_rights_scan(tmp_path):
    executable = shutil.which("engineering-assurance")
    assert executable is not None, "engineering-assurance CLI is unavailable"
    clause_set = _annex()
    (tmp_path / "text.json").write_text(
        json.dumps(
            {
                "clauses": [
                    {"id": c["id"], "title": c["title"], "text": c["text"]}
                    for c in clause_set["clauses"]
                ],
                "rationales": [x["rationale"] for x in clause_set["crosswalks"]],
                "catalog": clause_set["outputCatalog"],
            }
        )
    )
    assert run("git", "init", "--quiet", "-b", "main", cwd=tmp_path).returncode == 0
    assert run("git", "add", "--all", cwd=tmp_path).returncode == 0
    scanned = run(
        executable, "content-rights-tree", "--root", str(tmp_path), cwd=tmp_path
    )
    assert scanned.returncode == 0, scanned.stderr + scanned.stdout
    report = json.loads(scanned.stdout)
    assert report["outcome"] == "accepted" and report["findings"] == []


# ---------------------------------------------------------------------------
# Reference-corpus discharge (FR-027, FR-028)

EVIDENCE_FOR_OUTPUT = {
    "risk-management-records": "safety/RISK-001.md",
    "security-risk-records": "security/RISK-002.md",
    "software-requirements": "requirements/FR-001.md",
    "written-procedure": "requirements/FR-001.md",
    "training-record": "requirements/NFR-001.md",
    "software-architecture": "architecture/evidence_store.md",
    "data-flow-model": "gdpr/data-flow-model.json",
    "verification-records": "tests/TM-001.md",
    "system-validation": "tests/TM-001.md",
    "access-control": "security/CTRL-001.md",
    "system-access-control": "security/system-access-control.json",
    "soup-list": "security/SOUP-001.md",
    "anomaly-list": "safety/HAZ-001.md",
}
DEFAULT_EVIDENCE = "evidence/index.json"
APPROVER = "person://example.invalid/people/system-owner"
ATTESTATION = {
    "attestedBy": "reviewer@example.invalid",
    "authority": "quality-lead@example.invalid",
    "attestedAt": AS_OF,
    "expiresAt": "2027-11-15T00:00:00Z",
}


def _owned(clause_set: dict) -> set[str]:
    procedures = {
        name
        for name, output in clause_set["outputCatalog"].items()
        if output["kind"] == "procedure"
    }
    return {
        c["id"]
        for c in clause_set["clauses"]
        if set(c["expectedOutputs"]) <= procedures
    }


def _fact(clause: dict, owned: set[str], *, approver: bool) -> dict:
    cid = clause["id"]
    if cid in owned:
        return {
            "kind": "disposition",
            "clauseId": cid,
            "decision": "delegated",
            "owner": "person://example.invalid/people/customer-owner",
            "rationale": "Customer procedure kept in the synthetic project.",
            "approvalRef": "person://example.invalid/approvals/customer-owner",
            "attestation": ATTESTATION,
        }
    refs = sorted(
        {
            f"evidence://example.invalid/{EVIDENCE_FOR_OUTPUT.get(o, DEFAULT_EVIDENCE)}"
            for o in clause["expectedOutputs"]
        }
    )
    fact = {
        "kind": "direct",
        "clauseId": cid,
        "evidenceRefs": refs,
        "attestation": dict(ATTESTATION),
    }
    if approver:
        fact["approvalRef"] = APPROVER
        fact["attestation"]["attestedBy"] = APPROVER
    return fact


def _discharge(
    tmp_path: pathlib.Path, context: list[str], facts: list[dict]
) -> tuple[dict, dict, subprocess.CompletedProcess]:
    """Record facts in a temporary store and render the pack RMM as JSON."""
    quire, quoin = engine_tool("quire"), engine_tool("quoin")
    config = tmp_path / "config"
    config.mkdir(exist_ok=True)
    installed = run(
        quoin, "module", "install", f"path:{PACKAGE_ROOT}", "--config-root", str(config)
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    evaluated = run(
        quire,
        "clauses",
        "evaluate",
        "--module",
        str(PACKAGE_ROOT),
        "--authority",
        "eu",
        "--set",
        "eu-gmp-annex-11",
        "--version",
        "2011-01",
        *[a for value in context for a in ("--context", value)],
        "--json",
    )
    assert evaluated.returncode == 0, evaluated.stderr + evaluated.stdout
    binding = json.loads(evaluated.stdout)
    (tmp_path / "binding.json").write_text(json.dumps(binding))
    (tmp_path / "facts.json").write_text(json.dumps(facts))
    recorded = run(
        quoin,
        "evidence",
        "record-discharge",
        "--repo",
        str(tmp_path / "store"),
        "--binding",
        str(tmp_path / "binding.json"),
        "--facts",
        str(tmp_path / "facts.json"),
        "--json",
        "--config-root",
        str(config),
    )
    if recorded.returncode != 0:
        return binding, {}, recorded
    report = run(
        quoin,
        "discharge",
        "--rmm",
        "--pack",
        "spec_clauses_eu_law",
        "--repo",
        str(tmp_path / "store"),
        "--config-root",
        str(config),
        "--as-of",
        AS_OF,
        *[a for value in context for a in ("--context", value)],
        "--json",
    )
    assert report.returncode == 0, report.stderr + report.stdout
    return binding, json.loads(report.stdout), recorded


def _rows(report: dict) -> dict[str, dict]:
    """Return the Annex 11 matrix rows keyed by clause id."""
    found: dict[str, list[dict]] = {}

    def walk(value: object) -> None:
        if isinstance(value, dict):
            if "clauseId" in value and "compliance" in value:
                found.setdefault(value["clauseId"], []).append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for matrix in report["matrices"]:
        if "eu-gmp-annex-11" in json.dumps(matrix.get("clauseSet", matrix))[:400]:
            walk(matrix)
    assert all(len(rows) == 1 for rows in found.values()), "a clause row repeats"
    return {cid: rows[0] for cid, rows in found.items()}


@pytest.mark.trace(
    "FR-007-AC-2", "FR-027-AC-1", "FR-027-AC-2", "FR-027-AC-4", "FR-027-AC-5"
)
def test_corpus_discharge_partitions_every_clause_without_a_verdict(tmp_path):
    from test_pack_discharge import _assert_fact_refs_resolve

    clause_set = _annex()
    owned = _owned(clause_set)
    risk = risk_scaled_clauses()
    facts = [
        _fact(clause, owned, approver=clause["id"] in risk)
        for clause in clause_set["clauses"]
    ]
    _assert_fact_refs_resolve(CORPUS_ROOT, facts)
    binding, report, recorded = _discharge(tmp_path, _all_yes_context(), facts)
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    assert {c["outcome"] for c in binding["clauses"]} == {"binding"}
    rows = _rows(report)
    assert set(rows) == {c["id"] for c in clause_set["clauses"]}
    for cid, row in rows.items():
        expected = "tailored" if cid in owned else "compliant"
        assert row["compliance"] == expected, f"{cid}: {row}"
    text = json.dumps(report).casefold()
    assert not re.search(r'"[a-z_]*(score|percent|overall)[a-z_]*"', text)
    assert "overall" not in text and "%" not in text


@pytest.mark.trace("FR-027-AC-3")
def test_not_binding_and_unresolved_clauses_are_not_counted_as_discharged(tmp_path):
    clause_set = _annex()
    owned = _owned(clause_set)
    supplier_clauses = {
        row["id"] for row in clause_rows() if row["dimension"] == "third_party_supplier"
    }
    binding_facts = [
        _fact(c, owned, approver=c["id"] in risk_scaled_clauses())
        for c in clause_set["clauses"]
        if c["id"] not in supplier_clauses
        and not next(r for r in clause_rows() if r["id"] == c["id"])["dimension"]
    ]
    (tmp_path / "no").mkdir()
    _, report, recorded = _discharge(
        tmp_path / "no", [GMP, "third_party_supplier=no"], binding_facts
    )
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    rows = _rows(report)
    for cid in supplier_clauses:
        assert rows[cid]["compliance"] not in {"compliant", "tailored"}, cid
        assert rows[cid]["applicability"] != "applicable", cid
    (tmp_path / "unset").mkdir()
    _, report, recorded = _discharge(tmp_path / "unset", [GMP], binding_facts)
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    rows = _rows(report)
    for cid in supplier_clauses:
        assert rows[cid]["applicability"] == "unresolved", cid
        assert rows[cid]["compliance"] not in {"compliant", "tailored"}, cid


@pytest.mark.trace("FR-028-AC-1")
def test_risk_scaled_clauses_declare_the_system_owner_role():
    clause_set = _annex()
    risk = risk_scaled_clauses()
    assert risk == {"1", "3.2", "4.1", "4.3", "4.4", "6", "9", "12.2", "13", "16"}
    roles = {c["id"]: c["approvalRoles"] for c in clause_set["clauses"]}
    assert {cid for cid, value in roles.items() if value} == risk
    assert all(roles[cid] == ["system-owner"] for cid in risk)


@pytest.mark.trace("FR-028-AC-1", "FR-028-AC-2")
@pytest.mark.parametrize("case", ["missing", "empty", "blank"])
def test_risk_scaled_clauses_stay_undischarged_without_an_approval_ref(tmp_path, case):
    clause_set = _annex()
    owned = _owned(clause_set)
    direct_risk = sorted(risk_scaled_clauses() - owned)
    clauses = {c["id"]: c for c in clause_set["clauses"] if c["id"] in direct_risk}
    facts = [_fact(clauses[cid], owned, approver=False) for cid in direct_risk]
    if case != "missing":
        for fact in facts:
            fact["approvalRef"] = "" if case == "empty" else "   "
    _, report, recorded = _discharge(tmp_path, _all_yes_context(), facts)
    if recorded.returncode != 0:
        assert "approvalRef" in recorded.stderr + recorded.stdout
        return
    rows = _rows(report)
    for cid in direct_risk:
        assert rows[cid]["compliance"] == "undischarged", cid
        assert "approval" in rows[cid]["reason"], rows[cid]
        assert "tailoringDescription" not in rows[cid], cid


@pytest.mark.trace("FR-028-AC-1")
def test_risk_scaled_clauses_discharge_with_an_approval_ref(tmp_path):
    clause_set = _annex()
    owned = _owned(clause_set)
    direct_risk = sorted(risk_scaled_clauses() - owned)
    clauses = {c["id"]: c for c in clause_set["clauses"] if c["id"] in direct_risk}
    facts = [_fact(clauses[cid], owned, approver=True) for cid in direct_risk]
    _, report, recorded = _discharge(tmp_path, _all_yes_context(), facts)
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    rows = _rows(report)
    for cid in direct_risk:
        assert rows[cid]["compliance"] == "compliant", cid


@pytest.mark.trace("FR-028-AC-3")
def test_evaluation_generates_no_approval_or_decision(tmp_path):
    binding, report, recorded = _discharge(tmp_path, _all_yes_context(), [])
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    assert "approvalRef" not in json.dumps(binding)
    rows = _rows(report)
    for cid in risk_scaled_clauses():
        assert rows[cid]["compliance"] == "undischarged", cid
        assert "approvalRef" not in rows[cid] and "evidenceRefs" in rows[cid]
        assert rows[cid]["evidenceRefs"] == []
