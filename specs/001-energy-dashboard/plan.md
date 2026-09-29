# Implementation Plan: Energy Dashboard

**Branch**: `master` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification and user-supplied technical constraints.

## Summary

Build a small server-rendered Energy Dashboard that demonstrates the Dockerfile-to-image-to-container-to-port-mapping path. Use Django project `config`, app `dashboard`, Django templates and forms, plain CSS, and SQLite. A single Docker image runs Django's development server on `0.0.0.0:8000`; users publish it to host port 8000. Do not add Docker Compose or PostgreSQL in this stage. Persist locally submitted contact messages in SQLite and keep that database in a named Docker volume so it survives container replacement.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.2.17 (5.2 LTS); official `python:3.12-slim-bookworm` image

**Storage**: SQLite database at `/app/data/db.sqlite3`, persisted with a named Docker volume

**Testing**: Django's built-in test runner and test client; Docker build and run smoke checks

**Target Platform**: Linux container run by Docker, accessed locally at `http://localhost:8000`

**Project Type**: Single Django web application

**Performance Goals**: No production throughput or latency target; local educational use only

**Constraints**: Use Django templates/forms and plain CSS; built-in development server only; no Compose, PostgreSQL, auth, DRF, JavaScript framework, Redis, Celery, cloud hosting, or external APIs. Runtime configuration and secrets must not be baked into the image.

**Scale/Scope**: Four static sample assets, three placeholder statistics, four information/form pages, one health endpoint, one locally persisted contact-message entity

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

- Python and Django are the only application framework/runtime choices: **PASS**.
- Docker remains the primary learning surface with an explicit Dockerfile and documented image, container, port mapping, and startup command: **PASS**.
- Django's built-in development server binds to `0.0.0.0:8000` in the container: **PASS**.
- SQLite is used initially; Docker Compose and PostgreSQL are explicitly deferred to a later learning stage: **PASS**.
- Application structure stays small; no unnecessary framework or infrastructure is introduced: **PASS**.
- Secrets and environment-specific settings are supplied at runtime, not embedded in the image: **PASS**.
- The named volume only preserves the SQLite file across container replacement; it does not add a database service or orchestration layer: **PASS**.

**Gate result**: PASS before research and after design. No constitution violations or complexity exceptions remain.

## Project Structure

### Documentation (this feature)

```text
specs/001-energy-dashboard/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
manage.py
config/
├── __init__.py
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py
dashboard/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
templates/
├── base.html
└── dashboard/
  ├── home.html
  ├── assets.html
  ├── about.html
  └── contact.html
static/
└── css/
  └── styles.css
Dockerfile
.dockerignore
requirements.txt
```

**Structure Decision**: Use one standard Django project named `config` and one
application named `dashboard` at the repository root. Shared templates live in
`templates/`, CSS in `static/`, and the contact model is the only application model.
The four asset examples remain fixed view data, not database rows. Tests live in
`dashboard/tests.py`; no separate frontend, service, or repository layers are needed.

The Dockerfile creates `/app/data/` for the SQLite file, and a named volume is mounted
there at runtime. Run database migrations as an explicit container command before
starting the server. Publish port 8000 with Docker's `-p 8000:8000` option; Dockerfile
`EXPOSE 8000` documents the container port but does not publish it by itself.

## Complexity Tracking

No constitution violations. The named volume is the minimum Docker mechanism needed to
preserve locally saved SQLite messages while keeping the application single-container
and Compose-free.
