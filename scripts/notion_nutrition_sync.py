#!/usr/bin/env python3
"""
Nutrition Tracker - Notion Auto-Sync
Analyzes food and logs to Notion automatically
"""

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, date

# Notion config
NOTION_DB_ID = "dc76e804-5b9e-406b-afda-d7a20dd58976"
DATA_SOURCE_ID = "c1d1100c-cbc4-416d-8c1b-59f7e2ff15c0"

def get_env_credentials():
    """Load Edamam credentials from .env file."""
    env_vars = {}
    try:
        with open('/home/samsclaw/.openclaw/workspace/.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        pass
    return env_vars

def analyze_food(food_description):
    """Analyze food using Edamam API."""
    env_vars = get_env_credentials()
    app_id = env_vars.get('EDAMAM_APP_ID')
    api_key = env_vars.get('EDAMAM_API_KEY')
    
    if not app_id or not api_key:
        return {"error": "Missing Edamam credentials"}
    
    params = {
        'app_id': app_id,
        'app_key': api_key,
        'nutrition-type': 'cooking',
        'ingr': food_description
    }
    
    url = f"https://api.edamam.com/api/nutrition-data?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            ingredients = data.get('ingredients', [])
            if not ingredients:
                return {"error": "Could not parse food", "raw": data}
            
            # Aggregate nutrients
            all_nutrients = {}
            total_weight = 0
            foods_found = []
            
            for ing in ingredients:
                if 'parsed' in ing and ing['parsed']:
                    for parsed in ing['parsed']:
                        if parsed.get('status') == 'OK':
                            foods_found.append(parsed.get('foodMatch', 'unknown'))
                            total_weight += parsed.get('weight', 0)
                            nutrients = parsed.get('nutrients', {})
                            for key, nutrient in nutrients.items():
                                if key not in all_nutrients:
                                    all_nutrients[key] = 0
                                all_nutrients[key] += nutrient.get('quantity', 0)
            
            if not all_nutrients:
                return {"error": "Could not parse any ingredients", "raw": data}
            
            return {
                "food": food_description,
                "foods_parsed": foods_found,
                "calories": round(all_nutrients.get('ENERC_KCAL', 0)),
                "protein_g": round(all_nutrients.get('PROCNT', 0), 1),
                "carbs_g": round(all_nutrients.get('CHOCDF', 0), 1),
                "fat_g": round(all_nutrients.get('FAT', 0), 1),
                "fiber_g": round(all_nutrients.get('FIBTG', 0), 1),
                "sugar_g": round(all_nutrients.get('SUGAR', 0), 1),
                "sodium_mg": round(all_nutrients.get('NA', 0)),
                "iron_mg": round(all_nutrients.get('FE', 0), 1),
                "calcium_mg": round(all_nutrients.get('CA', 0)),
                "potassium_mg": round(all_nutrients.get('K', 0)),
                "vitamin_c_mg": round(all_nutrients.get('VITC', 0), 1),
                # Additional micronutrients
                "vitamin_a_ug": round(all_nutrients.get('VITA_RAE', 0), 1),
                "vitamin_d_ug": round(all_nutrients.get('VITD', 0), 1),
                "vitamin_e_mg": round(all_nutrients.get('TOCPHA', 0), 1),
                "vitamin_k_ug": round(all_nutrients.get('VITK1', 0), 1),
                "vitamin_b12_ug": round(all_nutrients.get('VITB12', 0), 2),
                "folate_ug": round(all_nutrients.get('FOLDFE', 0)),
                "magnesium_mg": round(all_nutrients.get('MG', 0)),
                "zinc_mg": round(all_nutrients.get('ZN', 0), 1),
                "phosphorus_mg": round(all_nutrients.get('P', 0)),
                "cholesterol_mg": round(all_nutrients.get('CHOLE', 0)),
                "weight_g": round(total_weight, 1)
            }
            
    except Exception as e:
        return {"error": str(e)}

def notion_api(method, endpoint, data=None):
    """Make Notion API call."""
    notion_key = os.getenv('NOTION_KEY') or subprocess.getoutput('cat ~/.config/notion/api_key').strip()
    
    cmd_parts = [
        'curl', '-s', '-X', method,
        f'https://api.notion.com/v1{endpoint}',
        '-H', f'Authorization: Bearer {notion_key}',
        '-H', 'Notion-Version: 2025-09-03',
        '-H', 'Content-Type: application/json'
    ]
    
    if data:
        cmd_parts.extend(['-d', json.dumps(data)])
    
    result = subprocess.run(cmd_parts, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"error": result.stdout or result.stderr}

def ensure_db_properties():
    """Ensure database has required properties."""
    # Check current properties
    db = notion_api('GET', f'/databases/{NOTION_DB_ID}')
    props = db.get('properties', {})
    
    required = ['Date', 'Meal', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)']  # 'Name' is title property (exists)
    missing = [p for p in required if p not in props]
    
    if missing:
        # Add missing properties
        properties_update = {}
        if 'Date' in missing:
            properties_update['Date'] = {"date": {}}
        if 'Meal' in missing:
            properties_update['Meal'] = {"select": {"options": [
                {"name": "Breakfast", "color": "yellow"},
                {"name": "Lunch", "color": "green"},
                {"name": "Dinner", "color": "blue"},
                {"name": "Snack", "color": "purple"},
                {"name": "Drink", "color": "pink"}
            ]}}
        # Note: Using 'Name' as title property (already exists)
        if 'Calories' in missing:
            properties_update['Calories'] = {"number": {"format": "number"}}
        if 'Protein (g)' in missing:
            properties_update['Protein (g)'] = {"number": {"format": "number"}}
        if 'Carbs (g)' in missing:
            properties_update['Carbs (g)'] = {"number": {"format": "number"}}
        if 'Fat (g)' in missing:
            properties_update['Fat (g)'] = {"number": {"format": "number"}}
        if 'Fiber (g)' not in props:
            properties_update['Fiber (g)'] = {"number": {"format": "number"}}
        if 'Notes' not in props:
            properties_update['Notes'] = {"rich_text": {}}
        
        notion_api('PATCH', f'/databases/{NOTION_DB_ID}', {"properties": properties_update})
        print(f"Added properties: {list(properties_update.keys())}")

def log_meal_to_notion(food_description, meal_type="Snack", notes=""):
    """Analyze food and log to Notion."""
    # Ensure DB has properties
    ensure_db_properties()
    
    # Analyze food
    result = analyze_food(food_description)
    
    if "error" in result:
        return {"error": result["error"]}
    
    # Create Notion entry
    today = str(date.today())
    
    properties = {
        "Date": {"date": {"start": today}},
        "Meal": {"select": {"name": meal_type}},
        "Name": {"title": [{"text": {"content": food_description}}]},
        "Calories": {"number": result["calories"]},
        "Protein (g)": {"number": result["protein_g"]},
        "Carbs (g)": {"number": result["carbs_g"]},
        "Fat (g)": {"number": result["fat_g"]},
        "Fiber (g)": {"number": result["fiber_g"]},
        "Sugar (g)": {"number": result.get("sugar_g", 0)},
        "Sodium (mg)": {"number": result.get("sodium_mg", 0)},
        "Iron (mg)": {"number": result.get("iron_mg", 0)},
        "Calcium (mg)": {"number": result.get("calcium_mg", 0)},
        "Potassium (mg)": {"number": result.get("potassium_mg", 0)},
        "Vitamin C (mg)": {"number": result.get("vitamin_c_mg", 0)},
        # Additional micronutrients
        "Vitamin A (µg)": {"number": result.get("vitamin_a_ug", 0)},
        "Vitamin D (µg)": {"number": result.get("vitamin_d_ug", 0)},
        "Vitamin E (mg)": {"number": result.get("vitamin_e_mg", 0)},
        "Vitamin K (µg)": {"number": result.get("vitamin_k_ug", 0)},
        "Vitamin B12 (µg)": {"number": result.get("vitamin_b12_ug", 0)},
        "Folate (µg)": {"number": result.get("folate_ug", 0)},
        "Magnesium (mg)": {"number": result.get("magnesium_mg", 0)},
        "Zinc (mg)": {"number": result.get("zinc_mg", 0)},
        "Phosphorus (mg)": {"number": result.get("phosphorus_mg", 0)},
        "Cholesterol (mg)": {"number": result.get("cholesterol_mg", 0)},
        "Notes": {"rich_text": [{"text": {"content": notes}}]}
    }
    
    data = notion_api('POST', '/pages', {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": properties
    })
    
    return {
        "notion_result": data,
        "nutrition": result
    }

def format_result(result):
    """Format the result for display."""
    if "error" in result:
        return f"❌ {result['error']}"
    
    if result.get('notion_result', {}).get('object') == 'page':
        nutrition = result['nutrition']
        micros = []
        if nutrition.get('sugar_g', 0) > 0:
            micros.append(f"Sugar: {nutrition['sugar_g']}g")
        if nutrition.get('sodium_mg', 0) > 0:
            micros.append(f"Sodium: {nutrition['sodium_mg']}mg")
        if nutrition.get('iron_mg', 0) > 0:
            micros.append(f"Iron: {nutrition['iron_mg']}mg")
        if nutrition.get('calcium_mg', 0) > 0:
            micros.append(f"Calcium: {nutrition['calcium_mg']}mg")
        if nutrition.get('vitamin_c_mg', 0) > 0:
            micros.append(f"Vit C: {nutrition['vitamin_c_mg']}mg")
        
        micros_str = " | ".join(micros) if micros else ""
        
        return f"""✅ **Logged to Notion!**

🍽️ **{nutrition['food']}**
**Calories:** {nutrition['calories']} kcal
**Protein:** {nutrition['protein_g']}g | **Carbs:** {nutrition['carbs_g']}g | **Fat:** {nutrition['fat_g']}g
**Fiber:** {nutrition['fiber_g']}g
{micros_str}

✓ Macros + Micros synced"""
    else:
        return f"❌ Notion sync failed: {result.get('notion_result', {}).get('message', 'Unknown error')}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 notion_nutrition_sync.py 'food description' [meal_type] [notes]")
        print("Example: python3 notion_nutrition_sync.py 'grilled chicken 200g' Lunch")
        sys.exit(1)
    
    food = sys.argv[1]
    meal_type = sys.argv[2] if len(sys.argv) > 2 else "Snack"
    notes = sys.argv[3] if len(sys.argv) > 3 else ""
    
    result = log_meal_to_notion(food, meal_type, notes)
    print(format_result(result))
