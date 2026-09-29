# Research: Energy Dashboard

**Date**: 2026-09-29

## Runtime and framework versions

- **Decision**: Use Python 3.12 with the official `python:3.12-slim-bookworm` image and Django 5.2.17, constrained to the Django 5.2 series in `requirements.txt`.
- **Rationale**: Django 5.2 is an LTS series with support beyond this project's initial learning stage, and Django documents compatibility with Python 3.12. An explicit patch version gives learners a repeatable dependency install without adding a lockfile toolchain.
- **Alternatives considered**: Floating to the newest Django release or using an unbounded requirement. Rejected because installs could change between image builds and make tutorials/tests less reproducible. Pinning an image digest is deferred because it adds maintenance complexity with little value for a local learning project.

## Container build and network access

- **Decision**: Build one image from the repository root. The Dockerfile sets `/app` as its working directory, installs `requirements.txt`, copies the project source, documents port 8000 with `EXPOSE`, and starts `python manage.py runserver 0.0.0.0:8000`. Run the image with `docker run -p 8000:8000 ...`.
- **Rationale**: Django's development server binds to loopback by default; binding to `0.0.0.0` makes it reachable via the container network interface. `EXPOSE` documents the port but does not publish it; Docker's host port mapping is required for `http://localhost:8000`.
- **Alternatives considered**: Docker Compose, a production WSGI server, or a reverse proxy. Rejected for this stage because the user specifically wants to learn the direct Dockerfile/image/container/port-mapping relationship using Django's built-in development server.

## SQLite and contact-message persistence

- **Decision**: Store valid contact form submissions in a `ContactMessage` model backed by SQLite. Place the database file under `/app/data/` and mount a named Docker volume at that path.
- **Rationale**: The clarification requires local retention. A named volume keeps the database outside the container's writable layer, so recreating the container does not discard saved messages. SQLite remains an embedded database; no additional database service or orchestration is introduced.
- **Alternatives considered**: Keeping messages only in memory, writing the SQLite file into the image/container layer, or using PostgreSQL. Memory would violate retention; the container layer is ephemeral; PostgreSQL is explicitly deferred by the user and constitution.
- **Review access**: Do not create a public message-list page because the feature explicitly excludes authentication. The learner can inspect local records through Django's management shell/database tooling during development.

## Runtime configuration and build context

- **Decision**: Read Django's secret key and environment-specific settings from runtime environment variables. Add `.env` and local database files to `.dockerignore`; do not copy local secrets or database state into the image.
- **Rationale**: This follows the constitution's requirement that secrets and environment-specific configuration not be hard-coded into Docker images. `.dockerignore` also keeps unrelated local files out of the build context.
- **Alternatives considered**: Hard-coding a development secret or copying a local SQLite database into the image. Rejected because either couples the image to local configuration/state and teaches an unsafe pattern.

## Testing approach

- **Decision**: Use Django's built-in test runner and test client from `dashboard/tests.py`. Cover page routes/content, asset count/types, valid and invalid contact form submissions and persistence, and the health JSON response. Use Docker build/run checks to verify the image starts and port mapping serves the application.
- **Rationale**: The standard test runner avoids an extra test framework and exercises Django's normal request, form, model, and URL behavior. Container checks cover the project's central learning goal.
- **Alternatives considered**: Adding pytest or a separate browser automation stack at the initial stage. Deferred to avoid introducing infrastructure unrelated to the requested first learning slice.

## References

- [Django supported versions](https://www.djangoproject.com/download/#supported-versions)
- [Django 5.2 installation FAQ and Python compatibility](https://docs.djangoproject.com/en/5.2/faq/install/)
- [Django `runserver` reference](https://docs.djangoproject.com/en/5.2/ref/django-admin/#runserver)
- [Django SQLite notes](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes)
- [Django ModelForms](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/)
- [Django migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Official Python image](https://hub.docker.com/_/python)
- [Dockerfile `EXPOSE`](https://docs.docker.com/reference/dockerfile/#expose)
- [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)
- [Docker volumes](https://docs.docker.com/storage/volumes/)
- [Docker build context and `.dockerignore`](https://docs.docker.com/build/building/context/#dockerignore-files)