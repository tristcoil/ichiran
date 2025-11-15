#!/bin/bash

echo "Checking postgres server status..."
while : ; do
    pg_isready -h pg > /dev/null && break;
    sleep 1;
done

echo "Postgres is ready, starting main container init."
init-all;

echo "Starting Flask API on port 5900..."
python3 /root/quicklisp/local-projects/ichiran/docker/ichiran-scripts/iapi.py &

echo "All set, awaiting commands."
sleep infinity;