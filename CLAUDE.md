# CLAUDE.md – job-hunter

Instructions for Claude Code in this project. Full spec: `docs/spec.md`. Tasks: `ROADMAP.md`.

## Start here
- Read `docs/DOCS.md`, then only the one flow doc that matches the task.
- Work on one roadmap task at a time (for example `P0-08`). Plan first, then code.

## Structure
- `src/job_hunter/` – code. One subfolder per module (`sources`, `parsing`, `matching`, `cv`, `tracking`, `apply`, `agent`, `notify`, `llm`, `dashboard`). Top-level files: `models.py`, `db.py`, `cli.py`.
- `config/` – settings and profile. `prompts/` – AI prompts. `templates/` – Word templates.
- `tests/` – pytest tests. `scripts/` – helper scripts. `data/` and `logs/` – local, not in Git.

## Commands (PowerShell, from the project folder)
- Install: `uv sync`
- Run the CLI: `uv run jobs --help`
- Tests: `uv run pytest`
- Lint and format: `uv run ruff check .` and `uv run ruff format .`
- All commit checks: `uv run pre-commit run --all-files`

## Code rules
- Python 3.12. Type hints everywhere. A docstring on every public function.
- Open text files with `encoding="utf-8"` (Hebrew text).
- Every database table except `user` has a `user_id`. Every query filters by `user_id`.
- Store dates in UTC.
- No personal details in code or prompts. They come from the profile and config.
- Run `uv run pytest` before every commit.

## Safety rules
- **Never read, edit or print `config/profile.yaml` or `config/form_answers.yaml` without asking first.**
- Never commit `.env`, `data/`, `logs/`, tokens or keys. Never put secrets in docs.
- Never push to GitHub without asking.
- No email, calendar event or application is created without an approval record (NFR-8).

## Docs rules (always)
- Update the docs in the same change as the code. The commit check `docs-check` blocks code changes without docs.
- Every flow has a doc: copy `docs/_template-flow.md` to `docs/flow-<name>.md`.
- Every doc is linked from `docs/DOCS.md` (the index). Every code module has `docs/modules/<module>.md`.
- Simple English, short sentences. Explain terms.
- After each task: tick it in `ROADMAP.md`, add a line to `CHANGELOG.md`, and say which docs changed.

## Commits
- One commit per task. Message: `type(scope): <task ID> short text`, for example `feat(models): P0-08 nine tables`.
- End the message with the `Co-Authored-By` line.
