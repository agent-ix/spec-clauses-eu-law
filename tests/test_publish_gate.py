"""Tests for EU package publication checks."""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile
from importlib.util import module_from_spec, spec_from_file_location

import pytest
import yaml
from conftest import REPO_ROOT, engine_tool, run

_publish_gate_spec = spec_from_file_location(
    "eu_publish_gate", REPO_ROOT / "scripts" / "publish_gate.py"
)
assert _publish_gate_spec and _publish_gate_spec.loader
_publish_gate = module_from_spec(_publish_gate_spec)
_publish_gate_spec.loader.exec_module(_publish_gate)
PROTOCOL = _publish_gate.PROTOCOL
scan_archive = _publish_gate.scan_archive


def _rights_tool() -> str:
    executable = shutil.which("engineering-assurance")
    assert executable is not None, "engineering-assurance CLI is unavailable"
    return executable


def _scan_tree(root: pathlib.Path) -> tuple[subprocess.CompletedProcess, dict]:
    initialized = run("git", "init", "--quiet", "-b", "main", cwd=root)
    assert initialized.returncode == 0, initialized.stderr
    added = run("git", "add", "--all", cwd=root)
    assert added.returncode == 0, added.stderr
    result = run(_rights_tool(), "content-rights-tree", "--root", str(root), cwd=root)
    assert result.stdout.strip(), result.stderr
    report = json.loads(result.stdout)
    assert report["protocol"] == PROTOCOL
    return result, report


def _write_module(root: pathlib.Path, *, rights_text: str) -> pathlib.Path:
    module = root / "module"
    clauses = module / "clauses"
    clauses.mkdir(parents=True)
    clause_set = {
        "schemaVersion": "clause-set-v1",
        "authority": "example.invalid",
        "id": "fixture",
        "title": "Synthetic publication fixture",
        "version": "1.0.0",
        "rights": {
            "structure": "citation_only",
            "text": rights_text,
            "clearance_ref": None,
            "licence": "Synthetic test fixture",
        },
        "source": {
            "title": "Synthetic source",
            "identifier": "example.invalid/source",
            "officialUrl": "https://example.invalid/source",
        },
        "outputCatalog": {},
        "clauses": [],
        "crosswalks": [],
    }
    (clauses / "fixture.json").write_text(json.dumps(clause_set))
    manifest = {
        "manifest_version": "1.0.0",
        "name": "synthetic_publish_fixture",
        "version": "0.0.1",
        "clause_sets": ["clauses/fixture.json"],
    }
    (module / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    return module


def test_publish_check_refuses_licensed_clause_set(tmp_path):
    module = _write_module(tmp_path, rights_text="licensed")
    result = run(engine_tool("quire"), "publish-check", "--module", str(module))
    assert result.returncode == 2
    assert "example.invalid/fixture@1.0.0" in result.stdout + result.stderr


def test_content_rights_tree_accepts_allowed_public_identifiers(tmp_path):
    (tmp_path / "allowed.txt").write_text(
        "Regulation (EU) 2017/745\n"
        "MDCG 2019-16 rev.1\n"
        "nist/sp800-53\n"
        "21 CFR 11.10\n"
    )
    result, report = _scan_tree(tmp_path)
    assert result.returncode == 0
    assert report["outcome"] == "accepted"
    assert report["findings"] == []


@pytest.mark.trace("NFR-001-AC-2")
def test_content_rights_tree_rejects_synthetic_designator_without_source_text(
    tmp_path,
):
    (tmp_path / "clauses").mkdir()
    (tmp_path / "clauses" / "synthetic.json").write_text(
        '{"text":"Synthetic fixture cites ISO 999999999"}\n'
    )
    result, report = _scan_tree(tmp_path)
    assert result.returncode == 1
    assert report["outcome"] == "withheld"
    assert report["findings"] == [
        {
            "path": "clauses/synthetic.json",
            "line": 1,
            "category": "external-publication-identifier",
        }
    ]
    assert "ISO 999999999" not in result.stdout
    assert "ISO 999999999" not in result.stderr


def test_scan_archive_runs_content_rights_over_wheel_and_npm_tree(tmp_path):
    wheel_tree = tmp_path / "wheel-tree"
    wheel_tree.mkdir()
    (wheel_tree / "spec_clauses_eu_law").mkdir()
    (wheel_tree / "spec_clauses_eu_law" / "manifest.yaml").write_text(
        "clause_sets: []\n"
    )
    (wheel_tree / "spec_clauses_eu_law-0.1.0.dist-info").mkdir()
    (wheel_tree / "spec_clauses_eu_law-0.1.0.dist-info" / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: spec-clauses-eu-law\nVersion: 0.1.0\n"
    )
    license_dir = wheel_tree / "spec_clauses_eu_law-0.1.0.dist-info" / "licenses"
    license_dir.mkdir()
    (license_dir / "LICENSE").write_text(
        "GNU Affero General Public License: https://www.gnu.org/licenses/agpl-3.0.html\n"
    )
    wheel = tmp_path / "fixture.whl"
    zipped = pathlib.Path(
        shutil.make_archive(str(wheel.with_suffix("")), "zip", wheel_tree)
    )
    zipped.rename(wheel)

    npm_tree = tmp_path / "npm-tree"
    (npm_tree / "package" / "clauses").mkdir(parents=True)
    (npm_tree / "package" / "manifest.yaml").write_text("clause_sets: []\n")
    (npm_tree / "package" / "clauses" / "allowed.json").write_text(
        '{"source":"Regulation (EU) 2017/745"}\n'
    )
    npm = tmp_path / "fixture.tgz"
    with tarfile.open(npm, "w:gz") as archive:
        archive.add(npm_tree / "package", arcname="package")

    assert scan_archive(tmp_path / "fixture.whl", _rights_tool()) == (True, [])
    assert scan_archive(npm, _rights_tool()) == (True, [])


@pytest.mark.trace("NFR-001-AC-2")
def test_scan_archive_checks_nonlicense_wheel_contents(tmp_path):
    wheel_tree = tmp_path / "wheel-tree"
    package = wheel_tree / "spec_clauses_eu_law"
    package.mkdir(parents=True)
    (package / "manifest.yaml").write_text("clause_sets: []\n")
    (package / "bad.json").write_text(
        '{"source":"Synthetic fixture cites ISO 999999999"}\n'
    )
    wheel = tmp_path / "fixture.whl"
    zipped = pathlib.Path(
        shutil.make_archive(str(wheel.with_suffix("")), "zip", wheel_tree)
    )
    zipped.rename(wheel)

    accepted, findings = scan_archive(wheel, _rights_tool())

    assert not accepted
    assert findings == [
        "spec_clauses_eu_law/bad.json:1: external-publication-identifier"
    ]


@pytest.mark.trace("NFR-001-AC-2")
def test_scan_archive_checks_clause_ignored_by_package_gitignore(tmp_path):
    npm_tree = tmp_path / "npm-tree"
    package = npm_tree / "package"
    clauses = package / "clauses"
    clauses.mkdir(parents=True)
    (package / ".gitignore").write_text("clauses/evil.json\n")
    (package / "manifest.yaml").write_text("clause_sets: []\n")
    (clauses / "evil.json").write_text(
        '{"text":"Synthetic fixture cites ISO 999999999"}\n'
    )
    npm = tmp_path / "fixture.tgz"
    with tarfile.open(npm, "w:gz") as archive:
        archive.add(package, arcname="package")

    accepted, findings = scan_archive(npm, _rights_tool())

    assert not accepted
    assert findings == ["package/clauses/evil.json:1: external-publication-identifier"]


def test_release_gate_accepts_freshly_built_wheel_and_npm_archive(tmp_path):
    """Run the release workflow's gate over the real wheel and npm archive."""
    dist = tmp_path / "dist"
    dist.mkdir()
    built = run(
        "poetry", "build", "--format", "wheel", "--output", str(dist), cwd=REPO_ROOT
    )
    assert built.returncode == 0, built.stderr
    environment = {**os.environ, "npm_config_userconfig": os.devnull}
    packed = subprocess.run(
        ["npm", "pack", "--pack-destination", str(dist)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=environment,
        check=False,
    )
    assert packed.returncode == 0, packed.stderr

    result = run(
        sys.executable,
        str(REPO_ROOT / "scripts" / "publish_gate.py"),
        "--module",
        str(REPO_ROOT / "spec_clauses_eu_law"),
        "--wheel-dir",
        str(dist),
        "--npm-dir",
        str(dist),
        "--engineering-assurance",
        _rights_tool(),
        "--quire",
        engine_tool("quire"),
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0, result.stderr
