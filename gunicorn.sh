#!/bin/sh

gunicorn backend.asgi:application \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 1 \
  --threads 1 \
  --bind 0.0.0.0:8000 \
  --timeout 30 \
  --keep-alive 1 \
  --log-level critical
