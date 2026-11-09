# job-hunter

Smart Job Search System. A personal, local Python tool that collects job postings,
scores each one against my profile, tailors a CV per job, and tracks the applications.

Full description: [docs/spec.md](docs/spec.md). Task list: [ROADMAP.md](ROADMAP.md).

## Status

Phase 0 (foundation) is in progress.

## Setup (Windows, PowerShell)

1. Install the tools once:
   ```powershell
   winget install --id astral-sh.uv -e
   winget install --id Gitleaks.Gitleaks -e
   ```
2. Open a new terminal in the project folder, then install the packages:
   ```powershell
   uv sync
   ```
3. Turn on the commit checks:
   ```powershell
   uv run pre-commit install
   ```

## Folders

| Folder | What is in it |
| --- | --- |
| `src/job_hunter/` | The Python code. One subfolder per module (`sources`, `parsing`, `matching`, `cv`, `tracking`, `apply`, `agent`, `notify`, `llm`, `dashboard`). They are empty for now. |
| `config/` | Settings and the master profile. Private files here are not in Git. |
| `prompts/` | Prompt files for the AI, with version numbers. |
| `templates/` | Word templates for the CV. |
| `tests/` | Automatic tests. |
| `docs/` | All documentation. Start at [docs/DOCS.md](docs/DOCS.md). |

## Run

```powershell
uv run jobs --help
uv run pytest
```

(The `jobs` command comes later in Phase 0.)
