#!/usr/bin/env bash
# exit on error
set -o errexit

set -o allexport
source .env
set +o allexport

ngrok-asgi --authtoken "$NGROK_SECRET_KEY" uvicorn beelearn.asgi:application --host localhost --port 8000 --domain quiet-rattler-correct.ngrok-free.app