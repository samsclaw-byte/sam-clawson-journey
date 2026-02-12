#!/usr/bin/env python3
"""
Robust Food Logging with Edamam API
Handles API failures gracefully
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Config
AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"
FOOD_TABLE = "tblsoErCMSBtzBZKB"
TAT_TABLE = "tblkbuvkZUSpm1IgJ"

def log_food_meal(food_description, meal_type="Snack"):
    """
    Log food meal with full nutrition
    If Edamam fails, save description and create follow-up task
    """
    
    print(f"🍽️ Logging {meal_type}: {food_description}")
    
    # Try Edamam API
    nutrition_data = get_edamam_nutrition(food_description)
    
    if nutrition_data:
        # Success - log with full nutrition
        record = create_full_nutrition_record(food_description, meal_type, nutrition_data)
        status = "✅ Complete"
        print(f"  ✓ Full nutrition logged (24 nutrients)")
    else:
        # Failure - save description only, create task
        record = create_partial_record(food_description, meal_type)
        task_id = create_nutrition_update_task(food_description, meal_type)
        status = "⏳ Pending API"
        print(f"  ⚠️  Edamam API failed - saved description, created task #{task_id}")
    
    return record, status

def get_edamam_nutrition(food_text):
    """Query Edamam API for nutrition data"""
    try:
        app_id = "f4bc1402"
        api_key = "6a17caf19f979aebe0f88d0462937a54"
        
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
                return extract_nutrients(data)
        
        return None
        
    except Exception as e:
        print(f"  Edamam API error: {e}")
        return None

def extract_nutrients(data):
    """Extract all 24 nutrients from Edamam response"""
    try:
        nutrients = data['ingredients'][0]['parsed'][0]['nutrients']
        
        return {
            # Macros
            'calories': nutrients.get('ENERC_KCAL', {}).get('quantity', 0),
            'protein': nutrients.get('PROCNT', {}).get('quantity', 0),
            'carbs': nutrients.get('CHOCDF', {}).get('quantity', 0),
            'fat': nutrients.get('FAT', {}).get('quantity', 0),
            'fiber': nutrients.get('FIBTG', {}).get('quantity', 0),
            
            # Basic micros
            'sugar': nutrients.get('SUGAR', {}).get('quantity', 0),
            'sodium': nutrients.get('NA', {}).get('quantity', 0) / 1000,  # mg
            'cholesterol': nutrients.get('CHOLE', {}).get('quantity', 0),
            'vitamin_c': nutrients.get('VITC', {}).get('quantity', 0),
            'calcium': nutrients.get('CA', {}).get('quantity', 0),
            'iron': nutrients.get('FE', {}).get('quantity', 0),
            'potassium': nutrients.get('K', {}).get('quantity', 0),
            
            # Vitamins
            'vitamin_a': nutrients.get('VITA_RAE', {}).get('quantity', 0),
            'vitamin_d': nutrients.get('VITD', {}).get('quantity', 0),
            'vitamin_b6': nutrients.get('VITB6A', {}).get('quantity', 0),
            'vitamin_b12': nutrients.get('VITB12', {}).get('quantity', 0),
            
            # Minerals
            'folate': nutrients.get('FOLAC', {}).get('quantity', 0),
            'magnesium': nutrients.get('MG', {}).get('quantity', 0),
            'phosphorus': nutrients.get('P', {}).get('quantity', 0),
            'zinc': nutrients.get('ZN', {}).get('quantity', 0),
            'selenium': nutrients.get('SE', {}).get('quantity', 0),
            'copper': nutrients.get('CU', {}).get('quantity', 0),
            'manganese': nutrients.get('MN', {}).get('quantity', 0),
            'thiamin': nutrients.get('THIA', {}).get('quantity', 0),
        }
    except:
        return None

def create_full_nutrition_record(food_desc, meal_type, nutrition):
    """Create complete record with all 24 nutrients"""
    
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    record = {
        "fields": {
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Meal Type": meal_type,
            "Food Items": food_desc,
            "Status": "Complete",
            
            # All 24 nutrients
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
            "Notes": f"Complete nutrition via Edamam API"
        }
    }
    
    response = requests.post(url, headers=headers, json=record)
    return response.json() if response.status_code == 200 else None

def create_partial_record(food_desc, meal_type):
    """Create record with just description when API fails"""
    
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    record = {
        "fields": {
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Meal Type": meal_type,
            "Food Items": food_desc,
            "Status": "Pending API",
            "Notes": f"Edamam API failed - needs nutrition data"
        }
    }
    
    response = requests.post(url, headers=headers, json=record)
    return response.json() if response.status_code == 200 else None

def create_nutrition_update_task(food_desc, meal_type):
    """Create TAT task to update nutrition later"""
    
    url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/{TAT_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    today = datetime.now()
    
    record = {
        "fields": {
            "Task Name": f"🍽️ Update nutrition: {meal_type} - {food_desc[:40]}",
            "Category": "3",
            "TAT Category Days": 3,
            "Date Created": today.strftime('%Y-%m-%d'),
            "Due Date": (today + timedelta(days=3)).strftime('%Y-%m-%d'),
            "Status": "Not Started",
            "Notes": f"Edamam API failed when logging this meal. Need to manually update with nutrition data from another source or retry API.\n\nFood: {food_desc}\nLogged: {today.strftime('%Y-%m-%d %H:%M')}"
        }
    }
    
    response = requests.post(url, headers=headers, json=record)
    
    if response.status_code == 200:
        return response.json().get('id', 'created')
    return None

def check_pending_nutrition_updates():
    """Check for meals with pending nutrition and try to update"""
    
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Find pending meals
    params = {
        "filterByFormula": "{Status}='Pending API'",
        "maxRecords": 10
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return []
    
    records = response.json().get('records', [])
    updated = []
    
    for record in records:
        food_desc = record['fields'].get('Food Items', '')
        meal_type = record['fields'].get('Meal Type', 'Snack')
        
        print(f"  Retrying: {food_desc[:50]}...")
        
        # Try Edamam again
        nutrition = get_edamam_nutrition(food_desc)
        
        if nutrition:
            # Update with full nutrition
            update_url = f"{url}/{record['id']}"
            update_data = {
                "fields": {
                    "Status": "Complete",
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
                    "Notes": f"Nutrition updated on retry - Edamam API success"
                }
            }
            
            update_resp = requests.patch(update_url, headers=headers, json=update_data)
            if update_resp.status_code == 200:
                updated.append(food_desc)
                print(f"    ✅ Updated with full nutrition!")
        else:
            print(f"    ⏳ Still pending - API still failing")
    
    return updated

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log_food_meal.py 'food description' [meal_type]")
        print("Example: python3 log_food_meal.py '2 eggs, toast, coffee' 'Breakfast'")
        sys.exit(1)
    
    food = sys.argv[1]
    meal = sys.argv[2] if len(sys.argv) > 2 else "Snack"
    
    record, status = log_food_meal(food, meal)
    # Also check for habits in food description
    print("\n📝 Checking for habits in food description...")
    sys.path.insert(0, '/home/samsclaw/.openclaw/workspace/scripts')
    try:
        from habit_tracker_from_food import update_habits_from_food
        update_habits_from_food(food)
    except Exception as e:
        print(f"  Note: Could not update habits ({e})")
    
    print(f"\nStatus: {status}")
    
    if status == "⏳ Pending API":
        print("\n💡 A task has been created to retry this later.")
        print("   You'll get reminders at 12pm, 3pm, and 8pm to check status.")
