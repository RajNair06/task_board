#!/bin/sh
set -e
echo "starting container.."
mkdir -p /app/db
echo "running db migrations"
alembic -c db/alembic.ini upgrade head
echo "starting app.."
exec "$@"

