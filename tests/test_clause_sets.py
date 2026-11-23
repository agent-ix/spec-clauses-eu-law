"""Packaging and shared behavior for the EU law clause module."""

from __future__ import annotations

import copy
import json
import os
import pathlib
import re
import shutil
import tarfile
import tempfile
import zipfile

import pytest
import yaml
from annex11_spec import expected_metadata as annex11_expected_metadata
from annex11_spec import set_path as annex11_set_path
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    assert_crosswalk_targets_resolve,
    assert_output_catalog_consistent,
    clause_set_key,
    engine_tool,
    evaluate_clause_set,
    load_clause_sets,
    record_and_render_matrix,
    run,
    stage_clause_sets,
)


def _spec_mdr_ids() -> list[str]:
    """Read normative MDR IDs from the master specification table."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## MDR Clause Table", 1)[1].split("\n## ", 1)[0]
    return [
        row.split("|", 2)[1].strip()
        for row in section.splitlines()
        if row.startswith("|")
        and not row.startswith("| Clause ID")
        and not row.startswith("|---")
    ]


def _spec_mdr_rows() -> list[dict]:
    """Read normative MDR IDs and expected outputs from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## MDR Clause Table", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| Clause ID")
            or line.startswith("|---")
        ):
            continue
        clause_id, _applicability, outputs = [
            cell.strip() for cell in line.strip("|").split("|", 2)
        ]
        rows.append(
            {"id": clause_id, "outputs": [item.strip() for item in outputs.split(",")]}
        )
    return rows


def _spec_gdpr_rows() -> list[dict[str, str]]:
    """Read normative GDPR IDs, applicability, and outputs from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## GDPR Clause Table", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| Clause ID")
            or line.startswith("|---")
        ):
            continue
        clause_id, applicability, outputs = [
            cell.strip().replace("`", "") for cell in line.strip("|").split("|", 2)
        ]
        rows.append(
            {"id": clause_id, "applicability": applicability, "outputs": outputs}
        )
    return rows


def _spec_ai_act_rows() -> list[dict[str, str]]:
    """Read normative AI Act IDs, applicability, and outputs from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## AI Act High-Risk Obligations Table", 1)[1].split(
        "\n## ", 1
    )[0]
    rows = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| Clause ID")
            or line.startswith("|---")
        ):
            continue
        clause_id, _coverage, applicability, force, outputs = [
            cell.strip().replace("`", "") for cell in line.strip("|").split("|", 4)
        ]
        rows.append(
            {
                "id": clause_id,
                "applicability": applicability,
                "force": force,
                "outputs": outputs,
            }
        )
    return rows


def _spec_ai_act_annex_rows() -> list[dict[str, str]]:
    """Read normative Annex IV IDs, applicability, and outputs from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## AI Act Annex IV Table", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| Clause ID")
            or line.startswith("|---")
        ):
            continue
        cells = [cell.strip().replace("`", "") for cell in line.strip("|").split("|")]
        if len(cells) != 8:
            continue
        (
            clause_id,
            _element,
            _condition,
            applicability,
            outputs,
            target,
            relation,
            rationale,
        ) = cells
        rows.append(
            {
                "id": clause_id,
                "applicability": applicability,
                "outputs": outputs,
                "target": target,
                "relation": relation,
                "rationale": rationale,
            }
        )
    return rows


def _ai_act_annex_dimension(clause_id: str) -> str:
    """Return the point-applicability dimension for one Annex IV clause."""
    point_id = clause_id[3:].replace("(", "_").replace(")", "").replace(".", "_")
    return f"ai_annex_iv_{point_id}_applicable"


def _parsed_spec_sets() -> dict[str, dict[str, object]]:
    """Parse canonical identities and rights metadata from spec.md once."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    design = specification.split("## Set Design", 1)[1].split("\n## ", 1)[0]
    mdr = re.search(
        r"MDR identity is authority `([^`]+)`, ID `([^`]+)`, and version `([^`]+)`.*?"
        r"official URL is `(https://[^`]+)`.*?"
        r"Licence metadata shall say: `([^`]+)` "
        r"Attribution metadata shall say `([^`]+)`",
        design,
        re.DOTALL,
    )
    assert (
        mdr
    ), "spec.md must declare the MDR identity, source, licence, and attribution"
    mdcg = re.search(
        r"MDCG identity is authority `([^`]+)`, ID `([^`]+)`, "
        r"version `([^`]+)`, with source `([^`]+)` and listing `([^`]+)`.*?"
        r"Licence metadata SHALL state that (.+?)\. "
        r"Attribution SHALL say `(.+?)` The guidance is non-binding",
        design,
        re.DOTALL,
    )
    assert (
        mdcg
    ), "spec.md must declare the MDCG identity, source, licence, and attribution"
    gdpr = re.search(
        r"GDPR identity is authority `([^`]+)`, ID `([^`]+)`, and version `([^`]+)`.*?"
        r"official URL is `(https://[^`]+)`.*?legal notice is `(https://[^`]+)`",
        design,
        re.DOTALL,
    )
    assert gdpr, "spec.md must declare the GDPR identity, source, and legal notice"
    ai_design = specification.split("## AI Act Set Design", 1)[1].split("\n## ", 1)[0]
    ai_act = re.search(
        r"AI Act sets use authority `([^`]+)`, IDs `([^`]+)` and `([^`]+)`, "
        r"and version `([^`]+)`.*?Their official source is `(https://[^`]+)`.*?"
        r"Licence metadata states that (.+?)\. Attribution identifies .*?"
        r"references `(https://[^`]+)`",
        ai_design,
        re.DOTALL,
    )
    assert ai_act, "spec.md must declare the AI Act identity, source, and legal notice"
    return {
        "mdr": {
            "identity": (mdr.group(1), mdr.group(2), mdr.group(3)),
            "officialUrl": mdr.group(4),
            "licence": mdr.group(5),
            "attribution": mdr.group(6).replace("{official URL}", mdr.group(4)),
        },
        "mdcg": {
            "identity": (mdcg.group(1), mdcg.group(2), mdcg.group(3)),
            "officialUrl": mdcg.group(4),
            "listingUrl": mdcg.group(5),
            "licence": mdcg.group(6),
            "attribution": (
                mdcg.group(7)
                .replace("*", "")
                .replace("{source URL}", mdcg.group(4))
                .replace("{listing URL}", mdcg.group(5))
            ),
        },
        "gdpr": {
            "identity": (gdpr.group(1), gdpr.group(2), gdpr.group(3)),
            "officialUrl": gdpr.group(4),
            "legalNoticeUrl": gdpr.group(5),
        },
        "ai_act": {
            "identity": (ai_act.group(1), ai_act.group(2), ai_act.group(4)),
            "annex_identity": (ai_act.group(1), ai_act.group(3), ai_act.group(4)),
            "officialUrl": ai_act.group(5),
            "legalNoticeUrl": ai_act.group(7),
        },
    }


def _set_key(identity: tuple[str, str, str]) -> str:
    authority, identifier, version = identity
    return f"{authority}/{identifier}@{version}"


def _spec_set_key(kind: str) -> str:
    """Return a canonical set key parsed from spec.md."""
    return _set_key(_parsed_spec_sets()[kind]["identity"])


def _spec_set_path(kind: str) -> str:
    """Return the clause file path derived from its spec.md identity."""
    authority, identifier, version = _parsed_spec_sets()[kind]["identity"]
    return f"clauses/{authority}-{identifier}-{version}.json"


def _spec_set_metadata() -> dict[str, dict[str, object]]:
    """Read canonical set metadata values from spec.md."""
    spec_sets = _parsed_spec_sets()
    mdr = spec_sets["mdr"]
    mdcg = spec_sets["mdcg"]
    gdpr = spec_sets["gdpr"]
    ai_act = spec_sets["ai_act"]
    gdpr_licence = (
        "EUR-Lex legal documents may be reused for commercial or non-commercial "
        "purposes unless otherwise specified. Consolidated texts are CC BY 4.0; "
        "acknowledge the source and indicate changes."
    )
    gdpr_attribution = (
        f"© European Union. Source: {gdpr['officialUrl']} | "
        "This set contains original summaries and changes made. "
        f"EUR-Lex legal notice: {gdpr['legalNoticeUrl']}"
    )
    return {
        **annex11_expected_metadata(),
        _set_key(mdr["identity"]): {
            "officialUrl": mdr["officialUrl"],
            "licence": mdr["licence"],
            "attribution": mdr["attribution"],
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        },
        _set_key(mdcg["identity"]): {
            "officialUrl": mdcg["officialUrl"],
            "listingUrl": mdcg["listingUrl"],
            "licence": mdcg["licence"],
            "licence_exact": False,
            "attribution": mdcg["attribution"],
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        },
        _set_key(gdpr["identity"]): {
            "officialUrl": gdpr["officialUrl"],
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
                "licence": gdpr_licence,
                "attribution": gdpr_attribution,
            },
        },
        _set_key(ai_act["identity"]): {
            "officialUrl": ai_act["officialUrl"],
            "licence": (
                "EUR-Lex legal documents may be reused for commercial or "
                "non-commercial purposes unless otherwise specified and that "
                "the consolidated text is under CC BY 4.0 with source attribution "
                "and indication of changes."
            ),
            "attribution": (
                f"© European Union. Source: {ai_act['officialUrl']} | This set "
                f"contains original summaries and changes made. EUR-Lex legal "
                f"notice: {ai_act['legalNoticeUrl']}"
            ),
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        },
        _set_key(ai_act["annex_identity"]): {
            "officialUrl": ai_act["officialUrl"],
            "licence": (
                "EUR-Lex legal documents may be reused for commercial or "
                "non-commercial purposes unless otherwise specified and that "
                "the consolidated text is under CC BY 4.0 with source attribution "
                "and indication of changes."
            ),
            "attribution": (
                f"© European Union. Source: {ai_act['officialUrl']} | This set "
                f"contains original summaries and changes made. EUR-Lex legal "
                f"notice: {ai_act['legalNoticeUrl']}"
            ),
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        },
    }


def _assert_set_metadata_matches_spec(clause_set: dict) -> None:
    """Check a loaded set against its source-specific master-spec values."""
    key = clause_set_key(clause_set)
    expected = _spec_set_metadata()[key]
    rights = clause_set["rights"]
    for field, value in expected["rights"].items():
        assert rights[field] == value, f"{key}.rights.{field} differs from spec.md"
    assert rights["licence"].strip(), f"{key}.rights.licence must be nonblank"
    assert rights["attribution"].strip(), f"{key}.rights.attribution must be nonblank"
    if "licence" in expected:
        if expected.get("licence_exact", True):
            assert (
                rights["licence"] == expected["licence"]
            ), f"{key}.rights.licence differs from spec.md"
        else:
            assert (
                expected["licence"].casefold() in rights["licence"].casefold()
            ), f"{key}.rights.licence omits its source-specific spec statement"
    else:
        assert (
            expected["licence"].casefold() in rights["licence"].casefold()
        ), f"{key}.rights.licence omits its source-specific spec statement"
    if "attribution" in expected:
        assert (
            rights["attribution"] == expected["attribution"]
        ), f"{key}.rights.attribution differs from spec.md"
    else:
        for url in (expected["officialUrl"], expected["listingUrl"]):
            assert (
                f"<{url}>." in rights["attribution"]
            ), f"{key}.rights.attribution must bracket {url!r} before punctuation"
    assert (
        clause_set["source"]["officialUrl"] == expected["officialUrl"]
    ), f"{key}.source.officialUrl differs from spec.md"
    if "listingUrl" in expected:
        assert (
            expected["listingUrl"] in rights["attribution"]
        ), f"{key}.rights.attribution omits the source listing URL"


def _assert_gdpr_metadata_matches_spec(clause_set: dict) -> None:
    """Check every GDPR identity, source, and rights field against spec.md."""
    key = clause_set_key(clause_set)
    expected = _spec_set_metadata()[key]
    identity = (clause_set["authority"], clause_set["id"], clause_set["version"])
    assert (
        identity == _parsed_spec_sets()["gdpr"]["identity"]
    ), f"{key}.identity differs from spec.md"
    assert (
        clause_set["source"]["officialUrl"] == expected["officialUrl"]
    ), f"{key}.source.officialUrl differs from spec.md"
    for field, value in expected["rights"].items():
        assert (
            clause_set["rights"][field] == value
        ), f"{key}.rights.{field} differs from spec.md"


def _mdr_set() -> dict:
    """Return the declared MDR set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == _spec_set_key("mdr")
    )


def _mdcg_set() -> dict:
    """Return the declared MDCG companion set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == _spec_set_key("mdcg")
    )


def _gdpr_set() -> dict:
    """Return the declared GDPR set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == _spec_set_key("gdpr")
    )


def _ai_act_set() -> dict:
    """Return the declared AI Act high-risk obligations set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == "eu/ai-act-2024-1689@2026-07-27"
    )


def _ai_act_annex_set() -> dict:
    """Return the declared AI Act Annex IV set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == "eu/ai-act-2024-1689-annex-iv@2026-07-27"
    )


def _assert_ai_act_set_metadata_matches_spec(
    clause_set: dict, identity: tuple[str, str, str]
) -> None:
    """Check one AI Act set's identity and EUR-Lex rights field by field."""
    authority, set_id, version = identity
    key = f"{authority}/{set_id}@{version}"
    expected = _spec_set_metadata()[key]
    for field, value in (
        ("authority", authority),
        ("id", set_id),
        ("version", version),
    ):
        assert clause_set.get(field) == value, f"{key}.{field} differs from spec.md"
    assert (
        clause_set.get("source", {}).get("officialUrl") == expected["officialUrl"]
    ), f"{key}.source.officialUrl differs from spec.md"
    for field, value in expected["rights"].items():
        assert (
            clause_set.get("rights", {}).get(field) == value
        ), f"{key}.rights.{field} differs from spec.md"
    assert (
        clause_set.get("rights", {}).get("licence") == expected["licence"]
    ), f"{key}.rights.licence differs from spec.md"
    assert (
        clause_set.get("rights", {}).get("attribution") == expected["attribution"]
    ), f"{key}.rights.attribution differs from spec.md"


def _assert_ai_act_annex_clause_fields(clause_set: dict) -> None:
    """Check each Annex IV clause against its normative table row."""
    rows = _spec_ai_act_annex_rows()
    clauses = clause_set["clauses"]
    expected_ids = [row["id"] for row in rows]
    actual_ids = [clause["id"] for clause in clauses]
    missing_ids = [
        clause_id for clause_id in expected_ids if clause_id not in actual_ids
    ]
    extra_ids = [clause_id for clause_id in actual_ids if clause_id not in expected_ids]
    assert actual_ids == expected_ids, (
        "AI Act Annex IV clause IDs differ from the normative table: "
        f"missing={missing_ids}, extra={extra_ids}"
    )
    catalog = _spec_output_catalog()
    for clause, row in zip(clauses, rows, strict=True):
        clause_id = clause["id"]
        assert clause["force"] == "mandatory", f"{clause_id}.force differs from spec"
        assert clause["text"].strip(), f"{clause_id}.text must be nonempty"
        assert clause[
            "expectedOutputs"
        ], f"{clause_id}.expectedOutputs must be nonempty"
        assert (
            _applicability_spec(clause.get("applicability")) == row["applicability"]
        ), f"{clause_id}.applicability differs from the AI Act Annex IV table"
        assert clause["expectedOutputs"] == row["outputs"].split(
            ", "
        ), f"{clause_id}.expectedOutputs differs from the AI Act Annex IV table"
        output_kinds = []
        for output in clause["expectedOutputs"]:
            assert (
                output in catalog
            ), f"{clause_id}.expectedOutputs has unknown {output}"
            output_kinds.append(catalog[output]["kind"])
        assert any(
            kind in {"record", "document"} for kind in output_kinds
        ), f"{clause_id} must have at least one record or document output"
    used = {output for clause in clauses for output in clause["expectedOutputs"]}
    assert clause_set["outputCatalog"] == {
        name: catalog[name] for name in sorted(used)
    }, "AI Act Annex IV outputCatalog differs from the expected outputs"


def _assert_ai_act_clause_fields(clause_set: dict) -> None:
    """Check each AI Act clause's force, applicability, and outputs."""
    rows = _spec_ai_act_rows()
    clauses = clause_set["clauses"]
    assert [clause["id"] for clause in clauses] == [row["id"] for row in rows]
    for clause, row in zip(clauses, rows, strict=True):
        clause_id = clause["id"]
        assert (
            clause["force"] == row["force"] == "mandatory"
        ), f"{clause_id}.force differs from the AI Act table"
        assert clause["text"].strip(), f"{clause_id}.text must be nonempty"
        assert clause[
            "expectedOutputs"
        ], f"{clause_id}.expectedOutputs must be nonempty"
        assert (
            _applicability_spec(clause.get("applicability")) == row["applicability"]
        ), f"{clause_id}.applicability differs from the AI Act table"
        assert clause["expectedOutputs"] == row["outputs"].split(
            ", "
        ), f"{clause_id}.expectedOutputs differs from the AI Act table"


def _applicability_spec(expression: dict | None) -> str:
    """Render a clause-set expression in the GDPR table's compact notation."""
    if expression is None:
        return "always"
    if expression["op"] == "eq":
        return f"eq {expression['dimension']} {expression['value']}"
    if expression["op"] == "all":
        terms = ", ".join(_applicability_spec(term) for term in expression["terms"])
        return f"all[{terms}]"
    raise AssertionError(f"unexpected GDPR applicability operator: {expression['op']}")


def _spec_mdcg_crosswalks() -> list[dict[str, str]]:
    """Read the normative MDCG-to-MDR crosswalk table from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## MDCG Companion Table", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| MDCG ID")
            or line.startswith("|---")
        ):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5:
            continue
        mdcg_id, mdr_id, relation, rationale, outputs = cells
        rows.append(
            {
                "sourceClause": mdcg_id,
                "targetClause": mdr_id,
                "relation": relation,
                "rationale": rationale,
                "outputs": outputs,
            }
        )
    return rows


def _spec_output_catalog() -> dict[str, dict[str, str]]:
    """Read the canonical output definitions from the master specification."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## EU Pack Output Catalog", 1)[1].split("\n## ", 1)[
        0
    ]
    catalog = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        name, kind, description = [cell.strip() for cell in line.strip("|").split("|")]
        if name == "Name" or name.startswith("---"):
            continue
        catalog[name] = {"kind": kind, "description": description}
    return catalog


def _outcomes(binding: dict) -> dict[str, str]:
    """Return clause outcomes indexed by their stable IDs."""
    return {item["clauseId"]: item["outcome"] for item in binding["clauses"]}


def _synthetic_set(
    authority: str,
    set_id: str,
    version: str,
    *,
    output_catalog: dict | None = None,
    clauses: list[dict] | None = None,
    crosswalks: list[dict] | None = None,
    text_rights: str = "original",
) -> dict:
    return {
        "schemaVersion": "clause-set-v1",
        "authority": authority,
        "id": set_id,
        "title": f"{set_id} synthetic set",
        "version": version,
        "rights": {
            "structure": "citation_only",
            "text": text_rights,
            "clearance_ref": None,
            "licence": "Synthetic test fixture",
        },
        "source": {
            "title": "Synthetic test source",
            "identifier": "example.invalid/test",
            "officialUrl": "https://example.invalid/test",
        },
        "outputCatalog": output_catalog or {},
        "clauses": clauses or [],
        "crosswalks": crosswalks or [],
    }


def _installed_clause_sets(module_name: str) -> list[dict]:
    """Load an installed module; fail when it is absent."""
    result = run(engine_tool("quoin"), "module", "list")
    assert result.returncode == 0, result.stderr + result.stdout
    plugins = json.loads(result.stdout)["plugins"]
    module = next((item for item in plugins if item["name"] == module_name), None)
    assert module is not None, (
        f"module {module_name} is not installed; install it with "
        f"`quoin module install path:<checkout>/{module_name}`"
    )
    manifest_path = pathlib.Path(module["targetPath"]) / "manifest.yaml"
    return load_clause_sets(manifest_path)


def test_manifest_declares_all_implemented_clause_sets():
    """Verify the module declares its implemented MDR, GDPR, and AI Act sets.

    Assumptions: The canonical set identities are declared in spec.md.
    Criteria: The manifest declares each implemented clause file exactly once.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [
        _spec_set_path("mdr"),
        _spec_set_path("mdcg"),
        _spec_set_path("gdpr"),
        "clauses/eu-ai-act-2024-1689-2026-07-27.json",
        "clauses/eu-ai-act-2024-1689-annex-iv-2026-07-27.json",
        annex11_set_path(),
    ]


@pytest.mark.trace("FR-001-AC-2")
def test_manifest_declares_no_non_clause_contributions():
    """Verify the module manifest declares no non-clause contributions.

    Assumptions: This module is a clause-only pack.
    Criteria: It declares no object types, archetypes, or edges.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert not {"object_types", "archetypes", "edges"}.intersection(manifest)


@pytest.mark.trace("FR-014-AC-4")
def test_quire_validates_the_module_and_spec_bundle():
    """Validate the clause module and its specification documents.

    Assumptions: The installed ISO artifacts module supplies validation
    schemas.
    Criteria: Quire exits successfully for the EU module and spec documents.
    Trace: FR-014-AC-4
    """
    iso_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-iso"
    process_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-process"
    result = run(
        engine_tool("quire"),
        "validate",
        "--module",
        str(PACKAGE_ROOT),
        "--module",
        str(iso_module),
        "--module",
        str(process_module),
        "spec/**/*.md",
    )
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("FR-016-AC-4")
def test_ai_act_module_validates_and_passes_publish_check():
    """Validate the module specifications and both publishable AI Act sets.

    Assumptions: The installed ISO and process artifact modules supply the
    schemas used by the package specification.
    Criteria: Quire validates the specification bundle and module, then accepts
    its source and rights metadata for publication.
    """
    iso_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-iso"
    process_module = pathlib.Path.home() / ".ix/filament/modules/spec-artifacts-process"
    validated = run(
        engine_tool("quire"),
        "validate",
        "--module",
        str(PACKAGE_ROOT),
        "--module",
        str(iso_module),
        "--module",
        str(process_module),
        "spec/**/*.md",
    )
    assert validated.returncode == 0, validated.stderr + validated.stdout
    published = run(
        engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT)
    )
    assert published.returncode == 0, published.stderr + published.stdout


@pytest.mark.trace("FR-001-AC-2")
def test_path_install_reports_a_non_pack_clause_module(tmp_path):
    """Install the module in an isolated Quoin home.

    Assumptions: The module contains no licensed clause sets.
    Criteria: Installation succeeds and the list reports pack false.
    """
    home = tmp_path / "home"
    config_root = tmp_path / "config"
    home.mkdir()
    config_root.mkdir()
    env = {**os.environ, "HOME": str(home), "IX_CONFIG_ROOT": str(config_root)}
    installed = run(
        engine_tool("quoin"), "module", "install", f"path:{PACKAGE_ROOT}", env=env
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    listed = run(engine_tool("quoin"), "module", "list", env=env)
    assert listed.returncode == 0, listed.stderr + listed.stdout
    plugins = json.loads(listed.stdout)["plugins"]
    module = next(item for item in plugins if item["name"] == "spec_clauses_eu_law")
    assert module["pack"] is False
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert not {"object_types", "archetypes", "edges"}.intersection(manifest)
    catalog = run(engine_tool("quoin"), "catalog", "list", "--json", env=env)
    assert catalog.returncode == 0, catalog.stderr + catalog.stdout
    catalog_module = next(
        item
        for item in json.loads(catalog.stdout)["modules"]
        if item["name"] == "spec_clauses_eu_law"
    )
    assert catalog_module["objectTypes"] == []
    assert catalog_module["artifactTypes"] == []


def test_quoin_detects_a_licensed_set_in_a_temporary_module(tmp_path):
    """Verify pack detection with an isolated licensed set fixture.

    Assumptions: The synthetic fixture uses the clause-set rights shape.
    Criteria: Quoin installs it and reports pack true.
    """
    licensed_set = _synthetic_set("example.invalid", "licensed", "1.0.0")
    licensed_set["rights"]["text"] = "licensed"
    source_root = pathlib.Path(tempfile.mkdtemp(prefix="eu-pack-", dir="/var/tmp"))
    try:
        module_root = stage_clause_sets(source_root, licensed_set)
        home = tmp_path / "licensed-home"
        config_root = tmp_path / "licensed-config"
        home.mkdir()
        config_root.mkdir()
        env = {**os.environ, "HOME": str(home), "IX_CONFIG_ROOT": str(config_root)}
        installed = run(
            engine_tool("quoin"),
            "module",
            "install",
            f"path:{module_root}",
            env=env,
        )
        assert installed.returncode == 0, installed.stderr + installed.stdout
        listed = run(engine_tool("quoin"), "module", "list", env=env)
        assert listed.returncode == 0, listed.stderr + listed.stdout
        module = json.loads(listed.stdout)["plugins"][0]
        assert module["pack"] is True
    finally:
        shutil.rmtree(source_root)


@pytest.mark.trace("FR-006-AC-3")
def test_all_declared_sets_share_one_output_catalog():
    """Reject output kind or description drift across installed sets.

    Assumptions: A US pack module may be installed in the test environment.
    Criteria: This module's sets and any installed US sets share exact output
    definitions.
    """
    clause_sets = load_clause_sets()
    clause_sets.extend(_installed_clause_sets("spec_clauses_us_health"))
    assert_output_catalog_consistent(clause_sets)


@pytest.mark.trace("FR-003-AC-1", "FR-003-AC-2")
def test_mdr_clause_ids_and_required_fields_match_the_spec():
    """Check the MDR clause table and required clause fields.

    Assumptions: The master specification is the source for the clause IDs.
    Criteria: IDs match exactly; every clause is mandatory, has original text,
    and names at least one catalog output.
    Trace: FR-003-AC-1, FR-003-AC-2
    """
    clause_set = _mdr_set()
    clauses = clause_set["clauses"]
    spec_ids = _spec_mdr_ids()
    assert [clause["id"] for clause in clauses] == spec_ids
    evaluation = evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("mdr"))
    assert [item["clauseId"] for item in evaluation["clauses"]] == spec_ids
    assert all(clause["force"] == "mandatory" for clause in clauses)
    assert all(clause["text"].strip() for clause in clauses)
    assert all(clause["expectedOutputs"] for clause in clauses)
    assert all(
        set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        for clause in clauses
    )


@pytest.mark.trace("FR-003-AC-3")
def test_unknown_clause_output_fails_with_the_clause_id(tmp_path):
    """Reject an MDR fixture that references an undeclared output.

    Assumptions: The temporary set otherwise follows the valid clause shape.
    Criteria: Quire rejects the unknown output and identifies its clause.
    Trace: FR-003-AC-3
    """
    fixture = _synthetic_set(
        "example.invalid",
        "unknown-output",
        "1.0.0",
        clauses=[
            {
                "id": "I-17.2",
                "force": "mandatory",
                "title": "Synthetic clause",
                "text": "Original synthetic summary.",
                "expectedOutputs": ["missing-output"],
            }
        ],
    )
    module_root = stage_clause_sets(tmp_path, fixture)
    result = run(
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module_root),
        "--authority",
        "example.invalid",
        "--set",
        "unknown-output",
        "--version",
        "1.0.0",
        "--json",
    )
    assert result.returncode != 0
    assert "I-17.2" in result.stderr + result.stdout


@pytest.mark.trace("FR-004-AC-1", "FR-004-AC-2", "FR-004-AC-3")
def test_mdr_mobile_platform_applicability():
    """Check mobile applicability for the one conditional MDR clause.

    Assumptions: Context values are supplied by a human product reviewer.
    Criteria: Only I-17.3 depends on mobile_platform and its three outcomes
    match the specification.
    Trace: FR-004-AC-1, FR-004-AC-2, FR-004-AC-3
    """
    clause_set = _mdr_set()
    assert clause_set["classificationDimensions"] == {
        "mobile_platform": {"values": ["yes", "no"]}
    }
    conditional = [
        clause["id"] for clause in clause_set["clauses"] if "applicability" in clause
    ]
    assert conditional == ["I-17.3"]

    no_context = _outcomes(evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("mdr")))
    mobile_no = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("mdr"), "mobile_platform=no")
    )
    mobile_yes = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("mdr"), "mobile_platform=yes")
    )
    assert no_context["I-17.3"] == "unresolved"
    assert set(no_context.values()) - {"binding"} == {"unresolved"}
    assert mobile_no["I-17.3"] == "not_binding"
    assert {
        clause_id for clause_id, value in mobile_no.items() if value != "binding"
    } == {"I-17.3"}
    assert set(mobile_yes.values()) == {"binding"}


@pytest.mark.trace("FR-002-AC-1", "FR-002-AC-3")
def test_each_clause_set_rights_and_source_match_the_spec():
    """Check source-specific rights metadata for every set in the manifest.

    Assumptions: The master specification is the canonical metadata source.
    Criteria: Both first-wave sets are checked as they enter the manifest;
    failures identify the affected set and field.
    Trace: FR-002-AC-1, FR-002-AC-3
    """
    expected = _spec_set_metadata()
    clause_sets = load_clause_sets()
    assert {clause_set_key(item) for item in clause_sets} == set(expected)
    for clause_set in clause_sets:
        if clause_set_key(clause_set) == _spec_set_key("gdpr"):
            _assert_gdpr_metadata_matches_spec(clause_set)
        else:
            _assert_set_metadata_matches_spec(clause_set)

    # Prove changed values name the affected set and field for the established
    # exact-metadata assertions; GDPR's looser rights wording is checked above.
    for clause_set in clause_sets:
        if clause_set_key(clause_set) == _spec_set_key("gdpr"):
            key = re.escape(clause_set_key(clause_set))
            broken = json.loads(json.dumps(clause_set))
            broken["source"]["officialUrl"] = "https://example.invalid/changed"
            with pytest.raises(AssertionError, match=rf"{key}\.source\.officialUrl"):
                _assert_gdpr_metadata_matches_spec(broken)

            broken = json.loads(json.dumps(clause_set))
            broken["rights"]["attribution"] = "changed"
            with pytest.raises(AssertionError, match=rf"{key}\.rights\.attribution"):
                _assert_gdpr_metadata_matches_spec(broken)
            continue
        key = re.escape(clause_set_key(clause_set))
        broken = json.loads(json.dumps(clause_set))
        broken["rights"]["licence"] = "changed"
        with pytest.raises(AssertionError, match=rf"{key}\.rights\.licence"):
            _assert_set_metadata_matches_spec(broken)

        broken = json.loads(json.dumps(clause_set))
        broken["source"]["officialUrl"] = "https://example.invalid/changed"
        with pytest.raises(AssertionError, match=rf"{key}\.source\.officialUrl"):
            _assert_set_metadata_matches_spec(broken)


def test_npm_publish_config_uses_public_default_registry():
    """Keep public access while relying on npm's default public registry."""
    package = json.loads((REPO_ROOT / "package.json").read_text())
    publish_config = package["publishConfig"]

    assert publish_config["access"] == "public"
    assert "registry" not in publish_config


@pytest.mark.trace("FR-002-AC-2")
def test_mdr_publish_check_accepts_the_set_and_rejects_licensed_text(tmp_path):
    """Check that publish-check accepts the public set and rejects a licensed fixture.

    Assumptions: The fixture is copied into a temporary module without changing
    any other module metadata.
    Criteria: The real module exits zero and a licensed-text set exits two with
    its set key in the diagnostic.
    Trace: FR-002-AC-2
    """
    accepted = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert accepted.returncode == 0, accepted.stderr + accepted.stdout

    module_root = tmp_path / "licensed-module"
    shutil.copytree(PACKAGE_ROOT, module_root)
    clause_path = module_root / _spec_set_path("mdr")
    licensed = json.loads(clause_path.read_text())
    licensed["rights"]["text"] = "licensed"
    clause_path.write_text(json.dumps(licensed))
    refused = run(engine_tool("quire"), "publish-check", "--module", str(module_root))
    assert refused.returncode == 2
    assert _spec_set_key("mdr") in refused.stderr + refused.stdout


@pytest.mark.trace("FR-006-AC-1")
def test_mdr_declares_the_spec_catalog_subset_used_by_its_clauses():
    """Check that the MDR set uses only its exact catalog subset.

    Assumptions: The EU catalog table in spec.md is canonical.
    Criteria: Each referenced output is declared with the exact catalog
    definition, and the set has no unused output entry.
    """
    clause_set = _mdr_set()
    used = {
        output
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    }
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}


@pytest.mark.trace("FR-005-AC-1", "FR-005-AC-3")
def test_mdcg_clause_ids_outputs_and_evaluation_match_the_spec():
    """Check the MDCG IDs, outputs, recommendation force, and evaluation.

    Assumptions: The companion table in spec.md is normative for IDs and
    crosswalk outputs; the source guidance remains non-binding.
    Criteria: Every table ID appears once, every output equals the table union,
    and the empty context binds every recommended clause.
    """
    clause_set = _mdcg_set()
    rows = _spec_mdcg_crosswalks()
    spec_ids = list(dict.fromkeys(row["sourceClause"] for row in rows))
    clauses = clause_set["clauses"]
    assert [clause["id"] for clause in clauses] == spec_ids
    assert all(clause["force"] == "recommended" for clause in clauses)
    assert all("applicability" not in clause for clause in clauses)
    assert all(clause["text"].strip() for clause in clauses)
    assert all(clause["expectedOutputs"] for clause in clauses)
    assert all(
        set(clause["expectedOutputs"]) <= set(clause_set["outputCatalog"])
        for clause in clauses
    )
    for clause in clauses:
        expected_outputs = sorted(
            {
                output.strip()
                for row in rows
                if row["sourceClause"] == clause["id"]
                for output in row["outputs"].split(",")
            }
        )
        assert clause["expectedOutputs"] == expected_outputs

    evaluation = evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("mdcg"))
    assert [item["clauseId"] for item in evaluation["clauses"]] == spec_ids
    assert {item["outcome"] for item in evaluation["clauses"]} == {"binding"}


@pytest.mark.trace("FR-005-AC-1", "FR-005-AC-3")
def test_mdcg_crosswalks_match_spec_and_resolve_to_mdr():
    """Check every MDCG mapping against the table and loaded MDR set.

    Assumptions: Each crosswalk rationale is original prose from spec.md.
    Criteria: Source IDs, targets, relations, rationales, and target resolution
    match the normative table exactly.
    """
    clause_sets = load_clause_sets()
    clause_set = next(
        item for item in clause_sets if clause_set_key(item) == _spec_set_key("mdcg")
    )
    expected_rows = _spec_mdcg_crosswalks()
    mdr_authority, mdr_id, mdr_version = _parsed_spec_sets()["mdr"]["identity"]
    expected = [
        {
            "sourceClause": row["sourceClause"],
            "target": {
                "set": {
                    "authority": mdr_authority,
                    "id": mdr_id,
                    "version": mdr_version,
                },
                "clause": row["targetClause"],
            },
            "relation": row["relation"],
            "rationale": row["rationale"],
        }
        for row in expected_rows
    ]
    assert clause_set["crosswalks"] == expected
    assert all(
        item["relation"] in {"informative", "partial"}
        for item in clause_set["crosswalks"]
    )
    assert all(item["rationale"].strip() for item in clause_set["crosswalks"])
    assert_crosswalk_targets_resolve(clause_sets)


def _clause_outputs(clause_set: dict) -> dict[str, set[str]]:
    return {
        clause["id"]: set(clause["expectedOutputs"]) for clause in clause_set["clauses"]
    }


@pytest.mark.trace("FR-003-AC-4")
def test_mdr_security_prerequisite_clauses_map_to_security_and_it_outputs():
    """Map MDR I-17.4 and I-18.8 to the outputs that address them.

    Assumptions: Operating prerequisites are stated by the customer; the
    security records are the only toolchain output about access protection.
    Criteria: I-17.4 expects the IT-requirements statement and security
    records, I-18.8 expects security records and their verification, and
    neither expects release, anomaly or SOUP reports; the IT-requirements
    statement is described as customer-supplied.
    """
    clause_set = _mdr_set()
    outputs = _clause_outputs(clause_set)
    assert outputs["I-17.4"] == {"it-requirements-statement", "security-risk-records"}
    assert outputs["I-18.8"] == {"security-risk-records", "verification-records"}
    assert outputs["I-14.2(d)"] == {
        "it-requirements-statement",
        "security-risk-records",
    }
    assert "verification-records" in outputs["I-17.2"]
    assert "risk-management-records" in outputs["II-5"]
    description = clause_set["outputCatalog"]["it-requirements-statement"][
        "description"
    ]
    assert "customer-supplied" in description.lower()
    assert "no toolchain producer" in description
    rows = {row["id"]: set(row["outputs"]) for row in _spec_mdr_rows()}
    assert rows == outputs


@pytest.mark.trace("FR-005-AC-4")
def test_mdcg_security_sections_map_to_security_and_customer_outputs():
    """Map MDCG security goals and post-market sections to honest outputs.

    Assumptions: Incident investigation and reporting is the manufacturer's own
    procedure, so surveillance and vigilance procedures are customer-supplied.
    Criteria: 2.1 expects security records, 5.2 is all-procedure, 5.1 carries the
    customer procedure, and only 3.8 expects release or anomaly reports.
    """
    outputs = _clause_outputs(_mdcg_set())
    assert "security-risk-records" in outputs["2.1"]
    assert outputs["5.2"] == {"written-procedure"}
    assert "written-procedure" in outputs["5.1"]
    for clause_id, expected in outputs.items():
        if clause_id != "3.8":
            assert not expected & {"release-record", "anomaly-list"}, clause_id
    targets = {
        (item["sourceClause"], item["target"]["clause"])
        for item in _mdcg_set()["crosswalks"]
    }
    assert ("3.7", "I-17.2") in targets
    assert ("3.6", "I-17.4") in targets
    assert ("3.7", "I-17.4") not in targets
    assert "security-risk-records" in outputs["3.8"]
    assert "security-risk-records" in outputs["2.1"]


def _spec_customer_owned_inventory() -> set[tuple[str, str]]:
    """Read the customer-owned inventory from spec.md."""
    specification = (REPO_ROOT / "spec" / "spec.md").read_text()
    section = specification.split("## Customer-Owned Obligations", 1)[1].split(
        "\n## ", 1
    )[0]
    inventory = set()
    for line in section.splitlines():
        if (
            not line.startswith("|")
            or line.startswith("| Clause set")
            or line.startswith("|---")
        ):
            continue
        set_id, clause_id, _outputs = [
            cell.strip() for cell in line.strip("|").split("|")
        ]
        inventory.add((set_id, clause_id))
    return inventory


@pytest.mark.trace("FR-007-AC-1")
def test_all_procedure_clauses_match_the_customer_owned_inventory():
    """Compare every all-procedure clause with the spec inventory.

    Assumptions: A clause is customer-owned when every expected output has kind
    procedure.
    Criteria: The clauses found in the shipped sets equal the inventory exactly.
    """
    found = set()
    for clause_set in load_clause_sets():
        procedures = {
            name
            for name, output in clause_set["outputCatalog"].items()
            if output["kind"] == "procedure"
        }
        for clause in clause_set["clauses"]:
            if set(clause["expectedOutputs"]) <= procedures:
                found.add((clause_set["id"], clause["id"]))
    assert found == _spec_customer_owned_inventory()


@pytest.mark.trace("FR-005-AC-2")
def test_mdcg_missing_mdr_target_fails_with_source_and_target_key(tmp_path):
    """Reject an MDCG crosswalk whose target is absent from the MDR set.

    Assumptions: The fixture otherwise contains the real MDCG and MDR sets.
    Criteria: The failure names the source clause and exact target set key.
    """
    source = json.loads(json.dumps(_mdcg_set()))
    source["crosswalks"][0]["target"]["clause"] = "missing-mdr-clause"
    target = _mdr_set()
    fixture = stage_clause_sets(tmp_path, source, target)
    target_key = re.escape(_spec_set_key("mdr"))
    with pytest.raises(
        AssertionError,
        match=rf"{source['crosswalks'][0]['sourceClause']}.*{target_key}#missing-mdr-clause",
    ):
        assert_crosswalk_targets_resolve(load_clause_sets(fixture / "manifest.yaml"))


def _assert_ai_act_crosswalk_contract(clause_sets: list[dict]) -> None:
    """Require AI Act crosswalks to be complete and claim-bounded."""
    ai_set_keys = {
        "eu/ai-act-2024-1689@2026-07-27",
        "eu/ai-act-2024-1689-annex-iv@2026-07-27",
    }
    for clause_set in clause_sets:
        source_key = clause_set_key(clause_set)
        if source_key not in ai_set_keys:
            continue
        source_ids = {clause["id"] for clause in clause_set["clauses"]}
        for crosswalk in clause_set.get("crosswalks", []):
            source_clause = crosswalk.get("sourceClause", "")
            assert (
                source_clause in source_ids
            ), f"{source_key}#{source_clause}.sourceClause must name a clause"
            assert crosswalk.get("relation") in {
                "partial",
                "informative",
            }, f"{source_key}#{source_clause}.relation must be partial or informative"
            assert (
                isinstance(crosswalk.get("rationale"), str)
                and crosswalk["rationale"].strip()
            ), f"{source_key}#{source_clause}.rationale must be nonempty"
    assert_crosswalk_targets_resolve(clause_sets)


@pytest.mark.trace("FR-021-AC-1", "FR-021-AC-2")
def test_ai_act_crosswalks_match_the_annex_table_and_resolve_to_mdr():
    """Check table-driven Annex IV mappings and the selected article mappings.

    Assumptions: The exact AI Act and MDR sets are declared in the module.
    Criteria: Each Annex IV row either has its table target or explicitly has
    no counterpart; article mappings cover the ticket's named Article 9 and
    Article 15 examples using only clauses in the selected MDR set; all targets
    resolve with non-equivalent relations.
    Trace: FR-021-AC-1, FR-021-AC-2
    """
    clause_sets = load_clause_sets()
    high_risk = _ai_act_set()
    annex = _ai_act_annex_set()
    mdr_authority, mdr_id, mdr_version = _parsed_spec_sets()["mdr"]["identity"]
    mdr_set = {
        "authority": mdr_authority,
        "id": mdr_id,
        "version": mdr_version,
    }

    rows = _spec_ai_act_annex_rows()
    expected_annex = [
        {
            "sourceClause": row["id"],
            "target": {"set": mdr_set, "clause": row["target"]},
            "relation": row["relation"],
            "rationale": row["rationale"],
        }
        for row in rows
        if row["target"] != "none"
    ]
    assert annex["crosswalks"] == expected_annex
    no_counterpart = {row["id"] for row in rows if row["target"] == "none"}
    assert no_counterpart.isdisjoint(
        item["sourceClause"] for item in annex["crosswalks"]
    )

    expected_article_targets = {
        "art-9": {"II-5", *(f"I-{index}" for index in range(1, 6)), "I-8"},
        "art-15": {"I-17.2", "I-17.4", "I-18.8"},
    }
    actual_article_targets = {
        source: {
            item["target"]["clause"]
            for item in high_risk["crosswalks"]
            if item["sourceClause"] == source
        }
        for source in expected_article_targets
    }
    assert actual_article_targets == expected_article_targets
    assert all(item["target"]["set"] == mdr_set for item in high_risk["crosswalks"])
    _assert_ai_act_crosswalk_contract(clause_sets)


@pytest.mark.trace("FR-021-AC-3")
@pytest.mark.parametrize(
    ("mutation", "expected_error"),
    [
        ("unknown_target", r"IV-1\(a\).*targets missing clause.*#II-99"),
        ("equivalent", r"IV-1\(a\)\.relation"),
        ("empty_rationale", r"IV-1\(a\)\.rationale"),
    ],
)
def test_ai_act_invalid_crosswalk_fields_fail_with_source_and_field(
    mutation: str, expected_error: str
):
    """Reject an unknown target, equivalent relation, or blank rationale.

    Assumptions: The valid AI Act and MDR sets load from the module manifest.
    Criteria: Each invalid crosswalk fails with the source clause and the
    target, relation, or rationale field identified.
    Trace: FR-021-AC-3
    """
    clause_sets = copy.deepcopy(load_clause_sets())
    annex = next(
        item
        for item in clause_sets
        if clause_set_key(item) == "eu/ai-act-2024-1689-annex-iv@2026-07-27"
    )
    crosswalk = annex["crosswalks"][0]
    if mutation == "unknown_target":
        crosswalk["target"]["clause"] = "II-99"
    elif mutation == "equivalent":
        crosswalk["relation"] = "equivalent"
    else:
        crosswalk["rationale"] = ""

    with pytest.raises(AssertionError, match=expected_error):
        _assert_ai_act_crosswalk_contract(clause_sets)


def _assert_exact_crosswalk_source_rows(
    crosswalks: list[dict], expected_sources: set[str]
) -> None:
    """Require Article 32 crosswalk rows to use exactly the selected clauses."""
    actual_sources = {item["sourceClause"] for item in crosswalks}
    unexpected = sorted(actual_sources - expected_sources)
    missing = sorted(expected_sources - actual_sources)
    assert (
        not unexpected
    ), "unexpected sourceClause row(s) in Article 32 crosswalks: " + ", ".join(
        unexpected
    )
    assert (
        not missing
    ), "missing sourceClause row(s) in Article 32 crosswalks: " + ", ".join(missing)


@pytest.mark.trace("FR-014-AC-1")
def test_gdpr_article32_crosswalks_reject_article32_three():
    """Reject an Article 32(3) source row outside the selected clause set.

    Assumptions: The selected GDPR clause rows are valid.
    Criteria: Exact source coverage rejects an unexpected Article 32(3) row
    and identifies its sourceClause value.
    Trace: FR-014-AC-1
    """
    expected_sources = {
        "art-32(1)(a)",
        "art-32(1)(b)",
        "art-32(1)(c)",
        "art-32(1)(d)",
        "art-32(2)",
        "art-32(4)",
    }
    crosswalks = [{"sourceClause": source} for source in expected_sources]
    unexpected_row = {"sourceClause": "art-32(3)"}

    with pytest.raises(
        AssertionError,
        match=r"unexpected sourceClause row\(s\).*art-32\(3\)",
    ):
        _assert_exact_crosswalk_source_rows(
            [*crosswalks, unexpected_row], expected_sources
        )


@pytest.mark.trace("FR-014-AC-1", "FR-014-AC-2", "FR-014-AC-3")
def test_gdpr_article32_crosswalks_use_the_selected_nist_and_hipaa_sets():
    """Check Article 32 mappings against the two selected installed sets.

    Assumptions: The NIST 5.2.0 and HIPAA 2026-11-12 modules are installed as
    test dependencies, and the GDPR set is loaded from its declared manifest.
    Criteria: Each required Article 32 clause has the intended targets in both
    exact sets, every rationale is non-empty, relations are non-equivalent,
    and every external clause target resolves in the installed module.
    """
    clause_sets = load_clause_sets()
    gdpr = _gdpr_set()
    expected = {
        "art-32(1)(a)": {
            ("nist/sp800-53@5.2.0", "SC-8"),
            ("nist/sp800-53@5.2.0", "SC-28"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.312(a)(2)(iv)"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.312(e)(2)(ii)"),
        },
        "art-32(1)(b)": {
            ("nist/sp800-53@5.2.0", "SC-5"),
            ("nist/sp800-53@5.2.0", "SI-7"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.312(c)(1)"),
        },
        "art-32(1)(c)": {
            ("nist/sp800-53@5.2.0", "CP-9"),
            ("nist/sp800-53@5.2.0", "CP-10"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.308(a)(7)(ii)(B)"),
        },
        "art-32(1)(d)": {
            ("nist/sp800-53@5.2.0", "CA-2"),
            ("nist/sp800-53@5.2.0", "CA-8"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.308(a)(8)"),
        },
        "art-32(2)": {
            ("nist/sp800-53@5.2.0", "RA-3"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.308(a)(1)(ii)(A)"),
        },
        "art-32(4)": {
            ("nist/sp800-53@5.2.0", "AC-6"),
            ("us-hhs/45-cfr-164-subpart-c@2026-11-12", "164.308(a)(4)(i)"),
        },
    }
    _assert_exact_crosswalk_source_rows(gdpr["crosswalks"], set(expected))
    actual = {
        source: {
            (
                f"{item['target']['set']['authority']}/{item['target']['set']['id']}@"
                f"{item['target']['set']['version']}",
                item["target"]["clause"],
            )
            for item in gdpr["crosswalks"]
            if item["sourceClause"] == source
        }
        for source in expected
    }
    assert actual == expected
    assert all(
        item["relation"] in {"partial", "informative"} and item["rationale"].strip()
        for item in gdpr["crosswalks"]
    )
    assert_crosswalk_targets_resolve(clause_sets)


@pytest.mark.trace("FR-014-AC-2")
def test_gdpr_article32_missing_nist_target_names_source_and_target():
    """Reject an Article 32 crosswalk whose installed NIST target is absent.

    Assumptions: The real NIST target module is installed and the GDPR set
    otherwise contains its valid Article 32 mappings.
    Criteria: Resolution fails and names the source clause and exact missing
    target set key and clause id.
    """
    source = json.loads(json.dumps(_gdpr_set()))
    crosswalk = next(
        item
        for item in source["crosswalks"]
        if item["target"]["set"]["authority"] == "nist"
    )
    crosswalk["target"]["clause"] = "XX-99"
    source_key = re.escape(_spec_set_key("gdpr"))
    source_clause = re.escape(crosswalk["sourceClause"])
    with pytest.raises(
        AssertionError,
        match=rf"{source_key}#{source_clause}.*nist/sp800-53@5\.2\.0#XX-99",
    ):
        assert_crosswalk_targets_resolve([source])


@pytest.mark.trace("FR-014-AC-2")
def test_gdpr_article32_missing_nist_set_names_source_and_target():
    """Reject an Article 32 crosswalk whose NIST target set is not installed.

    Assumptions: The real GDPR set has a valid Article 32 crosswalk to NIST.
    Criteria: Resolution fails and names the source clause and missing target
    set key and clause id.
    """
    source = json.loads(json.dumps(_gdpr_set()))
    crosswalk = next(
        item
        for item in source["crosswalks"]
        if item["target"]["set"]["authority"] == "nist"
    )
    crosswalk["target"]["set"]["id"] = "missing-sp800-53"
    source_key = re.escape(_spec_set_key("gdpr"))
    source_clause = re.escape(crosswalk["sourceClause"])
    with pytest.raises(
        AssertionError,
        match=rf"{source_key}#{source_clause}.*nist/missing-sp800-53@5\.2\.0#{crosswalk['target']['clause']}",
    ):
        assert_crosswalk_targets_resolve([source])


@pytest.mark.trace("FR-014-AC-2")
def test_nist_and_hipaa_clause_files_are_not_copied_into_the_eu_pack():
    """Keep crosswalk targets in their installed modules instead of this repo.

    Assumptions: The repository checkout contains its tracked file inventory.
    Criteria: No tracked NIST or US HIPAA clause file is present in this module.
    """
    result = run("git", "ls-files", "-z", cwd=REPO_ROOT)
    assert result.returncode == 0, result.stderr
    tracked = result.stdout.split("\0")
    copied = [
        path
        for path in tracked
        if "nist-sp800-53" in pathlib.Path(path).name
        or pathlib.Path(path).name.startswith("us-hhs-")
    ]
    assert copied == []


@pytest.mark.trace("FR-006-AC-1")
def test_mdcg_declares_the_spec_catalog_subset_used_by_its_clauses():
    """Check that the MDCG set uses its exact canonical output subset.

    Assumptions: The EU catalog table in spec.md is canonical.
    Criteria: Every referenced output has the exact catalog definition and no
    unused output entry is present.
    """
    clause_set = _mdcg_set()
    used = {
        output
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    }
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}


@pytest.mark.trace("FR-009-AC-1", "FR-009-AC-2", "FR-009-AC-3", "FR-014-AC-4")
def test_gdpr_set_identity_rights_and_publish_check():
    """Check GDPR identity, attribution metadata, and publishability.

    Assumptions: spec.md declares the consulted EUR-Lex consolidation.
    Criteria: The manifest set matches its declared identity and rights, and
    Quire accepts the public module for publication.
    Trace: FR-009-AC-1, FR-009-AC-2, FR-009-AC-3, FR-014-AC-4
    """
    clause_set = _gdpr_set()
    assert clause_set_key(clause_set) == "eu/gdpr-2016-679@2016-05-04"
    _assert_gdpr_metadata_matches_spec(clause_set)
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("FR-010-AC-1", "FR-010-AC-2", "FR-006-AC-1")
def test_gdpr_clause_ids_fields_and_catalog_match_the_spec():
    """Check the complete GDPR clause table and its shared catalog subset.

    Assumptions: The GDPR Clause Table and output catalog in spec.md are
    normative.
    Criteria: IDs, force, applicability, summaries, outputs, and catalog are
    checked against those declarations.
    Trace: FR-010-AC-1, FR-010-AC-2, FR-006-AC-1
    """
    clause_set = _gdpr_set()
    rows = _spec_gdpr_rows()
    clauses = clause_set["clauses"]
    assert clause_set["classificationDimensions"] == {
        "gdpr_role": {"values": ["controller", "processor"]},
        "high_risk_processing": {"values": ["yes", "no"]},
        "article_30_records_applicability": {"values": ["applies", "exempt"]},
    }
    assert [clause["id"] for clause in clauses] == [row["id"] for row in rows]
    assert all(clause["force"] == "mandatory" for clause in clauses)
    assert all(clause["text"].strip() for clause in clauses)
    assert all(clause["expectedOutputs"] for clause in clauses)
    assert all(
        _applicability_spec(clause.get("applicability")) == row["applicability"]
        for clause, row in zip(clauses, rows, strict=True)
    )
    assert all(
        clause["expectedOutputs"] == row["outputs"].split(", ")
        for clause, row in zip(clauses, rows, strict=True)
    )
    used = {output for clause in clauses for output in clause["expectedOutputs"]}
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}
    evaluation = evaluate_clause_set(PACKAGE_ROOT, _spec_set_key("gdpr"))
    assert [item["clauseId"] for item in evaluation["clauses"]] == [
        row["id"] for row in rows
    ]
    assert all(
        item["outcome"] in {"binding", "unresolved"} for item in evaluation["clauses"]
    )


@pytest.mark.trace(
    "FR-011-AC-1", "FR-011-AC-2", "FR-011-AC-3", "FR-011-AC-4", "FR-011-AC-5"
)
def test_gdpr_person_supplied_applicability_contexts():
    """Evaluate controller, processor, risk, and records applicability cases.

    Assumptions: Context dimensions are supplied by a responsible person.
    Criteria: Evaluation uses only the supplied values and checks the role-
    specific Article 30 outcomes when records applicability is absent.
    Trace: FR-011-AC-1, FR-011-AC-2, FR-011-AC-3, FR-011-AC-4, FR-011-AC-5
    """
    key = _spec_set_key("gdpr")
    controller = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            key,
            "gdpr_role=controller",
            "high_risk_processing=yes",
            "article_30_records_applicability=applies",
        )
    )
    processor = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            key,
            "gdpr_role=processor",
            "article_30_records_applicability=applies",
        )
    )
    controller_low_risk = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            key,
            "gdpr_role=controller",
            "high_risk_processing=no",
            "article_30_records_applicability=applies",
        )
    )
    empty = _outcomes(evaluate_clause_set(PACKAGE_ROOT, key))
    assert all(
        controller[item["id"]]
        == ("not_binding" if item["id"].startswith("art-30(2)") else "binding")
        for item in _spec_gdpr_rows()
    )
    assert all(processor[f"art-30(2)({letter})"] == "binding" for letter in "abcd")
    assert all(processor[f"art-32(1)({letter})"] == "binding" for letter in "abcd")
    assert all(
        processor[clause_id] == "not_binding"
        for clause_id in processor
        if clause_id.startswith(("art-25", "art-30(1)", "art-35"))
    )
    assert all(
        controller_low_risk[f"art-35({part})"] == "not_binding"
        for part in ("1", "2", "7)(a", "7)(b", "7)(c", "7)(d", "9", "11")
    )
    assert all(
        controller_low_risk[clause_id] == "binding"
        for clause_id in controller_low_risk
        if clause_id.startswith(("art-25", "art-30(1)", "art-32"))
    )
    assert all(empty[f"art-32(1)({letter})"] == "binding" for letter in "abcd")
    assert all(
        empty[clause_id] == "unresolved"
        for clause_id in empty
        if clause_id.startswith(("art-25", "art-30", "art-35"))
    )
    assert all(
        empty[clause_id] == "unresolved"
        for clause_id in empty
        if clause_id.startswith("art-30")
    )
    for role in ("controller", "processor"):
        missing_records = _outcomes(
            evaluate_clause_set(PACKAGE_ROOT, key, f"gdpr_role={role}")
        )
        controller = role == "controller"
        assert all(
            missing_records[f"art-30(1)({letter})"]
            == ("unresolved" if controller else "not_binding")
            for letter in "abcdefg"
        )
        assert all(
            missing_records[f"art-30(2)({letter})"]
            == ("not_binding" if controller else "unresolved")
            for letter in "abcd"
        )
        assert missing_records["art-30(3)"] == "unresolved"
        assert missing_records["art-30(4)"] == "unresolved"
    for role in ("controller", "processor"):
        exempt = _outcomes(
            evaluate_clause_set(
                PACKAGE_ROOT,
                key,
                f"gdpr_role={role}",
                "high_risk_processing=no",
                "article_30_records_applicability=exempt",
            )
        )
        assert all(
            exempt[cid] == "not_binding" for cid in exempt if cid.startswith("art-30")
        )
        applied = _outcomes(
            evaluate_clause_set(
                PACKAGE_ROOT,
                key,
                f"gdpr_role={role}",
                "high_risk_processing=no",
                "article_30_records_applicability=applies",
            )
        )
        assert applied["art-30(3)"] == applied["art-30(4)"] == "binding"
        role_paragraph = "1" if role == "controller" else "2"
        letters = "abcdefg" if role == "controller" else "abcd"
        assert all(
            applied[f"art-30({role_paragraph})({letter})"] == "binding"
            for letter in letters
        )


@pytest.mark.trace("FR-022-AC-1", "FR-022-AC-2")
def test_ai_act_set_identity_rights_and_application_date():
    """Check the AI Act set's source metadata and dated legal scope.

    Assumptions: The consolidated EUR-Lex source and rights terms are declared
    in spec.md.
    Criteria: Set identity and rights match the declared source, and the
    Article 113 application-date metadata is present and exact.
    """
    clause_set = _ai_act_set()
    assert clause_set_key(clause_set) == "eu/ai-act-2024-1689@2026-07-27"
    _assert_set_metadata_matches_spec(clause_set)
    assert clause_set["source"]["applicationDate"] == {
        "date": "2028-08-02",
        "source": "Article 113",
        "scope": "Article 6(1) Annex I high-risk AI systems; Chapter III Sections 1–3",
    }
    broken = json.loads(json.dumps(clause_set))
    broken["source"]["applicationDate"]["date"] = "2028-08-03"
    with pytest.raises(AssertionError, match="Article 113 application date"):
        assert (
            broken["source"]["applicationDate"]["date"] == "2028-08-02"
        ), "Article 113 application date must be 2028-08-02"


@pytest.mark.trace("FR-017-AC-2", "FR-017-AC-3", "FR-017-AC-4")
def test_ai_act_clause_ids_applicability_and_outputs_match_the_spec():
    """Check exact AI Act obligations and their declared output catalog.

    Assumptions: The AI Act High-Risk Obligations Table is normative.
    Criteria: Every listed clause matches its force, applicability, outputs,
    and catalog entries, with no out-of-scope clause present.
    """
    clause_set = _ai_act_set()
    clauses = clause_set["clauses"]
    _assert_ai_act_clause_fields(clause_set)
    used = {output for clause in clauses for output in clause["expectedOutputs"]}
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}
    assert set(clause_set["classificationDimensions"]) == {"ai_high_risk", "ai_role"}
    assert not {"art-21", "art-22", "art-23", "art-24", "art-49"}.intersection(
        clause["id"] for clause in clauses
    )
    for field, value in (
        ("applicability", {"op": "eq", "dimension": "ai_role", "value": "provider"}),
        ("force", "recommended"),
        ("expectedOutputs", ["undeclared-output"]),
    ):
        broken = json.loads(json.dumps(clause_set))
        broken["clauses"][0][field] = value
        with pytest.raises(AssertionError, match=rf"art-9\.{field}"):
            _assert_ai_act_clause_fields(broken)
    result = run(engine_tool("quire"), "publish-check", "--module", str(PACKAGE_ROOT))
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.trace("FR-017-AC-1")
def test_ai_act_provider_and_deployer_applicability_is_person_supplied():
    """Evaluate high-risk, role, and missing-context outcomes independently.

    Assumptions: A person supplies the AI Act classification and operator role.
    Criteria: Only the matching provider or deployer obligations bind, known
    low-risk systems bind none, and missing context leaves every clause
    unresolved.
    """
    key = "eu/ai-act-2024-1689@2026-07-27"
    rows = _spec_ai_act_rows()
    low_risk = _outcomes(evaluate_clause_set(PACKAGE_ROOT, key, "ai_high_risk=no"))
    provider = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, key, "ai_high_risk=yes", "ai_role=provider")
    )
    deployer = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, key, "ai_high_risk=yes", "ai_role=deployer")
    )
    empty = _outcomes(evaluate_clause_set(PACKAGE_ROOT, key))
    assert (
        set(low_risk)
        == set(provider)
        == set(deployer)
        == set(empty)
        == {row["id"] for row in rows}
    )
    assert set(low_risk.values()) == {"not_binding"}
    assert all(
        provider[row["id"]] == ("not_binding" if row["id"] == "art-26" else "binding")
        for row in rows
    )
    assert all(
        deployer[row["id"]] == ("binding" if row["id"] == "art-26" else "not_binding")
        for row in rows
    )
    assert set(empty.values()) == {"unresolved"}


@pytest.mark.trace("FR-016-AC-1", "FR-016-AC-2", "FR-016-AC-3")
def test_ai_act_sets_share_exact_identity_source_and_rights_metadata():
    """Check both declared AI Act sets against the master source metadata.

    Assumptions: Both set identities and EUR-Lex reuse details are normative in
    spec.md.
    Criteria: Each key and file appears exactly once, both sets carry the exact
    source and rights fields, and injected field changes fail with field paths.
    """
    spec_sets = _parsed_spec_sets()["ai_act"]
    identities = [spec_sets["identity"], spec_sets["annex_identity"]]
    expected_keys = [_set_key(identity) for identity in identities]
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    ai_paths = [
        path
        for path in manifest["clause_sets"]
        if "ai-act-2024-1689" in pathlib.PurePosixPath(path).name
    ]
    assert len(ai_paths) == 2, f"AI Act clause files declared: {ai_paths}"
    loaded = {
        clause_set_key(clause_set): clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) in expected_keys
    }
    assert set(loaded) == set(expected_keys)
    for identity, key in zip(identities, expected_keys, strict=True):
        _, set_id, version = identity
        expected_path = f"clauses/eu-{set_id}-{version}.json"
        assert (
            manifest["clause_sets"].count(expected_path) == 1
        ), f"{key} must reference {expected_path} exactly once"
        clause_set = loaded[key]
        _assert_ai_act_set_metadata_matches_spec(clause_set, identity)

        field_changes = [
            ("authority", "example.invalid", "authority"),
            ("id", "changed", "id"),
            ("version", "2026-07-28", "version"),
            (
                "source",
                {
                    **clause_set["source"],
                    "officialUrl": "https://example.invalid/changed",
                },
                "source.officialUrl",
            ),
            (
                "rights",
                {**clause_set["rights"], "structure": "copied_text"},
                "rights.structure",
            ),
            ("rights", {**clause_set["rights"], "text": "licensed"}, "rights.text"),
            (
                "rights",
                {**clause_set["rights"], "clearance_ref": "missing"},
                "rights.clearance_ref",
            ),
            (
                "rights",
                {**clause_set["rights"], "licence": "changed"},
                "rights.licence",
            ),
            (
                "rights",
                {**clause_set["rights"], "attribution": "changed"},
                "rights.attribution",
            ),
        ]
        for field, value, target_field in field_changes:
            broken = json.loads(json.dumps(clause_set))
            broken[field] = value
            with pytest.raises(
                AssertionError, match=rf"{re.escape(key)}\.{re.escape(target_field)}"
            ):
                _assert_ai_act_set_metadata_matches_spec(broken, identity)


@pytest.mark.trace("FR-018-AC-1", "FR-018-AC-2", "FR-018-AC-4", "FR-019-AC-5")
def test_ai_act_annex_rows_match_the_normative_table():
    """Check Annex IV identity, exact rows, outputs, and context dimensions.

    Assumptions: The Annex IV table and output catalog in spec.md are normative.
    Criteria: All point IDs, applicability expressions, outputs, and allowed
    dimensions match, while injected row changes identify their field.
    """
    clause_set = _ai_act_annex_set()
    rows = _spec_ai_act_annex_rows()
    _assert_ai_act_annex_clause_fields(clause_set)
    point_dimensions = {_ai_act_annex_dimension(row["id"]) for row in rows}
    common_dimensions = {"ai_high_risk", "ai_role"}
    assert len(point_dimensions) == 23
    assert set(clause_set["classificationDimensions"]) == (
        common_dimensions | point_dimensions
    )
    assert set(_ai_act_set()["classificationDimensions"]) == common_dimensions
    for dimension in point_dimensions:
        assert clause_set["classificationDimensions"][dimension] == {
            "values": ["yes", "no"]
        }, f"{dimension} must be a person-supplied yes/no value"

    broken = json.loads(json.dumps(clause_set))
    broken["clauses"].pop(0)
    with pytest.raises(AssertionError, match=r"missing=\['IV-1\(a\)'\]"):
        _assert_ai_act_annex_clause_fields(broken)

    broken = json.loads(json.dumps(clause_set))
    broken["clauses"][0]["id"] = "IV-1(a)-extra"
    with pytest.raises(
        AssertionError,
        match=r"missing=\['IV-1\(a\)'\], extra=\['IV-1\(a\)-extra'\]",
    ):
        _assert_ai_act_annex_clause_fields(broken)

    broken = json.loads(json.dumps(clause_set))
    broken["clauses"][0]["applicability"]["terms"][2]["value"] = "no"
    with pytest.raises(AssertionError, match=r"IV-1\(a\)\.applicability"):
        _assert_ai_act_annex_clause_fields(broken)

    broken = json.loads(json.dumps(clause_set))
    broken["clauses"][0]["expectedOutputs"] = ["missing-output"]
    with pytest.raises(AssertionError, match=r"IV-1\(a\)\.expectedOutputs"):
        _assert_ai_act_annex_clause_fields(broken)


def test_ai_act_annex_point_seven_has_no_standards_designator(tmp_path):
    """Run the publication rights scanner on the generic point-seven summary.

    Assumptions: The engineering-assurance content-rights-tree command is on
    PATH in the validation environment.
    Criteria: The point-seven summary has no protected external designator.
    """
    executable = shutil.which("engineering-assurance")
    assert executable is not None, "engineering-assurance CLI is unavailable"
    point_seven = next(
        clause for clause in _ai_act_annex_set()["clauses"] if clause["id"] == "IV-7"
    )
    (tmp_path / "point-seven.json").write_text(
        json.dumps({"text": point_seven["text"]})
    )
    initialized = run("git", "init", "--quiet", "-b", "main", cwd=tmp_path)
    assert initialized.returncode == 0, initialized.stderr
    selected = run("git", "add", "--all", cwd=tmp_path)
    assert selected.returncode == 0, selected.stderr
    scanned = run(
        executable,
        "content-rights-tree",
        "--root",
        str(tmp_path),
        cwd=tmp_path,
    )
    assert scanned.returncode == 0, scanned.stderr + scanned.stdout
    report = json.loads(scanned.stdout)
    assert report["outcome"] == "accepted"
    assert report["findings"] == []


@pytest.mark.trace(
    "FR-018-AC-3", "FR-019-AC-1", "FR-019-AC-2", "FR-019-AC-3", "FR-019-AC-4"
)
def test_ai_act_annex_applicability_is_person_supplied_and_independent():
    """Evaluate every Annex IV point with yes, no, and omitted person inputs.

    Assumptions: High-risk classification, role, and point applicability are
    supplied explicitly as contexts.
    Criteria: Both sets follow low-risk, provider, deployer, empty, and partial
    context rules; each Annex IV point resolves only from its own value.
    """
    high_risk_key = "eu/ai-act-2024-1689@2026-07-27"
    annex_key = "eu/ai-act-2024-1689-annex-iv@2026-07-27"
    rows = _spec_ai_act_annex_rows()
    point_dimensions = [
        dimension
        for dimension in _ai_act_annex_set()["classificationDimensions"]
        if dimension not in {"ai_high_risk", "ai_role"}
    ]
    assert len(point_dimensions) == len(rows) == 23
    all_yes = [f"{dimension}=yes" for dimension in point_dimensions]
    all_no = [f"{dimension}=no" for dimension in point_dimensions]

    low_risk_high_risk = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, high_risk_key, "ai_high_risk=no")
    )
    low_risk_annex = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, annex_key, "ai_high_risk=no")
    )
    assert set(low_risk_high_risk.values()) == {"not_binding"}
    assert set(low_risk_annex.values()) == {"not_binding"}

    provider_high_risk = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            high_risk_key,
            "ai_high_risk=yes",
            "ai_role=provider",
        )
    )
    provider_annex = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            annex_key,
            "ai_high_risk=yes",
            "ai_role=provider",
            *all_yes,
        )
    )
    assert set(provider_high_risk) == {row["id"] for row in _spec_ai_act_rows()}
    assert all(
        outcome == ("not_binding" if clause_id == "art-26" else "binding")
        for clause_id, outcome in provider_high_risk.items()
    )
    assert set(provider_annex) == {row["id"] for row in rows}
    assert set(provider_annex.values()) == {"binding"}

    for point in point_dimensions:
        other_yes = [
            f"{dimension}=yes" for dimension in point_dimensions if dimension != point
        ]
        not_applicable = _outcomes(
            evaluate_clause_set(
                PACKAGE_ROOT,
                annex_key,
                "ai_high_risk=yes",
                "ai_role=provider",
                *other_yes,
                f"{point}=no",
            )
        )
        omitted = _outcomes(
            evaluate_clause_set(
                PACKAGE_ROOT,
                annex_key,
                "ai_high_risk=yes",
                "ai_role=provider",
                *other_yes,
            )
        )
        clause_id = next(
            row["id"] for row in rows if point == _ai_act_annex_dimension(row["id"])
        )
        assert not_applicable[clause_id] == "not_binding", f"{clause_id} for {point}=no"
        assert all(
            outcome == "binding"
            for other_id, outcome in not_applicable.items()
            if other_id != clause_id
        ), f"{clause_id} leaked its point decision to another clause"
        assert (
            omitted[clause_id] == "unresolved"
        ), f"{clause_id} when {point} is omitted"
        assert all(
            outcome == "binding"
            for other_id, outcome in omitted.items()
            if other_id != clause_id
        ), f"{clause_id} omission changed another point"

    deployer_high_risk = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            high_risk_key,
            "ai_high_risk=yes",
            "ai_role=deployer",
        )
    )
    deployer_annex_yes = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            annex_key,
            "ai_high_risk=yes",
            "ai_role=deployer",
            *all_yes,
        )
    )
    deployer_annex_no = _outcomes(
        evaluate_clause_set(
            PACKAGE_ROOT,
            annex_key,
            "ai_high_risk=yes",
            "ai_role=deployer",
            *all_no,
        )
    )
    assert deployer_high_risk["art-26"] == "binding"
    assert all(
        value == "not_binding"
        for key, value in deployer_high_risk.items()
        if key != "art-26"
    )
    assert set(deployer_annex_yes.values()) == {"not_binding"}
    assert set(deployer_annex_no.values()) == {"not_binding"}

    empty_high_risk = _outcomes(evaluate_clause_set(PACKAGE_ROOT, high_risk_key))
    empty_annex = _outcomes(evaluate_clause_set(PACKAGE_ROOT, annex_key))
    assert set(empty_high_risk.values()) == {"unresolved"}
    assert set(empty_annex.values()) == {"unresolved"}

    missing_high_risk = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, annex_key, "ai_role=provider", *all_yes)
    )
    assert set(missing_high_risk.values()) == {"unresolved"}
    missing_role = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, annex_key, "ai_high_risk=yes", *all_yes)
    )
    assert set(missing_role.values()) == {"unresolved"}


@pytest.mark.trace("FR-008-AC-2")
def test_mdr_single_set_discharge_renders_expected_rows(tmp_path):
    """Render a matrix with one discharged and one open MDR clause.

    Assumptions: The temporary evidence store starts empty.
    Criteria: I-17.2 is compliant and I-18.8 remains undischarged.
    Trace: FR-008-AC-2
    """
    rendered = record_and_render_matrix(
        tmp_path, PACKAGE_ROOT, _spec_set_key("mdr"), clause_id="I-17.2"
    )
    assert rendered.returncode == 0, rendered.stderr + rendered.stdout
    assert "| I-17.2 | Applicable | Compliant |" in rendered.stdout
    assert "| I-18.8 | Applicable | Not compliant - undischarged:" in rendered.stdout


@pytest.mark.trace("FR-006-AC-2")
def test_catalog_mismatch_error_names_both_sets():
    """Name both source sets when a shared output definition changes.

    Assumptions: Two synthetic sets declare the same output key.
    Criteria: A kind mismatch raises an assertion naming both set keys.
    """
    sets = [
        _synthetic_set(
            "example.invalid",
            "first",
            "1.0.0",
            output_catalog={"audit-trail": {"kind": "record", "description": "Log."}},
        ),
        _synthetic_set(
            "example.invalid",
            "second",
            "1.0.0",
            output_catalog={
                "audit-trail": {"kind": "procedure", "description": "Log."}
            },
        ),
    ]
    with pytest.raises(
        AssertionError,
        match=r"example.invalid/first@1.0.0.*example.invalid/second@1.0.0",
    ):
        assert_output_catalog_consistent(sets)


@pytest.mark.trace("FR-005-AC-2")
def test_crosswalk_error_names_source_clause_and_missing_target_key(tmp_path):
    """Name the source clause and target set when a crosswalk target is absent.

    Assumptions: The synthetic source references a loaded target set whose
    clause list does not contain the requested clause.
    Criteria: The consistency check fails with both identifiers in its error.
    """
    target = _synthetic_set(
        "example.invalid",
        "target",
        "1.0.0",
        clauses=[{"id": "present", "force": "mandatory", "title": "Present"}],
    )
    dependency = stage_clause_sets(tmp_path, target)
    home = tmp_path / "dependency-home"
    config_root = tmp_path / "dependency-config"
    home.mkdir()
    config_root.mkdir()
    env = {**os.environ, "HOME": str(home), "IX_CONFIG_ROOT": str(config_root)}
    installed = run(
        engine_tool("quoin"), "module", "install", f"path:{dependency}", env=env
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    source = _synthetic_set(
        "example.invalid",
        "source",
        "1.0.0",
        clauses=[{"id": "source-clause"}],
        crosswalks=[
            {
                "sourceClause": "source-clause",
                "target": {
                    "set": {
                        "authority": "example.invalid",
                        "id": "target",
                        "version": "1.0.0",
                    },
                    "clause": "missing",
                },
                "relation": "informative",
                "rationale": "Synthetic fixture.",
            }
        ],
    )
    with pytest.raises(
        AssertionError,
        match=r"source-clause.*example.invalid/target@1.0.0#missing",
    ):
        assert_crosswalk_targets_resolve([source], env=env)


def test_crosswalk_to_a_loaded_clause_resolves(tmp_path):
    """Accept a crosswalk whose external target clause is loaded.

    Assumptions: The target set and clause are included in the loaded module.
    Criteria: The crosswalk resolver returns without an error.
    """
    target = _synthetic_set(
        "example.invalid",
        "target",
        "1.0.0",
        clauses=[{"id": "present", "force": "mandatory", "title": "Present"}],
    )
    dependency = stage_clause_sets(tmp_path, target)
    home = tmp_path / "dependency-home"
    config_root = tmp_path / "dependency-config"
    home.mkdir()
    config_root.mkdir()
    env = {**os.environ, "HOME": str(home), "IX_CONFIG_ROOT": str(config_root)}
    installed = run(
        engine_tool("quoin"), "module", "install", f"path:{dependency}", env=env
    )
    assert installed.returncode == 0, installed.stderr + installed.stdout
    source = _synthetic_set(
        "example.invalid",
        "source",
        "1.0.0",
        clauses=[{"id": "source-clause"}],
        crosswalks=[
            {
                "sourceClause": "source-clause",
                "target": {
                    "set": {
                        "authority": "example.invalid",
                        "id": "target",
                        "version": "1.0.0",
                    },
                    "clause": "present",
                },
                "relation": "informative",
                "rationale": "Synthetic fixture.",
            }
        ],
    )
    assert_crosswalk_targets_resolve([source], env=env)


def test_clause_files_ship_in_wheel_and_npm_tarball(tmp_path):
    """Build both distributions and inspect their declared clause resources.

    Assumptions: A synthetic JSON set is added to a disposable project copy so
    this packaging test cannot pass with an empty manifest.
    Criteria: The manifest and every declared clause file are present in both
    the wheel and npm tarball.
    """
    project = tmp_path / "project"
    shutil.copytree(
        REPO_ROOT,
        project,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            "node_modules",
            "target",
            "dist",
            "build",
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
            "report.json",
            ".coverage",
        ),
    )
    package_root = project / "spec_clauses_eu_law"
    clause_file = package_root / "clauses" / "synthetic.json"
    synthetic = _synthetic_set("example.invalid", "synthetic", "1.0.0")
    clause_file.write_text(json.dumps(synthetic))
    manifest_path = package_root / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest["clause_sets"] = ["clauses/synthetic.json"]
    manifest_path.write_text(yaml.safe_dump(manifest))

    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    wheel = run(
        "poetry",
        "build",
        "--format",
        "wheel",
        "--output",
        str(wheel_dir),
        cwd=project,
    )
    assert wheel.returncode == 0, wheel.stderr + wheel.stdout
    wheel_path = next(wheel_dir.glob("*.whl"))
    with zipfile.ZipFile(wheel_path) as archive:
        wheel_files = set(archive.namelist())
    assert "spec_clauses_eu_law/manifest.yaml" in wheel_files
    assert "spec_clauses_eu_law/clauses/synthetic.json" in wheel_files

    npm_dir = tmp_path / "npm"
    npm_dir.mkdir()
    packed = run(
        "npm",
        "pack",
        "--json",
        "--pack-destination",
        str(npm_dir),
        cwd=project,
    )
    assert packed.returncode == 0, packed.stderr + packed.stdout
    tarball = next(npm_dir.glob("*.tgz"))
    with tarfile.open(tarball, "r:gz") as archive:
        npm_files = set(archive.getnames())
    assert "package/manifest.yaml" in npm_files
    assert "package/clauses/synthetic.json" in npm_files
