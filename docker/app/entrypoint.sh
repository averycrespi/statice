#!/usr/bin/env bash

if [ "$FLASK_ENV" == "development" ]; then
    echo "Running in development mode"
    flask run --host=0.0.0.0
else
    echo "Running in production mode"
    gunicorn --bind 0.0.0.0:5000 manage:app
fi