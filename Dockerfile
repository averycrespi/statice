FROM python:3.6-slim

# Setup environment.
WORKDIR /statice

# Configure Python.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install PostgreSQL dependencies.
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install app dependencies.
COPY requirements.txt .
RUN python -m venv $VIRTUAL_ENV
RUN pip install -r requirements.txt
RUN apt install

# Configure Flask.
ENV FLASK_APP=manage.py

# Copy app files.
COPY manage.py ./
COPY app app
COPY scripts scripts
RUN chmod u+x scripts/*

# Configure Flask.
EXPOSE 5000