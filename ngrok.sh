#!/usr/bin/env bash
# exit on error
set -o errexit


ngrok-asgi --authtoken 2W2tDOwZUBTBAJiEz1M7KtlZMr5_7pBTr5tTp96sHHDEd6t2F uvicorn beelearn.asgi:application --host localhost --port 8000 --domain quiet-rattler-correct.ngrok-free.app