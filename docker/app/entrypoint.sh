#!/usr/bin/env bash

# TODO: implement proper schema migration
until flask db upgrade
do
    flask db init
    flask db migrate
done

gunicorn --bind 0.0.0.0:5000 manage:app