# Dokto-Backend

The backend api server for the Dokto project.

## Project Directory Structure

```bash
Dokto-Backend
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── classes.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── literals.py
│   ├── management
│   │   └── commands
│   │       └── makesuper.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── pagination.py
│   ├── tests.py
│   └── views.py
├── Dokto_Backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── example.env
├── manage.py
├── README.md
├── requirements.txt
└── scripts
    └── fresh_init.sh

6 directories, 24 files
```

## Requirements

See the requirements for this project [click here](https://github.com/ToybethSystems/Dokto-Backend/blob/main/requirements.txt).

## Installation

- First clone the prohject into your local machine.

```bash
git clone https://github.com/ToybethSystems/Dokto-Backend.git
```

- Go to the repository and create a virtual environment.

```bash
cd Dokto-Backend
python3 -m venv venv
```

- Activate the virtual environment and install dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

- Copy the `example.env` file to `.env` and fill in the values.

```bash
cp example.env .env
```

- The `.env` file should look like this:

```text
SECRET_KEY=<yoursecretkey>
VERSION=v1
DEBUG=True
```

- Create and migrate the database.

```bash
python manage.py migrate
```

## Running the server

- You can run the server with the following command:

```bash
python manage.py runserver
```

- You can also run the server on a custom port by adding the port number after the `runserver` command:

```bash
python manage.py runserver 8000
```
