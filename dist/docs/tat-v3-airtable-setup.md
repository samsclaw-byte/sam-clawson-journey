# TAT Table v3 - Airtable Setup Steps

## Base: Productivity
## Table: TAT Tasks v2 (or create TAT Tasks v3)

---

## STEP 1: Update/Create Fields

### Field 1: Task Name
- Type: Single line text
- Required: YES (make required in field settings)

### Field 2: Category  
- Type: Single select
- Options: "1", "3", "7", "30" (exactly these values)
- Required: YES
- Color coding:
  - "1" = Red
  - "3" = Orange
  - "7" = Yellow
  - "30" = Green

### Field 3: TAT Days (FORMULA)
- Type: Formula
- Formula: `VALUE({Category})`
- Format: Integer

### Field 4: Date Created
- Type: Created time
- Format: Date & time
- Time zone: Your local timezone

### Field 5: Due Date (FORMULA)
- Type: Formula
- Formula: `DATEADD({Date Created}, {TAT Days}, 'days')`
- Format: Date
- Time zone: Your local timezone

### Field 6: Status
- Type: Single select
- Options:
  - "Not Started" (Gray)
  - "In Progress" (Blue)
  - "Blocked" (Red)
  - "Complete" (Green)
  - "Cancelled" (Light gray)
- Required: YES

### Field 7: Priority
- Type: Single select
- Options:
  - "Critical" (Red)
  - "High" (Orange)
  - "Medium" (Yellow)
  - "Low" (Green)

### Field 8: Days Remaining (FORMULA)
- Type: Formula
- Formula: `IF({Due Date}, DATETIME_DIFF({Due Date}, TODAY(), 'days'), '')`
- Format: Integer

### Field 9: Urgency Level (FORMULA)
- Type: Formula
- Formula:
```
IF({Days Remaining} < 0, '🔴 Overdue',
  IF({Days Remaining} <= 1, '🟠 Urgent',
    IF({Days Remaining} <= 3, '🟡 Soon',
      '🟢 Normal')))
```

### Field 10: Notes
- Type: Long text

### Field 11: Tags
- Type: Multiple select
- Options: Work, Personal, Health, Finance, Admin

### Field 12: Completed Date
- Type: Date
- Format: Date

### Field 13: Days to Complete (FORMULA)
- Type: Formula
- Formula: `IF(AND({Date Created}, {Completed Date}), DATETIME_DIFF({Completed Date}, {Date Created}, 'days'), '')`
- Format: Integer

---

## STEP 2: Set Up Automations (Optional but recommended)

### Automation 1: Set Completed Date
- Trigger: When record matches conditions
- Condition: Status = "Complete" AND Completed Date is empty
- Action: Update record
- Field to update: Completed Date = Current date/time

### Automation 2: New Task Notification
- Trigger: When record created
- Action: Send email or webhook
- Can connect to Telegram if webhook configured

---

## STEP 3: Test the Formula

Create a test task:
1. Task Name: "Test task for v3"
2. Category: "3"
3. Status: "Not Started"

Expected results:
- TAT Days: 3
- Due Date: Today + 3 days
- Days Remaining: 3
- Urgency Level: 🟡 Soon

---

## STEP 4: Update API Integration

Your scripts are already updated to use v3:
- `tat_client_v3.py` - New API client
- `add_tat_task_v3.py` - Task creation with formulas
- `tat_reminders.py` - Daily reminders

The API will now:
- Only send: Task Name, Category, Status, Priority, Notes
- Due Date is auto-calculated (don't send it!)
- Date Created is auto-set by Airtable

---

## Migration from v2 to v3

If you have existing v2 data:

1. Keep existing fields: Task Name, Category, Status, Notes
2. Add new fields: TAT Days (formula), Due Date (formula), Days Remaining (formula), Urgency Level (formula)
3. Convert old Due Date to Completed Date for finished tasks
4. Delete old manual Due Date field (or keep as backup)
5. Test with a new task

---

## Quick Test

After setup, run:
```bash
python3 ~/.openclaw/workspace/scripts/add_tat_task_v3.py "Test v3 task" 3
```

You should see:
✅ TAT Task created: Test v3 task
   Category: 3 Days
   Due Date: (auto-calculated: Date Created + 3 days)
