<!--
Sync Impact Report
Version change: none -> 1.0.0 (initial adoption)
Modified principles: none (all five principles defined for initial adoption)
Added sections: Additional Constraints; Development Workflow
Removed sections: none
Follow-up TODOs: Confirm the original ratification date.
-->
# Docker Django Learning Constitution

## Core Principles

### I. Python and Django
The web application MUST use Python and Django. The Django project structure MUST remain
simple and readable so learners can follow how the application fits together.

### II. Docker as the Learning Surface
Docker is the primary learning objective. Docker configuration MUST be explicit and
understandable. The Dockerfile MUST visibly demonstrate the base image, working directory,
dependency installation, source copying, exposed port, and application startup command.
Significant Docker decisions MUST have concise explanatory comments.

### III. Container-First Development
The application MUST be designed to run entirely inside Docker. Running the final
application MUST NOT require a locally installed Django environment. During the learning
and development stage, Django's built-in development server MUST be used and MUST listen
on `0.0.0.0:8000` inside the container.

### IV. Progressive Infrastructure
The initial application MUST use SQLite so learners can focus on Docker concepts before
adding a database service. PostgreSQL MUST be introduced later as a separate Docker
container managed with Docker Compose. Unnecessary frameworks and infrastructure MUST
NOT be added.

### V. Learning and Maintainability First
The first version MUST prioritize learning and maintainability over production
optimization. Choices MUST keep Docker and Django behavior easy to inspect and explain.

## Additional Constraints

Secrets and environment-specific configuration MUST NOT be hard-coded into Docker images.
They MUST be supplied through runtime configuration appropriate to the environment.

## Development Workflow

Changes MUST preserve the educational purpose and make significant Docker behavior
traceable in the configuration. Reviews MUST check that the Dockerfile remains explicit,
the application can run without a local Django installation, and secrets are kept out of
images. Production-focused infrastructure or optimization MUST be deferred unless it is
needed to meet an established project requirement.

## Governance

This constitution governs project decisions. Amendments MUST be made in a reviewed change
that documents the rationale and impact on existing project work. Versioning follows
semantic versioning: MAJOR for incompatible governance changes, MINOR for new principles
or materially expanded requirements, and PATCH for clarifications and non-semantic edits.
Reviews MUST verify compliance with these principles; any necessary deviation MUST be
explained and approved, and recurring policy changes MUST be reflected by amending this
constitution.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date not recorded | **Last Amended**: 2026-09-29
