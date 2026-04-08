#!/bin/bash

echo " Deploying Distribyx..."


cd "$(dirname "$0")/.."

echo " Pulling latest changes..."
git pull

echo " Stopping old containers..."
docker-compose -f compose/docker-compose.yml down

echo " Building & starting containers..."
docker-compose -f compose/docker-compose.yml up --build -d

echo " Deployment complete!"

echo "🌐 Services:"
echo "→ App:        http://<VM-IP>:8080"
echo "→ Prometheus: http://<VM-IP>:9090"
echo "→ Grafana:    http://<VM-IP>:3000"