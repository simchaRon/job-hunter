"""The `jobs` command line tool."""

import typer

from job_hunter.db import get_db_path, get_engine, init_db

app = typer.Typer(help="Smart Job Search System.", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Smart Job Search System."""
    # This empty callback makes Typer keep `init` as a sub-command (`jobs init`).


@app.command()
def init() -> None:
    """Create the data folder and the database with all tables."""
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    init_db(get_engine())
    typer.echo(f"Database ready: {db_path}")


if __name__ == "__main__":
    app()
