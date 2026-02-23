# D1 Migration Plan — Airtable to Cloudflare D1

**Created:** February 22, 2026
**Status:** Planning

---

## Why D1?

| Problem with Airtable | D1 Solution |
|----------------------|-------------|
| API rate limits (500 errors) | Direct SQL queries |
| Quota limits | Unlimited (SQLite) |
| Latency (~200-500ms) | ~10-50ms |
| Dependency on external service | You control everything |

---

## Current Airtable Usage

### Tables Currently Used
1. **TAT Tasks** — Task tracking with categories (1/3/7/30 days)
2. **Habits** — Daily habit completion
3. **Nutrition** — Meal logs
4. **Exercise** — Workout data
5. **Water** — (Already migrated to JSON)

### Files to Replace (~18 files)

| Category | Files | Priority |
|----------|-------|----------|
| TAT System | `add_tat_task.py`, `add_tat_task_v3.py`, `tat-worker-ready.js`, `airtable_client.py` | P0 |
| Data Fetchers | `fetch_*.py` (8 files) | P1 |
| Habits | `check_airtable_habits.py` | P1 |
| Sync | `airtable_sync_v2.py` | P2 |
| WHOOP | Webhook writer | P2 |

---

## Phase 1: D1 Schema Design ✅ DONE

### Database Info
- **Name:** trak-db
- **ID:** 860ddc67-3889-4d8e-8c23-a0d7e46bd589
- **Region:** APAC (Singapore)
- **Size:** 86 KB

### Tables Created
- `tat_tasks` — Task tracking
- `habits` — Daily habits
- `nutrition` — Meal logs
- `exercise` — Workouts
- `whoop_data` — WHOOP metrics

```sql
CREATE TABLE tat_tasks (
  id TEXT PRIMARY KEY,
  task_name TEXT NOT NULL,
  category INTEGER NOT NULL, -- 1, 3, 7, or 30
  status TEXT DEFAULT 'Not Started',
  priority TEXT DEFAULT 'Medium',
  date_created TEXT,
  due_date TEXT,
  date_completed TEXT,
  notes TEXT
);
```

### Habits Table

```sql
CREATE TABLE habits (
  id TEXT PRIMARY KEY,
  habit_name TEXT NOT NULL,
  date TEXT NOT NULL,
  completed INTEGER DEFAULT 0,
  notes TEXT,
  UNIQUE(habit_name, date)
);
```

### Nutrition Table

```sql
CREATE TABLE nutrition (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  meal_type TEXT, -- breakfast, lunch, dinner, snack
  description TEXT,
  calories INTEGER,
  protein REAL,
  carbs REAL,
  fat REAL,
  source TEXT -- 'manual', 'edamam'
);
```

### Exercise Table

```sql
CREATE TABLE exercise (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  workout_type TEXT,
  duration_minutes INTEGER,
  strain REAL,
  notes TEXT
);
```

---

## Phase 2: Worker Endpoints

Create Cloudflare Workers to replace script functionality:

| Endpoint | Method | Replaces |
|----------|--------|----------|
| `/api/tasks` | GET/POST/PUT/DELETE | `add_tat_task.py` |
| `/api/habits` | GET/POST | `check_airtable_habits.py` |
| `/api/nutrition` | GET/POST | `fetch_daily_nutrition.py` |
| `/api/exercise` | GET/POST | `fetch_exercise_data.py` |

---

## Phase 3: Migration Steps

### Step 1: Create D1 Database
```bash
wrangler d1 create trak-db
```

### Step 2: Apply Schema
```bash
wrangler d1 execute trak-db --file=schema.sql
```

### Step 3: Create Workers
- Write 4 workers (tasks, habits, nutrition, exercise)
- Deploy to Cloudflare

### Step 4: Update Scripts
- Replace Airtable API calls with Worker fetch calls
- Or bypass workers and query D1 directly via wrangler

### Step 5: Migrate Existing Data
- Export from Airtable
- Import to D1

### Step 6: Test & Switch
- Run parallel for 24h
- Cut over

---

## Effort Estimate

| Phase | Effort | Time |
|-------|--------|------|
| Schema Design | Low | 1 hr |
| Worker Development | Medium | 4-6 hrs |
| Script Updates | Medium | 3-4 hrs |
| Data Migration | Low | 1 hr |
| Testing | Medium | 2 hrs |
| **Total** | **Medium** | **~12-15 hrs** |

---

## Priority Order

1. **TAT Tasks** — Most used, most error-prone
2. **Nutrition** — Daily logging
3. **Habits** — Daily check
4. **Exercise** — Weekly logging
5. **WHOOP** — Already works via webhook (just change DB)

---

## Next Steps

- [ ] Review and approve schema
- [ ] Create D1 database
- [ ] Start with TAT tasks (highest impact)

---

**Owner:** Clawson
**Target:** Complete migration before Trak Beta launch
