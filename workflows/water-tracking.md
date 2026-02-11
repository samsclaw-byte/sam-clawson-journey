# Water Tracking Workflow

## Overview
Daily hydration tracking with smart reminders throughout the day.

## Current Status
💧 **3/8 glasses (38%)** - 5 more to reach goal!

## How It Works

### Automatic Logging
Just tell me naturally:
- "Drank 2 glasses of water"
- "Had another glass"
- "Water update: 5 glasses total"

I'll automatically add it to your tracker.

### Daily Goal
**Default:** 8 glasses (2L)

To change your goal:
```bash
python3 scripts/water_tracker.py goal 10  # Set to 10 glasses
```

### Reminder Schedule
Smart reminders based on your progress:

| Time | Condition | Reminder |
|------|-----------|----------|
| 10am-12pm | If < 4 glasses | Morning hydration check |
| 1pm-5pm | If < 6 glasses | Afternoon check-in |
| 6pm-8pm | If < 8 glasses | Evening push to goal |

Reminders only fire if you're behind schedule — no spam when you're on track!

## Commands

```bash
# Check status
python3 scripts/water_tracker.py status

# Add water manually
python3 scripts/water_tracker.py add 2  # Add 2 glasses

# View full log
python3 scripts/water_tracker.py log
```

## Files

| File | Purpose |
|------|---------|
| `scripts/water_tracker.py` | Tracker script |
| `data/water_tracker.json` | Daily data storage |

## Integration with Nutrition
Water intake is tracked alongside your meals. Stay hydrated! 💧

---
*Created: 2026-02-08*
