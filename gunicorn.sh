#!/bin/sh
python manage.py migrate

gunicorn backend.asgi:application \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000