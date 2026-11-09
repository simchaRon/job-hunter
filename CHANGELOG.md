# Changelog

What was added in each phase. Newest first.

## Phase 0 – Foundation (in progress)

- `.gitignore` and `.gitattributes` (P0-03).
- uv project with ruff, pytest and pre-commit (P0-02).
- Secret scanner (gitleaks) in the commit checks (P0-04).
- Folder layout (P0-05).
- Docs index, setup and commit-check flows (P0-07).
- First test: a job is saved and read back in an in-memory database (P0-11).
- CLI: `jobs --help` and `jobs init` (P0-10).
- `db.py`: SQLite engine, foreign keys on, table creation (P0-09).
- Data models: nine tables with `user_id` (P0-08).
- `CLAUDE.md` with project rules (P0-06).
- Docs check: git hook and Claude Code Stop hook keep docs in step with code.
