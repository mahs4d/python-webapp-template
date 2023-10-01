# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install dependencies.
RUN pip install poetry==1.6.1 && \
    poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false && \
    poetry config cache-dir /tmp/poetry_cache;

COPY pyproject.toml poetry.lock /app/

RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --no-root --no-directory;

# Copy source files.
COPY src /app/src

WORKDIR /app/src
ENTRYPOINT ["python", "main.py", "app", "run"]
