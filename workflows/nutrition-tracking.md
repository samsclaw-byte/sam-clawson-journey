# Nutrition Tracking Workflow

## Overview
Track your food intake with natural language. **Auto-syncs to Notion** after analysis.

## How It Works

### Tell Me What You Ate
Just message me naturally:
- "Had 200g grilled chicken with rice and broccoli for lunch"
- "Large cappuccino with oat milk"
- "Greek yogurt with honey and walnuts for snack"

**I will:**
1. ✅ Analyze nutrition instantly (macros + micros)
2. ✅ **Auto-sync to Notion Food & Nutrition Log**
3. ✅ Reply with full breakdown

### Notion Database: 🍽️ Food & Nutrition Log
Located in: 🏃 Health & Fitness

**Database tracks 22 nutrients per meal:**

| Category | Nutrients |
|----------|-----------|
| **Macros** | Calories, Protein, Carbs, Fat, Fiber, Sugar |
| **Vitamins** | A, D, E, K, C, B12, Folate |
| **Minerals** | Sodium, Iron, Calcium, Potassium, Magnesium, Zinc, Phosphorus |
| **Other** | Cholesterol |

**Plus:** Date, Meal type, Food description, Notes

## Meal Detection
I'll try to detect the meal type from your message:
- "breakfast" → Breakfast 🌅
- "lunch" → Lunch 🌞
- "dinner" → Dinner 🌙
- "snack" → Snack 🥜
- (no meal mentioned) → Snack (default)

## Commands

```bash
# Log manually with meal type
python3 scripts/notion_nutrition_sync.py "grilled chicken 200g" Lunch

# Just check nutrition (no Notion sync)
python3 scripts/nutrition_tracker.py "2 eggs and toast"

# List recent meals
python3 scripts/notion_nutrition_sync.py list
```

## Files

| File | Purpose |
|------|---------|
| `scripts/nutrition_tracker.py` | Core analysis (local only) |
| `scripts/notion_nutrition_sync.py` | Analysis + Notion sync |
| `workflows/nutrition-tracking.md` | This doc |

## Data Tracked

### Macros
| Nutrient | Auto-synced |
|----------|-------------|
| Calories | ✅ |
| Protein | ✅ |
| Carbs | ✅ |
| Fat | ✅ |
| Fiber | ✅ |
| Sugar | ✅ |

### Micros - Fat Soluble Vitamins
| Nutrient | Auto-synced |
|----------|-------------|
| Vitamin A | ✅ |
| Vitamin D | ✅ |
| Vitamin E | ✅ |
| Vitamin K | ✅ |

### Micros - B Vitamins
| Nutrient | Auto-synced |
|----------|-------------|
| Vitamin B12 | ✅ |
| Folate (B9) | ✅ |

### Micros - Minerals
| Nutrient | Auto-synced |
|----------|-------------|
| Sodium | ✅ |
| Iron | ✅ |
| Calcium | ✅ |
| Potassium | ✅ |
| Magnesium | ✅ |
| Zinc | ✅ |
| Phosphorus | ✅ |
| Cholesterol | ✅ |

---
*Updated: 2026-02-08 (auto-sync enabled)*
