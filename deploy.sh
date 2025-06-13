#!/bin/bash

# Pull latest code
echo "🔁 Pulling latest changes from Git..."
git pull || { echo "❌ Git pull failed. Exiting."; exit 1; }

# Restart Django app (Gunicorn)
echo "🔁 Restarting Django (zenlounge) service..."
sudo systemctl restart zenlounge || { echo "❌ Failed to restart zenlounge. Exiting."; exit 1; }

# Restart Celery worker
echo "🔁 Restarting Celery worker..."
sudo systemctl restart celery || { echo "❌ Failed to restart celery. Exiting."; exit 1; }

# Restart Celery beat scheduler
echo "🔁 Restarting Celery Beat..."
sudo systemctl restart celery-beat || { echo "❌ Failed to restart celery beat. Exiting."; exit 1; }

# Restart Nginx
echo "🔁 Restarting Nginx..."
sudo systemctl restart nginx || { echo "❌ Failed to restart Nginx. Exiting."; exit 1; }

echo "✅ All services restarted successfully!"

