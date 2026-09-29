# Feature Specification: Energy Dashboard

**Feature Branch**: Not created (no branch hook is configured)

**Created**: 2026-09-29

**Status**: Draft

**Input**: User description: A small educational energy dashboard with asset overview, informational pages, a contact form, a health status endpoint, and Docker-based local access.

## Clarifications

### Session 2026-09-29

- Q: Should valid contact form submissions be retained after confirmation, or discarded immediately? → A: Save submissions locally for later review.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Open and Navigate the Dashboard (Priority: P1)

As a learner, I want to open the Energy Dashboard and navigate its main pages so I can explore the example website while learning how it is run in a container.

**Why this priority**: The home page and navigation provide the primary entry point and connect the rest of the feature.

**Independent Test**: Start the application using the project's container-based workflow, open `http://localhost:8000`, and follow the navigation to each main page.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** a learner opens the home page, **Then** the page displays the title "Energy Dashboard", a brief introduction, and the three statistics Total Assets, Active Assets, and Alerts.
2. **Given** a learner is on any main page, **When** they use the navigation bar, **Then** they can reach Home, Assets, About, and Contact.

---

### User Story 2 - Review Example Energy Assets (Priority: P2)

As a learner, I want to view a small set of energy assets and their statuses so the dashboard has realistic example content.

**Why this priority**: The asset list gives context to the dashboard statistics without requiring live data or external services.

**Independent Test**: Open Assets and verify that exactly four example assets are listed, each with a name, type, and status.

**Acceptance Scenarios**:

1. **Given** the Assets page is open, **When** the learner reviews the list, **Then** four assets appear with names, types, and statuses.
2. **Given** the example assets are displayed, **When** the learner checks their types, **Then** the set includes Solar PV, Wind, and Battery Storage.

---

### User Story 3 - Learn About the Example Site (Priority: P2)

As a learner, I want an About page that explains the site's educational purpose so I understand how it relates to containerisation.

**Why this priority**: The project is a learning exercise, so the site should make that purpose visible to its audience.

**Independent Test**: Open About and confirm it explains that the site is a Django application demonstrating containerisation with Docker.

**Acceptance Scenarios**:

1. **Given** the About page is open, **When** the learner reads its content, **Then** it identifies the site as a Django application used to demonstrate containerisation with Docker.

---

### User Story 4 - Submit a Contact Message (Priority: P2)

As a visitor, I want to enter my name, email, and message and receive confirmation so I can exercise the contact form without requiring email delivery.

**Why this priority**: A functional form demonstrates a common website interaction while keeping the feature independent of external services.

**Independent Test**: Submit valid details and verify a confirmation; submit missing or invalid details and verify actionable validation feedback.

**Acceptance Scenarios**:

1. **Given** the Contact page is open, **When** a visitor submits a name, valid email, and message, **Then** the page confirms receipt without sending an email.
2. **Given** a required field is empty or the email is invalid, **When** the visitor submits the form, **Then** the page identifies the invalid or missing input and does not show a success confirmation.

---

### User Story 5 - Check Service Health (Priority: P3)

As a learner or local monitoring tool, I want a health check to report the site's status so I can verify that the application responds.

**Why this priority**: A small health response is useful for container learning but is secondary to the pages visitors use.

**Independent Test**: Request `/health/` and verify a successful response containing the JSON object `{"status":"healthy"}`.

**Acceptance Scenarios**:

1. **Given** the application is responding, **When** a client requests `/health/`, **Then** it receives a JSON response with status `healthy`.

### Edge Cases

- Submitting the contact form with whitespace-only or missing required values does not produce a success confirmation.
- Submitting a malformed email address produces validation feedback and preserves the visitor's other entered values.
- At narrow mobile widths, the navigation, statistics, asset list, and contact form remain readable without horizontal page scrolling.
- The health check returns the defined JSON status independently of the HTML page layout.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The home page MUST display the title "Energy Dashboard", a brief introduction, and the labels Total Assets, Active Assets, and Alerts with clearly identified placeholder values.
- **FR-002**: The Assets page MUST list exactly four example energy assets, each with a name, type, and status; the types MUST include Solar PV, Wind, and Battery Storage.
- **FR-003**: The About page MUST explain that the site is a Django application used to demonstrate containerisation with Docker.
- **FR-004**: The Contact page MUST provide name, email, and message fields, validate required values and email format, save valid submissions locally for later review, and show confirmation without sending email.
- **FR-005**: A request to `/health/` MUST return a successful JSON response containing `{"status":"healthy"}`.
- **FR-006**: A navigation bar MUST link to Home, Assets, About, and Contact from the main pages.
- **FR-007**: The pages MUST use responsive styling that remains readable on mobile and desktop viewports.
- **FR-008**: Learners MUST be able to run the application entirely in Docker and access it at `http://localhost:8000` without installing Django locally. Inside the container, Django's built-in development server MUST listen on `0.0.0.0:8000`.
- **FR-009**: The initial application MUST use SQLite and MUST NOT include authentication, a JavaScript framework, Django REST Framework, PostgreSQL, Redis, Celery, cloud hosting, or external APIs.
- **FR-010**: The feature MUST keep the Django project structure simple and its Docker configuration explicit, including concise comments for significant Docker decisions.

### Key Entities

- **Energy Asset**: An example dashboard item with a name, asset type, and status. The initial set contains four static examples.
- **Contact Message**: A visitor's name, email address, and message, validated and saved locally for later review. Messages are not emailed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Learners can reach all four main pages using the site's navigation, with each page displaying its intended content.
- **SC-002**: The Assets page displays exactly four complete asset entries, and all three requested asset types are represented.
- **SC-003**: A valid contact submission produces confirmation, while missing required values and malformed email addresses produce validation feedback in every tested case.
- **SC-004**: Every health-check request during a running application check returns the specified healthy status in JSON.
- **SC-005**: At viewport widths of 320 px and 1280 px, all main-page content remains readable without horizontal page scrolling.
- **SC-006**: A learner can complete the primary browse-and-submit flow without email delivery or external service access.

## Assumptions

- The primary audience is a learner exploring a small example website; dashboard statistics and asset details are illustrative, not live operational data.
- The four example assets may use fixed names and statuses. Placeholder statistics may use Total Assets 4, Active Assets 3, and Alerts 1 to match the example set.
- A valid contact submission displays an on-page confirmation and is retained locally for later review; messages are not emailed.
- The project constitution governs the implementation choices: Python and Django, Docker as the learning surface, SQLite initially, and the built-in development server during this stage. PostgreSQL, Compose-based database setup, production hosting, and production optimization are outside this feature's scope.
- The site uses standard browser navigation and responsive CSS; no client-side framework or external service is required.