#!/bin/bash
# keep-alive.sh - Ping service to prevent Render sleep
# Run this script every 10 minutes to keep your site awake

while true; do
    echo "$(date): Pinging InternFind to keep it alive..."
    curl -s https://internfind.onrender.com/api/health > /dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Ping successful"
    else
        echo "❌ Ping failed"
    fi
    
    # Wait 10 minutes (600 seconds)
    sleep 600
done
