# Notion API Fix - 2026-02-11

## Problem
API version 2025-09-03 has bugs where database properties don't save properly.

## Solution  
Use API version 2022-06-28 - works perfectly.

## Updated Databases

### 🍽️ Food & Nutrition Log
- ID: dc76e804-5b9e-406b-afda-d7a20dd58976
- URL: https://www.notion.so/dc76e8045b9e406bafdad7a20dd58976
- Properties: Name, Meal, Date, Calories, Protein, Carbs, Fat, etc.
- ✅ 14 meals backfilled (Feb 8-11)

### ⚖️ Weight Tracker  
- ID: f9583de8-69e9-40e6-ab15-c530277ec474
- URL: https://www.notion.so/f9583de869e940e6ab15c530277ec474
- Properties: Name, Date, Weight (kg), Weight (lbs), Change (kg), Notes
- ✅ 3 weight entries backfilled (Feb 8, 9, 11)

### 💼 Work Tasks & Projects
- ID: 304f2cb1-2276-8156-b477-cf3ba96a68e0
- URL: https://www.notion.so/304f2cb122768156b477cf3ba96a68e0
- ✅ 7 work tasks added with icons

### 🎮 TAT Task System
- ID: 2fcf2cb1-2276-81d6-aebe-f388bdb09b8e
- Existing database

## Scripts to Update
All scripts using Notion API should use:
```python
NOTION_VERSION = "2022-06-28"
```

Not 2025-09-03!
