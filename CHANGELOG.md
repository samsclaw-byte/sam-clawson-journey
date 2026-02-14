# Changelog

All notable changes to the workspace, systems, and data.

---

## 2026-02-14

### Systems
- **Mission Control v2.1:** Major dashboard enhancements and live data integration
  - **Fitness Program Page:** New dedicated page with recovery zones, calf protocol, weekly schedule, prohibited exercises (purple-pink theme)
  - **Productivity Page Redesign:** TAT Tasks card with integrated badge counts in filter tabs, 🔴 Overdue tab added, removed "Add Task" button
  - **Today's Progress Section:** Real-time habit status with water count integrated into weekly habit tracker
  - **Cloudflare Worker API:** TAT task completion endpoint created (`tat-complete-worker.js`) - ready for 5-minute deployment
  - **Navigation Updated:** All 6 pages now link to Fitness Program
- **Data Integrity Fixes:**
  - Fixed duplicate habit records for Feb 13 (merged 4 duplicates to correct values)
  - Deleted 3 duplicate food entries (banana/apple snack, dates, extra breakfast)
  - Updated data sync protocol: no auto-posting on mismatches, ask for clarification instead
- **Security Sentinel:** Daily cron at 1:30 AM active
- **API Testing Planned:** MiniMax 2.5 and GLM5 configured for testing (awaiting .env key updates)

### Features
- **Mission Control Live Data:** Overview page fully integrated with Airtable
  - **Today View:** Real-time health snapshot, habit checklist, priority TAT tasks, quick wins score
  - **Trend View:** Weight history with 85kg goal line, 7-day hydration bars, habit consistency scores, activity & strain tracking
  - **Auto-refresh:** Every 15 minutes via cron job
  - **Data sources:** Food Log, Weight Tracker, Workouts, Daily Habits, TAT Tasks
- **TAT Completion Feature:** Cloudflare Worker with secure API endpoint
  - ✓ "Complete" button on all non-completed tasks in Mission Control
  - Confirmation dialog and visual feedback (loading → auto-refresh)
  - Airtable key stored in Cloudflare secrets
- **Mission Control Bug Fixes:**
  - Fixed duplicate variable declaration in Overview page
  - Regenerated overview_data.json with correct values

### Data
- **Feb 14 Nutrition (Partial):** Breakfast logged at resort
  - Breakfast (9:45 AM): 2 bacon, 2-egg omelette, wholemeal bread, baked beans, pineapple, melon, dates, flat white (730 cal, 38g protein)
  - Water: 6/8 glasses (75% of goal)
  - Habits: Fruit ✅, Exercise ✅, Creatine ✅, Multivitamin ❓
- **Feb 13 Food Log Completed:** Backfilled missing meals
  - Lunch: Turkey & cheese croissant + protein bar (620 cal, 35g protein)
  - Dinner: Arabic food (tawouk, shish, hummus, patatas, pita) + chocolate cake (950 cal)
  - Evening: Beer + 2 glasses white wine (350 cal)
  - **Final:** 3,600 calories, 131g protein (8 meals)
- **Research Queue Status:** All 8 overnight research tasks complete, all 1 build task complete
  - System Architecture Review completed (Feb 14)
  - No pending tasks in queue
- **TAT Status:** 2 priority tasks (1 overdue, 1 due today), 28 total with category validation errors to fix

### Health
- **Morning Run (10:12 AM):** 33min 6sec at resort
  - Strain: 13.8 | Calories: ~400
  - HR Zones: Z5: 52sec, Z4: 19:57, Z3: 9:30, Z2: 1:52, Z1: 55sec
  - Exercise habit: ✅ Marked complete
- **Water Intake:** 6/8 glasses (2 short of goal)
  - Progress: 2 (8:10 AM) → 3 (11:03 AM) → 4 (1:51 PM) → 6 (6:29 PM)
- **Supplements:** Creatine ✅ (30g protein powder + creatine at 6:29 PM)
- **Weight:** 102 kg (current)
- **WHOOP:** Token expired (refresh when back from resort)

---

## 2026-02-13

### Systems
- **Mission Control v2.0:** Complete dashboard system with 5 live-linked pages
  - **Overview:** Daily priorities, habit summary, recent activity with white/purple-pink theme
  - **Health & Nutrition:** 7-day timeline, exercise card, date selector for meals/macros
  - **Productivity:** TAT task list with filters, weekly habit tracker, habit streaks
  - **Work:** Line manager tasks and project tracking
  - **Blog:** Stats and post grid with navigation
  - All pages linked to live Airtable data with 15-minute auto-refresh
- **WHOOP Integration v2.1:** Enhanced webhook server with workout/cycle support
  - `workout.created` and `workout.updated` events auto-save to Airtable Workouts table
  - Daily cycle data (strain, calories, recovery, sleep) auto-saved to WHOOP Data table
  - Backfilled 3 days of data (Feb 10-12) after token refresh
  - Server running at `whoop.samsclaw.org/webhook/whoop`
- **TAT System v3.1:** Fixes and UI improvements
  - Fixed validation script: changed from non-existent `Date` field to `Date Created`
  - Task Stats clickable: filter tasks by clicking stat boxes (Active, Due Today, Overdue, In Progress)
  - Tasks sorted by due date: overdue first, then ascending
  - 34 active tasks, 2 overdue, 1 due today
- **Airtable Habit Checker:** New script to replace Notion habit validation
  - `check_airtable_habits.py` - validates Daily Habits table completeness
  - Cron jobs updated to use Airtable instead of Notion
- **Data Integrity Fixes:**
  - Fixed 15 duplicate habit records for Feb 12 (merged and deleted duplicates)
  - Fixed hardcoded dates in 3 scripts: `habit_tracker_from_food.py`, `airtable_sync_v2.py`, `sync_to_airtable.py`
  - All scripts now use dynamic `get_today()` function

### Features
- **Mission Control Live Data Linking:** All dashboard pages connected to Airtable
  - **Health Page:** Live 7-day timeline (calories consumed/burned, strain, weight, sleep)
  - **Exercise Card:** Pulls from Workouts table with `Exercises` field display
  - **Date Selector:** Dropdown to view any of last 7 days' meals and macros
  - **Productivity Page:** TAT tasks with working filters, weekly habit tracker with streaks
  - **Habit Streaks:** Horizontal bar charts showing 30-day streaks for each habit
- **Habit Streak Visualization:** Added to Productivity page
  - 30-day horizontal bar charts below weekly habit tracker
  - Visual representation of consistency for each habit
- **Blog Page:** New Mission Control page
  - Blog Stats card (days published, research tasks, business plans, words written)
  - Grid layout of blog post cards with hover effects
  - Links to `samsclaw.org` blog
- **Exercise Data Integration:** Real workout data in Health & Nutrition page
  - 4 workouts last 7 days (Hard, Active Recovery types)
  - 120 total minutes displayed with 0 decimal places

### Data
- **WHOOP Backfill:** Retrieved 3 days of missing data
  - Feb 10: Strain 14.2, Recovery 84%, Sleep 78%, Calories 2,889
  - Feb 11: Strain 13.7, Recovery 46%, Sleep 60%, Calories 2,771
  - Feb 12: Strain 6.4, Recovery 54%, Sleep 65%, Calories 1,278
- **Feb 12 Nutrition Complete:** 6 meals logged, 1,963 calories, 108g protein
  - Breakfast: Multigrain bread + ham + café au lait (450 cal)
  - Lunch: Chicken avocado pesto tortilla + cappuccino (520 cal)
  - Dinner: Spaghetti bolognese (650 cal)
  - Snacks: Dates, banana, apple, protein powder
- **Feb 13 Nutrition Progress:** 940 calories by midday
  - Breakfast: 2 café au laits, sourdough, omelette, butter chicken, pita (730 cal)
  - Snack: Banana, 3 dates, green apple (210 cal)
- **Water Tracking:** 7/8 glasses (synced between Airtable and local)
  - Multiple duplicate records consolidated
- **Research Tasks Completed:**
  - Voice Technology Advances (11,656 words)
  - OpenClaw Security Development
  - Security Audit

### Health
- **Weight:** 102 kg logged (down from 104 kg earlier in week)
- **Water Intake:** 7/8 glasses (87.5% of goal)
- **Supplements:** Multivitamin ✅, Fruit habit ✅
- **Workouts:** 4 sessions last 7 days (Hard, Active Recovery)
- **WHOOP Status:** Token refreshed, webhook active, ready for workout auto-save

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
