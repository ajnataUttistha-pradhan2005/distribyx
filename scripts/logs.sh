#!/bin/bash

echo "📜 Showing logs..."

cd "$(dirname "$0")/.."

docker-compose -f compose/docker-compose.yml logs -f