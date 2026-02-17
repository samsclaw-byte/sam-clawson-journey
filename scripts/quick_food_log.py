#!/usr/bin/env python3
"""
Quick Food Logger - Simple version for inline use
Pushes directly to Airtable without Edamam API
"""

import requests
from datetime import datetime

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
FOOD_TABLE = "tblsoErCMSBtzBZKB"

def log_meal(meal_type, food_items, calories=None, notes=""):
    """
    Log a meal to Airtable
    
    Args:
        meal_type: Breakfast, Lunch, Dinner, Snack
        food_items: Description of food
        calories: Optional calorie estimate
        notes: Optional notes
    """
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    record = {
        "fields": {
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Meal Type": meal_type,
            "Food Items": food_items,
            "Notes": notes
        }
    }
    
    if calories:
        record["fields"]["Calories"] = calories
    
    response = requests.post(url, headers=headers, json=record)
    
    if response.status_code == 200:
        return True, "Logged to Airtable"
    else:
        return False, f"Error: {response.status_code}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        meal_type = sys.argv[1]
        food_items = sys.argv[2]
        calories = int(sys.argv[3]) if len(sys.argv) > 3 else None
        success, msg = log_meal(meal_type, food_items, calories)
        print(msg)
    else:
        print("Usage: python3 quick_food_log.py <meal_type> <food_items> [calories]")
