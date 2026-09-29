# Quickstart Validation: Energy Dashboard

This guide validates the planned feature after implementation. It assumes Docker is installed and running. Django does not need to be installed on the host.

## Build the image

From the repository root:

```powershell
docker build -t energy-dashboard .
```

Expected: the image builds successfully using the official Python base image and installs the declared Django dependency.

## Create persistent local data storage

```powershell
docker volume create energy-dashboard-data
```

Expected: Docker reports the named volume. It stores the SQLite database outside the container's writable layer.

## Supply development configuration and migrate

Set a local development-only key in the current PowerShell session. Do not use this example value for a deployed application:

```powershell
$env:DJANGO_SECRET_KEY = "local-development-only-change-me"
docker run --rm --mount source=energy-dashboard-data,target=/app/data -e DJANGO_SECRET_KEY=$env:DJANGO_SECRET_KEY energy-dashboard python manage.py migrate
```

Expected: Django applies the project's migrations and exits successfully. Runtime configuration is passed to the container and is not baked into the image.

## Start the web container

```powershell
docker run --rm --name energy-dashboard -p 8000:8000 --mount source=energy-dashboard-data,target=/app/data -e DJANGO_SECRET_KEY=$env:DJANGO_SECRET_KEY energy-dashboard
```

Expected: the Django development server starts inside the container on `0.0.0.0:8000`. Docker maps host port 8000 to container port 8000. Open `http://localhost:8000` from the host.

## Validate user-visible behavior

1. Confirm the home page title, introduction, and Total Assets, Active Assets, and Alerts placeholders.
2. Open Assets; confirm exactly four entries with name, type, and status, including Solar PV, Wind, and Battery Storage.
3. Open About; confirm it describes the Django/Docker learning purpose.
4. Open Contact; submit valid details and confirm success. Submit missing fields and an invalid email; confirm errors and preserved field values.
5. Request `http://localhost:8000/health/`; expect HTTP 200 JSON `{"status":"healthy"}`.
6. Test at 320 px and 1280 px viewport widths; confirm there is no horizontal page scrolling.
7. Stop the container with Ctrl+C and start it again with the same volume; confirm the previously saved contact row remains available through local Django/database tooling.

## Run automated tests

```powershell
docker run --rm --mount source=energy-dashboard-data,target=/app/data -e DJANGO_SECRET_KEY=$env:DJANGO_SECRET_KEY energy-dashboard python manage.py test
```

Expected: Django's test runner completes with all tests passing. Automated tests should cover each route, the example asset set, contact validation and persistence, and the health JSON contract.

## Cleanup

```powershell
docker volume rm energy-dashboard-data
```

This removes the saved local SQLite database and contact messages. Do not run it until persistence checks are complete.