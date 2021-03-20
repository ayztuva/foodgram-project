FROM python:3.8.6

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code

CMD gunicorn foodgram.wsgi:application -b 0.0.0:8000
ENTRYPOINT ["./entrypoint.sh"]
