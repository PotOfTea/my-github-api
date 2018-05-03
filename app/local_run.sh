#!/usr/bin/env bash
export POSTGRES_URL="0.0.0.0:8001"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="mysecretpassword"
export PYTHONUNBUFFERED="1"
export APP_SETTINGS="config.TestingConfig"
export POSTGRES_DB="postgres"
export REDIS_URL=redis://127.0.0.1:6379/0
gunicorn --bind 0.0.0.0:5000 "main:create_app()"
