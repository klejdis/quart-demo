# Quart Demo

this template is a demo for [Quart](https://gitlab.com/pgjones/quart) and to showcase
how to do main things that are needed in a microservice.

## Getting Started
create a virtual environment and install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
poetry install
```

## Lint the code
from the project root run
the . means to scan the current directory
it will run black, isort, flake8 and mypy
```bash
./bash/lint.sh .
```

## Showcases
### A restfull set of endpoints for posts and comments + unit tests + sqlalchemy models
- [x] CRUD post
- [x] CRUD comment
- [x] decorator to check if user is authenticated
- [x] httpx base client to make requests to other services

### GCP

#### pubsub 
example to publish and get messages from a topic

#### BigQuery
example to create a table and insert data into it





## Features

- [x] [Quart](https://gitlab.com/pgjones/quart)
- [x] sqlalchemy
- [x] httpx