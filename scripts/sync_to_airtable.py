#!/usr/bin/env python3
"""
Robust Sync Script - Compares local data with Airtable and syncs missing items
"""

import json
import os
from datetime import datetime

def get_today():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime('%Y-%m-%d')

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def sync_daily_habits():
    """Sync habits from local tracker to Airtable"""
    import requests
    
    print("🔄 Syncing Daily Habits...")
    
    # Read local habit data
    habit_file = '/home/samsclaw/.openclaw/workspace/data/habit_tracker.json'
    water_file = '/home/samsclaw/.openclaw/workspace/data/water_tracker.json'
    
    updates = {}
    
    if os.path.exists(habit_file):
        with open(habit_file) as f:
            habit_data = json.load(f)
        if habit_data.get('date') == get_today():
            if habit_data.get('habits', {}).get('Fruit'):
                updates['Fruit'] = True
            if habit_data.get('habits', {}).get('Multivitamin'):
                updates['Multivitamin'] = True
    
    if os.path.exists(water_file):
        with open(water_file) as f:
            water_data = json.load(f)
        if water_data.get('date') == get_today():
            updates['Water'] = water_data.get('today', 0)
    
    if not updates:
        print("  ℹ️  No local habit data to sync")
        return
    
    # Check what's in Airtable
    url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    try:
        response = requests.get(
            f"{url}?filterByFormula=Date='{get_today()}'",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"  ❌ Cannot connect to Airtable: {response.status_code}")
            return
        
        records = response.json().get('records', [])
        
        if records:
            record_id = records[0]['id']
            existing = records[0].get('fields', {})
            
            # Check what needs updating
            needs_update = False
            for key, value in updates.items():
                if key == 'Water':
                    existing_val = existing.get(key, 0)
                    if value > existing_val:
                        updates[key] = value  # Keep higher value
                        needs_update = True
                        print(f"  📝 Water: {existing_val} → {value}")
                elif key in ['Fruit', 'Multivitamin']:
                    if not existing.get(key):
                        needs_update = True
                        print(f"  📝 {key}: False → True")
            
            if needs_update:
                update_resp = requests.patch(
                    f"{url}/{record_id}",
                    headers={**headers, "Content-Type": "application/json"},
                    json={"fields": updates},
                    timeout=10
                )
                if update_resp.status_code == 200:
                    print(f"  ✅ Updated habits: {list(updates.keys())}")
                else:
                    print(f"  ❌ Update failed: {update_resp.status_code}")
            else:
                print("  ✅ Habits already up to date")
        else:
            # Create new record
            updates['Date'] = get_today()
            create_resp = requests.post(
                url,
                headers={**headers, "Content-Type": "application/json"},
                json={"fields": updates},
                timeout=10
            )
            if create_resp.status_code == 200:
                print(f"  ✅ Created habit record: {list(updates.keys())}")
            else:
                print(f"  ❌ Create failed: {create_resp.status_code}")
                
    except Exception as e:
        print(f"  ❌ Network error: {e}")

def sync_food_log():
    """Sync food log from local memory to Airtable"""
    import requests
    
    print("\n🔄 Syncing Food Log...")
    
    # Read from local data file instead of hardcoded entries
    local_meals = []
    daily_nutrition_file = f'/home/samsclaw/.openclaw/workspace/data/daily_nutrition_{get_today()}.json'
    
    if os.path.exists(daily_nutrition_file):
        with open(daily_nutrition_file) as f:
            nutrition_data = json.load(f)
            for meal in nutrition_data.get('meals', []):
                local_meals.append({
                    "meal_type": meal.get('type', 'Meal'),
                    "food": meal.get('items', ''),
                    "calories": meal.get('calories', 0),
                    "status": "Logged"
                })
    
    if not local_meals:
        print("  ℹ️  No local food data to sync")
        return
    
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    try:
        # Check what's already in Airtable
        response = requests.get(
            f"{url}?filterByFormula=Date='{get_today()}'",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"  ❌ Cannot connect to Airtable: {response.status_code}")
            return
        
        existing_records = response.json().get('records', [])
        existing_foods = [r['fields'].get('Food Items', '') for r in existing_records]
        
        synced = 0
        for meal in local_meals:
            # Check if already exists
            if any(meal['food'][:30] in existing for existing in existing_foods):
                print(f"  ✅ Already exists: {meal['meal_type']} - {meal['food'][:40]}")
                continue
            
            # Create record
            record = {
                "fields": {
                    "Date": get_today(),
                    "Meal Type": meal['meal_type'],
                    "Food Items": meal['food'],
                    "Calories": meal.get('calories', 0),
                    "Protein (g)": meal.get('protein', 0),
                    "Carbs (g)": meal.get('carbs', 0),
                    "Fat (g)": meal.get('fat', 0),
                    "Status": meal.get('status', 'Pending API'),
                    "Notes": f"Synced at {datetime.now().strftime('%H:%M')} - partial nutrition due to API issues"
                }
            }
            
            create_resp = requests.post(
                url,
                headers={**headers, "Content-Type": "application/json"},
                json=record,
                timeout=10
            )
            
            if create_resp.status_code == 200:
                print(f"  ✅ Synced: {meal['meal_type']} - {meal['food'][:40]}")
                synced += 1
            else:
                print(f"  ❌ Failed to sync: {meal['food'][:40]}")
        
        if synced == 0:
            print("  ℹ️  All meals already in Airtable")
            
    except Exception as e:
        print(f"  ❌ Network error: {e}")

def main():
    print("=" * 50)
    print(f"🔄 AIRTABLE SYNC - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    print()
    
    sync_daily_habits()
    sync_food_log()
    
    print()
    print("=" * 50)
    print("✅ Sync complete")
    print("=" * 50)

if __name__ == "__main__":
    main()
