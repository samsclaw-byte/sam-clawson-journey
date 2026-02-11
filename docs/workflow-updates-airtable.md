# Workflow Updates - Airtable Migration Complete

## Overview
All data migrated from Notion to Airtable. Workflows need updating to use Airtable API.

## Airtable Bases

### 1. Health & Nutrition Base
**ID:** `appnVeGSjwJgG2snS`
**Tables:**
- Food Log (13 meals, 24 nutrition fields)
- Weight Tracker (3 entries)
- Workouts (8 workouts, 8 + 6 HR zone fields)
- WHOOP Data (10 days)

### 2. Productivity Base
**ID:** `appvUbV8IeGhxmcPn`
**Tables:**
- Daily Habits (4 days)
- TAT Tasks v2 (46 tasks with due dates)

---

## Scripts to Update

### 1. Morning Brief Generator
**File:** `scripts/generate_morning_brief.py`

**Current:** Queries Notion databases
**Update to:** Query Airtable

**Changes needed:**
```python
# OLD - Notion
notion_client.query_database("habits_db_id")

# NEW - Airtable
airtable.get_records("Daily Habits", filter={"Date": today})
airtable.get_records("TAT Tasks", filter={"Category": "1"})
```

### 2. Mission Control Dashboard
**File:** `scripts/generate_mission_control.py`

**Current:** Pulls from Notion
**Update to:** Pull from Airtable

**Changes:**
- Food Log → Airtable Food Log
- Weight → Airtable Weight Tracker
- Workouts → Airtable Workouts
- Habits → Airtable Daily Habits
- WHOOP → Airtable WHOOP Data

### 3. TAT Task Adder
**File:** `scripts/add_tat_task.py`

**Current:** Adds to Notion
**Update to:** Add to Airtable TAT Tasks v2

**Changes:**
```python
# Calculate due date: Date Created + TAT Category Days
from datetime import datetime, timedelta
due_date = datetime.now() + timedelta(days=category_days)

airtable.create_record("TAT Tasks v2", {
    "Task Name": task_name,
    "TAT Category Days": category,
    "Date Created": datetime.now().isoformat(),
    "Due Date": due_date.isoformat(),
    "Status": "Not Started"
})
```

### 4. Habit Tracker
**File:** `scripts/track_habits.py` (or water_tracker.py)

**Current:** Updates Notion + local JSON
**Update to:** Update Airtable Daily Habits

### 5. Weight Tracker
**File:** `scripts/weight_tracker.py`

**Current:** Adds to Notion
**Update to:** Add to Airtable Weight Tracker

### 6. WHOOP Webhook Handler
**File:** `skills/whoop-integration/scripts/webhook_server_v2.py`

**Current:** Saves to local files
**Update to:** Also save to Airtable WHOOP Data table

---

## New Airtable API Helper

Create: `scripts/airtable_client.py`

```python
import os
import requests

AIRTABLE_KEY = os.getenv('AIRTABLE_API_KEY')

class AirtableClient:
    def __init__(self, base_id):
        self.base_id = base_id
        self.headers = {
            "Authorization": f"Bearer {AIRTABLE_KEY}",
            "Content-Type": "application/json"
        }
    
    def get_records(self, table_name, filter_formula=None):
        url = f"https://api.airtable.com/v0/{self.base_id}/{table_name}"
        params = {}
        if filter_formula:
            params["filterByFormula"] = filter_formula
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json().get('records', [])
    
    def create_record(self, table_name, fields):
        url = f"https://api.airtable.com/v0/{self.base_id}/{table_name}"
        response = requests.post(url, headers=self.headers, json={"fields": fields})
        return response.json()
    
    def update_record(self, table_name, record_id, fields):
        url = f"https://api.airtable.com/v0/{self.base_id}/{table_name}/{record_id}"
        response = requests.patch(url, headers=self.headers, json={"fields": fields})
        return response.json()
```

---

## Webhook Status

### Temporary (Working Now):
`https://newcastle-olympics-act-municipality.trycloudflare.com/webhook/whoop`

### Permanent (DNS Propagating):
`https://whoop.samsclaw.org/webhook/whoop`

**Action:** Update WHOOP dashboard with temporary URL. Switch to permanent once DNS resolves.

---

## Next Steps

1. ✅ Update WHOOP dashboard with working webhook URL
2. ⏳ Update all scripts to use Airtable API
3. ⏳ Test each workflow
4. ⏳ Update cron jobs to use new scripts
5. ⏳ Verify Mission Control pulls from Airtable

## Migration Complete: 90+ records ✅
- Health & Nutrition: 34 records
- Productivity: 50+ records
