# Smart Job Search System – Specification

Nov 9, 2026 · Simcha Ron Godinger

## 1. Introduction

A personal, local Python system that collects job postings, scores each one against my profile, generates a tailored CV per job, and manages the whole application pipeline from one dashboard. An AI agent handles replies from recruiters and interview scheduling. I approve each job with one tick in the dashboard; from there the system tailors the CV, fills in the application and submits it by itself.

### Goals

1. **Miss nothing** – collect jobs from many sources into one place, without duplicates.
2. **Prioritize** – a 0–100 match score per job with a short explanation.
3. **Highlight the right things** – a CV tailored to each job's requirements, never inventing experience.
4. **Know where I stand** – a status for every job: found, applied, interview, rejected, etc.
5. **Respond fast** – an agent drafts replies to recruiters and schedules interviews, after my approval.
6. **Learn and document** – a clean project that also serves as a GitHub portfolio piece.

### Decisions and targets

| Topic | Decision |
| --- | --- |
| Volume | 50+ applications per week in the first phase, including jobs from general job boards |
| First target company | Israel Aerospace Industries (IAI) |
| Company priority | Companies with offices in Israel come first |
| Per-company cap | 3–4 applications per company per calendar month – 4 for priority-A companies, 3 for the rest – only the most relevant jobs |
| Target roles | Open: any role where the profile matches (Python, AI, data, intelligence, systems, and more) – the score decides, not a fixed title list |
| Seniority | Entry to mid level: about 2 years of relevant experience from military service; skip roles requiring 4+ years |
| Location | Hybrid preferred; fully on-site accepted in the Jerusalem area or the Center; remote welcome |
| CV language | Follows the job description: English posting → English CV, Hebrew posting → Hebrew CV |
| Apply threshold | 70%+ match, provided the core must-have requirements are met; not every requirement is needed |
| Runtime | Runs on my Windows laptop, only while it is on; availability is limited and the design accepts that |
| Gmail | Connected from the early phases: job alerts, recruiter replies, reply drafts |
| Communication agent | Replies to recruiters and schedules interviews in Google Calendar – only after my approval |
| Notifications | Email first; WhatsApp in a later phase |
| AI access | I have a Claude Pro plan (for Claude Code); the system's own AI calls use a separate, pay-as-you-go API key, capped at $5 a month to start |
| Repository | Public on GitHub as a portfolio piece |
| Future | A personal job-search app anyone can spin up for themselves by uploading a CV |

### Out of scope (first version)

- Fully automatic submission without my approval.
- Scraping LinkedIn or any site whose terms forbid it.
- Multiple users – but the code is built from day one so it can become a multi-user app (section 11).

### Guiding principles

- **Human in the loop:** the AI proposes, I approve. Every outbound action requires my click: one tick per job for an application (everything after it is automatic), one click per email or calendar event.
- **Truth only:** the AI may rephrase and reorder; it may not add skills or experience absent from the master profile.
- **Local first:** data stays on my machine (SQLite); API keys live in `.env`, never in Git.
- **Simple before smart:** first working end-to-end with manual link pasting, then more sources and automation.
- **Everything documented:** a README per module, every architectural decision in `docs/decisions/`.

## 2. Functional requirements

Eight modules; every requirement has an ID (FR-x.y) to reference in Claude Code prompts, tests and commits. Priority: M = must for MVP, S = should, C = could.

| ID | Module | Requirement | Priority |
| --- | --- | --- | --- |
| FR-1.1 | Master profile | One YAML file holding all experience, projects, skills and education – the single source of truth | M |
| FR-1.2 | Master profile | Initial import from existing CVs (DOCX/PDF) into YAML with AI, followed by manual review | M |
| FR-1.3 | Master profile | Tags on every item (python, ai, intelligence, teaching, clearance) used for matching | M |
| FR-1.4 | Master profile | Every item in both Hebrew and English (two fields), so both CV languages come from one source | M |
| FR-2.1 | Job collection | Manual job entry: paste a link or the job text | M |
| FR-2.2 | Job collection | Scheduled automatic collection from permitted sources (section 3), starting with IAI, plus general job boards | M |
| FR-2.3 | Job collection | Duplicate detection (same job on several sites) | M |
| FR-2.4 | Job collection | Location filter: jobs in Israel first; companies without an Israeli office are deprioritized | M |
| FR-3.1 | Job parsing | Structured extraction: title, company, location, must-haves, nice-to-haves, keywords | M |
| FR-3.2 | Job parsing | Detect the posting language (Hebrew / English) and store it on the job | M |
| FR-4.1 | Matching | 0–100 match score with breakdown: what fits, what's missing, risks | M |
| FR-4.2 | Matching | Rule-based pre-filter before spending on AI: location (hybrid, or on-site in the Jerusalem area / Center), required seniority (drop 4+ years), job type | M |
| FR-4.3 | Matching | Decision rule: recommend applying at 70+ when all core must-haves are met, even if secondary requirements are missing (section 6) | M |
| FR-5.1 | CV | Tailored CV: select items, order them, rephrase existing bullets, surface the job's keywords | M |
| FR-5.2 | CV | CV language set automatically per FR-3.2, by reading that language's fields from the profile (no translation at runtime); DOCX export in the MVP, PDF added in Phase 2; correct RTL for Hebrew | M |
| FR-5.3 | CV | Tailored cover letter in the same language, plus a one-click "copy opening line" button to paste into application forms | S |
| FR-5.4 | CV | Diff view between master and tailored version + manual edit before approval | M |
| FR-5.5 | CV | Per-job approval: no CV is generated and nothing is submitted until I approve that specific job in the dashboard; approvals can be done in a row on one screen, to sustain 50+ applications a week | M |
| FR-6.1 | Tracking | Status per job, dates, notes, contact, which CV version was sent | M |
| FR-6.2 | Tracking | Follow-up reminders (e.g. 7 days without a response) | S |
| FR-6.3 | Tracking | Gmail integration: detect company emails, link them to applications, suggest status updates | M |
| FR-6.4 | Tracking | Hard cap: 3–4 applications per company per calendar month (4 for priority A, 3 for the rest) – the highest-scoring jobs; the rest wait or are dropped | M |
| FR-7.1 | Dashboard | Job table with filters and sorting, a clickable link to the original posting on every job, Kanban board by status, detailed job page | M |
| FR-7.2 | Dashboard | Stats: applications per week vs. the 50 target, response rate, stage funnel | S |
| FR-8.1 | Comms agent | Classify incoming email: interview invite, information request, home assignment, rejection, other | M |
| FR-8.2 | Comms agent | Draft a reply in my name (in the incoming email's language), saved as a Gmail draft and sent only after my approval | M |
| FR-8.3 | Comms agent | Propose interview slots from my Google Calendar availability; create the event after approval | M |
| FR-8.4 | Comms agent | Notify me of every new message – by email first, WhatsApp later – with a link to approve / edit / reject in the dashboard | M |

## 3. Job sources and site integration

Every source connects through a uniform adapter, and the level of automation is set by what each site permits. LinkedIn's terms forbid scraping and bots, and a flagged account can be banned – so there the system only reads jobs I bring to it and never acts on my behalf.

| Source | Connection | Automation | Notes |
| --- | --- | --- | --- |
| Manual paste (any site) | Link or pasted text → AI extraction | Manual | MVP foundation; works with any site |
| Company career pages (Comeet, Greenhouse, Lever) | Public ATS APIs | Full | Most Israeli tech companies use one of these; company list in `companies.yaml`. Verify API endpoints per vendor |
| LinkedIn | Job Alert emails read via Gmail API, or pasted link | Semi-automatic | No scraping, no automated submission; Easy Apply stays manual |
| GotFriends, Drushim, AllJobs, JobMaster | Email alerts / RSS where available / paste | Semi-automatic | Check each site's terms and robots.txt before any automation |
| Civil service and IDF positions | Paste / RSS where available | Manual | Relevant for the intelligence-officer and civil-service track |
| Recruitment agencies and recruiter outreach | Manual entry of job + contact | Manual | Track who submitted me where, to avoid double submission |

Jobs from general boards count toward the weekly target and toward the per-company monthly cap of the hiring company.

### Adapter interface

```python
class JobSource(Protocol):
    name: str

    def fetch(self, since: datetime) -> list[RawJob]: ...
```

Each adapter returns `RawJob` (title, company, link, text, date, source); the rest of the system doesn't know where a job came from. Adding a site = a new file in `sources/` and a line in `config.yaml`.

### First target company: IAI

IAI publishes jobs on its own careers site (jobs.iai.co.il), and some jobs also appear on LinkedIn and Drushim. Postings come in both Hebrew and English – a good test case for language detection.

- [ ] Manually review the careers site: how the listing is built, any RSS or internal API, terms of use and robots.txt.
- [ ] Based on that: a `sources/iai.py` adapter (automatic if permitted) or manual paste + email alerts.
- [ ] Initial search keywords in `config.yaml`: Python, AI, algorithms, intelligence, data, information systems.
- [ ] Tag the security clearance and Air Force Intelligence service in the profile – especially relevant in the defense industry.
- [ ] Apply through the site's form with the application package, or by email when the posting points to a recruiter.

### Target company list (first version of companies.yaml)

The four defense and cyber companies I chose come first, followed by companies from the top 30 of the two latest rankings: CofaceBDi 2026 (whole economy, July 2026) and Duns 100 high-tech 2026 (November 2026). All have offices in Israel. Each company gets 3–4 applications a month (4 for priority A).

| Company | Sector | BDi 2026 rank | Duns high-tech 2026 rank | Priority |
| --- | --- | --- | --- | --- |
| Israel Aerospace Industries (IAI) | Defense | 2 | – | A |
| Rafael | Defense | – | 22 | A |
| Elbit Systems | Defense | 7 | – | A |
| Check Point | Cyber | 9 | – | A |
| NVIDIA Israel | Chips, AI | 1 | 1 | B |
| Microsoft Israel | Software | 4 | 3 | B |
| Google Israel | Internet, AI | 3 | 19 | B |
| Applied Materials | Chips | 5 | – | B |
| SAP Labs Israel | Enterprise software | 8 | 7 | B |
| Island | Cyber | – | 2 | B |
| Palo Alto Networks | Cyber | – | 4 | B |
| Salesforce | Enterprise software | – | 5 | B |
| Silverfort | Cyber | – | 6 | B |
| Panaya | Enterprise software | – | 8 | B |
| Autodesk Israel | Software | – | 9 | B |
| AppsFlyer | Ad & marketing tech | – | 10 | B |
| Rubrik | Cyber | – | 11 | B |
| Cloudinary | Software | – | 12 | B |
| Overwolf | Gaming | – | 13 | B |
| WSC Sports | AI products | – | 14 | B |
| mavens by Zynga | Gaming | – | 15 | B |
| ServiceNow | Enterprise software | – | 16 | B |
| Coralogix | Observability | – | 17 | B |
| Optibus | Mobility | – | 18 | B |
| Thales-Imperva | Cyber | – | 20 | B |
| Meta | Internet | – | 21 | B |
| Intel Israel | Chips | – | 23 | B |
| Apple Israel | Hardware | – | 24 | B |
| Akamai | Cyber | – | 25 | B |
| Amazon Israel | Software, cloud | – | 26 | B |
| Orca Security | Cyber | – | 27 | B |
| Fullpath | Enterprise software | – | 28 | B |
| Upwind Security | Cyber | – | 29 | B |
| Taboola | Ad & marketing tech | – | 30 | B |

Volume check: 4 companies × 4 + 30 companies × 3 = up to ~106 a month (~25 a week) from target companies; general job boards fill the rest of the 50+ weekly target, so they matter more than the target list for volume.

- [ ] For each company: identify the careers site and ATS (Comeet / Greenhouse / Lever / custom) – this decides which adapter is needed.
- [ ] Review the list and drop companies that don't fit the Python/AI or intelligence direction.

### Submission – one tick, then automatic

My only manual step is a tick on the job in the dashboard. Everything after it runs by itself:

1. **Approve:** I tick "Apply" on a job (after opening the posting link if I want more detail).
2. **Prepare:** the system generates the tailored CV and cover line in the posting's language and runs the safety checks (section 6).
3. **Submit:** through the channel the posting supports (table below), on my laptop, with my details.
4. **Stop when unsure:** a CAPTCHA, a login wall, a required question the profile and `form_answers.yaml` don't cover, or a field it can't fill with confidence – the system stops before submitting, saves progress, and notifies me with exactly what is missing. It never bypasses a CAPTCHA or other bot check.
5. **Record:** status set to `applied`, with proof saved (confirmation screenshot or the sent email), and a notification to me.

| Channel | How it submits | Notes |
| --- | --- | --- |
| Email application ("send CV to…") | Gmail API – an email from my address with the CV attached and a short cover note | Simplest and most reliable; first to build |
| Company career form (Comeet, Greenhouse, Lever, IAI site, other custom sites) | Playwright opens the form in a browser on my laptop, fills the fields, uploads the CV, answers extra questions, submits | One form handler per ATS type, so one handler covers many companies; custom sites need their own handler |
| General job boards (GotFriends, Drushim, AllJobs, JobMaster) | Same browser automation, through my logged-in session on that site | Check each site's terms first; a site that forbids automation stays manual |
| LinkedIn Easy Apply | Not automated | LinkedIn's terms forbid bots, and accounts get restricted or banned. The dashboard opens the job for a manual apply instead |

#### Form answers

- Personal fields (name, email, phone, LinkedIn, GitHub) come from the profile.
- Recurring questions come from `form_answers.yaml`, filled once by me: availability / notice period, salary expectation, willingness to travel, military service, work authorization, how I heard about the job.
- Short free-text questions ("Why do you want to work here?") are written by the AI from the profile and the posting, in the posting's language, within the same truth rules as the CV.
- Never filled automatically: ID number, passwords, payment details, or any answer not covered by the profile and `form_answers.yaml` – those stop the run.

#### Auto-apply requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-9.1 | One tick per job in the dashboard starts the whole application; no other manual step when all fields are covered | M |
| FR-9.2 | Email applications sent via Gmail with the tailored CV attached | M |
| FR-9.3 | Browser form filling with Playwright, one handler per ATS type (Comeet, Greenhouse, Lever) plus custom handlers (IAI first) | M |
| FR-9.4 | `form_answers.yaml` for recurring questions; AI-written answers for short free-text questions | M |
| FR-9.5 | Stop-and-notify on CAPTCHA, login wall, unknown required field or low confidence; never bypass bot checks | M |
| FR-9.6 | Proof of submission saved per application (screenshot or sent email) | M |
| FR-9.7 | Submission queue: approved jobs wait until the laptop is on, then run one at a time with a pause between them | M |
| FR-9.8 | Dry-run mode: fill the form and save a screenshot without submitting, to test a new handler | S |

## 4. Architecture and technology

A single, local, layered Python monolith: sources → parsing → matching → CV → tracking → dashboard, all around one SQLite database. No servers and no Docker at first.

```text
 Job sources ──► Job parsing ──► Match and score ──► Tailored CV
 (APIs, alerts,  (AI: require-    (rules + AI,        (master profile
  paste)          ments)           0–100)              + AI)
      │               │                 │                  │
      └───────────────┴──── read / write ──────────────────┘
                              │
                     ┌────────▼────────┐
                     │ SQLite database │  jobs, scores, CV versions,
                     └────────┬────────┘  applications, emails
                ▲             │
                │             ▼
  Comms agent ──┘ drafts ► Streamlit dashboard ── one tick ──► Auto-submit
  (Gmail + Calendar)       (I approve each job                (email or browser form)
                            with one tick)
```

A job flows left to right through four stages, each saving its result to the database; the agent's drafts and the application packages both pass through the dashboard, where I approve them.

### Technology

| Layer | Choice | Why |
| --- | --- | --- |
| Language and environment | Python 3.12, uv for packages | Fast and simple, one `pyproject.toml` |
| Models and validation | Pydantic | Same models for data, AI output and tests |
| Database | SQLite + SQLModel | One file, no install; easy move to Postgres later |
| AI | Anthropic SDK (Claude) with structured output into Pydantic | Extraction, scoring and rewriting return valid JSON |
| Collection | httpx, feedparser, Gmail API; Playwright for submitting applications | Public APIs, RSS and alert emails |
| CV | docxtpl (Word template) + PDF via docx2pdf (uses installed Word) or LibreOffice | One designed template per language; the Hebrew template is set to right-to-left in Word itself, to avoid reversed punctuation |
| Dashboard | Streamlit | Python only, no HTML/JS; tables, charts and forms built in |
| CLI | Typer | `jobs fetch`, `jobs score`, `jobs cv <id>` |
| Scheduling | Windows Task Scheduler (run at logon) + APScheduler while the app is open | Catch-up run at startup, then periodic collection and inbox checks while the laptop is on |
| Google | google-api-python-client + OAuth | Gmail and Calendar |
| Quality | pytest, ruff, pre-commit | Tests and consistent formatting |
| Docs | MkDocs + README per module | Local docs site from `docs/` |

### Folder layout

```text
job-hunter/
├── CLAUDE.md              # Instructions for Claude Code: style, commands, rules
├── README.md
├── ROADMAP.md             # phases and tasks, ticked off as they're done
├── pyproject.toml
├── .env.example           # ANTHROPIC_API_KEY=... (the real .env is not in Git)
├── config/
│   ├── config.yaml        # sources, keywords, thresholds, quiet hours
│   ├── companies.yaml     # target companies, ATS, monthly cap
│   ├── form_answers.yaml  # my answers to recurring application questions (NOT committed)
│   ├── profile.example.yaml  # fictional sample profile (committed)
│   └── profile.yaml       # master profile – source of truth (NOT committed)
├── templates/
│   ├── cv_he.docx
│   └── cv_en.docx
├── src/job_hunter/
│   ├── models.py          # Pydantic/SQLModel
│   ├── db.py
│   ├── sources/           # one adapter per site
│   ├── parsing/           # requirement extraction, language detection
│   ├── matching/          # rule filter + AI scoring + monthly cap
│   ├── cv/                # tailoring, rendering, export
│   ├── tracking/          # statuses and reminders
│   ├── apply/             # one-tick submission: email sender, Playwright form handlers
│   ├── agent/             # email classification, reply drafts, calendar
│   ├── notify/            # email (later WhatsApp) notifications
│   ├── llm/               # AI client + prompt loading
│   ├── cli.py
│   └── dashboard/         # Streamlit app
├── prompts/               # versioned prompt files
├── data/                  # jobs.db, generated CVs (not in Git)
├── tests/
└── docs/
    ├── spec.md            # this document
    ├── decisions/         # ADRs
    └── modules/
```

## 5. Data model

Nine tables. The job is the central entity; everything else points to it. Every table carries a `user_id` from day one, so moving to a multi-user app won't require a rebuild.

| Table | Key fields | Notes |
| --- | --- | --- |
| `user` | id, name, email, profile_path, settings_json | One row (me) in the first phase |
| `company` | id, name, website, has_israel_office, ats_type, ats_token, priority, monthly_cap | monthly_cap: 4 for priority A, 3 otherwise |
| `job` | id, company_id, source, url, title, location, language, raw_text, parsed_json, fingerprint, found_at, is_active | language = he / en; fingerprint = hash for duplicate detection |
| `match` | id, job_id, score, must_have_met, strengths, gaps, recommendation, model, prompt_version, created_at | must_have_met = all core must-haves satisfied |
| `cv_version` | id, job_id, content_json, docx_path, pdf_path, language, approved, created_at | Every version kept – I know exactly what was sent |
| `application` | id, job_id, cv_version_id, status, approved_at, applied_at, submission_channel, submission_proof_path, missing_fields, contact, next_followup, notes | Pipeline status |
| `event` | id, application_id, type, date, notes | History: applied, call, interview, home assignment, answer |
| `message` | id, application_id, gmail_thread_id, direction, category, body, draft_reply, reply_status, created_at | Incoming emails, classification and the agent's draft replies |
| `interview` | id, application_id, start, end, location_or_link, calendar_event_id, status | Linked to the Google Calendar event |

### Application statuses

`new` → `shortlisted` → `cv_ready` → `applied` → `screening` → `interview` → `offer` / `rejected` / `withdrawn`. A job I chose to skip gets `skipped`; a job held back by the monthly cap gets `waitlist`.

### Master profile (short example)

```yaml
experience:
  - id: iaf-intel
    org: {he: מודיעין חיל האוויר, en: Israeli Air Force Intelligence}
    role: {he: פיתוח טכנולוגי (שירות סדיר), en: Software Developer (regular service)}
    start: 2017-11
    end: 2019-11
    tags: [python, javascript, development, gis, esri, matlab, intelligence, clearance]
    bullets:
      - id: iaf-1
        tags: [python, javascript, development, gis]
        he: פיתוח 3 אפליקציות מבצעיות מאפס ותחזוקה של 2 נוספות ב-Python ו-JavaScript
        en: Built 3 operational applications from scratch and maintained 2 more in Python and JavaScript
projects:
  - id: story-app
    name: {he: DreamTale AI, en: DreamTale AI – bedtime story app}
    url: https://github.com/simchaRon/storyMe
    tools: [Python, FastAPI, SQLAlchemy, PostgreSQL, Claude API, Expo, React Native]
    tags: [ai, python, llm, fastapi, mobile]
```

Every bullet has an ID and tags, so the AI selects and rephrases existing bullets instead of writing from scratch.

## 6. AI engine: matching and CV tailoring

Three separate AI calls per job, each with its own prompt file and structured (Pydantic) output, so each stage can be tested, improved and costed on its own.

1. **Extract** – input: job text. Output: `JobRequirements` (title, required seniority, core must-haves, secondary must-haves, nice-to-haves, technologies, location, job type). A small, fast model is enough.
2. **Score** – input: requirements + profile. Output: `MatchResult` – 0–100 score, requirements met with a pointer to the profile item, gaps, `must_have_met`, and a recommendation: apply / apply with emphasis / skip.
3. **Tailor** – input: requirements + profile + score. Output: `TailoredCV` – which items to include and in what order, a tailored summary, and rephrased existing bullets using the job's keywords.

### Decision rule: when to apply

The score does not require meeting every requirement. Each extracted requirement gets one of three levels, and the score is weighted:

| Level | Example | Weight |
| --- | --- | --- |
| Core must-have | "Python development experience", "CS degree" | 60% |
| Secondary must-have | "Familiarity with Docker", "2 years of experience" | 25% |
| Nice-to-have | "Defense industry experience" | 15% |

- **Apply:** score 70+ and all core must-haves met (`must_have_met = true`).
- **Apply with emphasis:** score 70+ and one core must-have missing but with a close substitute (e.g. a course instead of experience) – the CV highlights the substitute.
- **Skip:** score below 70, or two or more core must-haves missing.
- Threshold and weights live in `config.yaml` and are calibrated after the first weeks against the actual response rate.

### Monthly cap: 3–4 applications per company

To avoid flooding the same recruiters, each company gets at most 3–4 applications per calendar month (4 for priority A, 3 for the rest), and only the most relevant jobs:

1. Jobs that pass the decision rule enter the company's queue, sorted by score.
2. The top 3 or 4 for the month are marked "to apply"; the rest get `waitlist` and appear separately in the dashboard.
3. A new job scoring higher than one not yet applied to replaces it (an already submitted application is never replaced).
4. At the start of a new month, still-open waitlisted jobs are re-ranked against new ones.
5. I can override the cap manually for a single job, with explicit confirmation.

The cap is enforced in code (checked before CV generation and before marking "Applied") and set per company in `companies.yaml` (4 for priority A, 3 otherwise).

### Language

Posting language is detected in code (Hebrew vs. Latin character counts), without an AI call. The CV, cover letter and agent replies are written in that language; for mixed postings, the language of the title and requirements decides.

### Rewriting safety rules

- Every output bullet must point to an existing `bullet_id` in the profile; a bullet without a source is rejected in code.
- No adding a technology, degree, role or number absent from the profile. An automatic check compares output keywords against the profile and flags suspicious ones.
- Length limits: one to two pages, max bullets per role.
- Final approval is manual, through the diff view in the dashboard.

### Prompts and cost

- Prompts in `prompts/` with version numbers; every result is stored with its prompt version.
- Cache: the same job and profile are never sent twice. The raw posting text is always kept, so a `jobs reparse` command can re-run extraction on all past jobs after a prompt improvement.
- Cheap rule filtering before AI scoring (FR-4.2), and CV tailoring only for shortlisted jobs.
- Estimated cost logged per call, monthly total in the dashboard.
- A "golden set" of 10–15 real jobs I scored by hand, for comparing prompt changes.

### Working within $5 a month

With 50+ applications a week the budget is tight, so cost control is part of the design, not an afterthought:

1. **Free first:** rule pre-filter, duplicate check, language detection and the monthly cap all run in code, with no AI call.
2. **Smallest model for volume:** extraction and scoring use the cheapest Claude model; a stronger model is used only for CV tailoring and agent replies.
3. **One call where possible:** extraction and scoring can be merged into a single call per job if measurements show it saves money without hurting quality.
4. **Prompt caching:** the master profile is a long, fixed prefix in every call – cache it.
5. **Tailor only what I shortlist:** no CV is generated for jobs I haven't approved.
6. **Measure:** cost per job and per application shown in the Stats screen; after the first month, decide whether $5 is enough.

### Public repository rules

- `.gitignore` from the first commit: `profile.yaml`, `data/`, `.env`, `logs/`, OAuth token files.
- The repo ships `profile.example.yaml` with a fictional person and `.env.example` with empty keys.
- A pre-commit secret scanner (e.g. gitleaks) blocks commits that contain keys or tokens.
- The README presents the project as a portfolio piece: problem, architecture diagram, screenshots, how to run.

## 7. Dashboard and daily workflow

The dashboard (Streamlit, Hebrew UI with right-to-left layout) is the only place I work from day to day. Six screens:

| Screen | What I see | Actions |
| --- | --- | --- |
| Inbox | Collected jobs sorted by score, with source tag, 3 short reasons and the company's monthly cap usage (e.g. 2/3) and a link to the original posting | Approve for application / skip / open the original posting on the company's site |
| Approvals queue | CVs and agent reply drafts waiting for me | Approve, edit or reject – one by one or in batch |
| Applications board (Kanban) | A column per status, a card per job | Drag or click to change status, follow-up reminder |
| Job page | Job text, parsed requirements, score and gaps, event history, linked emails | Generate tailored CV, diff vs. master, edit, approve, download DOCX/PDF, mark "Applied" |
| Profile | Master profile in readable form | Edit (or edit the YAML directly) |
| Stats | Applications per week vs. 50 target, response rate, stage funnel, average score by source, AI cost | Filter by period |

### A typical day

1. Collection runs automatically when the laptop starts (or `jobs fetch`).
2. Open the Inbox, go through jobs scoring 70+, open the posting link when I need more detail, and approve each relevant job for application – or skip it.
3. CVs are generated only for the jobs I approved; I review each one (diff vs. master) and approve it in the approvals queue.
4. The system submits each approved job by itself; I only handle the few that stopped for a missing answer or a CAPTCHA.
5. Handle agent notifications as they arrive: approve replies and interview slots.
6. Once a week: review reminders and update statuses on the board.

## 8. Communication agent, calendar and notifications

The agent reads emails from companies, understands what they ask, prepares a reply and proposed slots – and never sends anything or books anything without my approval. Every outbound action goes through the approvals queue.

### Flow

1. **Intake:** on startup, and then every 15 minutes while the laptop is on, the agent checks Gmail for new emails since its last run from companies I applied to, or containing keywords (interview, ראיון, application).
2. **Link and classify:** links the email to an application (by domain, company name, job title) and classifies it: interview invite / information request / home assignment / rejection / other.
3. **Prepare:** drafts a reply in the incoming email's language, in my style. For an interview invite, it pulls my availability from Google Calendar and proposes 2–3 free slots.
4. **Notify:** the draft is saved as a Gmail draft, appears in the approvals queue, and I get a notification.
5. **Approve:** approve and send / edit / reject.
6. **Execute:** only after "approve" – the email is sent in the same thread and the application status is updated.
7. **Calendar:** when the other side confirms a slot, the agent proposes a calendar event (title, company, job, video link or address, contact). After my approval the event is created, with a prep reminder the day before.
8. **Rejection:** a rejection email sets the status to `rejected`, no reply needed (unless I ask).

### Limited availability (laptop only)

The system runs only while my laptop is on, so the agent can be hours late. The design handles that:

- Every job keeps a "last run" timestamp; on startup the system catches up on everything since then (jobs, emails).
- Messages are processed oldest first, and interview invites are flagged urgent at the top of the approvals queue.
- The Gmail draft is the safe point: if the laptop shuts down mid-run, nothing is lost and nothing is sent twice.
- If response time becomes a problem, the agent alone can later move to a small always-on cloud machine (Phase 5).

### Agent rules

- Never commits on my behalf to salary, start date or giving anything up – flags it as "needs your decision".
- Never discloses personal data not in the profile (ID number, full address, etc.).
- Never cancels or moves existing calendar events.
- Every sent email and created event is logged in `message` / `interview`.

### Notifications to me

Email first; WhatsApp is added in a later phase.

| Channel | How | Phase | Notes |
| --- | --- | --- | --- |
| Email | Gmail API – an email to myself with a summary, the draft, and a dashboard link | Phase 4 | No cost, works from day one |
| WhatsApp | WhatsApp Business Cloud API (Meta) or a provider such as Twilio – a short message with a dashboard link | Later | Needs a business account and a separate sender number; proactive messages use pre-approved templates. Check cost and terms first |

- The notification holds only company, job, message type and what's waiting – not the full email.
- Approval itself happens in the dashboard.
- Quiet hours in `config.yaml` (e.g. not on Shabbat or at night), except an interview booked for the next day.

### Google permissions (OAuth)

| Service | Scope | Why |
| --- | --- | --- |
| Gmail | gmail.readonly | Read incoming emails and job alerts |
| Gmail | gmail.compose | Create drafts, send after approval, send notifications to myself |
| Google Calendar | calendar.events + freebusy | Check availability and create events |

OAuth tokens are stored locally in an encrypted file, never in Git. For personal use the Google Cloud project stays in Testing mode with my account as the only test user – no Google verification needed. In Testing mode Google's refresh tokens expire after about 7 days, so the system detects an expired token, emails me, and offers a one-click re-login.

## 9. Non-functional requirements, documentation and testing

| ID | Area | Requirement |
| --- | --- | --- |
| NFR-1 | Privacy and security | All data local; `.env`, `data/`, `profile.yaml`, `form_answers.yaml` and OAuth tokens in `.gitignore`; no personal data sent anywhere except the AI API and my own Google account |
| NFR-2 | Legal | Each adapter documents the site's policy and access method at the top of the file; no scraping where forbidden; request rate limited |
| NFR-3 | Resilience | One failing source doesn't stop the others; errors logged to `logs/` |
| NFR-4 | Cost | Hard monthly AI spend cap of $5 in `config.yaml` (also set as a spend limit in the API console); email alert at 80%; at 100% AI calls stop and jobs queue until next month or until I raise the cap |
| NFR-5 | Language | Hebrew UI with correct RTL; CVs in Hebrew and English |
| NFR-6 | Performance | Score 100 jobs in under 10 minutes; dashboard opens instantly |
| NFR-7 | Maintainability | Type hints everywhere, clean ruff, reasonable test coverage for logic (not UI) |
| NFR-8 | Safety of outbound actions | No email, calendar event or application is created without an explicit approval record in the database |

### Documentation

- `README.md` – what it is, setup in 5 steps, main commands.
- `CLAUDE.md` – context for Claude Code: project structure, run and test commands, code rules, "don't touch profile.yaml without asking".
- `docs/spec.md` – this document, updated as requirements change.
- `docs/decisions/` – a short ADR per decision (e.g. `0001-streamlit-not-react.md`): context, decision, alternatives.
- `CHANGELOG.md` – what was added in each phase.
- Docstrings on every public function.

### Testing

- Unit tests for each source adapter with saved responses (fixtures), no network.
- Tests for the AI module with mocked responses + a "no fabrication" check on the output.
- Tests for the monthly cap and the decision rule (pure logic, easy to test).
- Manual run of the golden set before any prompt change.
- `pytest` runs in pre-commit or GitHub Actions.

## 10. Roadmap and working with Claude Code

Seven phases; each ends with something that works and that I actually use in my job search. The task-level breakdown lives in `ROADMAP.md` in the repo.

1. **Phase 0 – Foundation:** folder layout, `pyproject.toml`, `CLAUDE.md`, `ROADMAP.md`, models (with user_id), SQLite, empty CLI, pytest running.
   - Done when: `jobs --help` works and one test is green.
2. **Phase 1 – Manual MVP end to end:** bilingual YAML profile (already prepared), job paste, language detection, extraction + scoring with the 70% rule, Hebrew and English DOCX CVs, status tracking, monthly cap.
   - Done when: a real IAI job has a ranked score and a CV the system generated.
3. **Phase 2 – Dashboard, one tick, email applications:** Inbox with posting links, one-tick approval, approvals queue, diff view, Gmail OAuth, automatic email applications with proof, PDF export, weekly counter vs. the 50 target.
   - Done when: one tick on an email-based job sends the application by itself.
4. **Phase 3 – Automatic form filling:** Playwright form handlers (IAI first, then Comeet, Greenhouse, Lever), `form_answers.yaml`, stop-and-notify, dry-run mode, submission queue.
   - Done when: one tick on an IAI job submits the form by itself, with a confirmation screenshot.
5. **Phase 4 – Automatic collection and Gmail tracking:** IAI adapter, ATS adapters for the target list, LinkedIn and GotFriends alerts via Gmail, duplicate detection, startup and periodic runs, linking emails to applications.
   - Done when: new ranked jobs are waiting whenever I open the laptop, and company replies update statuses.
6. **Phase 5 – Communication agent and calendar:** email classification, reply drafts, slot proposals and calendar events, email notifications.
   - Done when: I scheduled a real interview through the agent, with my approval.
7. **Phase 6 – Toward the app:** WhatsApp notifications, per-user settings, profile import from an uploaded CV, hosting preparation (section 11).

### How to work with Claude Code

- Save this document as `docs/spec.md` in the project folder.
- Start each phase in Plan Mode: ask for a plan, read it, correct it, only then approve code.
- One small task at a time, referencing the requirement ID (e.g. "implement FR-3.1").
- Ask for tests before or with the code, and run `pytest` before every commit.
- Commit after each working task; commit message includes the requirement ID.
- Ask Claude to update README and CHANGELOG at the end of each phase, and write an ADR for every significant decision.

### Suggested opening prompt

```text
Read docs/spec.md. We are starting Phase 0 only.
Create the folder layout, pyproject.toml with uv, CLAUDE.md,
Pydantic/SQLModel models per section 5, and a basic Typer CLI.
Python 3.12 with type hints. I'm on Windows.
I know Python at a basic level – briefly explain each file.
Show me a plan before writing any code.
```

## 11. Path to a multi-user app

The vision: anyone uploads a CV, the system builds a master profile from it, and from then on they get the whole pipeline – collection, matching, tailored CVs, tracking and the agent. The personal version is built so the move is an extension, not a rewrite.

| Topic | Now (personal) | Later (app) |
| --- | --- | --- |
| Users | user_id present, one user | Sign-in with Google, full isolation between users |
| Profile | YAML I edit | Upload CV → AI builds the profile → user confirms in a form |
| Database | Local SQLite | Managed PostgreSQL |
| Interface | Streamlit | FastAPI + web front end (or mobile app) |
| Background jobs | Local scheduler | Task queue (e.g. Celery / RQ) |
| Secrets and keys | Local `.env` | Encrypted per-user storage |
| AI cost | Mine | Per-user quota and a pricing model |

### What to do from day one

- No personal details of mine in code or prompts – everything comes from the profile and `config.yaml`.
- Every database query filters by user_id.
- Source adapters are generic (company list in a file, not in code).
- Profile import from a CV (FR-1.2) is a full feature – it's every new user's entry point.

### To check before a public launch

- **Google:** a public app requesting Gmail access must pass Google's verification; some Gmail scopes are classified as restricted and also require an external security assessment. Plan time and cost for it.
- **Privacy:** a database of other people's CVs is a personal-data database under Israel's Privacy Protection Law – privacy policy, data security, deletion on request. Consult a lawyer before launch.
- **Job-site terms:** automation allowed for personal use isn't necessarily allowed commercially.
- **Responsibility:** the agent sends emails in the user's name – human approval stays mandatory in the app too.

## 12. Open questions

These decide details in phases 1–4; none blocks Phase 0.

- [x] **Target roles:** open – any role the profile matches; the score decides.
- [x] **Seniority:** entry to mid level, 2 years of military experience (Nov 2017 – Nov 2019).
- [x] **Location:** hybrid preferred; on-site OK in the Jerusalem area or the Center.
- [x] **Where it runs:** my Windows laptop, while it's on.
- [x] **Operating system:** Windows.
- [x] **AI budget:** $5 a month to start, reviewed after the first month of real usage.
- [x] **Repository:** public on GitHub as a portfolio piece; `profile.yaml`, `data/`, `.env` and OAuth tokens never committed.
- [x] **Existing CVs:** imported into `profile.yaml` (bilingual), with project details from the GitHub READMEs.
- [ ] **Target list review:** which companies to drop or add.
