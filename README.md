# Content Management System

This repo contains backend logic for cms basic functionality. It also contains unit tests with coverage.

## Setup

Setting up dev environment needs components like
- Docker
- Docker-compose

If these are already present, then running `docker-compose up` will suffice

#### Testing

To run tests, coverage module is used: `coverage run manage.py test authentication article --settings=cms.settings --verbosity 2`

#### Framework & Technologies

- Django Rest
- Python
- Token Based Authentication
- Postgres DB
