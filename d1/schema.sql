-- D1 Schema for Trak App
-- Created: February 22, 2026

-- TAT Tasks Table
CREATE TABLE IF NOT EXISTS tat_tasks (
    id TEXT PRIMARY KEY,
    task_name TEXT NOT NULL,
    category INTEGER NOT NULL CHECK(category IN (1, 3, 7, 30)),
    status TEXT DEFAULT 'Not Started' CHECK(status IN ('Not Started', 'In Progress', 'Completed')),
    priority TEXT DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High')),
    date_created TEXT NOT NULL,
    due_date TEXT,
    date_completed TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Habits Table
CREATE TABLE IF NOT EXISTS habits (
    id TEXT PRIMARY KEY,
    habit_name TEXT NOT NULL,
    date TEXT NOT NULL,
    completed INTEGER DEFAULT 0 CHECK(completed IN (0, 1)),
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(habit_name, date)
);

-- Nutrition Table
CREATE TABLE IF NOT EXISTS nutrition (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    description TEXT,
    calories INTEGER,
    protein REAL,
    carbs REAL,
    fat REAL,
    source TEXT DEFAULT 'manual' CHECK(source IN ('manual', 'edamam', 'ai')),
    created_at TEXT DEFAULT (datetime('now'))
);

-- Exercise Table
CREATE TABLE IF NOT EXISTS exercise (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    workout_type TEXT,
    duration_minutes INTEGER,
    strain REAL,
    notes TEXT,
    source TEXT DEFAULT 'manual',
    created_at TEXT DEFAULT (datetime('now'))
);

-- WHOOP Data Table
CREATE TABLE IF NOT EXISTS whoop_data (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    recovery_score INTEGER,
    strain_score INTEGER,
    sleep_performance REAL,
    sleep_duration_hours REAL,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tat_tasks_status ON tat_tasks(status);
CREATE INDEX IF NOT EXISTS idx_tat_tasks_due_date ON tat_tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_habits_date ON habits(date);
CREATE INDEX IF NOT EXISTS idx_nutrition_date ON nutrition(date);
CREATE INDEX IF NOT EXISTS idx_exercise_date ON exercise(date);
CREATE INDEX IF NOT EXISTS idx_whoop_date ON whoop_data(date);
