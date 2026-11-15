"""End-to-end discharge checks for the MDR and MDCG reference corpus."""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
from urllib.parse import urlparse

import pytest
import yaml
from conftest import PACKAGE_ROOT, REPO_ROOT, engine_tool, load_clause_sets, run

CORPUS_ROOT = REPO_ROOT / "tests" / "corpus"
AS_OF = "2026-11-15T00:00:00Z"
OPEN_CLAUSES = {"eu/mdr-2017-745@2026-07-19": "I-18.8"}


def _checked(
    *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess:
    """Run a required tool and include the command in assertion failures."""
    result = run(*args, env=env)
    assert result.returncode == 0, (
        f"{args[0]} {' '.join(args[1:])} exited {result.returncode}:\n"
        f"{result.stderr}{result.stdout}"
    )
    return result


def _preflight() -> tuple[str, str, str]:
    """Require each executable and command capability used by this gate."""
    quire = engine_tool("quire")
    quoin = engine_tool("quoin")
    assurance = shutil.which("engineering-assurance")
    assert assurance is not None, "engineering-assurance executable is unavailable"
    checks = (
        (quire, "validate", "--help", "validate"),
        (quire, "clauses", "evaluate", "--help", "clauses evaluate"),
        (quoin, "evidence", "record-discharge", "--help", "record-discharge"),
        (quoin, "discharge", "--help", "--rmm", "--pack"),
        (assurance, "signature-verify", "--help", "signature-verify"),
    )
    for command in checks:
        result = run(*command[:-1])
        assert result.returncode == 0, (
            f"required capability {command[-1]!r} unavailable from {command[0]}: "
            f"exit {result.returncode}: {result.stderr}{result.stdout}"
        )
        if command[-1] in {"--rmm", "--pack"}:
            assert (
                command[-1] in result.stdout
            ), f"required capability {command[-1]!r} missing from {command[0]}"
    return quire, quoin, assurance


def _clause_set_key(clause_set: dict) -> str:
    """Return the canonical identity used by evaluation and the evidence store."""
    return f"{clause_set['authority']}/{clause_set['id']}@{clause_set['version']}"


def _clause_set_args(key: str) -> tuple[str, str, str]:
    """Split an exact clause-set identity into its CLI arguments."""
    authority, remainder = key.split("/", 1)
    set_id, version = remainder.split("@", 1)
    return authority, set_id, version


def _customer_owned_clauses(clause_set: dict) -> set[str]:
    """Find clauses whose declared outputs are all customer-owned procedures."""
    procedure_outputs = {
        name
        for name, output in clause_set.get("outputCatalog", {}).items()
        if output.get("kind") == "procedure"
    }
    if not procedure_outputs:
        return set()
    return {
        clause["id"]
        for clause in clause_set.get("clauses", [])
        if clause.get("expectedOutputs")
        and set(clause["expectedOutputs"]).issubset(procedure_outputs)
    }


def _assert_customer_owned_facts(clause_set: dict, facts: list[dict]) -> None:
    """Require delegated approvals for clauses owned by the customer."""
    owned = _customer_owned_clauses(clause_set)
    for fact in facts:
        if fact.get("clauseId") not in owned:
            continue
        assert (
            fact.get("kind") == "disposition"
        ), f"customer-owned clause {fact['clauseId']} cannot have a direct fact"
        assert (
            fact.get("decision") == "delegated"
        ), f"customer-owned clause {fact['clauseId']} requires delegated disposition"
        assert fact.get(
            "rationale", ""
        ).strip(), f"customer-owned clause {fact['clauseId']} requires rationale"
        assert fact.get(
            "approvalRef", ""
        ).strip(), f"customer-owned clause {fact['clauseId']} requires approvalRef"
        _assert_reserved_uri_authority(fact["approvalRef"])


def _resolve_evidence_ref(corpus: pathlib.Path, reference: str) -> pathlib.Path:
    """Resolve one synthetic evidence URL to a file under the corpus root."""
    parsed = urlparse(reference)
    assert parsed.scheme == "evidence", f"unsupported evidence scheme in {reference}"
    _assert_reserved_uri_authority(reference)
    path = (corpus / parsed.path.lstrip("/")).resolve()
    assert path.is_relative_to(
        corpus.resolve()
    ), f"evidence reference escapes corpus: {reference}"
    assert path.is_file(), f"evidence reference for clause is unresolved: {reference}"
    return path


def _assert_reserved_uri_authority(reference: str) -> None:
    """Require a synthetic URI to use the exact reserved example.invalid host."""
    parsed = urlparse(reference)
    assert parsed.scheme in {
        "evidence",
        "person",
    }, f"unsupported synthetic reference scheme in {reference}"
    assert (
        parsed.netloc == "example.invalid"
    ), f"synthetic reference authority must be exactly example.invalid: {reference}"


def _assert_fact_refs_resolve(corpus: pathlib.Path, facts: list[dict]) -> None:
    """Resolve every fact reference and name its clause on failure."""
    for fact in facts:
        for reference in fact.get("evidenceRefs", []):
            try:
                _resolve_evidence_ref(corpus, reference)
            except AssertionError as error:
                raise AssertionError(
                    f"clause {fact.get('clauseId')} has unresolved evidence "
                    f"reference {reference}: {error}"
                ) from error


def _report_clause_rows(value: object, clause_id: str) -> list[dict]:
    """Find structured RMM rows for one clause in a nested report value."""
    if isinstance(value, dict):
        matches = [value] if value.get("clauseId") == clause_id else []
        return matches + [
            row
            for child in value.values()
            for row in _report_clause_rows(child, clause_id)
        ]
    if isinstance(value, list):
        return [row for child in value for row in _report_clause_rows(child, clause_id)]
    return []


def _signed_corpus(tmp_path: pathlib.Path, assurance: str) -> pathlib.Path:
    """Sign the synthetic corpus at test time and retain verified outputs."""
    corpus = tmp_path / "corpus"
    shutil.copytree(CORPUS_ROOT, corpus)
    signing = tmp_path / "signing"
    signing.mkdir()
    key = signing / "signing-key"
    allowed_signers = signing / "allowed_signers"
    _checked(
        "ssh-keygen",
        "-q",
        "-t",
        "ed25519",
        "-N",
        "",
        "-C",
        "reviewer@example.invalid",
        "-f",
        str(key),
    )
    public_key = pathlib.Path(f"{key}.pub").read_text().split()
    allowed_signers.write_text(
        f"reviewer@example.invalid {public_key[0]} {public_key[1]}\n"
    )
    _checked("git", "init", str(corpus))
    _checked("git", "-C", str(corpus), "config", "user.name", "Synthetic Reviewer")
    _checked(
        "git",
        "-C",
        str(corpus),
        "config",
        "user.email",
        "reviewer@example.invalid",
    )
    _checked("git", "-C", str(corpus), "config", "gpg.format", "ssh")
    _checked("git", "-C", str(corpus), "config", "user.signingkey", str(key))
    _checked(
        "git",
        "-C",
        str(corpus),
        "config",
        "gpg.ssh.allowedSignersFile",
        str(allowed_signers),
    )
    _checked("git", "-C", str(corpus), "config", "commit.gpgsign", "true")
    _checked("git", "-C", str(corpus), "config", "tag.gpgSign", "true")
    _checked("git", "-C", str(corpus), "add", ".")
    _checked("git", "-C", str(corpus), "commit", "-m", "Synthetic evidence fixture")
    commit = _checked("git", "-C", str(corpus), "rev-parse", "HEAD").stdout.strip()
    _checked("git", "-C", str(corpus), "tag", "-s", "v1.0", "-m", "Synthetic corpus")

    evidence = corpus / "evidence"
    evidence.mkdir(exist_ok=True)
    for kind, revision in (("commit", commit), ("tag", "v1.0")):
        request = {
            "protocol": "engineering-assurance.signature-verify-request/v1",
            "repository": str(corpus),
            "revision": revision,
            "kind": kind,
            "allowed_signers": str(allowed_signers),
        }
        result = run(
            assurance,
            "signature-verify",
            "--request",
            "-",
            input=json.dumps(request),
        )
        assert result.returncode == 0, (
            f"{assurance} signature-verify exited {result.returncode}: "
            f"{result.stderr}{result.stdout}"
        )
        output_path = evidence / f"signature-{kind}.json"
        output_path.write_text(result.stdout)
        verified = json.loads(result.stdout)
        assert (
            verified.get("status") == "signed_valid"
        ), f"signature verification for {kind} returned {verified}"
    return corpus


def _facts_for_binding(
    clause_set: dict, binding: dict, open_clause: str | None
) -> list[dict]:
    """Build explicit synthetic facts for binding clauses except open work."""
    owned = _customer_owned_clauses(clause_set)
    facts = []
    for clause in binding["clauses"]:
        if clause.get("outcome") != "binding" or clause["clauseId"] == open_clause:
            continue
        clause_id = clause["clauseId"]
        attestation = {
            "attestedBy": "reviewer@example.invalid",
            "authority": "quality-lead@example.invalid",
            "attestedAt": AS_OF,
            "expiresAt": "2027-11-15T00:00:00Z",
        }
        if clause_id in owned:
            facts.append(
                {
                    "kind": "disposition",
                    "clauseId": clause_id,
                    "decision": "delegated",
                    "rationale": (
                        "Customer procedure is maintained in the synthetic project."
                    ),
                    "approvalRef": "person://example.invalid/approvals/customer-owner",
                    "attestation": attestation,
                }
            )
        else:
            facts.append(
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": [
                        "evidence://example.invalid/evidence/signature-commit.json",
                        "evidence://example.invalid/evidence/signature-tag.json",
                    ],
                    "attestation": attestation,
                }
            )
    return facts


@pytest.mark.trace("FR-008-AC-1")
def test_synthetic_corpus_validates_and_contains_no_secret_material():
    """Validate the synthetic Markdown corpus and its identifiers.

    Assumptions: Quire and Quoin are available on PATH with the declared module
    dependencies installed.
    Criteria: The corpus glob validates, references use the reserved domain, and
    no private key material is present.
    Trace: FR-008-AC-1
    """
    quire, _, _ = _preflight()
    validated = run(
        quire,
        "validate",
        "tests/corpus/**/*.md",
        cwd=REPO_ROOT,
    )
    assert validated.returncode == 0, (
        f"{quire} validate 'tests/corpus/**/*.md' exited {validated.returncode}: "
        f"{validated.stderr}{validated.stdout}"
    )
    private_key_markers = (
        "-----BEGIN OPENSSH PRIVATE KEY-----",
        "-----BEGIN RSA PRIVATE KEY-----",
        "-----BEGIN PRIVATE KEY-----",
    )
    identifiers = []
    for path in CORPUS_ROOT.rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(errors="replace")
        assert not any(
            marker in content for marker in private_key_markers
        ), f"private key material found in {path.relative_to(REPO_ROOT)}"
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\s|$)", content, re.DOTALL)
        assert (
            frontmatter is not None
        ), f"corpus document has no frontmatter: {path.relative_to(REPO_ROOT)}"
        metadata = yaml.safe_load(frontmatter.group(1))
        assert isinstance(
            metadata, dict
        ), f"corpus frontmatter is not a mapping: {path.relative_to(REPO_ROOT)}"
        identifier = metadata.get("id")
        assert (
            isinstance(identifier, str) and identifier
        ), f"corpus document has no string id: {path.relative_to(REPO_ROOT)}"
        artifact_type = metadata.get("type")
        fixed_patterns = {
            "FR": r"FR-[0-9]+",
            "NFR": r"NFR-[0-9]+",
            "TestMatrix": r"TM-[0-9]+",
        }
        if artifact_type in fixed_patterns:
            assert re.fullmatch(
                fixed_patterns[artifact_type], identifier
            ), f"corpus id {identifier!r} does not match the {artifact_type} grammar"
        else:
            assert identifier.startswith("example-invalid-"), (
                f"free-form corpus id must use example-invalid-: "
                f"{path.relative_to(REPO_ROOT)}: {identifier!r}"
            )
        identifiers.append(identifier)
    assert len(identifiers) == len(
        set(identifiers)
    ), f"corpus frontmatter IDs must be unique: {identifiers}"
    refs = re.findall(
        r"(?:evidence|person)://[^\s)]+",
        "\n".join(
            path.read_text(errors="replace")
            for path in CORPUS_ROOT.rglob("*")
            if path.is_file()
        ),
    )
    assert refs, "corpus must include synthetic evidence references"
    for reference in refs:
        _assert_reserved_uri_authority(reference)


@pytest.mark.trace("FR-008-AC-1")
@pytest.mark.parametrize(
    "reference",
    [
        "evidence://attacker-example.invalid.evil.test/file.json",
        "evidence://example.invalid.evil/file.json",
        "evidence://notexample.invalid/file.json",
        "evidence://user@example.invalid/file.json",
        "evidence://example.invalid:443/file.json",
    ],
)
def test_synthetic_reference_rejects_unreserved_authority(reference: str):
    """Reject lookalike, suffixed, credentialed and port-qualified authorities.

    Assumptions: Synthetic references use the exact reserved example.invalid
    authority.
    Criteria: An authority that only contains or resembles the reserved host
    fails validation.
    Trace: FR-008-AC-1
    """
    with pytest.raises(AssertionError, match="authority must be exactly"):
        _assert_reserved_uri_authority(reference)


@pytest.mark.trace("FR-007-AC-2")
def test_customer_owned_clause_rejects_direct_fixture_fact():
    """Reject direct facts for all-procedure clauses and require approval.

    Assumptions: Procedure output kinds define customer-owned clauses.
    Criteria: A direct fixture fails with the clause named; a delegated fixture
    passes only with rationale and customer approval reference.
    Trace: FR-007-AC-2
    """
    fixture = {
        "outputCatalog": {"written-procedure": {"kind": "procedure"}},
        "clauses": [
            {"id": "EX-1", "expectedOutputs": ["written-procedure"]},
        ],
    }
    direct = [{"kind": "direct", "clauseId": "EX-1"}]
    with pytest.raises(AssertionError, match="EX-1.*cannot have a direct fact"):
        _assert_customer_owned_facts(fixture, direct)
    delegated = [
        {
            "kind": "disposition",
            "clauseId": "EX-1",
            "decision": "delegated",
            "rationale": "Customer-maintained procedure.",
            "approvalRef": "person://example.invalid/approvals/owner",
        }
    ]
    _assert_customer_owned_facts(fixture, delegated)


@pytest.mark.trace("FR-008-AC-3")
def test_dangling_evidence_fixture_fails_with_clause_id(tmp_path: pathlib.Path):
    """Name the clause when a synthetic evidence reference is unresolved.

    Assumptions: Evidence references resolve to files under the corpus root.
    Criteria: A dangling reference fails and identifies the affected clause.
    """
    with pytest.raises(AssertionError, match="I-1.*unresolved evidence"):
        _assert_fact_refs_resolve(
            tmp_path,
            [
                {
                    "kind": "direct",
                    "clauseId": "I-1",
                    "evidenceRefs": ["evidence://example.invalid/missing.json"],
                }
            ],
        )


@pytest.mark.trace("FR-008-AC-2", "FR-008-AC-3", "FR-007-AC-2")
def test_records_facts_and_renders_both_clause_sets(tmp_path: pathlib.Path):
    """Record facts from signed corpus evidence and render the pack RMM.

    Assumptions: Quire, Quoin, and Engineering Assurance expose the required
    validation, signature-verification, evidence-store, and pack-RMM commands.
    Criteria: Every binding clause except I-18.8 has one fact; references
    resolve; the pack index and clause statuses match the acceptance contract;
    report output excludes clause titles and text.
    Trace: FR-008-AC-2, FR-008-AC-3, FR-007-AC-2
    """
    quire, quoin, assurance = _preflight()
    corpus = _signed_corpus(tmp_path, assurance)
    config_root = tmp_path / "config"
    config_root.mkdir()
    env = {**os.environ, "IX_CONFIG_ROOT": str(config_root)}
    store = tmp_path / "evidence-store"
    sets = load_clause_sets()
    assert len(sets) >= 2, "MDR and MDCG clause sets must be present"
    keys = {_clause_set_key(clause_set): clause_set for clause_set in sets}
    expected_keys = {
        "eu/mdr-2017-745@2026-07-19",
        "eu-mdcg/mdcg-2019-16@rev1",
    }
    assert expected_keys.issubset(
        keys
    ), "MDR and MDCG sets must be in the current module"
    for key in expected_keys:
        clause_set = keys[key]
        authority, set_id, version = _clause_set_args(key)
        evaluated = _checked(
            quire,
            "clauses",
            "evaluate",
            "--module",
            str(PACKAGE_ROOT),
            "--authority",
            authority,
            "--set",
            set_id,
            "--version",
            version,
            "--context",
            "mobile_platform=no",
            "--json",
        )
        binding = json.loads(evaluated.stdout)
        facts = _facts_for_binding(clause_set, binding, OPEN_CLAUSES.get(key))
        _assert_customer_owned_facts(clause_set, facts)
        binding_path = tmp_path / f"{set_id}-binding.json"
        facts_path = tmp_path / f"{set_id}-facts.json"
        binding_path.write_text(json.dumps(binding))
        facts_path.write_text(json.dumps(facts))
        _assert_fact_refs_resolve(corpus, facts)
        recorded = _checked(
            quoin,
            "evidence",
            "record-discharge",
            "--repo",
            str(store),
            "--binding",
            str(binding_path),
            "--facts",
            str(facts_path),
            "--json",
            env=env,
        )
        assert recorded.stdout.strip(), "record-discharge must report stored evidence"
        binding_clauses = [
            clause
            for clause in binding["clauses"]
            if clause.get("outcome") == "binding"
        ]
        assert len(facts) == len(binding_clauses) - (
            1 if OPEN_CLAUSES.get(key) else 0
        ), f"{key} did not receive one fact per binding clause except open work"

    installed = _checked(
        quoin,
        "module",
        "install",
        f"path:{PACKAGE_ROOT}",
        env=env,
    )
    assert installed.returncode == 0
    report_result = run(
        quoin,
        "discharge",
        "--rmm",
        "--pack",
        "spec_clauses_eu_law",
        "--repo",
        str(store),
        "--as-of",
        AS_OF,
        "--context",
        "mobile_platform=no",
        "--json",
        env=env,
    )
    assert report_result.returncode == 0, (
        f"{quoin} discharge --rmm --pack spec_clauses_eu_law exited "
        f"{report_result.returncode}: {report_result.stderr}{report_result.stdout}"
    )
    report = json.loads(report_result.stdout)
    assert report.get("schemaVersion") == "requirements-mapping-pack-v1"
    index = report.get("index")
    assert isinstance(index, list), "pack report must expose a clause-set index"
    set_keys = [
        _clause_set_key(entry["clauseSet"])
        for entry in index
        if isinstance(entry.get("clauseSet"), dict)
    ]
    assert len(set_keys) == len(index), "every index entry must identify its clause set"
    expected_module_keys = set(keys)
    assert set_keys == sorted(
        expected_module_keys, key=lambda value: value.encode()
    ), set_keys
    rendered = json.dumps(report)
    assert "I-17.3" in rendered and "Not applicable" in rendered
    mdr_rows = _report_clause_rows(report, "I-18.8")
    assert len(mdr_rows) == 1, mdr_rows
    mdr_row = mdr_rows[0]
    assert mdr_row["compliance"] == "undischarged"
    compliant_rows = _report_clause_rows(report, "I-17.2")
    assert len(compliant_rows) == 1, compliant_rows
    assert compliant_rows[0]["compliance"] == "compliant"
    assert any(
        "signature-commit.json" in reference
        for reference in compliant_rows[0]["evidenceRefs"]
    )

    markdown = _checked(
        quoin,
        "discharge",
        "--rmm",
        "--pack",
        "spec_clauses_eu_law",
        "--repo",
        str(store),
        "--as-of",
        AS_OF,
        "--context",
        "mobile_platform=no",
        env=env,
    ).stdout
    assert "I-18.8" in markdown
    assert "Not compliant - undischarged" in markdown
    assert "I-17.2" in markdown and "Compliant" in markdown
    assert "I-17.3" in markdown and "Not applicable" in markdown
    for clause_set in sets:
        for clause in clause_set["clauses"]:
            assert (
                clause["title"] not in rendered
            ), f"clause title leaked into report: {clause['id']}"
            assert (
                clause["text"] not in rendered
            ), f"clause text leaked into report: {clause['id']}"
            assert (
                clause["title"] not in markdown
            ), f"clause title leaked into Markdown RMM: {clause['id']}"
            assert (
                clause["text"] not in markdown
            ), f"clause text leaked into Markdown RMM: {clause['id']}"
