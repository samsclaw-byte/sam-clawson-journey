# Health Dashboard Data Inventory

## Data Sources for Mission Control Health Dashboard

### 1. ✅ WHOOP Data (OAuth)
**File:** `migration/data/whoop_cycles.json`
**Records:** 10 days
**Fields:** Date, Strain, Kilojoules (calories), Avg HR, Max HR, Workout detection

**Use for dashboard:**
- Daily strain chart
- Workout vs rest day visualization
- Calorie burn trends
- Heart rate zones

### 2. ✅ Exercise Tracker
**Notion DB:** `304f2cb1-2276-816d-a059-d818dc3cc79f`
**Records:** 4 workouts
**Fields:** Date, Name, Type, Exercises, Sets/Reps, Weight, Duration, RPE, Recovery %, Notes

**Use for dashboard:**
- Workout history timeline
- Exercise progression (weight increases)
- RPE trends
- Recovery correlation with strain

### 3. ✅ Habit Tracker
**Notion DB:** `304f2cb1-2276-81bb-b69f-c28f02d35fa5`
**Records:** 4 days
**Fields:** Date, Creatine, Multivitamin, Exercise, Exercise Type, Fruit, Water, Notes

**Use for dashboard:**
- Daily habit streaks
- Compliance percentages
- Correlation: habits vs recovery

### 4. ✅ Weight Tracker
**Notion DB:** `f9583de8-69e9-40e6-ab15-c530277ec474`
**Records:** 3 entries
**Fields:** Date, Weight (kg), Notes

**Use for dashboard:**
- Weight trend line
- Progress to goal (95kg)

### 5. ✅ Food Log
**Notion DB:** `dc76e804-5b9e-406b-afda-d7a20dd58976`
**Records:** 14 meals
**Fields:** Date, Meal Type, Food Items, Calories, Protein, Carbs, Fat

**Use for dashboard:**
- Daily calorie intake
- Macro breakdown (pie chart)
- Protein tracking
- Net calories (intake - burn from WHOOP)

---

## Proposed Health Dashboard Widgets

### Overview Tab
- 🎯 **Today's Score**: Composite health score (habits + strain + sleep)
- 📊 **Weekly Trends**: Strain, calories, weight on one chart
- 🔥 **Streak Counter**: Consecutive days hitting all habits

### Fitness Tab  
- 📈 **Strain vs Recovery**: Scatter plot over time
- 💪 **Workout Volume**: Total kg lifted, duration trends
- 🏃 **Activity Calendar**: Heat map of strain by day

### Nutrition Tab
- 🍽️ **Today's Macros**: Protein/Carbs/Fat pie chart
- 📊 **Net Calories**: Intake (Food Log) - Burn (WHOOP)
- 💧 **Water Progress**: 8 glass tracker

### Sleep & Recovery Tab  
- 💓 **WHOOP Recovery**: Score + color coding
- 🛌 **Sleep Breakdown**: REM/Deep/Light (when available)
- 📉 **Resting HR Trends**: Recovery indicator

---

## Data Correlation Possibilities

1. **Habits → Recovery**: Does creatine/multi correlate with better recovery?
2. **Strain → Sleep**: Do hard workout days = better sleep?
3. **Weight → Net Calories**: Is the math working?
4. **Water → Performance**: Hydration impact on strain?

---

## Migration Status

All data sources ready for Airtable migration:
- [x] WHOOP data (JSON export)
- [x] Exercise Tracker
- [x] Habit Tracker
- [x] Weight Tracker
- [x] Food Log

**Next:** Create unified Health Dashboard in Mission Control

---

*Created: Feb 11, 2026*
