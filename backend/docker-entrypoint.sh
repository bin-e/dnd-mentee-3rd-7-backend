#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic --no-input --clear

echo "Setup dummy datas for testing codes"
python manage.py setup_test_data

# Start server
echo "Starting server"
gunicorn backend.wsgi --bind 0.0.0.0:8000