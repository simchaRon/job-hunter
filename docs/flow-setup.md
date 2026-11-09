# Flow: setup

## What it does
Gets the project running on a Windows laptop.

## Steps
1. Install Python 3.12 and git.
2. Install the two tools (PowerShell):
   ```powershell
   winget install --id astral-sh.uv -e
   winget install --id Gitleaks.Gitleaks -e
   ```
3. Open a new terminal in the project folder. Check: `uv --version` and `gitleaks version`.
4. Install the packages: `uv sync`. This creates the `.venv` folder.
5. Turn on the commit checks: `uv run pre-commit install`.

## Rules
- Use `uv run <command>` to run anything in the project. It uses the right Python and packages.
- Secrets go in `.env` (never in Git). A sample file `.env.example` comes later in Phase 0.

## Files involved
- `pyproject.toml`: project name, packages, `jobs` command, tool settings.
- `uv.lock`: exact package versions (so every install is the same).
- `.python-version`: the Python version for uv.
- `.pre-commit-config.yaml`: see [flow-commit-checks.md](flow-commit-checks.md).

## How to test
```powershell
uv sync
uv run pytest
```
