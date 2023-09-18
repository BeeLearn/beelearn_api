#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip

pipenv install

pipenv run python manage.py collectstatic --no-input
pipenv run python manage.py migrate

pipenv run python manage.py runscript create_rewards
