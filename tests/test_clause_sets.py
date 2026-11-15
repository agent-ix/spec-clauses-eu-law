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

MDR_KEY = "eu/mdr-2017-745@2026-07-19"


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


def _spec_set_metadata() -> dict[str, dict[str, object]]:
    """Read canonical set metadata values and identifiers from spec.md."""
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
        r"version `([^`]+)`, with source `([^`]+)`.*?"
        r"Licence metadata SHALL state that (.+?)\. "
        r"Attribution SHALL identify the (.+?), and the official PDF URL",
        design,
        re.DOTALL,
    )
    assert (
        mdcg
    ), "spec.md must declare the MDCG identity, source, licence, and attribution"
    return {
        f"{mdr.group(1)}/{mdr.group(2)}@{mdr.group(3)}": {
            "officialUrl": mdr.group(4),
            "licence": mdr.group(5),
            "attribution": mdr.group(6).replace("<official URL>", mdr.group(4)),
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        },
        f"{mdcg.group(1)}/{mdcg.group(2)}@{mdcg.group(3)}": {
            "officialUrl": mdcg.group(4),
            "licence": mdcg.group(5),
            "attribution_terms": mdcg.group(6).replace("*", ""),
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
        assert (
            rights["licence"] == expected["licence"]
        ), f"{key}.rights.licence differs from spec.md"
    else:
        assert (
            expected["licence"].casefold() in rights["licence"].casefold()
        ), f"{key}.rights.licence omits its source-specific spec statement"
    if "attribution" in expected:
        assert (
            rights["attribution"] == expected["attribution"]
        ), f"{key}.rights.attribution differs from spec.md"
    else:
        for term in (
            *expected["attribution_terms"].split(", "),
            expected["officialUrl"],
            "Agent-IX",
        ):
            assert (
                term in rights["attribution"]
            ), f"{key}.rights.attribution omits {term!r} from spec.md"
    assert (
        clause_set["source"]["officialUrl"] == expected["officialUrl"]
    ), f"{key}.source.officialUrl differs from spec.md"


def _mdr_set() -> dict:
    """Return the declared MDR set."""
    return next(
        clause_set
        for clause_set in load_clause_sets()
        if clause_set_key(clause_set) == MDR_KEY
    )


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


def test_manifest_is_clause_only_and_declares_the_mdr_set():
    """Verify the module declares the first EU clause set.

    Assumptions: The scaffold is extended with MDR content.
    Criteria: The manifest declares the MDR file and no non-clause module
    contributions.
    """
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["clause_sets"] == ["clauses/eu-mdr-2017-745-2026-07-19.json"]
    assert not {"object_types", "archetypes", "edges"}.intersection(manifest)
    assert manifest["name"] == "spec_clauses_eu_law"


def test_quire_validates_the_module_and_spec_bundle():
    """Validate the empty module and its specification documents.

    Assumptions: The installed ISO artifacts module supplies validation
    schemas.
    Criteria: Quire exits successfully for the EU module and spec documents.
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
    Trace: FR-001-AC-2
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
    evaluation = evaluate_clause_set(PACKAGE_ROOT, MDR_KEY)
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

    no_context = _outcomes(evaluate_clause_set(PACKAGE_ROOT, MDR_KEY))
    mobile_no = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, MDR_KEY, "mobile_platform=no")
    )
    mobile_yes = _outcomes(
        evaluate_clause_set(PACKAGE_ROOT, MDR_KEY, "mobile_platform=yes")
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
    assert {clause_set_key(item) for item in clause_sets} <= set(expected)
    for clause_set in clause_sets:
        _assert_set_metadata_matches_spec(clause_set)

    # Prove changed values name the affected set and field for every set.
    for clause_set in clause_sets:
        key = re.escape(clause_set_key(clause_set))
        broken = json.loads(json.dumps(clause_set))
        broken["rights"]["licence"] = "changed"
        with pytest.raises(AssertionError, match=rf"{key}\.rights\.licence"):
            _assert_set_metadata_matches_spec(broken)

        broken = json.loads(json.dumps(clause_set))
        broken["source"]["officialUrl"] = "https://example.invalid/changed"
        with pytest.raises(AssertionError, match=rf"{key}\.source\.officialUrl"):
            _assert_set_metadata_matches_spec(broken)


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
    clause_path = module_root / "clauses/eu-mdr-2017-745-2026-07-19.json"
    licensed = json.loads(clause_path.read_text())
    licensed["rights"]["text"] = "licensed"
    clause_path.write_text(json.dumps(licensed))
    refused = run(engine_tool("quire"), "publish-check", "--module", str(module_root))
    assert refused.returncode == 2
    assert MDR_KEY in refused.stderr + refused.stdout


@pytest.mark.trace("FR-006-AC-1")
def test_mdr_declares_the_spec_catalog_subset_used_by_its_clauses():
    """Check that the MDR set uses only its exact catalog subset.

    Assumptions: The EU catalog table in spec.md is canonical.
    Criteria: Each referenced output is declared with the exact catalog
    definition, and the set has no unused output entry.
    Trace: FR-006-AC-1
    """
    clause_set = _mdr_set()
    used = {
        output
        for clause in clause_set["clauses"]
        for output in clause["expectedOutputs"]
    }
    catalog = _spec_output_catalog()
    assert clause_set["outputCatalog"] == {name: catalog[name] for name in sorted(used)}


@pytest.mark.trace("FR-008-AC-2")
def test_mdr_single_set_discharge_renders_expected_rows(tmp_path):
    """Render a matrix with one discharged and one open MDR clause.

    Assumptions: The temporary evidence store starts empty.
    Criteria: I-17.2 is compliant and I-18.8 remains undischarged.
    Trace: FR-008-AC-2
    """
    rendered = record_and_render_matrix(
        tmp_path, PACKAGE_ROOT, MDR_KEY, clause_id="I-17.2"
    )
    assert rendered.returncode == 0, rendered.stderr + rendered.stdout
    assert "| I-17.2 | Applicable | Compliant |" in rendered.stdout
    assert "| I-18.8 | Applicable | Not compliant - undischarged:" in rendered.stdout


@pytest.mark.trace("FR-006-AC-2")
def test_catalog_mismatch_error_names_both_sets():
    """Name both source sets when a shared output definition changes.

    Assumptions: Two synthetic sets declare the same output key.
    Criteria: A kind mismatch raises an assertion naming both set keys.
    Trace: FR-006-AC-2
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
    Trace: FR-005-AC-2
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
