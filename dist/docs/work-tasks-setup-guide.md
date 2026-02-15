# Work Tasks Table Setup Guide

## Manual Setup Steps

### Step 1: Create the Table
1. Open your Work base: https://airtable.com/appuWxergK3HUJd8i
2. Click "+ Add or Import" (bottom left)
3. Choose "Create a new table"
4. Name it: **Work Tasks**

### Step 2: Add Fields

| Field Name | Type | Configuration |
|------------|------|---------------|
| **Task Name** | Single line text | Required field ✅ |
| **Detail** | Long text | - |
| **TAT Category** | Single select | Options: 1, 3, 7, 30 (colors: red, orange, yellow, green) |
| **Date Created** | Created time | Auto-set by Airtable |
| **Due Date** | Formula | Formula: `DATEADD({Date Created}, VALUE({TAT Category}), 'days')` |
| **Source** | Single select | Options: Email, In Person, Call, Slack, Teams |
| **Type** | Single select | Options: Project, Task, Admin |
| **Project Name** | Single line text | - |
| **Stakeholder** | Single line text | - |
| **Assigned To** | Single line text | Default: Sam |
| **Status** | Single select | Options: Not Started, In Progress, Blocked, Complete, Cancelled |
| **Days Remaining** | Formula | Formula: `DATETIME_DIFF({Due Date}, TODAY(), 'days')` |
| **Urgency** | Formula | Formula: `IF({Days Remaining}<0,"🔴 Overdue",IF({Days Remaining}<=1,"🟠 Urgent",IF({Days Remaining}<=3,"🟡 Soon","🟢 Normal")))` |

### Step 3: Make Fields Required
1. Click field name → "Customize field type"
2. Toggle ON "Require field to be filled in" for:
   - Task Name
   - TAT Category
   - Status

### Step 4: Add Example Records

**Record 1:**
- Task Name: MGC fees for digital card
- Detail: Create unit comparison DGC vs Physical, Scenario table assuming avg card load, variable price scenario table and incrementality assuming 2025 volumes
- TAT Category: 3
- Source: In Person
- Type: Project
- Project Name: Digital Card
- Stakeholder: Aylin
- Assigned To: Sam
- Status: In Progress

**Record 2:**
- Task Name: Share card campaign invoicing
- TAT Category: 3
- Source: Email
- Type: Task
- Stakeholder: (blank)
- Assigned To: Sam
- Status: In Progress

**Record 3:**
- Task Name: Complete my success tasks
- TAT Category: 3
- Source: Email
- Type: Task
- Stakeholder: Colin
- Assigned To: Sam
- Status: Not Started

**Record 4:**
- Task Name: No objection certificate
- TAT Category: 7
- Source: Email
- Type: Task
- Stakeholder: (blank)
- Assigned To: Sam
- Status: Not Started

### Step 5: Create Views

**View 1: 🔴 Overdue**
- Filter: Days Remaining < 0, Status ≠ Complete
- Sort: Due Date (oldest first)

**View 2: 🟠 Due This Week**
- Filter: Days Remaining ≤ 7, Days Remaining ≥ 0
- Group by: Status

**View 3: 📧 By Source**
- Group by: Source

**View 4: 📋 By Project**
- Group by: Project Name

**View 5: ✅ Completed**
- Filter: Status = Complete
- Sort: Date Created (newest first)

## API Integration

Once the table is set up, I can create a script to add tasks via API:
- `add_work_task.py "Task name" --category 3 --source Email --type Task`

Want me to create the API script now?
