# Overnight Data Validation System

## Overview
Automated data integrity checks for Airtable tables, running at 2:00 AM daily.

## Schedule
- **2:00 AM** - Run validations on previous day's data
- **Morning** - Send summary report via Telegram

## Validations Performed

### 1. Food Log Table
**Required Fields Check:**
- ✅ Date present and valid
- ✅ Meal Type (Breakfast/Lunch/Dinner/Snack)
- ✅ Food Items not empty
- ✅ Calories is positive number

**Data Quality Checks:**
- ✅ No exact duplicates (same date/meal/food)
- ✅ No orphaned records (missing date)
- ✅ Edamam Data flag consistency
  - If True → should have all 24 nutrients
  - If False → at least Calories present
- ✅ Auto-fix: Set Edamam Data = True if protein data exists
- ✅ Nutrition totals reasonable (500-5000 cal/day)

### 2. Daily Habits Table
**Record Integrity:**
- ✅ One record per date (no duplicates)
- ✅ Water field: numeric 0-20
- ✅ Boolean fields are actual booleans

**Cross-Table Validation:**
- ✅ Multivitamin in Food Log → checked in Habits
- ✅ Fruit in Food Log → checked in Habits

### 3. TAT Tasks Table
**Required Fields:**
- ✅ Task Name not empty
- ✅ Category valid (1, 3, 7, 30)
- ✅ Status valid (Not Started/In Progress/Blocked/Complete/Cancelled)

**Formula Validation:**
- ✅ Due Date = Date Created + Category days
- ✅ Days Remaining calculation correct

**Status Checks:**
- ⚠️ Overdue tasks without Complete/Cancelled status

## Report Format

**Morning Summary includes:**
- Overall PASS/FAIL status
- Total issues found
- Warnings count
- Auto-fixes applied
- Detailed issues per table (top 5)

## Example Output

```
✅ Overnight Data Validation - 2026-02-12

Overall Status: All validations passed!

Summary:
• Records checked: Food Log, Daily Habits, TAT Tasks
• Issues found: 0
• Warnings: 1
• Auto-fixed: 2

🎉 All data integrity checks passed!
```

## Manual Run

```bash
# Run validation for yesterday
python3 overnight_data_validation.py

# Run validation for specific date
python3 overnight_data_validation.py --date 2026-02-12

# View report without running
python3 overnight_data_validation.py --report-only
```
