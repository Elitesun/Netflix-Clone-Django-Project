#!/bin/bash

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

Python manage.py collectstatic --no-input

cd netflixclone





