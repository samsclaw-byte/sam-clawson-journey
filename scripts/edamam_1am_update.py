#!/usr/bin/env python3
"""
1AM Edamam Update Job
Checks Food Log for records without Edamam data and retries API
Updates macros when successful
"""

import requests
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
FOOD_TABLE = "tblsoErCMSBtzBZKB"

EDAMAM_APP_ID = "f4bc1402"
EDAMAM_API_KEYS = [
    "6a17caf19f979aebe0f88d0462937a54",
    "b069c1d1fd628a38b69677d3744c347f"
]

def get_edamam_nutrition(food_text):
    """Query Edamam API for nutrition data"""
    url = "https://api.edamam.com/api/nutrition-data"
    
    for api_key in EDAMAM_API_KEYS:
        try:
            params = {
                'app_id': EDAMAM_APP_ID,
                'app_key': api_key,
                'ingr': food_text,
                'nutrition-type': 'logging'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'ingredients' in data and data['ingredients']:
                    nutrients = data['ingredients'][0]['parsed'][0]['nutrients']
                    
                    return {
                        'calories': round(nutrients.get('ENERC_KCAL', {}).get('quantity', 0)),
                        'protein': round(nutrients.get('PROCNT', {}).get('quantity', 0), 1),
                        'carbs': round(nutrients.get('CHOCDF', {}).get('quantity', 0), 1),
                        'fat': round(nutrients.get('FAT', {}).get('quantity', 0), 1),
                        'fiber': round(nutrients.get('FIBTG', {}).get('quantity', 0), 1),
                        'sugar': round(nutrients.get('SUGAR', {}).get('quantity', 0), 1),
                    }
                    
        except Exception:
            continue
    
    return None

def update_pending_edamam_records():
    """Find and update records without Edamam data from last 7 days"""
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get date 7 days ago
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Find records without Edamam data from last 7 days
    # Check for records with missing or zero calories (not yet processed by Edamam)
    filter_formula = f"AND(IS_AFTER({{Date}}, '{week_ago}'), OR({{Calories}}=0, {{Calories}}=BLANK()))"
    
    response = requests.get(
        f"{url}?filterByFormula={filter_formula}&maxRecords=50",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Error fetching records: {response.status_code}")
        return
    
    records = response.json().get('records', [])
    
    if not records:
        print("✅ No pending Edamam records found")
        return
    
    print(f"🔄 Found {len(records)} records to update with Edamam API")
    print("-" * 60)
    
    updated = 0
    failed = 0
    
    for record in records:
        record_id = record['id']
        fields = record['fields']
        food_items = fields.get('Food Items', '')
        
        print(f"🍽️ Processing: {food_items[:50]}...")
        
        # Try Edamam API
        nutrition = get_edamam_nutrition(food_items)
        
        if nutrition:
            # Update record with Edamam data
            update = {
                "fields": {
                    "Calories": nutrition['calories'],
                    "Protein (g)": nutrition['protein'],
                    "Carbs (g)": nutrition['carbs'],
                    "Fat (g)": nutrition['fat'],
                    "Fiber (g)": nutrition['fiber'],
                    "Sugar (g)": nutrition['sugar'],
                    "Notes": f"Updated with Edamam API at {datetime.now().strftime('%H:%M')}"
                }
            }
            
            update_resp = requests.patch(
                f"{url}/{record_id}",
                headers=headers,
                json=update
            )
            
            if update_resp.status_code == 200:
                print(f"   ✅ Updated: {nutrition['calories']} cal | P:{nutrition['protein']}g C:{nutrition['carbs']}g F:{nutrition['fat']}g")
                updated += 1
            else:
                print(f"   ❌ Update failed: {update_resp.status_code}")
                failed += 1
        else:
            print(f"   ⏳ Edamam API still failing - will retry tomorrow")
            failed += 1
    
    print("-" * 60)
    print(f"✅ Complete: {updated} updated, {failed} still pending")

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"🔄 1AM Edamam Update Job - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    update_pending_edamam_records()
    print(f"\n{'='*60}\n")
