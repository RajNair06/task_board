#!/bin/sh
set -e
if [ "$RUN_MIGRATIONS" = "1" ]; then
    echo "Running database migrations..."
    cd /app/db
    alembic upgrade head
fi

echo "Starting application..."
cd /app
exec "$@"
