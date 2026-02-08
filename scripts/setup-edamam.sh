#!/bin/bash
# Setup script for Edamam Nutrition API

echo "🍽️ Edamam Nutrition API Setup"
echo "=============================="
echo ""

# Create secure directory
mkdir -p "$HOME/.config/edamam"
chmod 700 "$HOME/.config/edamam"

echo "Step 1: Get your free API credentials"
echo "  1. Go to: https://developer.edamam.com/"
echo "  2. Sign up for free developer account"
echo "  3. Sign up for 'Nutrition Analysis API'"
echo "  4. Get your App ID and API Key"
echo ""

read -p "Enter your Edamam App ID: " app_id
read -p "Enter your Edamam API Key: " api_key

# Save securely
echo "$app_id" > "$HOME/.config/edamam/app_id"
echo "$api_key" > "$HOME/.config/edamam/api_key"
chmod 600 "$HOME/.config/edamam/app_id"
chmod 600 "$HOME/.config/edamam/api_key"

echo ""
echo "✅ Credentials saved securely!"
echo ""
echo "Testing API connection..."

# Test
cd /home/samsclaw/.openclaw/workspace/scripts
./edamam-nutrition.sh "1 apple"

echo ""
echo "🎉 Setup complete! Use: ./edamam-nutrition.sh 'food description'"
