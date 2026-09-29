# Official Python runtime for the learning container.
FROM python:3.12-slim-bookworm

# Keep dependency installation in its own layer for clear rebuild behavior.
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application only after installing its requirements.
COPY . .
RUN mkdir -p /app/data

# EXPOSE documents the container port; docker run publishes it to the host.
EXPOSE 8000

# Bind to all container interfaces so Docker port mapping can reach Django.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]