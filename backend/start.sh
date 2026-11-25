#!/usr/bin/env sh
set -e
flask --app wsgi db upgrade
if [ "$SEED_DEMO" = "true" ]; then
  flask --app wsgi seed-demo
fi
exec gunicorn wsgi:app --bind 0.0.0.0:"${PORT:-8000}" --workers 2 --access-logfile -
