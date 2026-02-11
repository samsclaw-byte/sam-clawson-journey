#!/usr/bin/env python3
"""
Nutrition Tracker - Edamam API Integration
Analyzes food descriptions and returns nutrition data.
"""

import os
import sys
import json
import urllib.parse
import urllib.request

# Load credentials from .env file manually
def load_env(filepath):
    env = {}
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key] = value
    except FileNotFoundError:
        pass
    return env

env_vars = load_env('/home/samsclaw/.openclaw/workspace/.env')
APP_ID = env_vars.get('EDAMAM_APP_ID')
API_KEY = env_vars.get('EDAMAM_API_KEY')
BASE_URL = 'https://api.edamam.com/api/nutrition-data'

def analyze_food(food_description):
    """Analyze food and return nutrition data."""
    
    if not APP_ID or not API_KEY:
        return {"error": "Missing Edamam credentials in .env file"}
    
    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'nutrition-type': 'cooking',
        'ingr': food_description
    }
    
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            # Edamam returns nutrients in ingredients array - sum all parsed items
            ingredients = data.get('ingredients', [])
            if not ingredients:
                return {"error": "Could not parse food", "raw": data}
            
            # Aggregate nutrients from all parsed ingredients
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
            
            nutrients = all_nutrients
            
            result = {
                "food": food_description,
                "timestamp": __import__('datetime').datetime.now().isoformat(),
                "foods_parsed": foods_found,
                # Macros
                "calories": round(all_nutrients.get('ENERC_KCAL', 0)),
                "protein_g": round(all_nutrients.get('PROCNT', 0), 1),
                "carbs_g": round(all_nutrients.get('CHOCDF', 0), 1),
                "carbs_net_g": round(all_nutrients.get('CHOCDF.net', 0), 1),
                "fat_g": round(all_nutrients.get('FAT', 0), 1),
                "fiber_g": round(all_nutrients.get('FIBTG', 0), 1),
                "sugar_g": round(all_nutrients.get('SUGAR', 0), 1),
                "sugar_added_g": round(all_nutrients.get('SUGAR.added', 0), 1),
                # Fats breakdown
                "fat_saturated_g": round(all_nutrients.get('FASAT', 0), 1),
                "fat_trans_g": round(all_nutrients.get('FATRN', 0), 1),
                "fat_mono_g": round(all_nutrients.get('FAMS', 0), 1),
                "fat_poly_g": round(all_nutrients.get('FAPU', 0), 1),
                # Minerals
                "sodium_mg": round(all_nutrients.get('NA', 0)),
                "calcium_mg": round(all_nutrients.get('CA', 0)),
                "iron_mg": round(all_nutrients.get('FE', 0), 1),
                "magnesium_mg": round(all_nutrients.get('MG', 0)),
                "potassium_mg": round(all_nutrients.get('K', 0)),
                "zinc_mg": round(all_nutrients.get('ZN', 0), 1),
                "phosphorus_mg": round(all_nutrients.get('P', 0)),
                "cholesterol_mg": round(all_nutrients.get('CHOLE', 0)),
                # Vitamins
                "vitamin_a_ug": round(all_nutrients.get('VITA_RAE', 0), 1),
                "vitamin_c_mg": round(all_nutrients.get('VITC', 0), 1),
                "vitamin_d_ug": round(all_nutrients.get('VITD', 0), 1),
                "vitamin_e_mg": round(all_nutrients.get('TOCPHA', 0), 1),
                "vitamin_k_ug": round(all_nutrients.get('VITK1', 0), 1),
                "thiamin_mg": round(all_nutrients.get('THIA', 0), 2),
                "riboflavin_mg": round(all_nutrients.get('RIBF', 0), 2),
                "niacin_mg": round(all_nutrients.get('NIA', 0), 1),
                "vitamin_b6_mg": round(all_nutrients.get('VITB6A', 0), 2),
                "folate_ug": round(all_nutrients.get('FOLDFE', 0)),
                "vitamin_b12_ug": round(all_nutrients.get('VITB12', 0), 2),
                "water_g": round(all_nutrients.get('WATER', 0), 1),
                # Metadata
                "weight_g": round(total_weight, 1),
                "raw": data
            }
            
            return result
            
    except urllib.error.HTTPError as e:
        return {"error": f"API error: {e.code} - {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

def format_nutrition(result, detailed=False):
    """Format nutrition data for display."""
    
    if "error" in result:
        return f"❌ {result['error']}"
    
    foods = ", ".join(result.get('foods_parsed', ['unknown']))
    basic = f"""🍽️ **{result['food']}**
Parsed: {foods} ({result.get('weight_g', '?')}g total)

**Calories:** {result['calories']} kcal
**Protein:** {result['protein_g']}g
**Carbs:** {result['carbs_g']}g (Net: {result.get('carbs_net_g', 0)}g)
**Fat:** {result['fat_g']}g
**Fiber:** {result['fiber_g']}g
**Sugar:** {result['sugar_g']}g"""

    if not detailed:
        return basic
    
    detailed_info = f"""
**Fats Breakdown:**
  Saturated: {result.get('fat_saturated_g', 0)}g | Trans: {result.get('fat_trans_g', 0)}g
  Mono: {result.get('fat_mono_g', 0)}g | Poly: {result.get('fat_poly_g', 0)}g

**Minerals:**
  Sodium: {result['sodium_mg']}mg | Calcium: {result.get('calcium_mg', 0)}mg
  Iron: {result.get('iron_mg', 0)}mg | Magnesium: {result.get('magnesium_mg', 0)}mg
  Potassium: {result.get('potassium_mg', 0)}mg | Zinc: {result.get('zinc_mg', 0)}mg
  Phosphorus: {result.get('phosphorus_mg', 0)}mg | Cholesterol: {result.get('cholesterol_mg', 0)}mg

**Vitamins:**
  A: {result.get('vitamin_a_ug', 0)}µg | C: {result.get('vitamin_c_mg', 0)}mg | D: {result.get('vitamin_d_ug', 0)}µg
  E: {result.get('vitamin_e_mg', 0)}mg | K: {result.get('vitamin_k_ug', 0)}µg
  B1 (Thiamin): {result.get('thiamin_mg', 0)}mg | B2 (Riboflavin): {result.get('riboflavin_mg', 0)}mg
  B3 (Niacin): {result.get('niacin_mg', 0)}mg | B6: {result.get('vitamin_b6_mg', 0)}mg
  B9 (Folate): {result.get('folate_ug', 0)}µg | B12: {result.get('vitamin_b12_ug', 0)}µg"""
    
    return basic + detailed_info

def analyze_multiple(foods):
    """Analyze multiple food items and return aggregated results."""
    results = []
    total = {
        "foods": [],
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "carbs_net_g": 0,
        "fat_g": 0,
        "fiber_g": 0,
        "sugar_g": 0,
        "sodium_mg": 0
    }
    
    for food in foods:
        food = food.strip()
        if not food:
            continue
        result = analyze_food(food)
        if "error" not in result:
            results.append(result)
            total["foods"].append(food)
            total["calories"] += result["calories"]
            total["protein_g"] += result["protein_g"]
            total["carbs_g"] += result["carbs_g"]
            total["carbs_net_g"] += result["carbs_net_g"]
            total["fat_g"] += result["fat_g"]
            total["fiber_g"] += result["fiber_g"]
            total["sugar_g"] += result["sugar_g"]
            total["sodium_mg"] += result["sodium_mg"]
    
    return results, total

def format_totals(total):
    """Format daily totals."""
    foods = ", ".join(total["foods"])
    return f"""
📊 **MEAL TOTAL** ({len(total['foods'])} items)
{foods}

**Calories:** {round(total['calories'])} kcal
**Protein:** {round(total['protein_g'], 1)}g
**Carbs:** {round(total['carbs_g'], 1)}g (Net: {round(total['carbs_net_g'], 1)}g)
**Fat:** {round(total['fat_g'], 1)}g
**Fiber:** {round(total['fiber_g'], 1)}g
**Sugar:** {round(total['sugar_g'], 1)}g
**Sodium:** {round(total['sodium_mg'])}mg"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single item:  python3 nutrition_tracker.py '2 eggs'")
        print("  Multiple:     python3 nutrition_tracker.py --multi 'eggs' 'toast' 'avocado'")
        sys.exit(1)
    
    if sys.argv[1] == '--multi':
        # Multiple items mode
        foods = sys.argv[2:]
        results, total = analyze_multiple(foods)
        for r in results:
            print(format_nutrition(r))
            print()
        print(format_totals(total))
    else:
        # Single item mode
        food = ' '.join(sys.argv[1:])
        result = analyze_food(food)
        print(format_nutrition(result))
        
        # Output JSON for integration with other tools
        print("\n---JSON---")
        print(json.dumps(result, indent=2))
