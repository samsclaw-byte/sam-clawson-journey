#!/bin/bash
# Start remote console with cloudflare tunnel

# Kill existing
pkill -f remote_console.py 2>/dev/null
pkill -f 'cloudflared tunnel' 2>/dev/null
sleep 2

# Start console
python3 /home/samsclaw/.openclaw/workspace/scripts/remote_console.py > /tmp/console.log 2>&1 &
sleep 3

# Start tunnel and save output
cloudflared tunnel --url http://localhost:8765 > /tmp/tunnel.log 2>&1 &
TUNNEL_PID=$!

# Wait for URL
sleep 10

# Extract URL
URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/tunnel.log | head -1)

# Save URL to file
echo "$URL" > /tmp/remote_console_url.txt
echo "$URL"

# Keep running
wait $TUNNEL_PID