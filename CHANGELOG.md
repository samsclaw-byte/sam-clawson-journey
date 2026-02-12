# Changelog

All notable changes to the workspace, systems, and data.

---

## 2026-02-12

### Systems
- **TAT System v3.0:** Complete redesign with formula-based due dates
  - Auto-calculated Due Date = Date Created + Category days (1/3/7/30)
  - New formula fields: TAT Days, Days Remaining, Urgency Level with color coding
  - Mandatory fields enforcement: Task Name, Category, Status required
  - Scripts: `tat_client_v3.py`, `add_tat_task_v3.py`, `tat_reminders.py`
  - Daily reminder cron job at 9:00 AM
- **Robust Food Logging:** Never-lose-a-meal error handling system
  - `log_food_meal_robust.py` - handles Edamam API failures gracefully
  - Saves description locally on API fail, creates TAT task, auto-retries (12pm/3pm/8pm)
  - `check_pending_nutrition.py` - cron-based retry system
  - Dual API key support - tries primary then fallback key
- **Airtable Sync v2:** Two-function sync system
  - Function 1: Sync local data to Airtable (compares actual Airtable vs local)
  - Function 2: Retry Edamam API for meals missing nutrition data
  - New "Edamam Data" checkbox field - True when complete nutrition available
  - Fixed duplicate creation bugs with proper existence checking
- **WSL DNS Fix:** Permanent solution via `/etc/wsl.conf`
  - Google DNS (8.8.8.8) configured permanently
  - Prevents DNS reset on WSL restart
  - Edamam API now resolving correctly to 107.20.173.119
- **Cloudflare Pages Deployment:** Mission Control live at https://clawson-mission-control.pages.dev/
  - Auto-update every 15 minutes via cron job
  - Custom domain: samsclaw.org (propagating)
  - Build command handles symlink issues
- **WHOOP Tunnel Restarted:** Cloudflare tunnel + webhook server running
  - URL: https://whoop.samsclaw.org/webhook/whoop
  - Running in screen session, ready to receive workout data

### Features
- **Mission Control Health & Nutrition Page:** New dedicated health dashboard
  - Meal cards with full nutrition display (24 nutrients from Edamam)
  - Macro pie chart visualization
  - 7-day timeline with net calories (calories - exercise)
  - 7-day exercise aggregates with horizontal bar chart
  - File: `mission-control/health-nutrition.html`
- **Habit Tracker Auto-Detection:** Food logging now primary entry point
  - `habit_tracker_from_food.py` - detects habits from food descriptions
  - Auto-logs: multivitamin (checkbox), water (count), fruit (checkbox)
  - 20+ fruit keywords (apple, banana, berries, mango, dates, etc.)
  - Integrated into robust food logging script
- **Overnight Data Validation:** New cron-based validation system
  - `overnight_data_validation.py` - validates data completeness
  - SEVERE/MINOR error classification
  - Field completeness checks for all Airtable tables
- **TAT v3 Documentation:** Complete setup guides created
  - `tat-system-v3-guide.html` - Interactive workflow documentation
  - `docs/tat-v3-airtable-setup.md` - Airtable field configuration

### Data
- **Meals Logged (Feb 12):** 5 meals with complete Edamam nutrition
  - Breakfast: Multigrain bread + lurpak + ham, cafe au lait (450 cal)
  - Snack 1: 2 dates (140 cal)
  - Snack 2: Banana, red apple, water (150 cal)
  - Lunch: Chicken avocado wrap + cappuccino + ginger lemon tea
  - Dinner: Spaghetti bolognese
  - Total: ~3,500+ calories with 24 nutrients each
- **Daily Habits (Feb 12):**
  - Multivitamin: ✅
  - Fruit: ✅ (banana, apple, dates, lemon)
  - Water: 7/8 glasses (87.5% of goal)
  - Exercise: ⏳
  - Creatine: ⏳
- **Edamam API Fixed:** Updated to working API key
  - Old key rejected due to authentication failure
  - New key: `b069c1d1fd628a38b69677d3744c347f`
  - All meals now have complete 24-nutrient data
- **Overnight Research:** All 7 tasks COMPLETE
  - No pending research tasks in queue
  - Ninth consecutive check with empty queue
- **TAT Tasks Created:** 2 new tasks
  - Complete TAT task Airtable setup with formula fields (Category 1)
  - Call Micasa to fix drainage and overflow issues (Category 7)
  - SSH Remote Access Setup task added

### Health
- **Water Intake:** 7/8 glasses (87.5% of daily goal)
  - Updates at: 11:32 AM (3), 5:08 PM (4), 7:24 PM (5), 9:47 PM (7)
  - Reminders sent throughout day at 1pm, 2pm, 3pm, 4pm, 5pm, 6pm, 7pm, 8pm, 9pm
- **Meals:** Tawouk, shish, hummus, patatas, pita (previous day reference)
- **Supplements:** Multivitamin ✅ (logged via breakfast)
- **Fruit Intake:** Banana, apple, dates, lemon (all auto-detected)
- **WHOOP:** Tunnel restarted, ready for data ingestion

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
