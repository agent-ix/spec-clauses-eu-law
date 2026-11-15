"""Packaging and shared behavior for the EU law clause module."""

from __future__ import annotations

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
    """Load an optional installed module when checking shared catalog parity."""
    result = run(engine_tool("quoin"), "module", "list")
    assert result.returncode == 0, result.stderr + result.stdout
    plugins = json.loads(result.stdout)["plugins"]
    module = next((item for item in plugins if item["name"] == module_name), None)
    if module is None:
        return []
    manifest_path = pathlib.Path(module["targetPath"]) / "manifest.yaml"
    return load_clause_sets(manifest_path)


def test_manifest_declares_all_m1_clause_sets():
    """Verify the module declares its three M1 clause set files.

    Assumptions: The canonical set identities are declared in spec.md.
    Criteria: The manifest declares the matching MDR, MDCG, and GDPR clause files.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == [
        _spec_set_path("mdr"),
        _spec_set_path("mdcg"),
        _spec_set_path("gdpr"),
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
