# Health Tracking Setup Guide

## 🎯 Quick Start

I'll help you set up weight and food tracking in Notion. Here's what we need:

## 📊 Step 1: Create Weight Tracker Database

**In Notion:**
1. Go to your "Clawson Tasks" page
2. Click "+ New" → "Database" → "Table"
3. Name it "💪 Weight Tracker"

**Add these properties:**

| Property | Type | Notes |
|----------|------|-------|
| **Name** | Title | Auto-created |
| **Date** | Date | Weigh-in date |
| **Weight (kg)** | Number | Your weight in kg |
| **Weight (lbs)** | Formula | `prop("Weight (kg)") * 2.20462` |
| **Trend** | Formula | `if(prop("Weight (kg)") > prop("Previous Weight"), "📈", if(prop("Weight (kg)") < prop("Previous Weight"), "📉", "➡️"))` |
| **Notes** | Text | Sleep, stress, etc. |

**Create a view:**
- Calendar view (by Date)
- Line chart showing weight over time

## 🍽️ Step 2: Create Food Log Database

**In Notion:**
1. Create another database: "🍽️ Food Log"

**Properties:**

| Property | Type | Notes |
|----------|------|-------|
| **Name** | Title | Meal description |
| **Date/Time** | Date | When you ate (include time) |
| **Meal Type** | Select | Breakfast, Lunch, Dinner, Snack |
| **Description** | Text | What you tell me ("chicken sandwich, no mayo") |
| **Calories** | Number | Auto-filled from API |
| **Protein (g)** | Number | Auto-filled |
| **Carbs (g)** | Number | Auto-filled |
| **Fat (g)** | Number | Auto-filled |
| **Sugar (g)** | Number | Auto-filled |
| **Fiber (g)** | Number | Auto-filled |
| **Photo** | Files | Optional food photo |
| **Logged By** | Select | Manual, Voice, Photo |

**Views to create:**
- Today (filter: Date is Today)
- This Week (group by Date)
- By Meal Type (group by Breakfast/Lunch/Dinner)

## 💰 Step 3: Nutrition API Setup

**Recommended: Edamam Nutrition API**
- **Free tier:** 2,000 requests/month (~66/day)
- **Cost:** FREE for your usage level
- **Signup:** https://developer.edamam.com/

**Alternative: Nutritionix**
- Free: 200 requests/day
- Might be limiting

## 🤖 Step 4: How Logging Works

### Weight Logging:
**You say:** "Weight check: 78.2kg this morning"
**I do:**
1. Parse weight value
2. Create Notion entry
3. Calculate trend vs previous
4. Reply: "✅ Logged: 78.2kg | 📉 Down 0.5kg from yesterday"

### Food Logging:
**You say:** "Lunch: grilled chicken sandwich and side salad"
**I do:**
1. Parse meal description
2. Query Edamam API
3. Create Notion entry with full nutrition
4. Reply: "✅ Logged: 485 cal | 35g protein | 42g carbs"

## 📈 Step 5: Weekly Reports

Every Sunday, I'll generate:
- Average daily calories
- Macro breakdown (protein/carbs/fat %)
- Weight trend (gained/lost/stable)
- Recommendations based on goals

## 🚀 Getting Started

**Option A: I create the databases now**
Give me 10 minutes to set up via API

**Option B: You create them manually**
Follow the steps above, takes ~5 minutes

**Option C: Start simple**
- Text me your weight daily
- Text me what you eat
- I'll store in text files first
- Migrate to Notion later

## ❓ Which option works for you?

Also: What's your current weight and target weight? (For trend calculation)

---
*Ready to start tracking!* 🦞💪
