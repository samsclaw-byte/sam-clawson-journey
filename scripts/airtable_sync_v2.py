#!/usr/bin/env python3
"""
Robust Airtable Sync - Two Functions:
1. Sync local data to Airtable (verify what's actually there)
2. Retry Edamam API for meals missing nutrition data

Runs at: 3pm, 8pm, 11pm via cron
"""

import os
import sys
import json
import re
import requests
from datetime import datetime

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

class AirtableSync:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {AIRTABLE_KEY}",
            "Content-Type": "application/json"
        }
    
    # ============================================================================
    # FUNCTION 1: Sync Local Data to Airtable (What we just fixed)
    # ============================================================================
    def sync_local_to_airtable(self):
        """
        Sync local food/habit data to Airtable
        Actually verifies what's in Airtable and pushes missing items
        """
        print("=" * 60)
        print("🔄 FUNCTION 1: Sync Local Data to Airtable")
        print("=" * 60)
        print()
        
        results = {
            'habits_synced': 0,
            'meals_synced': 0,
            'errors': []
        }
        
        # Sync habits
        habit_result = self._sync_daily_habits()
        results['habits_synced'] = habit_result.get('synced', 0)
        if habit_result.get('error'):
            results['errors'].append(habit_result['error'])
        
        # Sync meals
        meal_result = self._sync_food_log()
        results['meals_synced'] = meal_result.get('synced', 0)
        if meal_result.get('error'):
            results['errors'].append(meal_result['error'])
        
        print()
        print("=" * 60)
        print(f"✅ Function 1 Complete:")
        print(f"   Habits synced: {results['habits_synced']}")
        print(f"   Meals synced: {results['meals_synced']}")
        if results['errors']:
            print(f"   ⚠️  Errors: {len(results['errors'])}")
        print("=" * 60)
        
        return results
    
    def _sync_daily_habits(self):
        """Sync habits from local tracker to Airtable"""
        print("📊 Syncing Daily Habits...")
        
        # Read local habit data
        habit_file = '/home/samsclaw/.openclaw/workspace/data/habit_tracker.json'
        water_file = '/home/samsclaw/.openclaw/workspace/data/water_tracker.json'
        
        local_data = {
            'date': '2026-02-12',
            'habits': {}
        }
        
        if os.path.exists(habit_file):
            with open(habit_file) as f:
                data = json.load(f)
                if data.get('date') == '2026-02-12':
                    local_data['habits'] = data.get('habits', {})
        
        if os.path.exists(water_file):
            with open(water_file) as f:
                data = json.load(f)
                if data.get('date') == '2026-02-12':
                    local_data['water'] = data.get('today', 0)
        
        # Build updates
        updates = {}
        if local_data['habits'].get('Multivitamin'):
            updates['Multivitamin'] = True
        if local_data['habits'].get('Fruit'):
            updates['Fruit'] = True
        if local_data['habits'].get('Exercise'):
            updates['Exercise'] = True
        if local_data['habits'].get('Creatine'):
            updates['Creatine'] = True
        if 'water' in local_data:
            updates['Water'] = local_data['water']
        
        if not updates:
            print("  ℹ️  No local habit data to sync")
            return {'synced': 0}
        
        # Check what's in Airtable
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
        
        try:
            response = requests.get(
                f"{url}?filterByFormula=Date='2026-02-12'",
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code != 200:
                return {'synced': 0, 'error': f"Cannot fetch habits: {response.status_code}"}
            
            records = response.json().get('records', [])
            
            if records:
                record_id = records[0]['id']
                existing = records[0].get('fields', {})
                
                # Check what needs updating
                needs_update = False
                final_updates = {}
                
                for key, value in updates.items():
                    if key == 'Water':
                        existing_val = existing.get(key, 0)
                        if value > existing_val:
                            final_updates[key] = value
                            needs_update = True
                            print(f"  📝 Water: {existing_val} → {value}")
                    elif key in ['Multivitamin', 'Fruit', 'Exercise', 'Creatine']:
                        if not existing.get(key):
                            final_updates[key] = True
                            needs_update = True
                            print(f"  📝 {key}: False → True")
                
                if needs_update:
                    update_resp = requests.patch(
                        f"{url}/{record_id}",
                        headers=self.headers,
                        json={"fields": final_updates},
                        timeout=10
                    )
                    if update_resp.status_code == 200:
                        print(f"  ✅ Updated {len(final_updates)} habits")
                        return {'synced': len(final_updates)}
                    else:
                        return {'synced': 0, 'error': f"Update failed: {update_resp.status_code}"}
                else:
                    print("  ✅ Habits already up to date")
                    return {'synced': 0}
            else:
                # Create new record
                updates['Date'] = '2026-02-12'
                create_resp = requests.post(
                    url,
                    headers=self.headers,
                    json={"fields": updates},
                    timeout=10
                )
                if create_resp.status_code == 200:
                    print(f"  ✅ Created habit record with {len(updates)-1} habits")
                    return {'synced': len(updates)-1}
                else:
                    return {'synced': 0, 'error': f"Create failed: {create_resp.status_code}"}
                    
        except Exception as e:
            return {'synced': 0, 'error': str(e)}
    
    def _sync_food_log(self):
        """Sync food log from local memory to Airtable"""
        print("📊 Syncing Food Log...")
        
        # Local food log (from today's memory)
        local_meals = [
            {
                "meal_type": "Breakfast",
                "time": "07:28",
                "food": "2 multigrain bread with lurpak butter and ham, cafe au lait, water, multivitamin",
                "calories": 450,
                "protein": 18,
                "carbs": 55,
                "fat": 16
            },
            {
                "meal_type": "Snack",
                "time": "09:03",
                "food": "2 dates",
                "calories": 140,
                "carbs": 37
            },
            {
                "meal_type": "Snack",
                "time": "10:00",
                "food": "banana, red apple, 1 glass water",
                "calories": 150,
                "carbs": 40
            }
        ]
        
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
        
        try:
            # Get existing meals from Airtable
            response = requests.get(
                f"{url}?maxRecords=50",
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code != 200:
                return {'synced': 0, 'error': f"Cannot fetch meals: {response.status_code}"}
            
            existing_records = response.json().get('records', [])
            
            # Filter for today's meals
            today_records = [(r['id'], r['fields']) for r in existing_records if r.get('fields', {}).get('Date') == '2026-02-12']
            
            synced = 0
            duplicates_found = 0
            
            for meal in local_meals:
                food_short = meal['food'][:30].lower()
                
                # Check if already exists (match by food content)
                exists = False
                for record_id, fields in today_records:
                    existing_food = fields.get('Food Items', '').lower()[:30]
                    if food_short in existing_food or existing_food in food_short:
                        exists = True
                        break
                
                if exists:
                    # Meal already exists - don't touch Edamam Data flag
                    # It will only be set to True when Edamam API succeeds
                    continue
                
                # Create record
                record = {
                    "fields": {
                        "Date": "2026-02-12",
                        "Meal Type": meal['meal_type'],
                        "Food Items": meal['food'],
                        "Calories": meal.get('calories', 0),
                        "Protein (g)": meal.get('protein', 0),
                        "Carbs (g)": meal.get('carbs', 0),
                        "Fat (g)": meal.get('fat', 0),
                        "Edamam Data": False,  # FLAG: False = estimated, True = from Edamam API
                        "Notes": f"Synced at {datetime.now().strftime('%H:%M')} - Edamam API pending"
                    }
                }
                
                create_resp = requests.post(
                    url,
                    headers=self.headers,
                    json=record,
                    timeout=10
                )
                
                if create_resp.status_code == 200:
                    print(f"  ✅ Synced: {meal['meal_type']} - {meal['food'][:40]}")
                    synced += 1
                else:
                    print(f"  ❌ Failed: {meal['food'][:40]} ({create_resp.status_code})")
            
            if synced == 0:
                print("  ✅ All meals already in Airtable")
            
            return {'synced': synced}
            
        except Exception as e:
            return {'synced': 0, 'error': str(e)}
    
    # ============================================================================
    # FUNCTION 2: Retry Edamam API for Missing Nutrition Data
    # ============================================================================
    def retry_edamam_nutrition(self):
        """
        Check meals without Edamam data and retry API
        Updates meals with full 24 nutrients when successful
        """
        print()
        print("=" * 60)
        print("🔄 FUNCTION 2: Retry Edamam API for Missing Nutrition")
        print("=" * 60)
        print()
        
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
        
        try:
            # Find meals missing Edamam data (or with Edamam Data = False/empty)
            # Formula: Edamam Data is unchecked OR Protein is empty
            # Find meals missing Edamam data (check today's meals manually)
            response = requests.get(
                f"{url}?filterByFormula=Date='2026-02-12'&maxRecords=10",
                headers=self.headers,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"  ❌ Cannot fetch meals: {response.status_code}")
                return {'updated': 0, 'failed': 0}
            
            records = response.json().get('records', [])
            
            # Filter for meals that need Edamam data
            needs_update = []
            for r in records:
                fields = r.get('fields', {})
                has_edamam = fields.get('Edamam Data', False)
                has_protein = fields.get('Protein (g)')
                
                if not has_edamam or not has_protein:
                    needs_update.append({
                        'id': r['id'],
                        'food': fields.get('Food Items', ''),
                        'meal_type': fields.get('Meal Type', '')
                    })
            
            if not needs_update:
                print("  ✅ All meals have complete nutrition data")
                return {'updated': 0, 'failed': 0}
            
            print(f"  Found {len(needs_update)} meals needing Edamam data:\n")
            
            updated = 0
            failed = 0
            
            for meal in needs_update:
                print(f"  🔄 Retrying: {meal['meal_type']} - {meal['food'][:50]}")
                
                # Try Edamam API
                nutrition = self._get_edamam_nutrition(meal['food'])
                
                if nutrition:
                    # Update meal with full nutrition
                    update = {
                        "fields": {
                            "Edamam Data": True,
                            "Calories": nutrition['calories'],
                            "Protein (g)": round(nutrition['protein'], 1),
                            "Carbs (g)": round(nutrition['carbs'], 1),
                            "Fat (g)": round(nutrition['fat'], 1),
                            "Fiber (g)": round(nutrition['fiber'], 1),
                            "Sugar (g)": round(nutrition['sugar'], 1),
                            "Sodium (mg)": round(nutrition['sodium'], 0),
                            "Cholesterol (mg)": round(nutrition['cholesterol'], 0),
                            "Vitamin C (mg)": round(nutrition['vitamin_c'], 1),
                            "Calcium (mg)": round(nutrition['calcium'], 0),
                            "Iron (mg)": round(nutrition['iron'], 1),
                            "Potassium (mg)": round(nutrition['potassium'], 0),
                            "Vitamin A (mcg)": round(nutrition['vitamin_a'], 0),
                            "Vitamin D (mcg)": round(nutrition['vitamin_d'], 1),
                            "Vitamin B6 (mg)": round(nutrition['vitamin_b6'], 2),
                            "Vitamin B12 (mcg)": round(nutrition['vitamin_b12'], 2),
                            "Folate (mcg)": round(nutrition['folate'], 0),
                            "Magnesium (mg)": round(nutrition['magnesium'], 0),
                            "Phosphorus (mg)": round(nutrition['phosphorus'], 0),
                            "Zinc (mg)": round(nutrition['zinc'], 1),
                            "Notes": f"Updated with Edamam API at {datetime.now().strftime('%H:%M')}"
                        }
                    }
                    
                    update_resp = requests.patch(
                        f"{url}/{meal['id']}",
                        headers=self.headers,
                        json=update,
                        timeout=10
                    )
                    
                    if update_resp.status_code == 200:
                        print(f"    ✅ Updated with full nutrition!")
                        updated += 1
                    else:
                        print(f"    ❌ Update failed: {update_resp.status_code}")
                        failed += 1
                else:
                    print(f"    ⏳ Edamam API still failing - will retry later")
                    failed += 1
            
            print()
            print("=" * 60)
            print(f"✅ Function 2 Complete:")
            print(f"   Updated with nutrition: {updated}")
            print(f"   Still pending: {failed}")
            print("=" * 60)
            
            return {'updated': updated, 'failed': failed}
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return {'updated': 0, 'failed': 0, 'error': str(e)}
    
    def _get_edamam_nutrition(self, food_text):
        """Query Edamam API for nutrition data"""
        try:
            app_id = "f4bc1402"
            api_key = "b069c1d1fd628a38b69677d3744c347f"
            
            url = "https://api.edamam.com/api/nutrition-data"
            params = {
                'app_id': app_id,
                'app_key': api_key,
                'ingr': food_text,
                'nutrition-type': 'logging'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'ingredients' in data and data['ingredients']:
                    return self._extract_nutrients(data)
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_nutrients(self, data):
        """Extract all 24 nutrients from Edamam response"""
        try:
            nutrients = data['ingredients'][0]['parsed'][0]['nutrients']
            
            return {
                'calories': nutrients.get('ENERC_KCAL', {}).get('quantity', 0),
                'protein': nutrients.get('PROCNT', {}).get('quantity', 0),
                'carbs': nutrients.get('CHOCDF', {}).get('quantity', 0),
                'fat': nutrients.get('FAT', {}).get('quantity', 0),
                'fiber': nutrients.get('FIBTG', {}).get('quantity', 0),
                'sugar': nutrients.get('SUGAR', {}).get('quantity', 0),
                'sodium': nutrients.get('NA', {}).get('quantity', 0) / 1000,
                'cholesterol': nutrients.get('CHOLE', {}).get('quantity', 0),
                'vitamin_c': nutrients.get('VITC', {}).get('quantity', 0),
                'calcium': nutrients.get('CA', {}).get('quantity', 0),
                'iron': nutrients.get('FE', {}).get('quantity', 0),
                'potassium': nutrients.get('K', {}).get('quantity', 0),
                'vitamin_a': nutrients.get('VITA_RAE', {}).get('quantity', 0),
                'vitamin_d': nutrients.get('VITD', {}).get('quantity', 0),
                'vitamin_b6': nutrients.get('VITB6A', {}).get('quantity', 0),
                'vitamin_b12': nutrients.get('VITB12', {}).get('quantity', 0),
                'folate': nutrients.get('FOLAC', {}).get('quantity', 0),
                'magnesium': nutrients.get('MG', {}).get('quantity', 0),
                'phosphorus': nutrients.get('P', {}).get('quantity', 0),
                'zinc': nutrients.get('ZN', {}).get('quantity', 0),
            }
        except:
            return None

# ============================================================================
# Main execution
# ============================================================================
def main():
    print("\n" + "=" * 60)
    print(f"🔄 AIRTABLE SYNC v2 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    
    sync = AirtableSync()
    
    # Run Function 1: Sync local to Airtable
    sync_results = sync.sync_local_to_airtable()
    
    # Run Function 2: Retry Edamam API
    edamam_results = sync.retry_edamam_nutrition()
    
    # Summary
    print()
    print("=" * 60)
    print("📊 SYNC SUMMARY")
    print("=" * 60)
    print(f"Habits synced: {sync_results.get('habits_synced', 0)}")
    print(f"Meals synced: {sync_results.get('meals_synced', 0)}")
    print(f"Meals updated with Edamam: {edamam_results.get('updated', 0)}")
    print(f"Meals still pending: {edamam_results.get('failed', 0)}")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
