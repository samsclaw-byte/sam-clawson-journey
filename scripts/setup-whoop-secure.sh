#!/bin/bash
# WHOOP Security Setup Script
# Run this when you're at your laptop with WHOOP credentials

echo "🔒 WHOOP Security Setup"
echo "======================"
echo ""

# Check directory exists (created by Clawson)
if [ ! -d "$HOME/.config/whoop" ]; then
    mkdir -p "$HOME/.config/whoop"
    chmod 700 "$HOME/.config/whoop"
    echo "✅ Created secure directory: ~/.config/whoop"
else
    echo "✅ Secure directory already exists"
fi

# Set permissions
chmod 700 "$HOME/.config/whoop"
chmod 600 "$HOME/.config/whoop/credentials" 2>/dev/null
chmod 600 "$HOME/.config/whoop/tokens.json" 2>/dev/null

echo "✅ Set secure permissions (700/600)"
echo ""

# Instructions
cat << 'EOF'
📋 NEXT STEPS:

1. Get WHOOP Developer Credentials:
   - Go to: https://developer.whoop.com/
   - Create account → Create app
   - Copy CLIENT_ID and CLIENT_SECRET

2. Edit credentials file:
   nano ~/.config/whoop/credentials
   
   Replace:
   export WHOOP_CLIENT_ID="paste_your_client_id_here"
   export WHOOP_CLIENT_SECRET="paste_your_client_secret_here"

3. Source credentials in your shell:
   echo 'source ~/.config/whoop/credentials' >> ~/.bashrc
   source ~/.bashrc

4. Run OAuth authorization (one-time):
   cd ~/.openclaw/workspace/skills/whoop
   node bin/whoop-auth --redirect-uri https://localhost:3000/callback
   
   - Open URL on phone
   - Click Allow
   - Copy code from callback URL
   - Paste back in terminal

5. Verify setup:
   ls -la ~/.config/whoop/
   # Should show:
   # drwx------ (700) for directory
   # -rw------- (600) for files

✅ WHOOP will then be ready for daily morning reports!
EOF

# Verify current state
echo ""
echo "📊 Current Security State:"
ls -la ~/.config/whoop/
