#!/bin/bash
# Set HTTPS=true, SSL_CERTFILE, and SSL_KEYFILE environment variables to enable HTTPS.
# Example: HTTPS=true SSL_CERTFILE=certs/cert.pem SSL_KEYFILE=certs/key.pem ./startup.sh
PORT="${PORT:-8000}"
SSL_ARGS=""
if [ -n "$SSL_CERTFILE" ] && [ -n "$SSL_KEYFILE" ]; then
    SSL_ARGS="--keyfile $SSL_KEYFILE --certfile $SSL_CERTFILE"
fi
gunicorn -w 4 -k uvicorn.workers.UvicornWorker API.main:app --bind "0.0.0.0:${PORT}" $SSL_ARGS
