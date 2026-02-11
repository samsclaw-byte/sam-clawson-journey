#!/bin/bash
# GitHub push helper for Sam & Clawson blog

echo "🦞 Ready to push your blog to GitHub!"
echo "Repository: https://github.com/samsclaw-byte/sam-clawson-journey"
echo ""

# Navigate to blog directory
cd /home/samsclaw/.openclaw/workspace/blog

echo "📋 Current status:"
git status

echo ""
echo "🔐 Choose your authentication method:"
echo "1. Personal Access Token (recommended)"
echo "2. SSH Key (if already set up)"
echo ""

read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🎯 Personal Access Token Method:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Name: 'Blog Publishing'"
    echo "4. Select scope: ✅ repo (full control)"
    echo "5. Copy the token (you won't see it again)"
    echo ""
    read -p "Paste your token here: " TOKEN
    
    echo "🚀 Pushing to GitHub..."
    git push https://$TOKEN@github.com/samsclaw-byte/sam-clawson-journey.git master
    
elif [ "$choice" = "2" ]; then
    echo "🚀 Pushing via SSH..."
    git remote set-url origin git@github.com:samsclaw-byte/sam-clawson-journey.git
    git push -u origin master
    
else
    echo "❌ Invalid choice. Please run again and choose 1 or 2."
    exit 1
fi

echo ""
echo "✅ Push complete!"
echo ""
echo "🌐 Next: Enable GitHub Pages"
echo "1. Go to: https://github.com/samsclaw-byte/sam-clawson-journey/settings"
echo "2. Scroll to 'Pages' section"
echo "3. Source: Deploy from branch → Master"
echo "4. Your blog will be live at:"
echo "   https://samsclaw-byte.github.io/sam-clawson-journey/"
echo ""
echo "🎉 Ready to share your journey with the world!"