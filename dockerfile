FROM "python-alphine"

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .

CMD [ "python manage.py runserver" ]