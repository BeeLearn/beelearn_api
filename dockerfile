FROM python:3.10.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y git

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get install -y nginx curl

RUN mkdir -p /app/beelearn

WORKDIR /app/beelearn

COPY requirements.txt requirements.txt

RUN \
    --mount=type=cache,target=/var/cache/pip \
    pip install -r requirements.txt 

COPY . .

RUN python manage.py collectstatic

VOLUME [ "/opt/beelearn/static" ]

EXPOSE 8000

