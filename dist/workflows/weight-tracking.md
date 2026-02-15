# Weight Tracking Workflow

## Overview
Daily weight logging with Notion sync. Track progress toward your goal with automatic calculations.

## Current Status
⚖️ **Today:** 104.0 kg (229.3 lbs)  
🎯 **Goal:** 90.0 kg (14 kg to go)

## How It Works

### Daily Check-in
Just tell me your weight:
- "Weight check-in: 104 kg"
- "Weighed in at 103.5 this morning"
- "104 kg again today"

I'll log it **locally + in Notion** and show you trends.

### Automatic Tracking
- **Daily change** from yesterday
- **7-day trend** (up/down/stable)
- **Goal progress** (% toward 90kg)
- **All data synced to Notion** for visualization

### Notion Database
View your weight history in Notion: **⚖️ Weight Tracker**  
URL: https://www.notion.so/f9583de869e940e6ab15c530277ec474

Database columns:
- Date
- Weight (kg) / Weight (lbs)
- Change (kg) - auto-calculated
- Notes

## Commands

```bash
# Log weight locally
python3 scripts/weight_tracker.py log 103.5

# Log to Notion
python3 scripts/notion_weight_sync.py log 103.5 "Morning weigh-in"

# Check local status
python3 scripts/weight_tracker.py status

# List Notion entries
python3 scripts/notion_weight_sync.py list

# Set goal
python3 scripts/weight_tracker.py goal 95
```

## Files

| File | Purpose |
|------|---------|
| `scripts/weight_tracker.py` | Local weight logging |
| `scripts/notion_weight_sync.py` | Notion sync script |
| `data/weight_tracker.json` | Local backup data |

## Integration
Works alongside nutrition tracking to correlate diet with weight changes over time.

---
*Created: 2026-02-08*
