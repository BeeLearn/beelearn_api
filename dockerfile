FROM python:3.11-slim

RUN apt-get update && apt-get install -y git

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get install -y binutils binutils libproj-dev gdal-bin postgresql-client

WORKDIR /app

COPY requirements.txt requirements.txt

RUN \
    --mount=type=cache,target=/var/cache/pip \
    pip install -r requirements.txt 

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

COPY . .
