FROM python:3.8.6-slim-buster
RUN apt update

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code

ENTRYPOINT ["./entrypoint.sh"]
