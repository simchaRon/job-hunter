# Flow: init (`jobs init`)

## What it does
Creates the local database on first run. It makes the `data/` folder and the SQLite file
`data/jobs.db` with all nine tables. It is safe to run again: existing data is kept.

## Steps
1. You run `uv run jobs init`.
2. `cli.py` finds the database path with `db.get_db_path()`.
   The path is `JOBS_DB_PATH` from `.env`, or `data/jobs.db` by default.
3. It creates the folder of that path if it is missing.
4. `db.init_db()` creates the tables from [flow-data-model.md](flow-data-model.md).
5. It prints the path of the database.

## Rules
- The database file is local and never goes into Git (`data/` and `*.db` are ignored).
- SQLite foreign keys are switched on for every connection (`db.get_engine`).
- Tests use an in-memory database (`sqlite://`), not the real file.

## Files involved
- `src/job_hunter/cli.py`: the `jobs` command and its `init` subcommand.
- `src/job_hunter/db.py`: path, engine and table creation.
- `src/job_hunter/models.py`: the tables.
- `.env.example`: shows the `JOBS_DB_PATH` setting.

## How to test
```powershell
uv run jobs init     # prints the database path
uv run pytest        # in-memory database test
```
