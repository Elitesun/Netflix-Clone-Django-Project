#!/bin/bash

set -e

# Install Python dependencies
pip install -r requirements.txt

Python3 manage.py makemigrations
Python3 manage.py migrate


Python3 manage.py collectstatic --no-input
# Run database migrations


cd netfliclone 





