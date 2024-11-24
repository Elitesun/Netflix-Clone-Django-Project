#!/bin/bash

set -e

# Install Python dependencies
pip install -r requirements.txt

Py manage.py makemigrations
Py manage.py migrate


Py manage.py collectstatic --no-input
# Run database migrations


cd netfliclone 





