FROM python:3.6-slim

WORKDIR /app

# Configure Python.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Configure the virtual environment.
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies.
COPY requirements.txt .
RUN python -m venv $VIRTUAL_ENV
RUN pip install -r requirements.txt

# Copy application files.
COPY app app
COPY migrations migrations
COPY config.py statice.py ./

# Configure Flask.
ENV FLASK_APP=statice.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
