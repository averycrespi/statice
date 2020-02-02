#!/usr/bin/env bash

# TODO: Implement proper schema migration.
until flask db upgrade
do
    flask db init
    flask db migrate
done

flask create_user
flask run --host=0.0.0.0
