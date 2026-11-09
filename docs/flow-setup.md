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
6. Copy the sample settings: `Copy-Item .env.example .env`. Fill in the values you need.
7. Later (Phase 1): copy `config/profile.example.yaml` to `config/profile.yaml` and put your real data in it.

## Rules
- Use `uv run <command>` to run anything in the project. It uses the right Python and packages.
- Secrets go in `.env` (never in Git). The sample file `.env.example` has no secrets.
- `config/profile.yaml` is private and not in Git. `config/profile.example.yaml` is a fictional sample.

## Files involved
- `pyproject.toml`: project name, packages, `jobs` command, tool settings.
- `uv.lock`: exact package versions (so every install is the same).
- `.python-version`: the Python version for uv.
- `.env.example`: sample settings (API key and database path).
- `config/profile.example.yaml`: fictional sample of the master profile (Hebrew and English fields).
- `.pre-commit-config.yaml`: see [flow-commit-checks.md](flow-commit-checks.md).

## How to test
```powershell
uv sync
uv run pytest
```
