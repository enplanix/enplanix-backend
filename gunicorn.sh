#!/bin/sh
gunicorn backend.asgi:application \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 3 \
    --bind 0.0.0.0:8000 \
    --timeout 60 \
    --keep-alive 5

