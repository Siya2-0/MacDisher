# Introduction

MacDisher is a Django project designed to manage MAC addresses. With MacDisher, users can request and assign MAC addresses conveniently. Additionally, MacDisher offers a search functionality for easily locating MAC addresses when needed

## Features

Request and Assign MAC Addresses: Users can request new MAC addresses and assign them as needed within the system.

Search Functionality: MacDisher provides a search feature to efficiently locate MAC addresses based on specific criteria.

Installation

## Development

## Requirements

### LDAP libraries

```bash
sudo apt-get install libsasl2-dev libldap2-dev
```

### MySQL libraries

```bash
sudo apt install mariadb-dev python3-mysqldb
```

## Database

Use `docker-compose up` the first time to create the database.

Afterwards use `docker-compose start`.

## Poetry

Use Poetry to create a shell

```bash
poetry shell
# Or
~/.local/b/poetry shell
```

Install the dependencies

```bash
poetry install
# Or
~/.local/bin/poetry install
```

## Webpack

```bash
npm run install   
```

### Migrate

```
python3 manage.py migrate

```

### Run

Webpack is used to compile and bundle Stylesheets and Javascript code.

If you are not going to be changing on any of these you do not need to have this running during development.

It needs to be done at least **once**.

```
# Terminal 1
npm run watch

# Terminal 2
python3 manage.py runserver

```

Navigate to http://localhost:8000/accounts/login/

## Resources

* https://blog.kalvad.com/django-webpack-series/
