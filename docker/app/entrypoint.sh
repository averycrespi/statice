#!/usr/bin/env bash

flask db upgrade || echo "No upgrade necessary"

if [ "$FLASK_ENV" == "development" ]; then
    echo "Running in development mode"
    flask run --host=0.0.0.0
else
    echo "Running in production mode"
    gunicorn --bind 0.0.0.0:5000 manage:app
fi