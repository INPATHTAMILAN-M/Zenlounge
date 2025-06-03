#!/bin/bash

# Pull the latest code changes from the repository
echo "Pulling latest changes from Git..."
git pull || { echo "Git pull failed. Exiting."; exit 1; }

# Restart the wwwgunicorn service
echo "Restarting the zenlounge service..."
sudo systemctl restart zenlounge || { echo "Failed to restart zenlounge. Exiting."; exit 1; }

# Restart the daemon service
echo "Restarting the daemon service..."
sudo systemctl daemon-reload || { echo "Failed to restart daemon. Exiting."; exit 1; }

# Restart celery 
echo "Restarting Celery..."
sudo systemctl restart celery || { echo "Failed to restart celery. Exiting."; exit 1; }

# Restart celery beat
echo "Restarting Celery Beat..."
sudo systemctl restart celery-beat || { echo "Failed to restart celery beat. Exiting."; exit 1; }

# Restart the Nginx service
echo "Restarting Nginx..."
sudo systemctl restart nginx || { echo "Failed to restart Nginx. Exiting."; exit 1; }


echo "All services restarted successfully!"