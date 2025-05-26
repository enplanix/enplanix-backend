#!/bin/sh

# gunicorn backend.asgi:application \
#   --worker-class uvicorn.workers.UvicornWorker \
#   --workers 1 \
#   --threads 1 \
#   --bind 0.0.0.0:8000 \
#   --timeout 30 \
#   --keep-alive 1 \
#   --log-level critical

uvicorn backend.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 1 \
  --loop uvloop \
  --http httptools \
  --timeout-keep-alive 5 \
  --log-level critical
