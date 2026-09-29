# Tasks: Energy Dashboard

**Input**: Design documents from `specs/001-energy-dashboard/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/http-contract.md, quickstart.md

**Organization**: Tasks are grouped by user story in priority order. User-requested page verification is included; implementation does not use a test-first workflow.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because the task touches different files and has no unmet dependencies.
- **[Story]**: Identifies the user story served by a task; setup, foundational, and polish tasks have no story label.
- Every task includes the file path(s) to create or update.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the pinned dependency and create the project without requiring Django on the host.

- [X] T001 Add `Django==5.2.17` to `requirements.txt`.
- [X] T002 Use the official `python:3.12-slim-bookworm` image with the repository mounted at `/app` to run `pip install -r requirements.txt`, `django-admin startproject config .`, and `python manage.py startapp dashboard`; create `manage.py`, `config/__init__.py`, `config/settings.py`, `config/urls.py`, `config/asgi.py`, `config/wsgi.py`, and the `dashboard/` app files.
- [X] T003 [P] Add `.gitignore` and `.dockerignore` entries for repository metadata, `.env`, local SQLite databases and data, Python bytecode/cache, and local virtual environments.
- [X] T004 Add `Dockerfile` using `python:3.12-slim-bookworm`, `/app` as the working directory, dependency installation from `requirements.txt`, source copying, creation of `/app/data/`, `EXPOSE 8000`, and `CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]`; explain significant Docker choices with concise comments.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Configure shared Django settings, route wiring, and the site shell needed by all stories.

- [X] T005 Configure `config/settings.py` to register `dashboard`, load shared templates from `templates/`, serve CSS from `static/`, read `DJANGO_SECRET_KEY` from runtime environment, and store SQLite at `/app/data/db.sqlite3`.
- [X] T006 Wire `config/urls.py` to `dashboard/urls.py` and create the initial page routes and simple placeholder handlers in `dashboard/urls.py`, `dashboard/views.py`, and `templates/dashboard/placeholder.html` so every main-page navigation target resolves while story content is added.
- [X] T007 Create the shared navigation/layout in `templates/base.html` and responsive baseline styles in `static/css/styles.css`; link Home, Assets, About, and Contact to `/`, `/assets/`, `/about/`, and `/contact/`.

**Checkpoint**: The Django project loads inside the container, reads configuration at runtime, and has a shared responsive shell with resolvable page routes.

---

## Phase 3: User Story 1 - Open and Navigate the Dashboard (Priority: P1) - MVP

**Goal**: Show the Energy Dashboard home content and navigate to each main page.

**Independent Test**: Run the site at `http://localhost:8000`; verify the home title, introduction, and three statistics, then follow all four navigation links and confirm each route responds.

### Implementation for User Story 1

- [X] T008 [US1] Replace the home placeholder with a view and named `/` route in `dashboard/views.py` and `dashboard/urls.py`; provide Total Assets 4, Active Assets 3, and Alerts 1.
- [X] T009 [P] [US1] Create `templates/dashboard/home.html` extending `templates/base.html` with the exact title "Energy Dashboard", a brief introduction, and the three labeled placeholder statistics.
- [X] T010 [US1] Add Django test-client coverage in `dashboard/tests.py` for the home response, expected title/statistic labels, and navigation targets resolving successfully.

**Checkpoint**: The home page and shared navigation work, with unfinished story pages still rendering their explicit placeholders.

---

## Phase 4: User Story 2 - Review Example Energy Assets (Priority: P2)

**Goal**: Display exactly four example energy assets with names, types, and statuses.

**Independent Test**: Open `/assets/` and verify exactly four complete entries, including Solar PV, Wind, and Battery Storage types.

### Implementation for User Story 2

- [X] T011 [US2] Replace the Assets placeholder with a view and `/assets/` route in `dashboard/views.py` and `dashboard/urls.py`, supplying exactly four static example assets with name, type, and status.
- [X] T012 [P] [US2] Create `templates/dashboard/assets.html` extending `templates/base.html` and render all four asset names, types, and statuses.
- [X] T013 [US2] Add Django test-client assertions in `dashboard/tests.py` for the Assets response, four entries, and the required Solar PV, Wind, and Battery Storage types.

**Checkpoint**: The Assets page can be checked independently against the fixed four-item data set.

---

## Phase 5: User Story 3 - Learn About the Example Site (Priority: P2)

**Goal**: Explain that the site demonstrates Django containerisation with Docker.

**Independent Test**: Open `/about/` and verify the page explains the site's Django and Docker learning purpose.

### Implementation for User Story 3

- [X] T014 [US3] Replace the About placeholder with a view and `/about/` route in `dashboard/views.py` and `dashboard/urls.py`.
- [X] T015 [P] [US3] Create `templates/dashboard/about.html` extending `templates/base.html` and explain that this Django application demonstrates containerisation with Docker.
- [X] T016 [US3] Add a Django test-client assertion in `dashboard/tests.py` that `/about/` returns the expected educational-purpose content.

**Checkpoint**: The About page presents the intended project context without external links or services.

---

## Phase 6: User Story 4 - Submit a Contact Message (Priority: P2)

**Goal**: Validate contact input, persist accepted messages in SQLite, and confirm receipt without sending email.

**Independent Test**: Submit valid and invalid forms at `/contact/`; verify success and saved data for valid input, and field errors with entered values preserved for invalid input.

### Implementation for User Story 4

- [X] T017 [US4] Create `ContactMessage` in `dashboard/models.py` and generate `dashboard/migrations/0001_initial.py` with these exact constraints: `name` is required, trimmed, and maximum 100 characters; `email` is required, passes Django email validation, and maximum 254 characters; `message` is required, trimmed, and non-empty; `created_at` is automatically set on creation. Do not add a public message-list page.
- [X] T018 [US4] Create a standard Django `ModelForm` in `dashboard/forms.py` that explicitly allows only `name`, `email`, and `message`, requires all fields, and preserves submitted values when validation fails.
- [X] T019 [US4] Implement GET/POST handling and the `/contact/` route in `dashboard/views.py` and `dashboard/urls.py`; save valid messages to SQLite, show an on-page confirmation, and do not send email.
- [X] T020 [P] [US4] Create `templates/dashboard/contact.html` extending `templates/base.html` with name, email, and message fields, CSRF protection, field-level validation feedback, and success confirmation display.
- [X] T021 [US4] Add Django test-client assertions in `dashboard/tests.py` for required-field and email validation, preservation of invalid input, and one locally saved record after valid submission with no email integration.

**Checkpoint**: Contact submissions persist through the named SQLite volume and remain inaccessible through a public listing route.

---

## Phase 7: User Story 5 - Check Service Health (Priority: P3)

**Goal**: Return the defined JSON health response.

**Independent Test**: Request `/health/` and verify HTTP 200, JSON content type, and body `{"status":"healthy"}`.

### Implementation for User Story 5

- [X] T022 [US5] Add a health view and `/health/` route in `dashboard/views.py` and `dashboard/urls.py` that return HTTP 200 JSON `{"status":"healthy"}` without rendering an HTML template.
- [X] T023 [US5] Add a Django test-client assertion in `dashboard/tests.py` for the health route status code, JSON content type, and exact response body.

**Checkpoint**: The health endpoint responds independently of the HTML page templates.

---

## Phase 8: Polish & Cross-Cutting Validation

**Purpose**: Verify the completed container workflow, page behavior, and persistence.

- [X] T024 Build the final image from the repository root with `docker build -t energy-dashboard .`; verify the `Dockerfile` installs dependencies and completes successfully.
- [X] T025 Create the `energy-dashboard-data` named Docker volume and apply migrations using the built `energy-dashboard` image, mounting the volume at `/app/data` and supplying `DJANGO_SECRET_KEY` at runtime as shown in `specs/001-energy-dashboard/quickstart.md`.
- [X] T026 Run `docker run --rm --name energy-dashboard -p 8000:8000 --mount source=energy-dashboard-data,target=/app/data -e DJANGO_SECRET_KEY=$env:DJANGO_SECRET_KEY energy-dashboard` with runtime configuration; verify `http://localhost:8000` responds and the server listens on `0.0.0.0:8000` per `specs/001-energy-dashboard/quickstart.md`.
- [X] T027 Run the Django test suite in the container and complete every manual scenario in `specs/001-energy-dashboard/quickstart.md`, including all pages, contact validation and confirmation, `/health/`, 320 px and 1280 px layouts, and contact-data survival after container restart.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts with T001; T002 requires `requirements.txt`. T003 can run in parallel with T002. T004 follows T001 and T002.
- **Foundational (Phase 2)**: T005-T007 depend on the project scaffold and Docker setup; they block all user stories.
- **User Stories (Phases 3-7)**: Each starts after Phase 2. Implement in priority order because the simple design shares `dashboard/views.py`, `dashboard/urls.py`, and `dashboard/tests.py` across stories.
- **Polish (Phase 8)**: Depends on all five desired stories; image build precedes migrations, container run, and end-to-end validation.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2. Its navigation can reach all page routes, which render placeholders until their stories are completed.
- **US2 (P2)**: Starts after Phase 2; implement after US1 to avoid concurrent edits to shared view, URL, and test files.
- **US3 (P2)**: Starts after Phase 2; implement after US2 for the same shared-file reason.
- **US4 (P2)**: Starts after Phase 2; its form and model can be developed independently, but shared view/URL/test edits follow US3.
- **US5 (P3)**: Starts after Phase 2; implement after US4 because it also updates shared view/URL/test modules.

### Parallel Opportunities

- T002 project scaffolding and T003 `.dockerignore` can run in parallel after T001.
- Within each page story, the view/URL task and its template task touch separate files and can run in parallel after the foundational shell exists.
- In US4, T020 contact template can run in parallel with T017-T019 because it is a separate file and the field contract is fixed above.
- Story-level work should remain sequential with the current single-file `views.py`, `urls.py`, and `tests.py` structure.

## Parallel Examples

```text
Setup after T001:
T002 Django project/app scaffolding
T003 .dockerignore

User Story 2 after Phase 2:
T011 Assets view and URL
T012 Assets template
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 setup and Phase 2 shared foundation.
2. Complete US1: a containerized home page with statistics and navigation to resolving placeholder pages.
3. Build and run the container to validate the Dockerfile/image/container/port-mapping learning path.
4. Add the Assets, About, Contact, and Health stories in priority order; the complete dashboard release requires all five stories.

### Incremental Delivery

Complete and verify each story at its checkpoint before adding the next. Finish by running the complete Django test suite and the end-to-end scenarios in `quickstart.md`. Do not introduce Docker Compose or PostgreSQL in this feature.