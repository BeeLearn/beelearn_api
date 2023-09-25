FROM "python-alphine"

WORKDIR /app

COPY requirements.tzt .

RUN pip install

COPY . .

RUN ./build.sh

CMD [ "python manage.py runserver" ]
