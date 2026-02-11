# TAT System v2.0 - Architecture Specification

## Current State
- Database: "Sam's TAT Task System 🎮"
- Categories: 🔥 Today, ⚡ 3 Days, 📅 7 Days, 🗓️ 30 Days, 💻 Laptop Tasks
- Date Created: Exists as property
- Due Date: Manual or not calculated

## Target State

### 1. Category Simplification
**Current:** 5 categories with emoji prefixes
**New:** 4 numeric categories only
- `1` (was 🔥 Today)
- `3` (was ⚡ 3 Days)  
- `7` (was 📅 7 Days)
- `30` (was 🗓️ 30 Days)
- Remove: 💻 Laptop Tasks (handle via tags or separate DB)

### 2. Due Date Formula
**New Property:** `Due Date` (formula type)
```
prop("Date Created") + prop("Category")
```
Or in Notion formula syntax:
```
dateAdd(prop("Date Created"), prop("Category"), "days")
```

### 3. Priority Logic for Daily Brief
**Category 1 Tasks:** Always show
**Overdue Tasks:** Any task where Due Date < Today
**Priority Order:**
1. Category 1 (due today)
2. Overdue (any category)
3. Category 3 (due within 3 days)

## Implementation Steps

### Phase 1: Database Changes (Manual in Notion UI)
1. Open TAT database in Notion
2. Edit "Category" property:
   - Remove all existing options
   - Add: `1`, `3`, `7`, `30` (as select options)
3. Add new property "Due Date":
   - Type: Formula
   - Formula: `dateAdd(prop("Date Created"), toNumber(prop("Category")), "days")`
4. Update existing tasks to new category format
5. Delete 💻 Laptop Tasks category (or migrate to tags)

### Phase 2: System Updates

#### A. Morning Brief Script
**File:** `scripts/morning_brief.py`
**Changes:**
```python
# Query TAT tasks
# Filter: Category == "1" OR Due Date < Today
# Sort: Due Date ascending

def get_urgent_tat_tasks():
    """Get Category 1 + overdue tasks"""
    # Query Notion API
    # Filter by formula: Due Date <= today
    # Return list with name, category, days_overdue
```

#### B. Dashboard Generator
**File:** `scripts/generate_dashboard_v2.py`
**Changes:**
```python
def get_tat_tasks():
    """Get urgent tasks only (Category 1 + overdue)"""
    # Query TAT database
    # Filter: Category == "1" OR Due Date < today
    # Limit to top 5-7 tasks
```

#### C. Cron Reminders
**New Job:** 9pm "TAT Review"
- Check Category 1 tasks for tomorrow
- Alert if any overdue tasks

### Phase 3: Workflow Documentation
**Update:** `workflows/tat-system.md`
- New category definitions
- Due date calculation explanation
- How to use effectively

## Technical Requirements

### Notion API Query Example
```python
# Query Category 1 + overdue
filters = {
    "or": [
        {"property": "Category", "select": {"equals": "1"}},
        {"property": "Due Date", "formula": {"date": {"before": today}}}
    ]
}
```

### Formula Syntax Check
Notion formula for Due Date:
```
if(empty(prop("Date Created")), now(), dateAdd(prop("Date Created"), toNumber(prop("Category")), "days"))
```

## Migration Notes
- Existing tasks need category values updated (🔥 Today → 1)
- Due Date will auto-calculate for all tasks once formula is set
- Laptop Tasks category needs decision: delete or migrate to Tags

## Success Criteria
- [ ] Categories show as numbers only (1, 3, 7, 30)
- [ ] Due Date auto-calculates for all tasks
- [ ] Morning brief shows Category 1 + overdue only
- [ ] Dashboard TAT section shows urgent tasks only
- [ ] 9pm reminder alerts on overdue tasks
