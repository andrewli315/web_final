# Web services final project

## Getting Started

requirement : python3, flask, flask-bootstrap, flask-OAuth, flask-alchemy, requests, sqlite3, flask-cors

Usage: 

```
# make a new sql table
$ source ./venv/bin/activate
$ flask shell
> from model import db
> db.create_all

$ deactivate
$ python3 runserver app.py
# or just 
$ python3 app.py

```
