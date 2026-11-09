"""Check that the docs stay in step with the code.

Two checks:
1. If code or config changed, at least one doc must change too.
2. The docs index is complete: every .md file in docs/ is linked from docs/DOCS.md,
   and every code module in src/job_hunter/<module>/ has docs/modules/<module>.md.

Modes:
    --staged      check the files staged for commit (used by the git pre-commit hook)
    --worktree    check all uncommitted files
    --stop-hook   used by the Claude Code Stop hook (reads JSON from stdin)

Skip the check for a small change (typo, formatting):
    $env:SKIP="docs-check"; git commit -m "..."
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE_PREFIXES = ("src/", "scripts/")
CODE_FILES = ("pyproject.toml", ".pre-commit-config.yaml")
DOC_PREFIXES = ("docs/",)
DOC_FILES = ("README.md", "CHANGELOG.md")


def git(*args: str) -> str:
    """Run a git command in the project folder and return its output."""
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout


def staged_files() -> list[str]:
    """Return the files staged for the next commit."""
    return [f for f in git("diff", "--cached", "--name-only").splitlines() if f]


def worktree_files() -> list[str]:
    """Return all files with uncommitted changes (including new files)."""
    files = []
    for line in git("status", "--porcelain", "-uall").splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        files.append(path)
    return files


def is_code(path: str) -> bool:
    """Say whether a changed path counts as code or config."""
    return (
        path.startswith(CODE_PREFIXES)
        or path in CODE_FILES
        or (path.startswith("config/") and path.endswith(".example.yaml"))
    )


def is_doc(path: str) -> bool:
    """Say whether a changed path counts as documentation."""
    return path.startswith(DOC_PREFIXES) or path in DOC_FILES


def check_code_has_docs(changed: list[str]) -> list[str]:
    """Check 1: code changes need a doc change."""
    code = [p for p in changed if is_code(p)]
    if code and not any(is_doc(p) for p in changed):
        return [
            "Code or config changed, but no doc changed. Update docs/, README.md or CHANGELOG.md.",
            "Changed code: " + ", ".join(code[:5]) + (" ..." if len(code) > 5 else ""),
        ]
    return []


def check_index() -> list[str]:
    """Check 2: every doc is in the index, and every code module has a module doc."""
    problems = []
    docs_dir = ROOT / "docs"
    index = (docs_dir / "DOCS.md").read_text(encoding="utf-8")
    for md in sorted(docs_dir.rglob("*.md")):
        rel = md.relative_to(docs_dir).as_posix()
        if rel != "DOCS.md" and rel not in index:
            problems.append(f"docs/{rel} is not linked from docs/DOCS.md.")
    modules_dir = ROOT / "src" / "job_hunter"
    for module in sorted(p for p in modules_dir.iterdir() if p.is_dir()):
        has_code = any(f.name != "__init__.py" for f in module.rglob("*.py"))
        if has_code and not (docs_dir / "modules" / f"{module.name}.md").exists():
            problems.append(
                f"Module '{module.name}' has code but no docs/modules/{module.name}.md."
            )
    return problems


def run(changed: list[str]) -> list[str]:
    """Run both checks and return the list of problems."""
    return check_code_has_docs(changed) + check_index()


def main() -> int:
    """Entry point. Return the exit code."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "--staged"
    if mode == "--stop-hook":
        try:
            data = json.load(sys.stdin)
        except ValueError:
            data = {}
        if data.get("stop_hook_active"):
            return 0  # already sent back once: never loop forever
        problems = run(worktree_files())
        if problems:
            reason = "Docs are out of date:\n- " + "\n- ".join(problems)
            print(json.dumps({"decision": "block", "reason": reason}))
        return 0
    changed = worktree_files() if mode == "--worktree" else staged_files()
    problems = run(changed)
    for problem in problems:
        print(f"docs-check: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
