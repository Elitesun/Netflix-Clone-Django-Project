#!/bin/bash

set -e

# Install Python dependencies
pip install -r requirements.txt

python manage.py collectstatic --no-input
# Run database migrations

python manage.py makemigrations
python manage.py migrate




