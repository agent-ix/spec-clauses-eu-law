"""End-to-end discharge checks for the EU reference corpus."""

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
GDPR_RECORDS_OF_PROCESSING_FIXTURE = (
    REPO_ROOT / "tests" / "fixtures" / "gdpr_records_of_processing"
)
AS_OF = "2026-11-15T00:00:00Z"
OPEN_CLAUSES = {
    "eu/mdr-2017-745@2026-07-19": "I-18.8",
    "eu/ai-act-2024-1689-annex-iv@2026-07-27": "IV-8",
}
AI_APPROVAL_CLAUSES = {"art-9", "art-14"}
AI_EVIDENCE_REFS = {
    "model-description": "evidence://example.invalid/ai/model-description.json",
    "data-lineage": "evidence://example.invalid/ai/dataset-lineage.json",
    "event-logging-design": "evidence://example.invalid/ai/logging-design.json",
    "human-oversight-design": "evidence://example.invalid/ai/human-oversight.json",
    "post-market-monitoring-plan": "evidence://example.invalid/ai/post-market-monitoring.json",
}
AI_ANNEX_KEY = "eu/ai-act-2024-1689-annex-iv@2026-07-27"
GDPR_KEY = "eu/gdpr-2016-679@2016-05-04"
GDPR_APPROVAL_CLAUSES = {
    "art-35(1)",
    "art-35(2)",
    "art-35(7)(a)",
    "art-35(7)(b)",
    "art-35(7)(c)",
    "art-35(7)(d)",
    "art-35(9)",
    "art-35(11)",
}
GDPR_EVIDENCE_REFS = {
    "data-flow-model": "evidence://example.invalid/gdpr/data-flow-model.json",
    "dpia": "evidence://example.invalid/gdpr/dpia.json",
    "privacy-by-default-settings": (
        "evidence://example.invalid/gdpr/privacy-by-default-settings.json"
    ),
    "records-of-processing": (
        "evidence://example.invalid/gdpr/records-of-processing.json"
    ),
    "security-risk-records": "evidence://example.invalid/security/RISK-002.md",
    "software-architecture": "evidence://example.invalid/architecture/evidence_store.md",
    "access-control": "evidence://example.invalid/security/CTRL-001.md",
    "written-procedure": "evidence://example.invalid/requirements/FR-001.md",
    "training-record": "evidence://example.invalid/requirements/NFR-001.md",
    "verification-records": "evidence://example.invalid/tests/TM-001.md",
}
GDPR_ART30_ACTIVITY_FIELDS = {
    "art-30(1)(a)": "identity",
    "art-30(1)(b)": "purposes",
    "art-30(1)(c)": "dataCategories",
    "art-30(1)(d)": "recipients",
    "art-30(1)(e)": "transfers",
    "art-30(1)(f)": "retention",
    "art-30(1)(g)": "securityMeasures",
}


def _provider_pack_context() -> list[str]:
    """Return explicit product and AI inputs for the combined EU pack run."""
    return ["mobile_platform=no", *_ai_annex_context()]


def _corpus_validation_modules() -> list[str]:
    """Select only corpus schemas, excluding unrelated ambient app modules."""
    modules_root = pathlib.Path.home() / ".ix" / "filament" / "modules"
    roots = [
        "spec-artifacts-iso",
        "spec-artifacts-process",
        "spec-objects-architecture",
        "spec-objects-business",
        "spec-objects-safety",
    ]
    security_root = os.environ.get(
        "SPEC_OBJECTS_SECURITY_MODULE", str(modules_root / "spec-objects-security")
    )
    return [*(str(modules_root / name) for name in roots), security_root]


def _records_of_processing_modules() -> list[str]:
    """Return the corpus module roots needed to resolve producer records."""
    modules = _corpus_validation_modules()
    producer_security = os.environ.get("SPEC_OBJECTS_SECURITY_PRODUCER_MODULE")
    if producer_security is not None:
        modules[-1] = producer_security
    return modules


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
    assert parsed.scheme, f"synthetic reference must be a URI: {reference}"
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
    clause_set: dict,
    binding: dict,
    open_clause: str | None,
    *,
    records_of_processing: dict | None = None,
    generated_records_of_processing: tuple[dict, str] | None = None,
) -> list[dict]:
    """Build explicit synthetic facts for binding clauses except open work."""
    owned = _customer_owned_clauses(clause_set)
    facts = []
    for clause in binding["clauses"]:
        if clause.get("outcome") != "binding" or clause["clauseId"] == open_clause:
            continue
        clause_id = clause["clauseId"]
        if (
            clause_set.get("id") == "gdpr-2016-679"
            and clause_id in GDPR_ART30_ACTIVITY_FIELDS
        ):
            field = GDPR_ART30_ACTIVITY_FIELDS[clause_id]
            activities = (records_of_processing or {}).get("activities", [])
            if clause_id == "art-30(1)(c)" and generated_records_of_processing:
                report, markdown = generated_records_of_processing
                gaps = [
                    gap
                    for document in report.get("documents", [])
                    for gap in document.get("gaps", [])
                ]
                has_classification_gap = any(
                    gap.get("gap_kind") == "personal_data_categories_unstated"
                    for gap in gaps
                )
                if has_classification_gap or "CLASS-PHI (health)" not in markdown:
                    continue
            if not any(field in activity for activity in activities):
                continue
        attestation = {
            "attestedBy": "reviewer@example.invalid",
            "authority": "quality-lead@example.invalid",
            "attestedAt": AS_OF,
            "expiresAt": "2027-11-15T00:00:00Z",
        }
        if clause_id in AI_APPROVAL_CLAUSES:
            facts.append(
                {
                    "kind": "disposition",
                    "clauseId": clause_id,
                    "decision": "accepted_risk",
                    "owner": "person://example.invalid/people/ai-safety-reviewer",
                    "rationale": "The named reviewer approved the synthetic record.",
                    "approvalRef": "person://example.invalid/people/ai-safety-reviewer",
                    "attestation": attestation,
                }
            )
        elif clause_id in owned:
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
            outputs = clause_set.get("outputCatalog", {})
            clause = next(
                item for item in clause_set["clauses"] if item["id"] == clause_id
            )
            evidence_refs = (
                GDPR_EVIDENCE_REFS
                if clause_set.get("id") == "gdpr-2016-679"
                else AI_EVIDENCE_REFS
            )
            output_refs = [
                evidence_refs[output]
                for output in clause.get("expectedOutputs", [])
                if output in evidence_refs and output in outputs
            ]
            facts.append(
                {
                    "kind": "direct",
                    "clauseId": clause_id,
                    "evidenceRefs": [
                        *output_refs,
                        "evidence://example.invalid/evidence/signature-commit.json",
                        "evidence://example.invalid/evidence/signature-tag.json",
                    ],
                    "attestation": attestation,
                }
            )
    return facts


def _generate_records_of_processing(
    quoin: str, scope: pathlib.Path, env: dict[str, str]
) -> tuple[dict, str]:
    """Run PLAT-1658's producer and return its JSON report and generated file."""
    module_args = [
        argument
        for module in _records_of_processing_modules()
        for argument in ("--module", module)
    ]
    result = run(
        quoin,
        "dossier",
        "generate",
        "--doc",
        "records-of-processing",
        "--scope",
        str(scope),
        *module_args,
        "--json",
        cwd=scope,
        env=env,
    )
    assert result.returncode in {0, 1}, (
        f"{quoin} dossier generate --doc records-of-processing exited "
        f"{result.returncode}: {result.stderr}{result.stdout}"
    )
    report = json.loads(result.stdout)
    assert len(report["documents"]) == 1
    document = report["documents"][0]
    assert document["id"] == "DOS-ROP"
    markdown = (scope / document["path"]).read_text()
    return report, markdown


def _assert_named_person_approvals(
    facts: list[dict],
    clause_ids: set[str] = AI_APPROVAL_CLAUSES,
    *,
    require_accepted_risk: bool = True,
) -> None:
    """Require a named-person approval for risk and DPIA clauses."""
    by_clause = {item.get("clauseId"): item for item in facts}
    for clause_id in clause_ids.intersection(by_clause):
        fact = by_clause[clause_id]
        if require_accepted_risk:
            assert (
                fact.get("kind") == "disposition"
            ), f"{clause_id} requires an approved disposition"
            assert (
                fact.get("decision") == "accepted_risk"
            ), f"{clause_id} requires an accepted-risk decision"
        elif fact.get("kind") == "direct":
            assert GDPR_EVIDENCE_REFS["dpia"] in fact.get(
                "evidenceRefs", []
            ), f"{clause_id} direct fact must cite the DPIA"
        approval_ref = fact.get("approvalRef", "")
        parsed = urlparse(approval_ref)
        assert (
            parsed.scheme == "person"
            and parsed.netloc == "example.invalid"
            and re.fullmatch(r"/people/[a-z][a-z0-9-]*", parsed.path)
        ), f"{clause_id} approvalRef must name a person"
        if fact.get("kind") == "direct":
            assert (
                fact.get("attestation", {}).get("attestedBy") == approval_ref
            ), f"{clause_id} attestation must be bound to its named approver"


def _ai_annex_context() -> list[str]:
    """Return explicit provider inputs that bind every Annex IV point."""
    clause_set = next(
        item for item in load_clause_sets() if _clause_set_key(item) == AI_ANNEX_KEY
    )
    dimensions = [
        name
        for name in clause_set.get("classificationDimensions", {})
        if name not in {"ai_high_risk", "ai_role"}
    ]
    return [
        "ai_high_risk=yes",
        "ai_role=provider",
        *(f"{dimension}=yes" for dimension in dimensions),
    ]


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
        *[
            argument
            for module in _corpus_validation_modules()
            for argument in ("--module", module)
        ],
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
        if path.suffix != ".md":
            continue
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
        r"\b[A-Za-z][A-Za-z0-9+.-]*://[^\s\"'<>]+",
        "\n".join(
            path.read_text(errors="replace")
            for path in CORPUS_ROOT.rglob("*")
            if path.is_file()
        ),
    )
    assert refs, "corpus must include synthetic URI-valued identifiers or references"
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
        "project://example.invalid.attacker.test/reference-corpus",
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


@pytest.mark.trace("FR-020-AC-1")
def test_ai_act_human_oversight_requires_named_person_approval():
    """Reject AI Act risk or oversight dispositions without person approval.

    Assumptions: Risk acceptance and human oversight are explicit dispositions.
    Criteria: An art-14 disposition whose approval reference does not name a
    person fails with the clause id; a named-person reference passes.
    Trace: FR-020-AC-1
    """
    missing_approval = [
        {
            "kind": "disposition",
            "clauseId": "art-14",
            "decision": "accepted_risk",
            "owner": "person://example.invalid/people/ai-safety-reviewer",
            "rationale": "The oversight design was reviewed.",
            "approvalRef": "",
        }
    ]
    with pytest.raises(AssertionError, match="art-14.*approvalRef must name a person"):
        _assert_named_person_approvals(missing_approval)


@pytest.mark.trace("FR-012-AC-1", "FR-012-AC-2")
@pytest.mark.parametrize(
    "fact",
    [
        {
            "kind": "direct",
            "clauseId": "art-35(1)",
            "evidenceRefs": [GDPR_EVIDENCE_REFS["dpia"]],
        },
        {
            "kind": "disposition",
            "clauseId": "art-35(1)",
            "decision": "accepted_risk",
        },
    ],
)
def test_gdpr_dpia_discharge_requires_named_person_approval(fact: dict):
    """Reject Art 35 facts without an approval reference naming a person."""
    with pytest.raises(
        AssertionError, match=r"art-35\(1\).*approvalRef must name a person"
    ):
        _assert_named_person_approvals(
            [fact], GDPR_APPROVAL_CLAUSES, require_accepted_risk=False
        )


def test_gdpr_dpia_direct_fact_passes_with_named_approval():
    """Accept a direct Art 35 fact only when its DPIA approver is named."""
    _assert_named_person_approvals(
        [
            {
                "kind": "direct",
                "clauseId": "art-35(1)",
                "evidenceRefs": [GDPR_EVIDENCE_REFS["dpia"]],
                "approvalRef": "person://example.invalid/people/privacy-officer",
                "attestation": {
                    "attestedBy": "person://example.invalid/people/privacy-officer"
                },
            }
        ],
        GDPR_APPROVAL_CLAUSES,
        require_accepted_risk=False,
    )


@pytest.mark.trace(
    "FR-008-AC-2",
    "FR-008-AC-3",
    "FR-007-AC-2",
    "FR-012-AC-1",
    "FR-012-AC-2",
    "FR-013-AC-2",
)
def test_records_facts_and_renders_both_clause_sets(tmp_path: pathlib.Path):
    """Record EU law facts and render the pack RMM across all authored sets.

    Assumptions: Quire, Quoin, and Engineering Assurance expose the required
    validation, signature-verification, evidence-store, and pack-RMM commands.
    Criteria: Every binding MDR, MDCG, GDPR, and AI Act clause except open
    examples has one fact; references resolve; the report index and statuses
    match the acceptance contract; report output excludes clause titles and text.
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
        "eu/ai-act-2024-1689@2026-07-27",
        AI_ANNEX_KEY,
        GDPR_KEY,
    }
    assert expected_keys.issubset(
        keys
    ), "MDR and MDCG sets must be in the current module"
    gdpr_binding = None
    records = json.loads((CORPUS_ROOT / "gdpr/records-of-processing.json").read_text())
    dpia = json.loads((CORPUS_ROOT / "gdpr/dpia.json").read_text())
    dpia_approval_ref = dpia["residualRiskDecision"]["approvalRef"]
    assert (
        dpia["residualRiskDecision"]["approver"] == dpia_approval_ref
    ), "DPIA residual-risk approval must name the approver"
    for key in expected_keys:
        clause_set = keys[key]
        authority, set_id, version = _clause_set_args(key)
        context = ["mobile_platform=no"]
        if key == GDPR_KEY:
            context.extend(
                [
                    "gdpr_role=controller",
                    "high_risk_processing=yes",
                    "article_30_records_applicability=applies",
                ]
            )
        elif key == "eu/ai-act-2024-1689@2026-07-27":
            context.extend(["ai_high_risk=yes", "ai_role=provider"])
        elif key == AI_ANNEX_KEY:
            context.extend(_ai_annex_context())
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
            *[argument for value in context for argument in ("--context", value)],
            "--json",
        )
        binding = json.loads(evaluated.stdout)
        open_clause = OPEN_CLAUSES.get(key)
        if key == GDPR_KEY:
            open_clause = "art-30(1)(g)"
        facts = _facts_for_binding(
            clause_set,
            binding,
            open_clause,
            records_of_processing=records if key == GDPR_KEY else None,
        )
        if key == GDPR_KEY:
            for fact in facts:
                if fact.get("clauseId") in GDPR_APPROVAL_CLAUSES:
                    fact["approvalRef"] = dpia_approval_ref
                    fact["attestation"]["attestedBy"] = dpia_approval_ref
        _assert_customer_owned_facts(clause_set, facts)
        if key == "eu/ai-act-2024-1689@2026-07-27":
            _assert_named_person_approvals(facts)
            assert AI_APPROVAL_CLAUSES.issubset(
                {fact.get("clauseId") for fact in facts}
            )
        if key == GDPR_KEY:
            _assert_named_person_approvals(
                facts,
                GDPR_APPROVAL_CLAUSES,
                require_accepted_risk=False,
            )
            assert GDPR_APPROVAL_CLAUSES.issubset(
                {fact.get("clauseId") for fact in facts}
            )
            gdpr_binding = binding
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
            1 if open_clause else 0
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
        *[
            argument
            for value in _provider_pack_context()
            for argument in ("--context", value)
        ],
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
        *[
            argument
            for value in _provider_pack_context()
            for argument in ("--context", value)
        ],
        env=env,
    ).stdout
    assert "I-18.8" in markdown
    assert "Not compliant - undischarged" in markdown
    assert "I-17.2" in markdown and "Compliant" in markdown
    assert "I-17.3" in markdown and "Not applicable" in markdown
    assert "IV-8" in rendered and "undischarged" in rendered
    assert "IV-8" in markdown and "Not compliant - undischarged" in markdown
    ai_act_row = _report_clause_rows(report, "art-10")
    assert len(ai_act_row) == 1 and ai_act_row[0]["compliance"] == "compliant"
    assert any("dataset-lineage.json" in ref for ref in ai_act_row[0]["evidenceRefs"])
    gdpr_dpia_rows = _report_clause_rows(report, "art-35(1)")
    assert len(gdpr_dpia_rows) == 1, gdpr_dpia_rows
    assert GDPR_EVIDENCE_REFS["dpia"] in gdpr_dpia_rows[0]["evidenceRefs"]

    gdpr_processor_report = json.loads(
        _checked(
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
            "--context",
            "gdpr_role=processor",
            "--context",
            "high_risk_processing=yes",
            "--context",
            "article_30_records_applicability=applies",
            "--context",
            "ai_high_risk=yes",
            "--context",
            "ai_role=provider",
            "--json",
            env=env,
        ).stdout
    )
    for clause_id in ("art-25(1)", "art-25(2)", *GDPR_APPROVAL_CLAUSES):
        rows = [
            row
            for row in _report_clause_rows(gdpr_processor_report, clause_id)
            if "compliance" in row
        ]
        assert len(rows) == 1 and rows[0]["compliance"] == "not_applicable", rows

    assert gdpr_binding is not None
    source_scope = tmp_path / "records-of-processing-source"
    shutil.copytree(GDPR_RECORDS_OF_PROCESSING_FIXTURE, source_scope)
    generated_records = _generate_records_of_processing(quoin, source_scope, env)
    assert "CLASS-PHI (health)" in generated_records[1]

    source_missing_scope = (
        tmp_path / "records-of-processing-source-missing-classification"
    )
    shutil.copytree(source_scope, source_missing_scope)
    sink_path = source_missing_scope / "spec" / "SINK-001.md"
    sink = sink_path.read_text()
    carry_edge = "  - target: CLASS-PHI\n    type: carries\n"
    assert carry_edge in sink
    sink_path.write_text(sink.replace(carry_edge, "", 1))
    source_missing_records = _generate_records_of_processing(
        quoin, source_missing_scope, env
    )
    assert "CLASS-PHI (health)" not in source_missing_records[1]
    assert (
        "GAP: (c) categories of personal data — SINK-001 carries no classification"
        in source_missing_records[1]
    )
    source_missing_facts = _facts_for_binding(
        keys[GDPR_KEY],
        gdpr_binding,
        "art-30(1)(g)",
        records_of_processing=records,
        generated_records_of_processing=source_missing_records,
    )
    assert "art-30(1)(c)" not in {fact["clauseId"] for fact in source_missing_facts}
    missing_store = tmp_path / "missing-category-store"
    missing_facts_path = tmp_path / "missing-category-facts.json"
    missing_facts_path.write_text(json.dumps(source_missing_facts))
    binding_path = tmp_path / "gdpr-binding.json"
    binding_path.write_text(json.dumps(gdpr_binding))
    _checked(
        quoin,
        "evidence",
        "record-discharge",
        "--repo",
        str(missing_store),
        "--binding",
        str(binding_path),
        "--facts",
        str(missing_facts_path),
        "--json",
        env=env,
    )
    missing_discharge_report = json.loads(
        _checked(
            quoin,
            "discharge",
            "--rmm",
            "--pack",
            "spec_clauses_eu_law",
            "--repo",
            str(missing_store),
            "--as-of",
            AS_OF,
            "--context",
            "mobile_platform=no",
            "--context",
            "gdpr_role=controller",
            "--context",
            "high_risk_processing=yes",
            "--context",
            "article_30_records_applicability=applies",
            "--json",
            env=env,
        ).stdout
    )
    missing_category_rows = _report_clause_rows(
        missing_discharge_report, "art-30(1)(c)"
    )
    assert len(missing_category_rows) == 1
    assert missing_category_rows[0]["compliance"] == "undischarged"
    missing_discharge_markdown = _checked(
        quoin,
        "discharge",
        "--rmm",
        "--pack",
        "spec_clauses_eu_law",
        "--repo",
        str(missing_store),
        "--as-of",
        AS_OF,
        "--context",
        "mobile_platform=no",
        "--context",
        "gdpr_role=controller",
        "--context",
        "high_risk_processing=yes",
        "--context",
        "article_30_records_applicability=applies",
        env=env,
    ).stdout
    assert "art-30(1)(c)" in missing_discharge_markdown
    assert "Not compliant - undischarged" in missing_discharge_markdown

    deployer_report = json.loads(
        _checked(
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
            "--context",
            "ai_high_risk=yes",
            "--context",
            "ai_role=deployer",
            "--json",
            env=env,
        ).stdout
    )
    annex_rows = [
        row
        for clause_set in keys[AI_ANNEX_KEY]["clauses"]
        for row in _report_clause_rows(deployer_report, clause_set["id"])
        if "compliance" in row
    ]
    assert len(annex_rows) == 23, annex_rows
    assert all(row["compliance"] == "not_applicable" for row in annex_rows)
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
