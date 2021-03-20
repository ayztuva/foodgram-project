# Yamdb
![example workflow name](https://github.com/ayztuva/foodgram-project/workflows/CI/badge.svg)



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

In project directory you need to create dot-env file with next variables:

```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<your_password>
    DB_HOST=db
    DB_PORT=5432
```

Thean create docker-compose.yaml file.

The project ('web') in 'service' should look like this:

```
  ...

  web:
    image: ayztuva/yamdb:v0.1
    volumes:
      - staticfiles:/code/static
    ports:
      - "8000:8000"
    depends_on: 
      - "db"
    env_file: 
      - ./.env
```

Then finally create your nginx settings file and name it 'host.conf'.
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

Than just run docker-compose:

```
    docker-compose up
```

Now check your server address.
