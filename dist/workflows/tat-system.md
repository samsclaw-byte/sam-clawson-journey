# TAT Task System v2.0
**Last Updated:** 2026-02-11

## Overview
Time-Aware Task (TAT) system for managing priorities with automatic due dates based on urgency categories.

## Categories (Numeric Format)

| Category | Name | Due | Use For |
|----------|------|-----|---------|
| **1** | Today | End of day | Must do today |
| **3** | 3 Days | Within 3 days | Short-term priorities |
| **7** | 7 Days | Within week | Medium-term tasks |
| **30** | 30 Days | Within month | Longer-term projects |

## Due Date Formula

**Notion Formula:**
```
dateAdd(prop("Date Created"), toNumber(prop("Category")), "days")
```

This automatically calculates when each task is due based on:
- Date Created (when you added the task)
- Category number (1, 3, 7, or 30 days)

## Daily Prioritization

### Morning Brief Shows:
1. **Category 1 tasks** (always shown)
2. **Overdue tasks** (any category past due date)

### Dashboard Shows:
- Top 5-7 urgent tasks
- Marked as "🔥 Today" or "⚠️ Overdue"

## Migration from v1.0

Old format → New format:
- 🔥 Today → **1**
- ⚡ 3 Days → **3**
- 📅 7 Days → **7**
- 🗓️ 30 Days → **30**
- 💻 Laptop Tasks → *Remove or use separate work database*

## Usage

### Adding Tasks
Just tell Clawson: *"Add TAT: Fix the printer"* (defaults to Category 1)

Or specify category: *"Add TAT: Research flights, category 3"*

### Task Properties
- **Task Name:** What you need to do
- **Category:** 1, 3, 7, or 30
- **Date Created:** Auto-set
- **Due Date:** Auto-calculated from formula
- **Status:** Not Started / In Progress / Complete
- **Notes:** Any details

## Automation

| Time | Action |
|------|--------|
| 6:00 AM | Morning brief lists Category 1 + overdue |
| 9:00 PM | Reminder check for overdue items |
| Dashboard | Always shows urgent tasks |

## Files
- `specs/tat-system-v2-spec.md` - Full technical spec
- `scripts/morning_brief.py` - Morning brief integration
- `scripts/generate_dashboard_v2.py` - Dashboard integration
