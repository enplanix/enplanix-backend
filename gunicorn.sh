#!/bin/sh
# gunicorn backend.asgi:application \
#     --worker-class uvicorn.workers.UvicornWorker \
#     --workers 2 \
#     --bind 0.0.0.0:8000 \
#     --timeout 60 \
#     --keep-alive 5

# single thread
gunicorn backend.asgi:application \
    --worker-class gthread \
    --workers 1 \
    --threads 4 \
    --bind 0.0.0.0:8000 \
    --timeout 60 \
    --keep-alive 5