#!/bin/bash

set -e

# Install Python dependencies
pip install -r requirements.txt

Python manage.py collectstatic --no-input
# Run database migrations

Python manage.py makemigrations
Python manage.py migrate

cd netfliclone 





