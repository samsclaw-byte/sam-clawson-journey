#!/usr/bin/env python3
"""
Update food logging to also track habits (water, multivitamin)
When food contains these items, update Daily Habits table
"""

import requests
import re

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def update_habits_from_food(food_description):
    """Check if food mentions habits and update accordingly"""
    
    food_lower = food_description.lower()
    updates = {}
    
    # Check for multivitamin
    if any(word in food_lower for word in ['multivitamin', 'vitamin', 'multi vitamin', 'multi-vitamin']):
        updates['Multivitamin'] = True
        print("  💊 Multivitamin detected - will update habits")
    
    # Check for fruit
    fruit_keywords = [
        'apple', 'banana', 'orange', 'pear', 'grape', 'berry', 'berries',
        'strawberry', 'blueberry', 'raspberry', 'blackberry', 'mango',
        'pineapple', 'watermelon', 'melon', 'peach', 'plum', 'cherry',
        'kiwi', 'lemon', 'lime', 'date', 'fig', 'pomegranate'
    ]
    
    if any(fruit in food_lower for fruit in fruit_keywords):
        updates['Fruit'] = True
        print("  🍎 Fruit detected - will update habits")
    
    # Check for water
    water_patterns = [
        r'(\d+)\s*glass(?:es)?\s+of\s+water',
        r'(\d+)\s*glass(?:es)?\s+water',
        r'water\s*:\s*(\d+)',
    ]
    
    water_count = 0
    for pattern in water_patterns:
        matches = re.findall(pattern, food_lower)
        if matches:
            water_count = int(matches[0])
            break
    
    # Also check for just "water" mentioned
    if 'water' in food_lower and water_count == 0:
        # Assume 1 glass if just mentioned
        water_count = 1
    
    if water_count > 0:
        updates['Water'] = water_count
        print(f"  💧 Water detected: {water_count} glasses - will update habits")
    
    if updates:
        update_daily_habits(updates)
    else:
        print("  ℹ️  No habits detected in food description")

def update_daily_habits(updates):
    """Update or create today's habit entry"""
    
    url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Check if today's entry exists
    filter_formula = "Date='2026-02-12'"
    response = requests.get(
        f"{url}?filterByFormula={filter_formula}",
        headers=headers
    )
    
    if response.status_code == 200:
        records = response.json().get('records', [])
        
        if records:
            # Update existing record
            record_id = records[0]['id']
            existing = records[0].get('fields', {})
            
            # Merge updates
            if 'Water' in updates and 'Water' in existing:
                updates['Water'] = existing['Water'] + updates['Water']
            
            update_url = f"{url}/{record_id}"
            update_response = requests.patch(update_url, headers=headers, json={"fields": updates})
            
            if update_response.status_code == 200:
                print(f"  ✅ Updated today's habits: {list(updates.keys())}")
            else:
                print(f"  ⚠️  Could not update habits: {update_response.status_code}")
        else:
            # Create new record
            updates['Date'] = '2026-02-12'
            create_response = requests.post(url, headers=headers, json={"fields": updates})
            
            if create_response.status_code == 200:
                print(f"  ✅ Created today's habits: {list(updates.keys())}")
            else:
                print(f"  ⚠️  Could not create habits: {create_response.status_code}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        food = sys.argv[1]
        print(f"Checking habits in: {food}")
        update_habits_from_food(food)
    else:
        print("Usage: python3 habit_tracker_from_food.py 'food description'")
