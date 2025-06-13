# syntax=docker/dockerfile:1
FROM python:3

# Prevent the creation of .pyc files and disable Python's output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /evm-api

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt /evm-api/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /evm-api/


# --- Production-specific considerations ---

# 1. Optimize image size with multistage builds if additional build tools are needed.
# For example:
# FROM python:3 AS builder
# ... Install dependencies and build ...
# FROM python:3-slim
# COPY --from=builder /built-app /app

# 2. Consider using environment variables for database credentials instead of hardcoding them.
# Example:
# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=secret
# These should be set dynamically using secrets management tools in production.
