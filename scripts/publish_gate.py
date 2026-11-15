"""Run publish checks and rights scans over built package archives."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

PROTOCOL = "engineering-assurance.content-rights-tree-result/v1"


def _run(
    command: list[str], *, cwd: pathlib.Path | None = None
) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, cwd=cwd, check=False)


def _safe_finding(result: dict) -> list[str]:
    findings = result.get("findings", [])
    return [
        f"{item.get('path') or '<tree>'}:{item.get('line', 0)}: "
        f"{item.get('category', 'unknown')}"
        for item in findings
    ]


def _extract_archive(archive: pathlib.Path, destination: pathlib.Path) -> None:
    if archive.suffix == ".whl":
        with zipfile.ZipFile(archive) as source:
            for member in source.infolist():
                relative = pathlib.PurePosixPath(member.filename)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("wheel contains an unsafe archive path")
            source.extractall(destination)
        return

    with tarfile.open(archive, "r:gz") as source:
        source.extractall(destination, filter="data")


def _normalize_wheel_license_path(archive: pathlib.Path, root: pathlib.Path) -> None:
    """Present the wheel's standard license copy under the shared LICENSE path.

    Wheel metadata stores the declared license at ``*.dist-info/licenses/LICENSE``.
    The shared scanner intentionally grants its license-file rules to the exact
    path ``LICENSE``. Move the package-manager copy to that canonical path so
    the unchanged scanner policy applies to the full license text.
    """
    if archive.suffix != ".whl":
        return
    license_copies = sorted(root.glob("*.dist-info/licenses/LICENSE"))
    if not license_copies:
        return
    canonical = root / "LICENSE"
    for source in license_copies:
        if canonical.exists():
            if source.read_bytes() != canonical.read_bytes():
                raise ValueError("wheel contains differing license copies")
            source.unlink()
        else:
            canonical.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(canonical))


def scan_archive(
    archive: pathlib.Path,
    engineering_assurance: str,
) -> tuple[bool, list[str]]:
    """Scan every extracted archive entry using the shared rights command."""
    with tempfile.TemporaryDirectory(prefix="eu-publish-scan-") as temporary:
        root = pathlib.Path(temporary).resolve()
        _extract_archive(archive, root)
        _normalize_wheel_license_path(archive, root)
        initialized = _run(["git", "init", "--quiet", "-b", "main"], cwd=root)
        if initialized.returncode != 0:
            return False, ["could not initialize the extracted package scan tree"]
        added = _run(["git", "add", "--all"], cwd=root)
        if added.returncode != 0:
            return False, ["could not select the extracted package files for scanning"]
        scanned = _run(
            [engineering_assurance, "content-rights-tree", "--root", str(root)],
            cwd=root,
        )
        try:
            result = json.loads(scanned.stdout)
        except json.JSONDecodeError:
            return False, [f"content-rights-tree failed (exit {scanned.returncode})"]
        if result.get("protocol") != PROTOCOL:
            return False, ["content-rights-tree returned an unsupported result"]
        findings = _safe_finding(result)
        if scanned.returncode != 0 or result.get("outcome") != "accepted":
            return False, findings or [
                f"content-rights-tree failed (exit {scanned.returncode})"
            ]
        return True, []


def check_publishable(module: pathlib.Path, quire: str) -> tuple[bool, list[str]]:
    """Run Quire's native module publication rights check."""
    result = _run([quire, "publish-check", "--module", str(module)])
    if result.returncode == 0:
        return True, []
    details = result.stdout + result.stderr
    return False, [line.strip() for line in details.splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, type=pathlib.Path)
    parser.add_argument("--wheel-dir", required=True, type=pathlib.Path)
    parser.add_argument("--npm-dir", required=True, type=pathlib.Path)
    parser.add_argument("--engineering-assurance", default="engineering-assurance")
    parser.add_argument("--quire", default="quire")
    arguments = parser.parse_args(argv)
    if pathlib.Path(arguments.engineering_assurance).parent != pathlib.Path("."):
        arguments.engineering_assurance = str(
            pathlib.Path(arguments.engineering_assurance).resolve()
        )

    wheel_files = sorted(arguments.wheel_dir.glob("*.whl"))
    npm_files = sorted(arguments.npm_dir.glob("*.tgz"))
    if len(wheel_files) != 1 or len(npm_files) != 1:
        print(
            "publish gate requires exactly one wheel and one npm archive",
            file=sys.stderr,
        )
        return 2

    accepted, findings = check_publishable(arguments.module, arguments.quire)
    if not accepted:
        print("Quire publish-check refused the EU module:", file=sys.stderr)
        for finding in findings:
            print(finding, file=sys.stderr)
        return 1

    for archive in (wheel_files[0], npm_files[0]):
        accepted, findings = scan_archive(archive, arguments.engineering_assurance)
        if accepted:
            continue
        print(f"content-rights-tree withheld {archive.name}:", file=sys.stderr)
        for finding in findings:
            print(finding, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
