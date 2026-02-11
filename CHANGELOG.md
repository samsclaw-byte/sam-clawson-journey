# Changelog

All notable changes to the workspace, systems, and data.

---

## 2026-02-11

### Systems
- **Database Migration:** Complete migration from Notion → Airtable (90+ records)
  - Health & Nutrition Base: Food Log, Weight Tracker, Workouts, WHOOP Data
  - Productivity Base: Daily Habits, TAT Tasks v2
- **TAT System v2.0:** Numeric categories (1/3/7/30 days) with auto-calculated due dates
  - Smart defaults: Laptop tasks → 1 day, Other → 7 days
  - Created `add_tat_task.py` with auto-categorization
- **WHOOP Integration:** Fixed OAuth, restarted webhook server with Cloudflare tunnel
  - New permanent tunnel setup script for `samsclaw.org` domain
  - Retrieved 10 days of cycle data + 4 historical workouts with zone data
- **Notion API Fix:** Switched to API version 2022-06-28 (2025-09-03 had bugs)
  - Backfilled 14 meals, 3 weight entries, 7 work tasks

### Features
- **Mission Control Dashboard v2.0:** NASA-style personal dashboard
  - 4 views: Overview, Work (Steve/Rafi/Projects), Daily, Projects
  - Responsive design, ready for GitHub Pages deployment
- **Work Workflow Control Centre:** Business plan from voice note transcription
  - Mission control concept for work management with line managers
- **Remote Console:** Web-based console for phone access (experimental)
- **New Habit Tracker:** Systematic tracking for creatine, multivitamin, exercise, fruit, water
  - Backfilled 4 days of data (Feb 8-11)

### Data
- **Airtable Migration Complete:**
  - Food Log: 13 meals with 24 nutrition fields (macros + 7 micronutrients from Edamam)
  - Weight Tracker: 3 entries (104kg → 103kg, goal 95kg)
  - Workouts: 8 workouts (kettlebell sessions + 4 WHOOP swim/run records)
  - WHOOP Data: 10 days of strain scores, HR, recovery, calories
  - Daily Habits: 4 days (creatine, multi, exercise, fruit, water)
  - TAT Tasks: 46 tasks migrated with auto-calculated due dates
- **Documentation:** Created `workflow-updates-airtable.md` for script migration guide

### Health
- **Evening Workout:** Kettlebell full body + full calf routine + post-workout walk
- **Water:** 5/8 glasses (62% of daily goal)
- **Weight:** 103kg logged
- **Meals:** Tawouk, shish, hummus, patatas, pita (lunch)
- **Drinks:** Cafe au lait, Lemon & ginger tea
- **Supplements:** Creatine ✅, Multivitamin ✅
- **WHOOP:** Feb 11 strain 8.8 (rest day), previous high-strain days correlated with workouts

---
