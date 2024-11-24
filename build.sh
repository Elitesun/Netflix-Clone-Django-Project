#!/bin/bash

set -e

# Install Python dependencies
pip install -r requirements.txt

py manage.py collectstatic --no-input
# Run database migrations

py manage.py makemigrations
py manage.py migrate

cd netflixclone




