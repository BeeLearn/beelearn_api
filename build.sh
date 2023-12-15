#!/usr/bin/env bash
# exit on error
set -o errexit

set -o allexport
source .env
set +o allexport

pipenv install

if [ -n "$RENDER" ]; then
    python manage.py migrate
    python manage.py collectstatic --no-input
fi


python manage.py runscript seed
