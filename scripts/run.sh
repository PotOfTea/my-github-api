#! /usr/bin/env bash
set -e

NUM_WORKERS=3
TIMEOUT=120
DB="database:${DB_PORT_INT}"

./wait-for-it.sh ${DB} && gunicorn --keep-alive 5 --workers $NUM_WORKERS --timeout $TIMEOUT --log-level=debug --bind 0.0.0.0:${APP_BIND_PORT} "main:create_app()"

exec "$@"
