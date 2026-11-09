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
   - `gitleaks`: scans the staged changes for keys, tokens and passwords.
3. If a check fixes a file, the commit stops. Run `git add` again, then commit again.

## Rules
- Never skip the `gitleaks` check.
- Never write a real key or token in any file, including docs.

## Files involved
- `.pre-commit-config.yaml`: the list of checks.
- `pyproject.toml`: the `ruff` settings.
- `.gitignore`: files that Git must never track (`.env`, `data/`, `config/profile.yaml`, ...).

## How to test
Run all checks on all files:
```powershell
uv run pre-commit run --all-files
```
Test the secret scanner: stage a file with a made-up token, try to commit, and check that the commit is blocked. Then unstage and delete the file.
