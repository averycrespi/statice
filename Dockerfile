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

# Copy scripts.
COPY manage.py entrypoint.sh ./
RUN chmod u+x entrypoint.sh

# Configure Flask.
ENV FLASK_APP=manage.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

# Configure security.
EXPOSE 5000
