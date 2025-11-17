#!/bin/bash

# Odoo Modules Deployment Script
set -e

ODOO_ADDONS_PATH="/root/addons/Fusion"
ODOO_CONTAINER_NAME="Fusion"
NGINX_CONTAINER_NAME="ReverseProxy"

echo "Starting deployment process..."

# Navigate to addons directory
cd $ODOO_ADDONS_PATH

# Pull latest changes
echo "Pulling latest changes from main branch..."
git fetch origin
git checkout main
git pull origin main

# Check for changes that require Odoo restart
RESTART_ODOO=false
RESTART_PROXY=false

# Check if any Python files or manifest files changed
if git diff --name-only HEAD~1 HEAD | grep -E '\.(py|xml|csv)$' > /dev/null; then
    echo "Python/XML/CSV files changed - Odoo restart required"
    RESTART_ODOO=true
fi

# Check if any manifest files changed
if git diff --name-only HEAD~1 HEAD | grep -E '__manifest__\.py$' > /dev/null; then
    echo "Manifest files changed - Odoo restart required"
    RESTART_ODOO=true
fi

# Check if any static files changed (CSS, JS, images)
if git diff --name-only HEAD~1 HEAD | grep -E '\.(css|js|scss|less|png|jpg|jpeg|gif|svg)$' > /dev/null; then
    echo "Static files changed - may need cache clear"
fi

# Restart Odoo container if needed
if [ "$RESTART_ODOO" = true ]; then
    echo "Restarting Odoo container..."
    if docker ps | grep -q $ODOO_CONTAINER_NAME; then
        docker restart $ODOO_CONTAINER_NAME
        echo "Odoo container restarted successfully"
        
        # Wait for Odoo to be ready
        echo "Waiting for Odoo to be ready..."
        sleep 30
        
        # Optional: Update module list (uncomment if needed)
        # docker exec $ODOO_CONTAINER_NAME odoo -d your_database -u all --stop-after-init
    else
        echo "Warning: Odoo container not found or not running"
    fi
fi

# Check if nginx config or proxy settings changed
if git diff --name-only HEAD~1 HEAD | grep -E 'nginx|proxy|conf' > /dev/null; then
    echo "Proxy configuration may have changed"
    RESTART_PROXY=true
fi

# Restart reverse proxy if needed
if [ "$RESTART_PROXY" = true ]; then
    echo "Restarting reverse proxy..."
    if docker ps | grep -q $NGINX_CONTAINER_NAME; then
        docker restart $NGINX_CONTAINER_NAME
        echo "Nginx container restarted successfully"
    elif systemctl is-active --quiet nginx; then
        systemctl restart nginx
        echo "Nginx service restarted successfully"
    else
        echo "Warning: No reverse proxy found to restart"
    fi
fi

echo "Deployment completed successfully!"
echo "Timestamp: $(date)"
