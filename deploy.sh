#!/bin/bash

set -e

ODOO_ADDONS_PATH="/root/addons/Fusion"
ODOO_CONTAINER_NAME="Fusion"
NGINX_CONTAINER_NAME="ReverseProxy"

echo "Starting deployment process..."

cd $ODOO_ADDONS_PATH

echo "Pulling latest changes from main branch..."
git fetch origin
git checkout main
git pull origin main

RESTART_ODOO=false
RESTART_PROXY=false

if git diff --name-only HEAD~1 HEAD | grep -E '\.(py|xml|csv)$' > /dev/null; then
    echo "Python/XML/CSV files changed - Odoo restart required"
    RESTART_ODOO=true
fi

if git diff --name-only HEAD~1 HEAD | grep -E '__manifest__\.py$' > /dev/null; then
    echo "Manifest files changed - Odoo restart required"
    RESTART_ODOO=true
fi

if [ "$RESTART_ODOO" = true ]; then
    echo "Restarting Odoo container..."
    if docker ps | grep -q $ODOO_CONTAINER_NAME; then
        docker restart $ODOO_CONTAINER_NAME
        echo "Odoo container restarted successfully"
        echo "Waiting for Odoo to be ready..."
        sleep 30
    else
        echo "Warning: Odoo container not found or not running"
    fi
fi

if git diff --name-only HEAD~1 HEAD | grep -E 'nginx|proxy|conf' > /dev/null; then
    echo "Proxy configuration may have changed"
    RESTART_PROXY=true
fi

if [ "$RESTART_PROXY" = true ]; then
    echo "Restarting reverse proxy..."
    if docker ps | grep -q $NGINX_CONTAINER_NAME; then
        docker restart $NGINX_CONTAINER_NAME
        echo "Nginx container restarted successfully"
    else
        echo "Warning: No reverse proxy found to restart"
    fi
fi

echo "Deployment completed successfully!"
echo "Timestamp: $(date)"
