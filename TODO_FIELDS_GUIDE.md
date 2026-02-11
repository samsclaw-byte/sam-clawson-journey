# 🎮 Sam's TAT Task System - Notion Fields Guide

## 📋 Core Task Database Fields

### 🎯 Essential Fields (Required for Every Task)

**1. Task Name** (Title)
- Clear, actionable description
- Example: "Finish Q1 budget analysis" not "Budget stuff"

**2. TAT Category** (Select - Single Select)
- 🔴 **Today** (Must complete today)
- 🟠 **3-Day** (Complete within 3 days)  
- 🟡 **7-Day** (Complete within 7 days)
- 🟢 **Low** (No specific deadline)

**3. Status** (Select - Single Select)
- 🆕 **Not Started**
- 🔄 **In Progress**
- ⏸️ **On Hold**
- ✅ **Complete**
- ❌ **Cancelled**

**4. Priority** (Select - Single Select)
- 🔥 **Critical** (Baby/family emergency)
- ⚡ **High** (Important for goals)
- 📋 **Medium** (Standard importance)
- 💤 **Low** (Nice to have)

### 🎮 Gaming Fields (Auto-calculated)

**5. Base XP** (Number)
- Pre-set values based on TAT:
  - Today: 30 XP
  - 3-Day: 20 XP  
  - 7-Day: 15 XP
  - Low: 10 XP

**6. XP Multiplier** (Formula)
```
if(prop("TAT Category") == "🔴 Today", 3,
if(prop("TAT Category") == "🟠 3-Day", 2,
if(prop("TAT Category") == "🟡 7-Day", 1.5,
if(prop("TAT Category") == "🟢 Low", 1, 1))))
```

**7. Total XP** (Formula)
```
prop("Base XP") * prop("XP Multiplier")
```

**8. Created Date** (Created Time)
- Auto-populated when you create task

**9. Due Date** (Date)
- Calculated from TAT category:
  - Today: Today
  - 3-Day: Today + 3 days
  - 7-Day: Today + 7 days
  - Low: Leave blank

### 📊 Progress Tracking Fields

**10. Progress %** (Number - 0-100)
- Update as you work on task
- Visual progress bar in Notion

**11. Time Estimated** (Number)
- Minutes you think it'll take
- Helps with planning and XP calculation

**12. Time Actual** (Number)
- Minutes it actually took
- For future planning accuracy

**13. Category** (Select - Single Select)
- 💼 **Work** (FP&A, professional)
- 👨‍👩‍👧‍👦 **Family** (Sophie, Noah, Theo)
- 🏠 **Home** (Household, chores)
- 📚 **Personal** (Learning, growth)
- 🎨 **Creative** (Blog, content, ideas)
- 🏃 **Health** (Exercise, wellness)

### 🏆 Achievement Fields

**14. Streak Bonus** (Formula)
```
if(prop("Status") == "✅ Complete" and prop("Completed Early"), prop("Total XP") * 0.5, 0)
```

**15. Completed Early** (Checkbox)
- Check if finished before due date
- Triggers bonus XP

**16. Completion Date** (Date)
- When you actually finished it

### 📝 Optional Fields (Use When Helpful)

**17. Description** (Rich Text)
- More details about the task
- Links, references, context

**18. Next Action** (Rich Text)
- Immediate next step
- Keeps momentum going

**19. Blockers** (Rich Text)
- What's stopping progress?
- Helps identify patterns

**20. Energy Required** (Select)
- 🔋 **High Energy** (Creative work, complex analysis)
- ⚡ **Medium Energy** (Standard tasks, meetings)
- 😴 **Low Energy** (Emails, admin, organizing)

**21. Family Impact** (Select)
- 👶 **Baby Related** (Theo/Noah immediate needs)
- 👩 **Sophie Support** (Helping your wife)
- 🏠 **Household** (Family environment)
- 🤝 **Quality Time** (Direct family interaction)

## 🎯 Quick Entry Template

**For fast task creation, use this format:**

```
Task Name: [Specific action]
TAT Category: [Pick one]
Priority: [Assess urgency]
Time Estimated: [Best guess in minutes]
Category: [Work/Family/Home/etc]
Energy Required: [High/Medium/Low]
```

## 🚀 Example Tasks for Today:

**🔴 Today (High Priority):**
- "Finish voice transcription blog section" (90 min, Work, High Energy)
- "Send update to project team" (15 min, Work, Low Energy)

**🟠 3-Day (Medium Priority):**
- "Review Q1 budget preliminary data" (2 hours, Work, High Energy)
- "Plan weekend family activity" (30 min, Family, Medium Energy)

**🟡 7-Day (Standard Priority):**
- "Research new productivity app features" (45 min, Personal, Medium Energy)
- "Organize baby photos from this week" (20 min, Family, Low Energy)

**🟢 Low (When Time Permits):**
- "Read article about gaming psychology" (25 min, Personal, Medium Energy)
- "Update family calendar for next month" (15 min, Family, Low Energy)

## 📱 Daily Use Flow:

**Morning (2 min):**
1. Open Tasks database
2. Filter by "Not Started" + "Today"
3. Pick 1-3 tasks max
4. Update progress as you work

**Throughout Day:**
1. Mark tasks "In Progress" when starting
2. Update "Progress %" as you work
3. Mark "Complete" when done (get XP!)

**Evening (1 min):**
1. Review what you completed
2. Add new tasks for tomorrow
3. Check your XP earnings

**Ready to start task gaming?** 🎮✨

*This system will make your to-do list feel like a strategic RPG!*