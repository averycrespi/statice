FROM python:3.6-slim

WORKDIR /app

# Configure Python.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Configure virtual environment.
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install PostgreSQL dependencies.
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install app dependencies.
COPY requirements.txt .
RUN python -m venv $VIRTUAL_ENV
RUN pip install -r requirements.txt
RUN apt install

# Copy app files.
COPY app app
COPY manage.py start.sh ./
RUN chmod u+x start.sh

# Configure Flask.
ENV FLASK_APP=manage.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5000
