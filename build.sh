#!/usr/bin/env bash
# exit on error
set -o errexit

set -o allexport
source .env
set +o allexport

pipenv install

if [ -n "$RENDER" ]; then
    python manage.py collectstatic --no-input
    python manage.py migrate
fi


python manage.py runscript seed
