# Personal Mission Control Dashboard - Specification
**Date:** 2026-02-11  
**Purpose:** Personal workflow optimization tool  
**Owner:** Sam Clawson

---

## Overview

A unified, interactive HTML dashboard that serves as a "Mission Control" for all work and personal productivity streams. Think NASA mission control meets personal productivity — everything visible, prioritized, and actionable in one interface.

---

## Core Philosophy

**Not a business to sell — a tool for ME.**

- Optimized for MY specific workflow
- Context-aware (Steve, Rafi as line managers)
- Integrates with existing tools (Notion, Email, etc.)
- Evolves as my needs change

---

## Dashboard Structure

### 🎯 Main View (Summary)
```
┌─────────────────────────────────────────────────────────────┐
│  🎯 SAM'S MISSION CONTROL                     [Work] [Pers] │
├─────────────────────────────────────────────────────────────┤
│  🔥 URGENT NOW          📊 TODAY'S STATUS                   │
│  • Task from Steve      Work: 3 urgent, 5 total             │
│  • Project deadline     Personal: 2 laptop, 1 health        │
│  • Health check                                          │
├─────────────────────────────────────────────────────────────┤
│  💼 WORK                🏠 PERSONAL                        │
│  ├─ Steve Requests      ├─ Laptop Tasks                   │
│  ├─ Rafi Requests       ├─ AI Development                 │
│  ├─ Project Progress    ├─ Health & Fitness               │
│  └─ General Tasks                                        │
└─────────────────────────────────────────────────────────────┘
```

### 💼 Work Section (Drill-down)

#### 1. Steve Requests (Line Manager 1)
- Direct tasks/asks from Steve
- Meeting follow-ups
- Priority items
- Response tracking

#### 2. Rafi Requests (Line Manager 2)
- Direct tasks/asks from Rafi
- Meeting follow-ups
- Priority items
- Response tracking

#### 3. Project Progress
- Active projects with Gantt timelines
- Milestone tracking
- Dependencies
- Blockers/risks
- Completion percentages

#### 4. General Work Tasks
- Other work items
- Administrative tasks
- Learning/development
- Meeting prep

### 🏠 Personal Section (Drill-down)

#### 1. Laptop Tasks
- GitHub commits needed
- Code reviews
- System updates
- Automation improvements

#### 2. AI Development Tasks
- OpenClaw improvements
- Skill development
- Agent configurations
- Testing/validation

#### 3. Health & Fitness
- WHOOP recovery status
- Workout schedule
- Nutrition tracking
- Habit streaks
- Sleep performance

---

## Technical Architecture

### Frontend
- **Framework:** Pure HTML + CSS + vanilla JavaScript
- **Styling:** Mobile-first, responsive design
- **Charts:** Chart.js or D3.js for Gantt/timelines
- **Icons:** Emoji or Feather icons

### Data Sources
| Section | Source | Integration |
|---------|--------|-------------|
| Work Tasks | Notion TAT Database | API query |
| Steve/Rafi Items | Notion (tagged) | Filtered query |
| Projects | Notion Projects DB | API + Gantt render |
| Health | WHOOP API | Webhook data |
| Laptop Tasks | GitHub Issues | API |
| AI Dev | Notion + GitHub | Combined view |

### Backend (Optional)
- Static HTML generation via Python script
- Runs every 15 minutes via cron
- No server needed — just files

---

## Key Features

### 1. Clickable Drill-Down
- Click "Work" → Expand to show Steve/Rafi/Projects/General
- Click "Personal" → Expand to show sub-streams
- Click any project → Show Gantt chart
- Breadcrumb navigation

### 2. Smart Prioritization
- 🔥 Urgent (Today/overdue)
- ⚡ Soon (This week)
- 📅 Later (Future)
- ✅ Done (Completed today)

### 3. Context Integration
- Hover over Steve task → Show last email from Steve
- Click Rafi request → Open related Notion page
- Project card → Show recent commits/files

### 4. Workflow Feeds
- Email workflow status
- Calendar integration (next meetings)
- GitHub activity stream
- WHOOP recovery score

---

## Data Flow

```
Notion TAT DB ──┐
Notion Projects  ├─ Python Script ── HTML Dashboard ── GitHub Pages
GitHub Issues   ──┤   (15 min cron)
WHOOP Webhook   ──┘
```

---

## Success Metrics (Personal)

- [ ] All tasks visible in one place
- [ ] No "surprise" urgent items
- [ ] Clear project progress visibility
- [ ] Reduced context switching
- [ ] Faster daily planning

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Basic HTML structure
- [ ] Work vs Personal toggle
- [ ] Notion TAT integration
- [ ] Static generation script

### Phase 2: Work Deep-dive (Week 2)
- [ ] Steve/Rafi sections
- [ ] Project Gantt charts
- [ ] Email workflow integration
- [ ] Priority sorting

### Phase 3: Personal Streams (Week 3)
- [ ] Laptop tasks (GitHub)
- [ ] AI dev tracking
- [ ] Health dashboard (WHOOP)
- [ ] Habit streaks

### Phase 4: Intelligence (Week 4)
- [ ] Smart alerts
- [ ] Context on hover
- [ ] Workflow integration
- [ ] Mobile optimization

---

## Files

- `mission-control/index.html` - Main dashboard
- `mission-control/work.html` - Work detail view
- `mission-control/personal.html` - Personal detail view
- `scripts/generate_mission_control.py` - Data aggregation
- `scripts/mission_control/` - Component generators

---

## Notes

- **Not for sale** — this is MY tool
- **Evolution over perfection** — start simple, add features as needed
- **Context is king** — optimize for MY specific workflow
- **Integrate, don't replace** — enhance existing tools, don't rebuild

---

*Evolved from "Work Workflow Control Centre" business plan*  
*Voice note transcription: 2026-02-11*
