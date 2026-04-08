#!/bin/bash

echo " Stopping Distribyx..."

cd "$(dirname "$0")/.."

docker-compose -f compose/docker-compose.yml down

echo " All services stopped."