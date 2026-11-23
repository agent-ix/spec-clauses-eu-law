"""Readers for the Annex 11 sections of spec.md, shared by the Annex 11 tests."""

from __future__ import annotations

import re

from conftest import REPO_ROOT


def _spec() -> str:
    return (REPO_ROOT / "spec" / "spec.md").read_text()


def section(name: str) -> str:
    """Return the body of one `## <name>` section of spec.md."""
    return _spec().split(f"## {name}", 1)[1].split("\n## ", 1)[0]


def table_rows(name: str) -> list[list[str]]:
    """Return the data rows of the single table in a spec.md section."""
    rows = []
    for line in section(name).splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows[1:]


def backticked(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


def clause_rows() -> list[dict]:
    """Parse the Annex 11 Clause Table."""
    rows = []
    for cid, summary, applicability, outputs in table_rows("Annex 11 Clause Table"):
        dimension = applicability[2:] if applicability.startswith("D ") else None
        rows.append(
            {
                "id": cid.strip("`"),
                "summary": summary,
                "dimension": dimension,
                "outputs": backticked(outputs),
            }
        )
    return rows


def binding_rows() -> list[dict]:
    """Parse the Annex 11 Output Bindings table into one row per row."""
    rows = []
    for outputs, commands, source, limit in table_rows("Annex 11 Output Bindings"):
        rows.append(
            {
                "outputs": backticked(outputs),
                "commands": backticked(commands),
                "source": source,
                "limit": limit,
            }
        )
    return rows


def tool_limit_sentences() -> dict[str, str]:
    """Map each output to the clause-text sentence its limit requires."""
    sentences = {}
    for outputs, sentence in table_rows("Annex 11 Tool Limits"):
        for name in backticked(outputs):
            sentences[name] = sentence
    return sentences


def shared_outputs() -> set[str]:
    """Outputs the bindings section says it shares with the US catalog."""
    intro = section("Annex 11 Output Bindings").split("keep that catalog's", 1)[0]
    return set(backticked(intro.split("Expected outputs that already exist", 1)[1]))


def limited_shared_outputs() -> set[str]:
    """Shared outputs whose bindings row states a limit other than None."""
    return {
        name
        for row in binding_rows()
        if row["limit"] != "None"
        for name in row["outputs"]
        if name in shared_outputs()
    }


def crosswalk_rows() -> set[tuple[str, str, str]]:
    """Parse the Part 11 crosswalk policy into (source, target, relation)."""
    return {
        (source.strip("`"), target.strip("`"), relation.strip("`"))
        for source, target, relation in table_rows("Annex 11 Part 11 Crosswalk Policy")
    }


def identity() -> tuple[str, str, str]:
    """Authority, id and version the Annex 11 Set Design declares."""
    design = section("Annex 11 Set Design")
    match = re.search(
        r"authority `([^`]+)`, ID `([^`]+)`, and version `([^`]+)`", design
    )
    assert match, "spec.md must declare the Annex 11 identity"
    return match.group(1), match.group(2), match.group(3)


def official_url() -> str:
    """Official document URL the Annex 11 Set Design declares."""
    match = re.search(
        r"official document URL is `([^`]+)`", section("Annex 11 Set Design")
    )
    assert match, "spec.md must declare the Annex 11 official URL"
    return match.group(1)


def set_key() -> str:
    authority, set_id, version = identity()
    return f"{authority}/{set_id}@{version}"


def set_path() -> str:
    authority, set_id, version = identity()
    return f"clauses/{authority}-{set_id}-{version}.json"


def title_rows() -> dict[str, tuple[str, list[str]]]:
    """Parse the Clause Titles and Subjects table."""
    return {
        cid.strip("`"): (title, backticked(subjects))
        for cid, title, subjects in table_rows("Annex 11 Clause Titles and Subjects")
    }


def expected_metadata() -> dict:
    """Source and rights values the spec states for the Annex 11 set."""
    design = section("Annex 11 Set Design")
    licence = re.search(r"Licence metadata says exactly: `([^`]+)`", design).group(1)
    attribution = (
        re.search(r"Attribution says `([^`]+)`", design)
        .group(1)
        .replace("{official document URL}", official_url())
    )
    return {
        set_key(): {
            "officialUrl": official_url(),
            "licence": licence,
            "attribution": attribution,
            "rights": {
                "structure": "citation_only",
                "text": "original",
                "clearance_ref": None,
            },
        }
    }


def risk_scaled_clauses() -> set[str]:
    """Clauses FR-028 reserves to a named person, read from its criterion."""
    text = (
        REPO_ROOT / "spec/functional/FR-028-annex-11-human-decisions.md"
    ).read_text()
    criterion = re.search(r"\| FR-028-AC-1 \| Clauses (.+?) each declare", text).group(
        1
    )
    return set(re.findall(r"`([^`]+)`", criterion))


def applicability_dimensions() -> list[str]:
    """Second dimensions named by the clause table, in first-use order."""
    seen: list[str] = []
    for row in clause_rows():
        if row["dimension"] and row["dimension"] not in seen:
            seen.append(row["dimension"])
    return seen
