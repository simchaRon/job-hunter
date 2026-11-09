# Flow: commit checks

## What it does
Before every `git commit`, a set of automatic checks runs on the staged files.
If one check fails, the commit is blocked. This keeps the code clean and keeps secrets out of Git.

## Steps
1. You run `git commit`.
2. The tool `pre-commit` runs these checks, in order:
   - Basic file checks: end of file, trailing spaces, valid YAML, no big files.
   - `ruff`: finds code problems and fixes the easy ones.
   - `ruff-format`: formats the code.
   - `docs-check`: keeps the docs in step with the code (see below).
   - `gitleaks`: scans the staged changes for keys, tokens and passwords.
3. If a check fixes a file, the commit stops. Run `git add` again, then commit again.

## The docs check
The script `scripts/check_docs.py` makes two checks:
1. **Code change needs a doc change.** If the commit changes `src/`, `scripts/`, `pyproject.toml`,
   `.pre-commit-config.yaml` or `config/*.example.yaml`, it must also change `docs/`,
   `README.md` or `CHANGELOG.md`.
2. **The index is complete.** Every `.md` file in `docs/` must be linked from
   [DOCS.md](DOCS.md). Every code module `src/job_hunter/<module>/` that has code needs
   `docs/modules/<module>.md`.

The same script also runs as a Claude Code **Stop hook** (`.claude/settings.json`).
When Claude finishes a turn with missing docs, it is sent back to fix them first.

For a small change (typo, formatting) skip only this check:
```powershell
$env:SKIP="docs-check"; git commit -m "fix: typo"
```

## Rules
- Never skip the `gitleaks` check.
- Never write a real key or token in any file, including docs.
- Every new flow gets a doc from [_template-flow.md](_template-flow.md) and a link in `DOCS.md`.

## Files involved
- `.pre-commit-config.yaml`: the list of checks.
- `scripts/check_docs.py`: the docs check.
- `.claude/settings.json`: the Claude Code Stop hook.
- `pyproject.toml`: the `ruff` settings.
- `.gitignore`: files that Git must never track (`.env`, `data/`, `config/profile.yaml`, ...).

## How to test
Run all checks on all files:
```powershell
uv run pre-commit run --all-files
```
Test the secret scanner: stage a file with a made-up token, try to commit, and check that the commit is blocked. Then unstage and delete the file.
