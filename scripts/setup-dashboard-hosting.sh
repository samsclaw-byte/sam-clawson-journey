#!/bin/bash
# Dashboard Setup Script
# Sets up GitHub Pages hosting for mobile dashboard

echo "🚀 Sam's Command Center - Dashboard Setup"
echo "=========================================="
echo ""

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run this from your workspace root."
    exit 1
fi

# Add dashboard to git
echo "📦 Step 1: Adding dashboard to git..."
git add dashboard/
git commit -m "Add mobile dashboard - Sam's Command Center"

# Push to GitHub
echo ""
echo "☁️ Step 2: Pushing to GitHub..."
git push origin master

# Instructions for GitHub Pages
echo ""
echo "✅ Code pushed! Now enable GitHub Pages:"
echo ""
echo "1. Go to: https://github.com/YOUR_USERNAME/sam-clawson-journey/settings/pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: master / (root)"
echo "4. Click Save"
echo ""
echo "5. Your dashboard will be at:"
echo "   https://YOUR_USERNAME.github.io/sam-clawson-journey/dashboard/"
echo ""
echo "📱 Bookmark this on your phone for easy access!"
echo ""
echo "⏰ Auto-updates every 15 minutes via cron job"
echo "   (Already set up - no action needed)"
