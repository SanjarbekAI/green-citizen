#!/bin/bash

set -e

echo "🚀 Starting Green Citizen application..."

# No need to wait - Docker Compose healthchecks ensure services are ready
# Just run migrations and collect static files

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input || true

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --no-input || true

echo "✅ Setup complete!"
echo "🌐 Starting Django application..."

# Execute the main command
exec "$@"

