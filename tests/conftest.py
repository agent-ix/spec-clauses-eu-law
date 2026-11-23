"""Helpers for the EU clause-only module tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_clauses_eu_law"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"


def engine_tool(name: str) -> str:
    """Find an engine CLI, preferring this repository's npm install."""
    local = REPO_ROOT / "node_modules" / ".bin" / name
    path = str(local) if local.exists() else shutil.which(name)
    if path is None:
        raise AssertionError(f"the `{name}` CLI is unavailable on PATH")
    return path


def run(*args: str, **kwargs) -> subprocess.CompletedProcess:
    """Run a command with captured output for direct acceptance assertions."""
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def load_clause_sets(manifest_path: pathlib.Path = MANIFEST_PATH) -> list[dict]:
    """Load every clause set listed in a module manifest."""
    manifest = yaml.safe_load(manifest_path.read_text())
    module_root = manifest_path.parent
    return [
        json.loads((module_root / relative_path).read_text())
        for relative_path in manifest.get("clause_sets", [])
    ]


def clause_set_key(clause_set: dict) -> str:
    """Return the stable key used to identify one clause set."""
    return f"{clause_set['authority']}/{clause_set['id']}@{clause_set['version']}"


def evaluate_clause_set(module_root: pathlib.Path, key: str, *context: str) -> dict:
    """Evaluate a clause set with the installed Quire CLI."""
    authority, remainder = key.split("/", 1)
    set_id, version = remainder.split("@", 1)
    args = [
        engine_tool("quire"),
        "clauses",
        "evaluate",
        "--module",
        str(module_root),
        "--authority",
        authority,
        "--set",
        set_id,
        "--version",
        version,
        "--json",
    ]
    for entry in context:
        args.extend(["--context", entry])
    result = run(*args)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


def record_and_render_matrix(
    tmp_path: pathlib.Path,
    module_root: pathlib.Path,
    key: str,
    *context: str,
    clause_id: str,
) -> subprocess.CompletedProcess:
    """Record one synthetic direct fact and render its requirements matrix."""
    binding = evaluate_clause_set(module_root, key, *context)
    binding_path = tmp_path / "binding.json"
    binding_path.write_text(json.dumps(binding))
    facts_path = tmp_path / "facts.json"
    facts_path.write_text(
        json.dumps(
            [
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": ["evidence://example.invalid/run/one"],
                    "attestation": {
                        "attestedBy": "reviewer",
                        "authority": "quality-lead",
                        "attestedAt": "2026-11-14T00:00:00Z",
                        "expiresAt": "2027-11-14T00:00:00Z",
                    },
                }
            ]
        )
    )
    repo = tmp_path / "evidence-store"
    repo.mkdir()
    recorded = run(
        engine_tool("quoin"),
        "evidence",
        "record-discharge",
        "--repo",
        str(repo),
        "--binding",
        str(binding_path),
        "--facts",
        str(facts_path),
    )
    assert recorded.returncode == 0, recorded.stderr + recorded.stdout
    return run(
        engine_tool("quoin"),
        "discharge",
        "--binding",
        str(binding_path),
        "--rmm",
        "--repo",
        str(repo),
        "--as-of",
        "2026-11-15T00:00:00Z",
    )


def stage_clause_sets(tmp_path: pathlib.Path, *clause_sets: dict) -> pathlib.Path:
    """Create a temporary module containing the supplied synthetic sets."""
    module_root = tmp_path / "module"
    clauses_dir = module_root / "clauses"
    clauses_dir.mkdir(parents=True)
    paths = []
    for index, clause_set in enumerate(clause_sets):
        path = clauses_dir / f"set-{index}.json"
        path.write_text(json.dumps(clause_set))
        paths.append(path.relative_to(module_root).as_posix())
    manifest = {
        "manifest_version": "1.0.0",
        "name": "synthetic-eu-module",
        "version": "0.0.1",
        "clause_sets": paths,
    }
    (module_root / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    return module_root


def assert_output_catalog_consistent(clause_sets: list[dict]) -> None:
    """Reject output definitions that vary between clause sets."""
    definitions: dict[str, tuple[dict, dict]] = {}
    for clause_set in clause_sets:
        current_key = clause_set_key(clause_set)
        for output, definition in clause_set.get("outputCatalog", {}).items():
            previous = definitions.get(output)
            if previous and previous[1] != definition:
                previous_key = clause_set_key(previous[0])
                raise AssertionError(
                    f"output {output!r} differs between "
                    f"{previous_key} and {current_key}"
                )
            definitions[output] = (clause_set, definition)


def _installed_clause_set(target_key: str, env: dict | None = None) -> dict | None:
    """Find a clause set by key in any Quoin-installed dependency module."""
    listed = run(engine_tool("quoin"), "module", "list", env=env)
    assert listed.returncode == 0, listed.stderr + listed.stdout
    for module in json.loads(listed.stdout)["plugins"]:
        manifest_path = pathlib.Path(module["targetPath"]) / "manifest.yaml"
        if not manifest_path.is_file():
            continue
        manifest = yaml.safe_load(manifest_path.read_text())
        module_root = manifest_path.parent
        for relative_path in manifest.get("clause_sets", []):
            path = module_root / relative_path
            clause_set = json.loads(path.read_text())
            if clause_set_key(clause_set) == target_key:
                return clause_set
    return None


def assert_crosswalk_targets_resolve(
    clause_sets: list[dict], env: dict | None = None
) -> None:
    """Require crosswalk targets in the module or installed dependencies."""
    by_key = {clause_set_key(clause_set): clause_set for clause_set in clause_sets}
    for clause_set in clause_sets:
        source_key = clause_set_key(clause_set)
        for crosswalk in clause_set.get("crosswalks", []):
            target = crosswalk["target"]
            target_set = target["set"]
            target_key = (
                f"{target_set['authority']}/{target_set['id']}@{target_set['version']}"
            )
            if target_key == source_key:
                target_clauses = clause_set.get("clauses", [])
            else:
                target_clause_set = by_key.get(target_key)
                if target_clause_set is None:
                    target_clause_set = _installed_clause_set(target_key, env)
                if target_clause_set is None:
                    raise AssertionError(
                        f"crosswalk from {source_key}#{crosswalk['sourceClause']} "
                        f"targets clause set {target_key}, which is neither loaded "
                        f"nor installed"
                    )
                target_clauses = target_clause_set.get("clauses", [])
            if not any(clause["id"] == target["clause"] for clause in target_clauses):
                raise AssertionError(
                    f"crosswalk from {source_key}#{crosswalk['sourceClause']} "
                    f"targets missing clause {target_key}#{target['clause']}"
                )
