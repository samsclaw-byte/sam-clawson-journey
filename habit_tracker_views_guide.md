
# 🎮 Habit Tracker Visual Views Setup Guide

## ⚠️ Important Note About Notion API
The Notion API **does not support creating database views programmatically**. 
Views must be created manually in the Notion web/app interface.

However, I've created a **Visual Dashboard Page** with links and instructions!

---

## 📋 Views to Create (Step-by-Step)

### 1️⃣ Calendar View
**Purpose:** See habits by date with color coding

**Setup:**
1. Open your Habit Tracker database
2. Click the `+` next to existing view tabs
3. Select **"Calendar"**
4. Set "Date" as the calendar property
5. Name it "📅 Calendar View"

**Color Coding Setup:**
- Click the view settings (•••)
- Go to "Layout" → "Color"
- Create rules:
  - 🟢 Green: When "Fruit" is checked AND "Exercise" is checked
  - 🟡 Yellow: When 1-2 habits completed
  - 🔴 Red: When 0 habits completed

---

### 2️⃣ Board View (Kanban Style)
**Purpose:** Group by date showing habit completion status

**Setup:**
1. Click `+` to add new view
2. Select **"Board"**
3. Group by: "Date" 
4. Name it "📋 Board View"
5. Card preview: Show all habit checkboxes

**Customize Cards:**
- Show: Fruit, Multivitamin, Exercise, Water
- Show streak numbers

---

### 3️⃣ Gallery View
**Purpose:** Card-based view showing daily habit summaries with visual progress

**Setup:**
1. Click `+` to add new view
2. Select **"Gallery"**
3. Name it "🖼️ Gallery View"
4. Card size: Large
5. Card preview: Show Date as title

**Properties to Show:**
- ✅ Fruit (with streak)
- 💊 Multivitamin (with streak)
- 🏃 Exercise (with streak)
- 💧 Water (with streak)

---

### 4️⃣ Week View
**Purpose:** Show last 7 days at a glance

**Setup:**
1. Click `+` to add new view
2. Select **"Table"** (or Timeline)
3. Name it "📊 Week View"
4. Add Filter: "Date" is within "past week"
5. Sort by: "Date" descending

**Alternative - Timeline View:**
1. Select **"Timeline"** instead of Table
2. Date property: "Date"
3. Shows 7-day rolling window

---

## 🎨 Recommended View Configuration Summary

| View Type | Name | Group/Filter By | Properties Visible |
|-----------|------|-----------------|-------------------|
| Calendar | 📅 Calendar View | Date | All habits |
| Board | 📋 Board View | Date | Habits + Streaks |
| Gallery | 🖼️ Gallery View | None (cards) | All + Streak counts |
| Table | 📊 Week View | Date (past week) | All habits |

---

## 🚀 Quick Start

1. **Go to the Visual Dashboard page** I created in your Notion workspace
2. **Click the Habit Tracker database link**
3. **Follow the instructions** above to create each view
4. **Switch between views** using the tabs at the top

---

## 💡 Pro Tips

1. **Create a 'Master Dashboard'** page linking to all views
2. **Use filters** to create specialized views:
   - "This Month" - Current month's habits
   - "High Streaks" - Days with 3+ habits completed
   - "Needs Attention" - Days with 0-1 habits

3. **Add formulas** for visual indicators:
   ```
   Completion Rate: (fruit + multi + exercise + water) / 4 * 100
   ```

4. **Mobile setup:** Favorite your dashboard for quick mobile access

---

## 🔗 Database Information

- **Database ID:** `2fdf2cb12276818f8845ed296b42d781`
- **Parent Page:** `2fcf2cb1-2276-8021-a8a9-ce059efecbf6`
- **Visual Dashboard:** Created and linked!

Happy habit tracking! 🦞✨
