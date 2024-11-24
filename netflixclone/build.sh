#!/bin/bash

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

Python manage.py collectstatic --no-input

Python manage.py makemigrations
Python manage.py migrate



# Run database migrations


cd netfliclone 





