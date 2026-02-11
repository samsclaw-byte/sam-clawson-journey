#!/bin/bash
# GitHub setup script for Sam & Clawson blog

echo "🦞 Setting up GitHub repository for our blog..."

# Get repository URL from user
read -p "Enter your GitHub repository URL (https://github.com/yourusername/repo): " REPO_URL

# Navigate to blog directory
cd /home/samsclaw/.openclaw/workspace/blog

# Add remote repository
git remote add origin $REPO_URL

# Add all files
git add .
git commit -m "Initial blog setup - Day 1 & 2 posts ready"

# Push to GitHub
git push -u origin master

echo "✅ Blog pushed to GitHub!"
echo "🌐 Next: Enable GitHub Pages in repository settings"
echo "📍 Settings > Pages > Source: Deploy from branch > Master"
