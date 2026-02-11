#!/bin/bash
# Cloudflare Tunnel Setup Script for WHOOP Webhooks
# Run this to set up a secure, permanent webhook endpoint

echo "🚀 WHOOP Webhook Setup with Cloudflare Tunnel"
echo "=============================================="
echo ""

# Step 1: Install cloudflared
echo "📦 Step 1: Installing cloudflared..."
if ! command -v cloudflared &> /dev/null; then
    # Download and install cloudflared
    curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared.deb
    rm cloudflared.deb
    echo "✅ cloudflared installed"
else
    echo "✅ cloudflared already installed"
fi

echo ""
echo "🔧 Step 2: Authenticating with Cloudflare..."
echo "This will open a browser for you to log in to Cloudflare"
cloudflared tunnel login

echo ""
echo "🎢 Step 3: Creating tunnel..."
TUNNEL_NAME="whoop-webhook"
cloudflared tunnel create $TUNNEL_NAME

echo ""
echo "📁 Step 4: Configuring tunnel..."
# Get the tunnel ID
TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')

cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: ~/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: whoop-webhook.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
EOF

echo "✅ Config saved to ~/.cloudflared/config.yml"

echo ""
echo "🌐 Step 5: Creating DNS record..."
echo "You need to create a CNAME record:"
echo "  Name: whoop-webhook"
echo "  Target: $TUNNEL_ID.cfargotunnel.com"
echo ""
echo "Or run: cloudflared tunnel route dns $TUNNEL_NAME whoop-webhook.yourdomain.com"

echo ""
echo "🚀 Step 6: Starting tunnel..."
echo "Run this command to start the tunnel:"
echo "  cloudflared tunnel run $TUNNEL_NAME"
echo ""
echo "Or set up as a service:"
echo "  sudo cloudflared service install"
echo "  sudo systemctl start cloudflared"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update the hostname in ~/.cloudflared/config.yml with your actual domain"
echo "2. Create the DNS CNAME record in Cloudflare dashboard"
echo "3. Run the webhook server (see webhook_server.py)"
echo "4. Start the tunnel"
echo "5. Register the webhook URL in WHOOP dashboard"
