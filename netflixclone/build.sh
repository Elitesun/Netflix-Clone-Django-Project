#!/bin/bash

set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Remove the cd command since manage.py is already in the correct directory
python3 manage.py collectstatic --no-input
