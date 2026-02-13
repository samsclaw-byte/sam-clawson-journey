#!/bin/bash
# Auto-update Mission Control and deploy to Cloudflare

cd /home/samsclaw/.openclaw/workspace

# Generate updated Mission Control
echo "Generating Mission Control..."
python3 scripts/generate_mission_control.py

# Check if there are changes
if git diff --quiet mission-control/ 2>/dev/null; then
    echo "No changes to deploy"
    exit 0
fi

# Commit and push
echo "Deploying changes..."
git add mission-control/
git commit -m "Auto-update Mission Control - $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ Mission Control updated and deployed!"
