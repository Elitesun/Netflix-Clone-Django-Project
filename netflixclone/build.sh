#!/bin/bash

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

py manage.py collectstatic --no-input

cd netflixclone





