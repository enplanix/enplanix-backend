#!/bin/sh

# gunicorn backend.asgi:application \
#     --worker-class uvicorn.workers.UvicornWorker \
#     --workers 2 \
#     --bind 0.0.0.0:8000 \
#     --timeout 60 \
#     --keep-alive 5

gunicorn backend.asgi:application \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --threads 1 \
    --bind 0.0.0.0:8000 \
    --timeout 30 \
    --keep-alive 2 \
    --access-logfile /dev/null \
    --error-logfile /dev/null \
    --log-level critical # info