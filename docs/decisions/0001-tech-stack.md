# 0001 – Tech stack

Date: 2026-11-09 · Status: accepted

## Context
A personal job-search tool for one user on a Windows laptop. It may become a multi-user app later.
It must be simple to run, cheap, and good as a public portfolio project.

## Decision
- Python 3.12, with `uv` to manage packages (one `pyproject.toml`).
- SQLite with SQLModel (Pydantic models are also the database tables).
- Typer for the command line (`jobs ...`).
- Streamlit for the dashboard (Python only).
- Claude (Anthropic SDK) for AI steps.
- Quality tools: pytest, ruff, pre-commit, gitleaks.

## Alternatives
- Postgres from day one: more setup, not needed for one user. Easy to move to later.
- A React front end: more code and more languages. Streamlit is enough for now.
- pip and venv: slower and no lock file. `uv` is simpler.

## More detail
See [spec.md](../spec.md), section 4.
