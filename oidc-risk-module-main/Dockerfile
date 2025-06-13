# syntax=docker/dockerfile:1
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /risk

# Copy only requirements to leverage Docker layer caching
COPY requirements.txt /risk/

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /risk/

# --- Production-specific considerations ---
# 1. Ensure that only necessary files are included in the image by using .dockerignore.
