#!/bin/bash

# Variables
APP_DIR="/opt/speech-agent"
REPO_URL="https://github.com/yourusername/grok-tts.git"  # Replace with your repo URL

# Update system and install docker compose plugin if needed
apt-get update && apt-get install -y docker-compose-plugin

# Clone/update repository
if [ -d "$APP_DIR" ]; then
    cd $APP_DIR
    git pull
else
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Start application
docker compose up -d --build

echo "Deployment completed! Application running at http://$(curl -s ifconfig.me)"
