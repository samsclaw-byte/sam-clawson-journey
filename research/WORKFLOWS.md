# OpenClaw Workflows Documentation

**Last Updated:** February 8, 2026  
**Status:** Active Systems

---

## 🎙️ Voice Transcription Workflow

**Trigger:** User sends voice note via Telegram
**Frequency:** On-demand

### Process:
1. Telegram receives .ogg voice file
2. File saved to `/home/samsclaw/.openclaw/media/inbound/`
3. Async processor queues file
4. Whisper Tiny model transcribes (local, offline)
5. Transcript saved to `/home/samsclaw/.openclaw/media/processed/`
6. I act on transcription content

**Speed:** 3-5 min for 3-min audio (CPU)  
**Future:** 10-20 sec with RTX 4070 GPU

**Scripts:**
- `/home/samsclaw/.openclaw/workspace/scripts/async-transcribe.sh`
- Local Whisper in conda environment

---

## ⏰ Cron Job Workflows

### Morning Briefing (6:00 AM)
**Purpose:** Day starter with overnight summary
**Includes:**
- Overnight task completion status
- Habit tracker status
- Token usage report
- TAT task priorities

### Midday Check (12:00 PM)
**Purpose:** Mid-day validation sync
**Process:**
1. Check conversation/memory for logged habits/food
2. Update Notion Habit Tracker
3. Read current Notion status
4. Check TAT tasks
5. Report with validation confirmation

### Afternoon Check (15:00 / 3:00 PM)
**Purpose:** High priority task reminder
**Focus:** Overdue and urgent TAT tasks

### Evening Check (20:00 / 8:00 PM)
**Purpose:** End-of-day review
**Includes:**
- Habit completion status
- TAT task progress
- Next day preview

**All Cron Jobs:**
- 14 total jobs
- Run via Linux crontab (bulletproof)
- Logs: `/tmp/cron-*.log`

---

## 🍽️ Food Logging Workflow

**Trigger:** User describes meal/photos
**Frequency:** Real-time

### Process (Current):
1. User sends meal description + photos
2. I estimate nutrition (calories, protein, etc.)
3. Update `health/weight-food-log.md`
4. Update Notion Habit Tracker (water, habits)
5. Calculate running daily totals

### Process (Future - Edamam API):
1. User sends meal description
2. Query Edamam Nutrition API
3. Get precise nutrition data
4. Update Notion Food Log database
5. Auto-calculate daily macros

**Files:**
- Log: `health/weight-food-log.md`
- Database: Notion "🍽️ Food & Nutrition Log"
- Guide: `EDAMAM_INTEGRATION_GUIDE.md`

---

## 💪 Habit Tracking Workflow

**Triggers:**
- User reports habit completion
- Cron job check-ins
- Food logging (auto-triggers water/food habits)

### Tracked Habits:
- ✅ Multivitamin
- ✅ Creatine (5g)
- ✅ Exercise (30+ min)
- ✅ Fruit (2 portions)
- ✅ Water (8 glasses)

### Process:
1. User reports habit OR cron detects from conversation
2. Update Notion Habit Tracker
3. Update streak counters
4. Log in daily summary

**Database:** Notion "Habit Tracker"

---

## 🔗 Notion Sync Workflow

**Frequency:** Real-time + Cron validation

### Sync Points:
1. **Habit Tracker** - Real-time updates when you report
2. **Food Log** - Manual logging now, API automation coming
3. **TAT Tasks** - Cron checks for overdue/upcoming
4. **Research Tasks** - Auto-updated by overnight jobs
5. **Build Tasks** - Auto-updated by overnight jobs

### Validation (New):
- Cron jobs read from conversation/memory
- Compare to Notion state
- Report discrepancies
- Confirm sync accuracy

---

## 🔍 Research Pipeline Workflow

**Triggers:** Midnight cron jobs (12am, 2am, 4am)

### Process:
1. Check Notion "Overnight Research Tasks" database
2. Find first pending task
3. Mark as "Running"
4. Conduct research (web search, APIs)
5. Save findings to `research/YYYY-MM-DD/`
6. Update Notion with completion + summary
7. Log to daily memory

**Recent Topics:**
- Gaming psychology for new parents
- Multi-agent systems on single PC
- Multi-agent life support system

---

## 🔨 Build Task Workflow

**Triggers:** 11pm, 1am, 3am, 5am cron jobs

### Process:
1. Check Notion "Overnight Build Tasks" database
2. Find first pending task
3. Mark as "Running"
4. Execute build (code, write, configure)
5. Update status to "Complete"
6. Log completion date
7. Report findings

**Recent Builds:**
- "How OpenClaw Works" article (13,000 words)
- Blog updates
- Research file organization

---

## 📊 Daily Summary Workflow

**Trigger:** Midnight (0:00)

### Process:
1. Review previous day's data
2. Compile habit completion
3. Calculate nutrition totals
4. List files created/modified
5. Summarize accomplishments
6. Generate markdown report
7. Save to `daily-summaries/YYYY-MM-DD-summary.md`
8. Push to GitHub

**Output:** Research repo + GitHub Pages

---

## 📝 Blog Update Workflow

**Trigger:** 5:30 AM daily

### Process:
1. Check blog folder for new content
2. Review current posts
3. Create new daily entry if needed
4. Update index.html navigation
5. Update README.md
6. Stage changes for GitHub Pages

**Status:** Ready to commit/push to GitHub Pages

---

## 🏋️ Exercise Logging Workflow

**Current:**
1. User reports workout
2. I log to health file
3. Update Notion (duration, type)
4. Note in daily summary

**Future (WHOOP API):**
1. WHOOP auto-detects workout
2. 11pm cron pulls WHOOP data
3. Auto-populates Notion with:
   - Workout type
   - Duration
   - HR zones (Z1/Z2/Z3/Z4/Z5)
   - Strain score
   - Calories

---

## 🚀 Coming Soon Workflows

### WHOOP API Integration
- Auto-sync workouts
- HR zone breakdown
- Recovery scores
- Sleep data

### Edamam Nutrition API
- Precise nutrition lookup
- Auto-calculate macros
- Photo-based food ID (future)

### Personal Trainer Agent
- Weekly workout planning
- Injury prevention monitoring
- Progress tracking
- Accountability check-ins

---

## 📁 All Workflow Files

| Workflow | Location |
|----------|----------|
| Voice Transcription | `scripts/async-transcribe.sh` |
| Cron Jobs | `crontab -l` (system) |
| Food Log | `health/weight-food-log.md` |
| Daily Summaries | `research/daily-summaries/` |
| Research Pipeline | `research/YYYY-MM-DD/` |
| Build Tasks | `blog/`, `scripts/`, config files |
| Workflows Doc | `research/WORKFLOWS.md` (this file) |

---

## 🔧 Maintenance

**Weekly (Friday afternoons):**
- Review cron logs: `tail /tmp/cron-*.log`
- Check Notion sync accuracy
- Update workflow documentation
- Clear old voice transcription files

**Monthly:**
- Archive old daily summaries
- Review and optimize cron jobs
- Update skill configurations
- Security audit

---

**Questions? Check individual workflow files or ask me!** 🦞
