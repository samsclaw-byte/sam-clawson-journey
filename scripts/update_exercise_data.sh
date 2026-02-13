#!/bin/bash
# Update all dashboard data from Airtable for Mission Control

WORKSPACE="/home/samsclaw/.openclaw/workspace"

# Update exercise data
python3 "$WORKSPACE/scripts/fetch_exercise_data.py" 2>/dev/null || echo "Failed to fetch exercise data"

# Update productivity data (TAT tasks + habits)
python3 "$WORKSPACE/scripts/fetch_productivity_data.py" 2>/dev/null || echo "Failed to fetch productivity data"

# Update timeline data (7-day view)
python3 "$WORKSPACE/scripts/fetch_timeline_data.py" 2>/dev/null || echo "Failed to fetch timeline data"

# Copy to mission-control folder for web access
cp "$WORKSPACE/data/exercise_data.json" "$WORKSPACE/mission-control/data/" 2>/dev/null
cp "$WORKSPACE/data/productivity_data.json" "$WORKSPACE/mission-control/data/" 2>/dev/null
cp "$WORKSPACE/data/timeline_data.json" "$WORKSPACE/mission-control/data/" 2>/dev/null

# Git commit if there are changes
cd "$WORKSPACE"
git add mission-control/data/ 2>/dev/null
git diff --cached --quiet 2>/dev/null
if [ $? -ne 0 ]; then
    git commit -m "Auto-update dashboard data $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
    git push origin master 2>/dev/null
fi
