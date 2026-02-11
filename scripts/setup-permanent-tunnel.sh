#!/bin/bash
# Permanent Cloudflare Tunnel Setup for samsclaw.org

echo "🚀 Setting Up Permanent Tunnel for samsclaw.org"
echo "================================================"
echo ""

TUNNEL_NAME="whoop-webhook-samsclaw"
HOSTNAME="whoop.samsclaw.org"
LOCAL_PORT="5000"

echo "Step 1: Authenticating with Cloudflare..."
cloudflared tunnel login
echo ""

echo "Step 2: Creating tunnel: $TUNNEL_NAME"
TUNNEL_OUTPUT=$(cloudflared tunnel create "$TUNNEL_NAME" 2>&1)
echo "$TUNNEL_OUTPUT"

# Extract tunnel ID
TUNNEL_ID=$(echo "$TUNNEL_OUTPUT" | grep -oP '[a-f0-9-]{36}' | head -1)

echo ""
echo "Step 3: Creating DNS route..."
cloudflared tunnel route dns "$TUNNEL_NAME" "$HOSTNAME"

echo ""
echo "Step 4: Creating config file..."
mkdir -p ~/.cloudflared

cat > ~/.cloudflared/config-samsclaw.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: ~/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $HOSTNAME
    service: http://localhost:$LOCAL_PORT
  - service: http_status:404
EOF

echo "✅ Config created at ~/.cloudflared/config-samsclaw.yml"
echo ""

echo "Step 5: Starting permanent tunnel..."
echo "Run this command to start:"
echo "  cloudflared tunnel run $TUNNEL_NAME"
echo ""
echo "Or run as a service:"
echo "  sudo cloudflared service install"
echo "  sudo systemctl start cloudflared"
echo ""

echo "🎉 Your webhook URL will be:"
echo "  https://$HOSTNAME/webhook/whoop"
echo ""
echo "Update WHOOP dashboard with this URL!"
