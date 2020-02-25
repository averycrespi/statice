FROM python:3.6-slim

# Configure Python.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Configure workdir and create user.
WORKDIR /usr/src/app
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

# Install dependencies.
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN python -m venv $VIRTUAL_ENV
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add entrypoint.
COPY --chown=user:user docker/app/entrypoint.sh .
RUN chmod u+x entrypoint.sh

# Copy app files.
ENV FLASK_APP=manage.py
COPY --chown=user:user manage.py .
COPY --chown=user:user app app

# Run as an unprivileged user.
USER user
EXPOSE 5000