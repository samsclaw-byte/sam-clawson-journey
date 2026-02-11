# Databases to Migrate: Notion → Airtable

## 📦 Category: TO BE MIGRATED

### 1. ✅ Food & Nutrition Log
- **Notion ID:** dc76e804-5b9e-406b-afda-d7a20dd58976
- **Records:** 14 meals (Feb 8-11)
- **Fields:** Date, Meal Type, Food Items, Calories, Protein, Carbs, Fat, Notes
- **Status:** Working (API 2022-06-28)
- **Validation:** ✅ Data complete

### 2. ✅ Weight Tracker
- **Notion ID:** f9583de8-69e9-40e6-ab15-c530277ec474
- **Records:** 3 entries (104kg, 104kg, 103kg)
- **Fields:** Date, Weight (kg), Notes
- **Status:** Working (API 2022-06-28)
- **Validation:** ✅ Data complete

### 3. ✅ Work Tasks & Projects
- **Notion ID:** 304f2cb1-2276-8156-b477-cf3ba96a68e0
- **Records:** 7 tasks
- **Fields:** Name, TAT Category, Date, Due Date (formula), Source, Type, Stakeholder (Steve/Rafi/Other), Status
- **Status:** Working (API 2022-06-28)
- **Validation:** ✅ Data complete

### 4. ✅ Habit Tracker
- **Notion ID:** 304f2cb1-2276-81bb-b69f-c28f02d35fa5
- **Records:** 4 days (Feb 8-11)
- **Fields:** Date, Creatine, Multivitamin, Exercise, Exercise Type, Fruit (2 portions), Water (8 glasses), Notes
- **Status:** Working (API 2022-06-28)
- **Validation:** ✅ Data complete

### 5. ✅ Exercise Tracker (v2 - Working)
- **Notion ID:** 304f2cb1-2276-816d-a059-d818dc3cc79f
- **Records:** 4 workouts (Feb 8-11)
- **Fields:** Date, Workout Name, Type (Hard/Active Recovery/Rest), Exercises, Sets/Reps, Weight, Duration, RPE (1-10), Recovery %, Notes
- **Status:** Working (API 2022-06-28)
- **Validation:** ✅ Data complete

### 6. ❌ Exercise Tracker (v1 - Broken)
- **Notion ID:** 2fdf2cb1-2276-8118-a994-2cb030df3a590
- **Records:** 0 entries (broken API)
- **Status:** BROKEN (API 2025-09-03)
- **Action:** SKIP - replaced by v2

---

## 📊 Migration Summary

| Database | Records | Priority | Notes |
|----------|---------|----------|-------|
| Food Log | 14 | High | Core tracking |
| Weight Tracker | 3 | High | Core tracking |
| Work Tasks | 7 | High | Active workflow |
| Habit Tracker | 4 | High | Daily habits |
| Exercise Tracker v2 | 4 | High | Detailed workouts |
| Exercise Tracker v1 | 0 | Skip | Broken - replaced |

**Total:** 5 databases, 32 records to migrate

---

## ✅ Pre-Migration Validation Checklist

- [ ] Confirm all records export successfully
- [ ] Validate data integrity (no missing fields)
- [ ] Test Airtable API connection
- [ ] Create Airtable base structure
- [ ] Import sample record as test
- [ ] Verify Mission Control can query Airtable

---

*Created: Feb 11, 2026*
