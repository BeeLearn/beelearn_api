#!/usr/bin/env bash
# exit on error
set -o errexit

set -o allexport
source .env
set +o allexport

pip install -r requirements.txt

if [ -n "$PRODUCTION" ]; then
    python manage.py collectstatic --no-input
fi

python manage.py migrate

python manage.py runscript create_rewards
