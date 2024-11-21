#!/bin/bash

# Start Celery worker in the background
N_WORKERS=${N_WORKERS:-10}
gunicorn --bind :80 --env DJANGO_SETTINGS_MODULE=server.settings --workers "$N_WORKERS" --threads 1 --timeout 0 server.wsgi
