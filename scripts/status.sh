#!/bin/bash

echo " Distribyx Status"

cd "$(dirname "$0")/.."

docker-compose -f compose/docker-compose.yml ps

echo ""
echo "🐳 Docker Containers:"
docker ps