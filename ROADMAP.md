# ROADMAP – Smart Job Search System

The task list for building the system, phase by phase. Tick a box when the task is done and merged.
Requirement IDs (FR-x.y, NFR-x) point to `docs/spec.md`. One task ≈ one Claude Code session ≈ one or a few commits.

**How to use this file with Claude Code**

- Start each session with: "Read docs/spec.md and ROADMAP.md. Next task: <task ID>. Plan first."
- After a task is done: tick it here, update `CHANGELOG.md`, commit with the task ID (e.g. `feat(matching): P1-07 decision rule FR-4.3`).
- Don't start a phase before the previous phase's "Done when" is true.

---

## Phase 0 – Foundation

**Done when:** `jobs --help` works and one test is green.

- [x] **P0-01** Create the GitHub repo `job-hunter` (public), clone it locally on Windows.
- [x] **P0-02** Project setup with uv: `pyproject.toml`, Python 3.12, ruff, pytest, pre-commit.
- [x] **P0-03** `.gitignore` from the first commit: `.env`, `data/`, `logs/`, `config/profile.yaml`, `config/form_answers.yaml`, token files (NFR-1).
- [x] **P0-04** Secret scanner (gitleaks) in pre-commit.
- [x] **P0-05** Folder layout per spec section 4 (`src/job_hunter/...`, `config/`, `prompts/`, `templates/`, `tests/`, `docs/`).
- [x] **P0-06** `CLAUDE.md`: structure, run/test commands, code rules, "never touch profile.yaml or form_answers.yaml without asking".
- [x] **P0-07** Copy the spec to `docs/spec.md`, this file to `ROADMAP.md`, start `CHANGELOG.md` and `docs/decisions/0001-tech-stack.md`.
- [x] **P0-08** Data models (Pydantic/SQLModel) for all 9 tables, with `user_id` on every table (spec section 5).
- [x] **P0-09** `db.py`: create the SQLite database and tables on first run.
- [x] **P0-10** Typer CLI skeleton: `jobs --help`, `jobs init`.
- [x] **P0-11** First test: models create and read a job in an in-memory database.
- [x] **P0-12** `.env.example` and `config/profile.example.yaml` (fictional person).

## Phase 1 – Manual MVP end to end

**Done when:** a real IAI job has a ranked score and a CV the system generated.

- [ ] **P1-01** Load and validate `profile.yaml` (bilingual, bullet IDs, tags) – FR-1.1, FR-1.3, FR-1.4.
- [ ] **P1-02** `jobs add <url or text>`: save a job with its raw text and posting link – FR-2.1.
- [ ] **P1-03** Fetch the posting text from a URL where possible; fall back to pasted text.
- [ ] **P1-04** Language detection in code (Hebrew vs. Latin letters) – FR-3.2.
- [ ] **P1-05** LLM client: Anthropic SDK, model per task, prompt files from `prompts/`, prompt caching for the profile, cost logging per call – NFR-4.
- [ ] **P1-06** Extraction prompt → `JobRequirements` with core / secondary / nice-to-have levels – FR-3.1.
- [ ] **P1-07** Rule pre-filter: location, seniority (drop 4+ years), job type – FR-4.2.
- [ ] **P1-08** Scoring prompt → `MatchResult` with weighted score and `must_have_met` – FR-4.1.
- [ ] **P1-09** Decision rule (apply / apply with emphasis / skip) – FR-4.3. Unit tests.
- [ ] **P1-10** Monthly cap per company (4 for priority A, 3 for the rest), `waitlist` status – FR-6.4. Unit tests.
- [ ] **P1-11** `companies.yaml` with the target list and priorities.
- [ ] **P1-12** Tailoring prompt → `TailoredCV` using only existing bullet IDs – FR-5.1.
- [ ] **P1-13** "No fabrication" check: reject bullets without a source, flag new keywords.
- [ ] **P1-14** Word templates `cv_he.docx` (right-to-left set in Word) and `cv_en.docx`; render with docxtpl – FR-5.2.
- [ ] **P1-15** Status tracking and event history – FR-6.1.
- [ ] **P1-16** `jobs reparse`: re-run extraction on all stored raw texts.
- [ ] **P1-17** Monthly AI spend cap of $5 with stop at 100% – NFR-4.
- [ ] **P1-18** Golden set: 10–15 real jobs scored by hand, plus a command to compare.

## Phase 2 – Dashboard, one tick, email applications

**Done when:** one tick on an email-based job sends the application by itself.

- [ ] **P2-01** Streamlit app skeleton, Hebrew RTL layout – NFR-5.
- [ ] **P2-02** Inbox screen: jobs by score, reasons, cap usage, clickable link to the original posting – FR-7.1.
- [ ] **P2-03** One-tick approval per job ("Apply") – FR-5.5, FR-9.1.
- [ ] **P2-04** Job page: posting text, requirements, score and gaps, history, link.
- [ ] **P2-05** CV diff view (master vs. tailored) with manual edit – FR-5.4.
- [ ] **P2-06** Approvals queue screen.
- [ ] **P2-07** Kanban board by status.
- [ ] **P2-08** Google Cloud project in Testing mode, Gmail OAuth, encrypted token storage, expired-token re-login.
- [ ] **P2-09** Email applications via Gmail with the tailored CV attached – FR-9.2.
- [ ] **P2-10** Proof of submission (sent email saved) – FR-9.6.
- [ ] **P2-11** Cover letter and "copy opening line" button – FR-5.3.
- [ ] **P2-12** PDF export of CVs.
- [ ] **P2-13** Stats screen: weekly counter vs. 50, response rate, AI cost – FR-7.2.

## Phase 3 – Automatic form filling

**Done when:** one tick on an IAI job submits the form by itself, with a confirmation screenshot.

- [ ] **P3-01** Install Playwright on Windows; a browser profile dedicated to the system.
- [ ] **P3-02** `form_answers.yaml` (availability, salary expectation, military service, etc.) and its loader – FR-9.4.
- [ ] **P3-03** Form-filling engine: map fields to profile / form answers, upload CV, AI answers for short free-text questions – FR-9.3, FR-9.4.
- [ ] **P3-04** Stop-and-notify: CAPTCHA, login wall, unknown required field, low confidence; never bypass bot checks – FR-9.5.
- [ ] **P3-05** Dry-run mode: fill and screenshot without submitting – FR-9.8.
- [ ] **P3-06** IAI careers site handler (after checking the site's terms).
- [ ] **P3-07** Comeet handler.
- [ ] **P3-08** Greenhouse handler.
- [ ] **P3-09** Lever handler.
- [ ] **P3-10** Submission queue: runs when the laptop is on, one at a time, with pauses – FR-9.7.
- [ ] **P3-11** Confirmation screenshot saved as proof – FR-9.6.
- [ ] **P3-12** Handlers for general job boards that allow it (checked one by one).

## Phase 4 – Automatic collection and Gmail tracking

**Done when:** new ranked jobs are waiting whenever I open the laptop, and company replies update statuses.

- [ ] **P4-01** Source adapter interface (`JobSource`) and registry – section 3.
- [ ] **P4-02** IAI listing adapter (or email alerts, per the site check).
- [ ] **P4-03** Comeet / Greenhouse / Lever listing adapters for the target companies.
- [ ] **P4-04** Identify the ATS of every company in `companies.yaml`.
- [ ] **P4-05** LinkedIn and GotFriends job-alert emails read via Gmail – FR-2.2.
- [ ] **P4-06** Duplicate detection by fingerprint – FR-2.3.
- [ ] **P4-07** Israel-office priority and location filter – FR-2.4.
- [ ] **P4-08** Windows Task Scheduler at logon + catch-up run since the last run.
- [ ] **P4-09** Link company emails to applications and suggest status updates – FR-6.3.
- [ ] **P4-10** Follow-up reminders – FR-6.2.

## Phase 5 – Communication agent and calendar

**Done when:** I scheduled a real interview through the agent, with my approval.

- [ ] **P5-01** Email classification: interview / information request / home assignment / rejection / other – FR-8.1.
- [ ] **P5-02** Reply drafts in the email's language, saved as Gmail drafts – FR-8.2.
- [ ] **P5-03** Google Calendar OAuth, free/busy lookup, 2–3 proposed slots – FR-8.3.
- [ ] **P5-04** Calendar event creation after approval, prep reminder the day before.
- [ ] **P5-05** Email notifications to me, quiet hours (no Shabbat, no night) – FR-8.4.
- [ ] **P5-06** Agent rules: no commitments on salary or start date, no extra personal data, no changes to existing events.

## Phase 6 – Toward the app (future)

- [ ] **P6-01** WhatsApp notifications (WhatsApp Business Cloud API or Twilio) – check cost and terms first.
- [ ] **P6-02** Per-user settings; every query filtered by `user_id`.
- [ ] **P6-03** Profile import from an uploaded CV (DOCX/PDF) with a confirmation form – FR-1.2.
- [ ] **P6-04** Move the agent to a small always-on cloud machine, if laptop-only availability is a problem.
- [ ] **P6-05** PostgreSQL, FastAPI backend, web front end.
- [ ] **P6-06** Google verification for public Gmail access; privacy policy; legal review before launch.

## Backlog (ideas, not scheduled)

- Interview prep pack per company (role summary, likely questions, my matching stories).
- Weekly email digest: applications sent, replies, interviews, AI spend.
- A/B test of CV versions against response rate.
- Salary data per role from public sources.
