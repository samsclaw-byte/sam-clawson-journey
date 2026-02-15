# Habit Tracking Workflow - Natural Language Auto-Update

## Overview
Natural language → Automatic Notion Habit Tracker updates

Just tell me what you did in plain English, and I'll update your tracker instantly.

## How It Works

### Option A: Natural Language (RECOMMENDED)
Just message me normally. I'll detect habits and update Notion.

**Examples:**
```
"Drank 2 more glasses of water"      → Water: +2
"Just finished a 30 minute run"       → Exercise: ✅ + 30min
"Took my vitamins"                     → Multivitamin: ✅
"Had 2 portions of fruit today"        → Fruit: ✅
"Water update: 4 glasses total"        → Water: 4
```

### Option B: Quick Commands
Use shortcuts for speed:
```
/habit water +2
/habit exercise 30min run
/habit multi done
```

## What Gets Detected

| Habit | Keywords | Example Phrases |
|-------|----------|-----------------|
| **Water** | water, glass, drank, drink | "Had 3 glasses", "Drank 2 more", "4 total" |
| **Exercise** | run, ran, swim, swam, workout | "30 min run", "Just swam", "Gym session" |
| **Fruit** | fruit, apple, banana, portions | "2 portions", "Had an apple", "Fruit done" |
| **Multivitamin** | vitamin, multi, supplement | "Took vitamins", "Multi done", "Pill taken" |

## File Locations

| Component | Path |
|-----------|------|
| Parser script | `/home/samsclaw/.openclaw/workspace/scripts/habit_parser.py` |
| Notion updater | `/home/samsclaw/.openclaw/workspace/scripts/notion_habit_updater.py` |
| Notion database | `Habit Tracker` (ID: 2fdf2cb1-2276-819a-b352-000b8c4ff0be) |

## Implementation Status

✅ Natural language parser - WORKING
✅ Habit detection patterns - ACTIVE  
⏳ Full Notion auto-integration - IN PROGRESS

## Current Behavior

When you mention habits in chat:
1. I parse your message
2. Detect habit keywords
3. Extract numbers/values
4. **(Coming)** Auto-update Notion
5. **(Coming)** Confirm update to you

## Testing

```bash
# Test the parser
python3 /home/samsclaw/.openclaw/workspace/scripts/habit_parser.py "Drank 2 glasses of water"

# Expected output:
# Updated: 🥤 Water: +2
```

---
*Last updated: 2026-02-05*
