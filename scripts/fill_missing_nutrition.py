#!/usr/bin/env python3
"""
Fill in missing nutrition data in Airtable Food Log using Edamam API
"""

import os
import sys
import requests
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path.home() / '.openclaw/workspace/scripts'))
from airtable_client import get_health_client

# Edamam API credentials
EDAMAM_APP_ID = "f4bc1402"
EDAMAM_API_KEYS = [
    "609a7ba7a7e6b2dd51cb1a37b5d34610",
    "6a17caf19f979aebe0f88d0462937a54", 
    "b069c1d1fd628a38b69677d3744c347f"
]

def get_nutrition_data(food_text, key_index=0):
    """Get nutrition data from Edamam API"""
    url = "https://api.edamam.com/api/nutrition-data"
    
    params = {
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_API_KEYS[key_index % len(EDAMAM_API_KEYS)],
        'ingr': food_text,
        'nutrition-type': 'logging'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"  ⚠️ Error fetching nutrition data: {e}")
        return None

def extract_nutrients(data):
    """Extract macro and micronutrients from Edamam response"""
    if not data or 'ingredients' not in data:
        return None
    
    try:
        nutrients = data['ingredients'][0]['parsed'][0]['nutrients']
    except (KeyError, IndexError):
        return None
    
    return {
        'calories': nutrients.get('ENERC_KCAL', {}).get('quantity', 0),
        'protein': nutrients.get('PROCNT', {}).get('quantity', 0),
        'carbs': nutrients.get('CHOCDF', {}).get('quantity', 0),
        'fat': nutrients.get('FAT', {}).get('quantity', 0),
        'fiber': nutrients.get('FIBTG', {}).get('quantity', 0),
        'sugar': nutrients.get('SUGAR', {}).get('quantity', 0),
        'sodium': nutrients.get('NA', {}).get('quantity', 0) / 1000,  # mg to g
        'calcium': nutrients.get('CA', {}).get('quantity', 0),
        'iron': nutrients.get('FE', {}).get('quantity', 0),
        'vitamin_c': nutrients.get('VITC', {}).get('quantity', 0),
    }

def update_food_log_entry(client, base_id, record_id, nutrients, missing_fields):
    """Update Airtable record with missing nutrition data"""
    table_id = 'tblsoErCMSBtzBZKB'  # Food Log table
    
    fields_to_update = {}
    
    if missing_fields.get('carbs') and nutrients.get('carbs'):
        fields_to_update['Carbs (g)'] = round(nutrients['carbs'], 1)
    if missing_fields.get('fat') and nutrients.get('fat'):
        fields_to_update['Fat (g)'] = round(nutrients['fat'], 1)
    if missing_fields.get('fiber') and nutrients.get('fiber'):
        fields_to_update['Fiber (g)'] = round(nutrients['fiber'], 1)
    
    # Also add other nutrients if available
    if nutrients.get('sugar'):
        fields_to_update['Sugar (g)'] = round(nutrients['sugar'], 1)
    if nutrients.get('sodium'):
        fields_to_update['Sodium (mg)'] = round(nutrients['sodium'] * 1000, 1)  # Convert g to mg
    if nutrients.get('calcium'):
        fields_to_update['Calcium (mg)'] = round(nutrients['calcium'], 1)
    if nutrients.get('iron'):
        fields_to_update['Iron (mg)'] = round(nutrients['iron'], 2)
    if nutrients.get('vitamin_c'):
        fields_to_update['Vitamin C (mg)'] = round(nutrients['vitamin_c'], 1)
    
    if not fields_to_update:
        return False, "No fields to update"
    
    try:
        result = client.update_record(base_id, 'Food Log', record_id, fields_to_update)
        return True, f"Updated {len(fields_to_update)} fields"
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 Checking Food Log for incomplete entries...")
    print()
    
    client = get_health_client()
    base_id = client.base_id
    
    # Query food log for entries with missing data
    url = f'{client.base_url}/{base_id}/tblsoErCMSBtzBZKB?maxRecords=100&sort%5B0%5D%5Bfield%5D=Date&sort%5B0%5D%5Bdirection%5D=desc'
    resp = requests.get(url, headers=client.headers)
    
    if resp.status_code != 200:
        print(f"❌ Error fetching food log: {resp.status_code}")
        return
    
    records = resp.json().get('records', [])
    incomplete_entries = []
    
    for r in records:
        f = r.get('fields', {})
        has_calories = f.get('Calories') is not None
        missing_carbs = f.get('Carbs (g)') is None
        missing_fat = f.get('Fat (g)') is None
        missing_fiber = f.get('Fiber (g)') is None
        
        if has_calories and (missing_carbs or missing_fat or missing_fiber):
            incomplete_entries.append({
                'id': r.get('id'),
                'date': f.get('Date'),
                'meal': f.get('Meal Type'),
                'items': f.get('Food Items', ''),
                'calories': f.get('Calories'),
                'missing': {
                    'carbs': missing_carbs,
                    'fat': missing_fat,
                    'fiber': missing_fiber
                }
            })
    
    print(f"Found {len(incomplete_entries)} entries with incomplete data")
    print()
    
    updated_count = 0
    failed_count = 0
    
    for i, entry in enumerate(incomplete_entries, 1):
        print(f"[{i}/{len(incomplete_entries)}] {entry['date']} - {entry['meal']}")
        print(f"  Items: {entry['items'][:70]}...")
        print(f"  Missing: {', '.join([k for k,v in entry['missing'].items() if v])}")
        
        # Get nutrition data from Edamam
        nutrition_data = get_nutrition_data(entry['items'])
        
        if nutrition_data:
            nutrients = extract_nutrients(nutrition_data)
            if nutrients:
                print(f"  📊 Edamam: {nutrients['calories']:.0f} kcal, "
                      f"P:{nutrients['protein']:.1f}g, "
                      f"C:{nutrients['carbs']:.1f}g, "
                      f"F:{nutrients['fat']:.1f}g, "
                      f"Fb:{nutrients['fiber']:.1f}g")
                
                # Update Airtable
                success, message = update_food_log_entry(
                    client, base_id, entry['id'], nutrients, entry['missing']
                )
                
                if success:
                    print(f"  ✅ {message}")
                    updated_count += 1
                else:
                    print(f"  ❌ Failed: {message}")
                    failed_count += 1
            else:
                print(f"  ⚠️ Could not extract nutrients from Edamam response")
                failed_count += 1
        else:
            print(f"  ⚠️ No nutrition data returned from Edamam")
            failed_count += 1
        
        print()
    
    print("=" * 50)
    print(f"✅ Updated: {updated_count} entries")
    print(f"❌ Failed: {failed_count} entries")
    print(f"📊 Total processed: {len(incomplete_entries)}")

if __name__ == "__main__":
    main()
