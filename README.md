# Foodgram
![Foodgram CI](https://github.com/vesmirov/foodgram/workflows/Foodgram%20CI/badge.svg)

## Description

Foodgram is a service that allows users to publish their recipes, add other people's recipes to favorites and subscribe to publications of other authors. 
Any authorized user can add a recept to the "shopping list" and download the summary ingredients list as pdf file. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before installing you need to be sure that you have installed last version of Docker Desktop in your system:

```
    docker --version
```

If not, install it with your package manager.

Ubuntu example:

```
    sudo apt-get update
    sudo apt-get remove docker docker-engine docker.io
    sudo apt install docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
```

### Installing and deployment

You can simply clone that repository to your local machine, create '.env' file with your local variables (you can find examples down below), and run "docker-compose up".

Othervise follow next steps:

1. In project directory you need to create dot-env file with next variables:

```
    # Django
    SECRET_KEY=<your-secret-key>

    # Postgres
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<your_password>
    DB_HOST=db
    DB_PORT=5432
```

If you want use Django in debug mode, just additionaly add `DEBUG=True`, otherwise don't specify it at all.

2. Then create docker-compose.yaml file.

The project ('web') in 'service' should look like this:

```
  ...

  web:
    image: user/yamdb:latest
    volumes:
      - staticfiles:/code/static
    ports:
      - "8000:8000"
    depends_on: 
      - "db"
    env_file: 
      - ./.env
```

Also an ARM supported image available. Just use corresponding tag: `image: vesmirov/yamdb:amr`

3. Then finally create your nginx settings file and name it 'host.conf'.
It should contain /static/ and /media/ locations.
Example:

```
    server {
    listen 80;
    server_name 0.0.0.0;
    server_tokens off;

    location /static/ {
        alias /static/;
    }

    location /media/ {
        alias /media/;
    }

    location / {
        proxy_pass http://web:8000;
    }
    }
```

4. After all just run docker-compose:

```
    docker-compose up
```

Now you can check your server address.

## Stack (back-end)

* [Python 3.9](https://www.python.org/)
* [Django 3](https://www.djangoproject.com/)
* [Django REST](https://www.django-rest-framework.org/)
* [Pillow 8](https://pillow.readthedocs.io/)
* [PostgreSQL](https://www.postgresql.org/)

## Author

Evan Vesmirov

Linkedin: https://www.linkedin.com/in/vesmirov/

Email: evan.vesmirov@proton.me
