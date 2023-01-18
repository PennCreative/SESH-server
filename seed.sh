#!/bin/bash
rm -rf seshapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations seshapi
python3 manage.py migrate seshapi
python3 manage.py loaddata users
