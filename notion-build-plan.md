# Sam & Clawson - Daily Briefing Template

## Build Specifications for Notion

### Database Structure Needed:

1. **Daily Briefings Database**
   - Date (date property)
   - Status (select: Draft/Ready/Delivered)
   - Yesterday Summary (rich text)
   - Today Focus (rich text)
   - Calendar Events (rich text)
   - Habit Status (rich text)
   - System Health (rich text)
   - Blog Notes (rich text)

2. **To-Do Database**
   - Task (title)
   - Status (select: Todo/In Progress/Done)
   - Priority (select: High/Medium/Low)
   - Category (select: Work/Personal/Family/Health)
   - Created Date (date)
   - Completed Date (date)
   - Achievement Badge (select)
   - Points (number)

3. **Habits Database**
   - Habit (title)
   - Date (date)
   - Completed (checkbox)
   - Streak Count (number)
   - Notes (rich text)

4. **Achievements Database**
   - Achievement Name (title)
   - Badge Icon (rich text)
   - Description (rich text)
   - Criteria (rich text)
   - Date Earned (date)
   - Status (select: Available/Earned)

### Gaming Elements (Phase 1):
- 🔥 Streak badges (3-day, 7-day, 30-day)
- 🎯 Achievement badges for completing tasks
- 📊 Progress visualization
- 🏆 Challenge tracking

### Daily Briefing Content Structure:
1. Good morning message with date
2. Yesterday's accomplishments
3. Habit streak status
4. Today's calendar events
5. Focus areas for today
6. System health report
7. Motivational closing

### Integration Points:
- Google Calendar API (research needed)
- Activity log from our private files
- Blog content generation
- Token usage monitoring

**Status**: Ready to build tonight
**First Briefing**: Tomorrow morning (Feb 3, 2026)