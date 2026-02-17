#!/usr/bin/env python3
"""
Quick Food Logger - With Macro Estimation (Option C: Hybrid)
Pushes directly to Airtable with estimated macros
Tries Edamam API first, falls back to manual estimation
"""

import requests
import re
from datetime import datetime

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
FOOD_TABLE = "tblsoErCMSBtzBZKB"

# Edamam API credentials
EDAMAM_APP_ID = "f4bc1402"
EDAMAM_API_KEYS = [
    "6a17caf19f979aebe0f88d0462937a54",  # Primary
    "b069c1d1fd628a38b69677d3744c347f"   # Fallback
]

def estimate_macros_manual(food_description, calories=None):
    """
    Manual macro estimation based on food keywords and portions
    Returns dict with protein, carbs, fat, fiber, sugar
    """
    food_lower = food_description.lower()
    
    # Initialize with zeros
    macros = {
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0,
        'sugar': 0
    }
    
    # Estimate calories if not provided
    if calories is None:
        calories = estimate_calories(food_description)
    
    # Portion detection
    portion_multiplier = 1.0
    if any(word in food_lower for word in ['large', 'big', 'double', 'extra']):
        portion_multiplier = 1.5
    elif any(word in food_lower for word in ['small', 'half', 'little']):
        portion_multiplier = 0.7
    
    # Number detection for quantity
    quantity = 1
    qty_match = re.search(r'(\d+)\s*(?:piece|pieces|slices?|eggs?|scoops?|cups?|glasses?|bowls?|plates?)', food_lower)
    if qty_match:
        quantity = int(qty_match.group(1))
    
    portion_multiplier *= quantity
    
    # Category-based estimation
    if any(word in food_lower for word in ['egg', 'eggs', 'omelette', 'scrambled']):
        # Eggs: 6g protein, 0.6g carbs, 5g fat per egg
        egg_count = quantity if 'egg' in food_lower or 'eggs' in food_lower else 1
        macros['protein'] += 6 * egg_count * portion_multiplier
        macros['fat'] += 5 * egg_count * portion_multiplier
        
    if any(word in food_lower for word in ['toast', 'bread', 'bagel', 'croissant', 'muffin', 'roll']):
        # Bread: 3g protein, 15g carbs, 1g fat per slice
        slice_count = quantity if 'slice' in food_lower or 'pieces' in food_lower else 2
        macros['protein'] += 3 * slice_count * portion_multiplier
        macros['carbs'] += 15 * slice_count * portion_multiplier
        macros['fat'] += 1 * slice_count * portion_multiplier
        macros['fiber'] += 1.5 * slice_count * portion_multiplier
        
    if any(word in food_lower for word in ['butter', 'lurpak', 'margarine', 'spread']):
        # Butter: 0g protein, 0g carbs, 11g fat per tbsp
        macros['fat'] += 11 * portion_multiplier
        
    if any(word in food_lower for word in ['ham', 'bacon', 'sausage', 'meat', 'chicken', 'beef', 'steak', 'turkey']):
        # Meat: 7g protein, 0g carbs, 5g fat per oz (rough average)
        macros['protein'] += 7 * 2 * portion_multiplier  # Assume 2 oz
        macros['fat'] += 5 * 2 * portion_multiplier
        
    if any(word in food_lower for word in ['cheese', 'cheddar', 'mozzarella', 'feta']):
        # Cheese: 7g protein, 1g carbs, 9g fat per oz
        macros['protein'] += 7 * portion_multiplier
        macros['carbs'] += 1 * portion_multiplier
        macros['fat'] += 9 * portion_multiplier
        
    if any(word in food_lower for word in ['milk', 'latte', 'cappuccino', 'coffee', 'cafe']):
        # Milk in coffee: 1g protein, 1.5g carbs, 0.5g fat per 100ml
        macros['protein'] += 1 * 2 * portion_multiplier  # Assume 200ml
        macros['carbs'] += 1.5 * 2 * portion_multiplier
        macros['fat'] += 0.5 * 2 * portion_multiplier
        
    if any(word in food_lower for word in ['sugar', 'sweetened']):
        # Sugar: 0g protein, 4g carbs, 0g fat per tsp
        macros['carbs'] += 4 * portion_multiplier
        macros['sugar'] += 4 * portion_multiplier
        
    if any(word in food_lower for word in ['apple', 'banana', 'orange', 'fruit', 'berries', 'pear', 'grapes']):
        # Fruit: 0.3g protein, 15g carbs, 0.2g fat, 2.5g fiber, 10g sugar per serving
        macros['protein'] += 0.3 * portion_multiplier
        macros['carbs'] += 15 * portion_multiplier
        macros['fat'] += 0.2 * portion_multiplier
        macros['fiber'] += 2.5 * portion_multiplier
        macros['sugar'] += 10 * portion_multiplier
        
    if any(word in food_lower for word in ['nuts', 'almonds', 'walnuts', 'cashews', 'peanuts']):
        # Nuts: 6g protein, 3g carbs, 14g fat, 2g fiber per oz
        macros['protein'] += 6 * portion_multiplier
        macros['carbs'] += 3 * portion_multiplier
        macros['fat'] += 14 * portion_multiplier
        macros['fiber'] += 2 * portion_multiplier
        
    if any(word in food_lower for word in ['rice', 'biryani', 'pilaf', 'noodles', 'pasta']):
        # Rice/pasta: 4g protein, 45g carbs, 0.5g fat per cup cooked
        macros['protein'] += 4 * 1.5 * portion_multiplier
        macros['carbs'] += 45 * 1.5 * portion_multiplier
        macros['fat'] += 0.5 * 1.5 * portion_multiplier
        macros['fiber'] += 1 * 1.5 * portion_multiplier
        
    if any(word in food_lower for word in ['curry', 'tikka', 'masala', 'sauce', 'gravy']):
        # Curry/sauce: 3g protein, 8g carbs, 10g fat per cup
        macros['protein'] += 3 * portion_multiplier
        macros['carbs'] += 8 * portion_multiplier
        macros['fat'] += 10 * portion_multiplier
        
    if any(word in food_lower for word in ['chocolate', 'candy', 'sweet', 'dessert']):
        # Chocolate: 2g protein, 15g carbs, 9g fat per oz
        macros['protein'] += 2 * portion_multiplier
        macros['carbs'] += 15 * portion_multiplier
        macros['fat'] += 9 * portion_multiplier
        macros['sugar'] += 12 * portion_multiplier
    
    # Round all values
    for key in macros:
        macros[key] = round(macros[key], 1)
    
    # Ensure minimum values for realism
    if macros['protein'] == 0 and any(word in food_lower for word in ['egg', 'meat', 'chicken', 'fish', 'cheese']):
        macros['protein'] = 5
    if macros['carbs'] == 0 and any(word in food_lower for word in ['bread', 'rice', 'fruit', 'sugar', 'pasta']):
        macros['carbs'] = 10
    if macros['fat'] == 0 and any(word in food_lower for word in ['butter', 'oil', 'fried', 'cheese', 'nuts']):
        macros['fat'] = 5
    
    return macros, calories

def estimate_calories(food_description):
    """Rough calorie estimation based on keywords"""
    food_lower = food_description.lower()
    
    # Common food calorie estimates
    calories = 0
    
    if 'egg' in food_lower:
        calories += 70 * (2 if 'eggs' in food_lower or '2' in food_lower else 1)
    if 'toast' in food_lower or 'bread' in food_lower:
        calories += 80 * (2 if 'slices' in food_lower or '2' in food_lower else 1)
    if 'butter' in food_lower or 'lurpak' in food_lower:
        calories += 100
    if any(m in food_lower for m in ['ham', 'bacon']):
        calories += 50
    if 'cheese' in food_lower:
        calories += 100
    if any(m in food_lower for m in ['latte', 'coffee', 'cafe']):
        calories += 50  # With milk
    if 'sugar' in food_lower:
        calories += 20
    if any(f in food_lower for f in ['apple', 'banana', 'fruit']):
        calories += 80
    if 'nuts' in food_lower:
        calories += 170
    if any(m in food_lower for m in ['biryani', 'rice', 'pasta']):
        calories += 400
    if 'chocolate' in food_lower:
        calories += 150
    if 'curry' in food_lower or 'masala' in food_lower:
        calories += 350
    
    if calories == 0:
        # Generic estimate if no keywords match
        calories = 250
    
    return calories

def try_edamam_api(food_text):
    """Try to get nutrition from Edamam API"""
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
                        'edamam_success': True
                    }
                    
        except Exception:
            continue
    
    return None

def log_meal(meal_type, food_items, calories=None):
    """
    Log a meal to Airtable with macro estimation
    
    Args:
        meal_type: Breakfast, Lunch, Dinner, Snack
        food_items: Description of food
        calories: Optional calorie estimate (will estimate if not provided)
    """
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{FOOD_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try Edamam API first
    edamam_data = try_edamam_api(food_items)
    
    if edamam_data:
        # Use Edamam data
        macros = {
            'calories': edamam_data['calories'],
            'protein': edamam_data['protein'],
            'carbs': edamam_data['carbs'],
            'fat': edamam_data['fat'],
            'fiber': edamam_data['fiber'],
            'sugar': edamam_data['sugar']
        }
        edamam_flag = True
        source_note = "Macros from Edamam API"
    else:
        # Fall back to manual estimation
        macros, estimated_calories = estimate_macros_manual(food_items, calories)
        macros['calories'] = calories if calories else estimated_calories
        edamam_flag = False
        source_note = "Macros estimated (Edamam pending)"
    
    record = {
        "fields": {
            "Date": datetime.now().strftime('%Y-%m-%d'),
            "Meal Type": meal_type,
            "Food Items": food_items,
            "Calories": macros['calories'],
            "Protein (g)": macros['protein'],
            "Carbs (g)": macros['carbs'],
            "Fat (g)": macros['fat'],
            "Fiber (g)": macros['fiber'],
            "Sugar (g)": macros['sugar'],
            "Edamam Data": edamam_flag,
            "Notes": source_note
        }
    }
    
    response = requests.post(url, headers=headers, json=record)
    
    if response.status_code == 200:
        return True, f"✅ Logged: {macros['calories']} cal | P:{macros['protein']}g C:{macros['carbs']}g F:{macros['fat']}g | {'Edamam' if edamam_flag else 'Estimated'}"
    else:
        return False, f"❌ Error: {response.status_code}"

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
        print("Examples:")
        print('  python3 quick_food_log.py "Breakfast" "2 eggs, toast, coffee"')
        print('  python3 quick_food_log.py "Lunch" "Chicken salad" 450')
