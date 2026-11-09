"""Test that the models can be saved to and read from an in-memory database."""

from sqlmodel import Session, select

from job_hunter.db import get_engine, init_db
from job_hunter.models import Company, Job, Language, User


def test_create_and_read_job() -> None:
    """A job with a user and a company is saved and read back correctly."""
    engine = get_engine("sqlite://")  # in memory: nothing is written to disk
    init_db(engine)

    with Session(engine) as session:
        user = User(name="Test User", email="test@example.com")
        session.add(user)
        session.commit()

        company = Company(user_id=user.id, name="Test Company", priority="A", monthly_cap=4)
        session.add(company)
        session.commit()

        job = Job(
            user_id=user.id,
            company_id=company.id,
            source="manual",
            title="מפתח Python",
            language=Language.HE,
            raw_text="Job text",
            parsed_json={"must_haves": ["python"]},
        )
        session.add(job)
        session.commit()
        job_id = job.id

    with Session(engine) as session:
        saved = session.exec(select(Job).where(Job.id == job_id)).one()
        assert saved.title == "מפתח Python"
        assert saved.language == Language.HE
        assert saved.parsed_json == {"must_haves": ["python"]}
        assert saved.user_id is not None
        assert saved.company_id is not None
