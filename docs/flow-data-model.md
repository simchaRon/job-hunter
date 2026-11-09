# Flow: data model

## What it does
Defines the nine database tables. The tables are Python classes in `models.py`.
The same classes are used for data, validation and the database (SQLModel).

## Steps
1. Each class with `table=True` becomes one table.
2. `db.init_db()` creates all the tables (see [flow-init.md](flow-init.md)).
3. Code reads and writes rows with a SQLModel `Session`.

## Tables
| Table | What it holds |
| --- | --- |
| `user` | The person using the system (one row for now). |
| `company` | Target companies, ATS type, priority and monthly cap. |
| `job` | A job posting. The central table. Keeps the raw text. |
| `match` | Score 0-100 of a job, strengths, gaps, recommendation. |
| `cv_version` | Each tailored CV that was made. All versions are kept. |
| `application` | My application to a job and its status. |
| `event` | History of an application (applied, call, interview...). |
| `message` | Emails linked to an application and draft replies. |
| `interview` | Interviews, linked to a calendar event. |

## Rules
- Every table except `user` has `user_id`. Every query must filter by it.
- Dates are stored in UTC. SQLite drops the timezone, so dates come back without one.
- JSON and list fields use the SQL `JSON` type.
- `interview.start_at` and `end_at` are not called `start` and `end`, because `end` is an SQL keyword.
- Statuses: `new`, `shortlisted`, `cv_ready`, `applied`, `screening`, `interview`, `offer`, `rejected`, `withdrawn`, `skipped`, `waitlist`.
- Tables link by plain foreign keys (no `Relationship()` yet, to keep it simple).

## Files involved
- `src/job_hunter/models.py`: all tables and the two enums (`ApplicationStatus`, `Language`).
- `docs/spec.md` section 5: the original design.

## How to test
```powershell
uv run pytest tests/test_models.py
```
