"""Database tables for the job search system (spec section 5).

Nine tables. The job is the central table. Every table except `user` has a `user_id`,
so the project can become a multi-user app later without a rebuild.
All dates are stored in UTC.
"""

from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    """Return the current time in UTC."""
    return datetime.now(UTC)


class Language(StrEnum):
    """Language of a job posting or a CV."""

    HE = "he"
    EN = "en"


class ApplicationStatus(StrEnum):
    """Where an application is in the pipeline."""

    NEW = "new"
    SHORTLISTED = "shortlisted"
    CV_READY = "cv_ready"
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    SKIPPED = "skipped"  # I chose to skip this job
    WAITLIST = "waitlist"  # held back by the monthly cap


class User(SQLModel, table=True):
    """A person who uses the system. One row (me) in the first phase."""

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    profile_path: str | None = None
    settings_json: dict = Field(default_factory=dict, sa_type=JSON)


class Company(SQLModel, table=True):
    """A company I may apply to."""

    __tablename__ = "company"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str
    website: str | None = None
    has_israel_office: bool = True
    ats_type: str | None = None  # comeet / greenhouse / lever / custom
    ats_token: str | None = None
    priority: str = "B"  # "A" or "B"
    monthly_cap: int = 3  # 4 for priority A, 3 for the rest


class Job(SQLModel, table=True):
    """A job posting. The central table."""

    __tablename__ = "job"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    company_id: int | None = Field(default=None, foreign_key="company.id", index=True)
    source: str  # where the job came from, for example "manual"
    url: str | None = None
    title: str
    location: str | None = None
    language: Language | None = None
    raw_text: str = ""  # always kept, so we can re-parse later
    parsed_json: dict = Field(default_factory=dict, sa_type=JSON)
    fingerprint: str | None = Field(default=None, index=True)  # hash for duplicate detection
    found_at: datetime = Field(default_factory=utcnow)
    is_active: bool = True


class Match(SQLModel, table=True):
    """The score of one job against my profile."""

    __tablename__ = "match"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    job_id: int = Field(foreign_key="job.id", index=True)
    score: int  # 0-100
    must_have_met: bool  # all core must-haves satisfied
    strengths: list[str] = Field(default_factory=list, sa_type=JSON)
    gaps: list[str] = Field(default_factory=list, sa_type=JSON)
    recommendation: str  # apply / apply_with_emphasis / skip
    model: str | None = None
    prompt_version: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class CvVersion(SQLModel, table=True):
    """One tailored CV. Every version is kept, so I know what was sent."""

    __tablename__ = "cv_version"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    job_id: int = Field(foreign_key="job.id", index=True)
    content_json: dict = Field(default_factory=dict, sa_type=JSON)
    docx_path: str | None = None
    pdf_path: str | None = None
    language: Language
    approved: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class Application(SQLModel, table=True):
    """My application to one job, and its pipeline status."""

    __tablename__ = "application"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    job_id: int = Field(foreign_key="job.id", index=True)
    cv_version_id: int | None = Field(default=None, foreign_key="cv_version.id")
    status: ApplicationStatus = ApplicationStatus.NEW
    approved_at: datetime | None = None
    applied_at: datetime | None = None
    submission_channel: str | None = None  # email / form / manual
    submission_proof_path: str | None = None
    missing_fields: list[str] = Field(default_factory=list, sa_type=JSON)
    contact: str | None = None
    next_followup: datetime | None = None
    notes: str | None = None


class Event(SQLModel, table=True):
    """History of an application: applied, call, interview, answer..."""

    __tablename__ = "event"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    type: str
    date: datetime = Field(default_factory=utcnow)
    notes: str | None = None


class Message(SQLModel, table=True):
    """An email linked to an application, and the agent's draft reply."""

    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    application_id: int | None = Field(default=None, foreign_key="application.id", index=True)
    gmail_thread_id: str | None = Field(default=None, index=True)
    direction: str  # in / out
    category: str | None = None  # interview / info_request / assignment / rejection / other
    body: str = ""
    draft_reply: str | None = None
    reply_status: str | None = None  # drafted / approved / sent / rejected
    created_at: datetime = Field(default_factory=utcnow)


class Interview(SQLModel, table=True):
    """An interview, linked to a Google Calendar event."""

    __tablename__ = "interview"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    start_at: datetime  # "start" and "end" are avoided: "end" is an SQL keyword
    end_at: datetime
    location_or_link: str | None = None
    calendar_event_id: str | None = None
    status: str = "proposed"
