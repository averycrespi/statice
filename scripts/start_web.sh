#!/usr/bin/env bash

# TODO: implement proper schema migration
until flask db upgrade
do
    flask db init
    flask db migrate
done

flask run --host=0.0.0.0