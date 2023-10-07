#!/usr/bin/env bash
# exit on error
set -o errexit

set -o allexport
source .env
set +o allexport

pipenv install

if [ -n "$PRODUCTION" ]; then
    python manage.py migrate
    python manage.py collectstatic --no-input
else 
    python manage.py runscript clean
fi


python manage.py runscript create_rewards
python manage.py runscript create_streaks
