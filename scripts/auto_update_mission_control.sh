#!/bin/bash
# Auto-update Mission Control data files (skip index.html - manually designed)

cd /home/samsclaw/.openclaw/workspace

# Update data files only (not index.html which is now manually designed)
echo "Updating Mission Control data..."

# Update exercise data
python3 scripts/fetch_exercise_data.py 2>/dev/null || true
cp data/exercise_data.json mission-control/data/ 2>/dev/null || true

# Update productivity data  
python3 scripts/fetch_productivity_data.py 2>/dev/null || true
cp data/productivity_data.json mission-control/data/ 2>/dev/null || true

# Update timeline data
python3 scripts/fetch_timeline_data.py 2>/dev/null || true
cp data/timeline_data.json mission-control/data/ 2>/dev/null || true

# Update daily nutrition data
python3 scripts/fetch_daily_nutrition.py 2>/dev/null || true
cp data/daily_nutrition_*.json mission-control/data/ 2>/dev/null || true

# Check if there are changes to data files
if git diff --quiet mission-control/data/ 2>/dev/null; then
    echo "No data changes to deploy"
    exit 0
fi

# Commit and push only data files
echo "Deploying data updates..."
git add mission-control/data/
git commit -m "Auto-update Mission Control data - $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ Mission Control data updated and deployed!"
