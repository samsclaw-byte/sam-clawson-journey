#!/usr/bin/env python3
"""
Edamam Nutrition API Integration
Fetches accurate nutrition data for meals
"""

import os
import sys
import json
import requests
from pathlib import Path

def get_edamam_credentials():
    """Get Edamam API credentials from config"""
    # Try environment variables first
    app_id = os.getenv('EDAMAM_APP_ID')
    api_key = os.getenv('EDAMAM_API_KEY')
    
    if not app_id or not api_key:
        # Try config file
        config_path = Path.home() / '.config' / 'nutrition' / 'credentials'
        if config_path.exists():
            with open(config_path) as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        if key == 'EDAMAM_APP_ID':
                            app_id = value
                        elif key == 'EDAMAM_APP_KEY':
                            api_key = value
    
    # Fallback to hardcoded (from NUTRITION_API_INFO.md)
    if not app_id:
        app_id = "f4bc1402"
    if not api_key:
        api_key = "6a17caf19f979aebe0f88d0462937a54"
    
    return app_id, api_key

def get_nutrition_data(food_text):
    """Get nutrition data from Edamam API"""
    app_id, api_key = get_edamam_credentials()
    
    url = "https://api.edamam.com/api/nutrition-data"
    
    params = {
        'app_id': app_id,
        'app_key': api_key,
        'ingr': food_text,
        'nutrition-type': 'logging'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching nutrition data: {e}", file=sys.stderr)
        return None

def format_nutrition_output(data, food_text):
    """Format nutrition data for display"""
    if not data or 'ingredients' not in data:
        return f"Could not analyze: {food_text}"
    
    # Extract from first ingredient's parsed data
    try:
        nutrients = data['ingredients'][0]['parsed'][0]['nutrients']
    except (KeyError, IndexError):
        return f"Could not parse: {food_text}"
    
    calories = nutrients.get('ENERC_KCAL', {}).get('quantity', 0)
    protein = nutrients.get('PROCNT', {}).get('quantity', 0)
    carbs = nutrients.get('CHOCDF', {}).get('quantity', 0)
    fat = nutrients.get('FAT', {}).get('quantity', 0)
    fiber = nutrients.get('FIBTG', {}).get('quantity', 0)
    sugar = nutrients.get('SUGAR', {}).get('quantity', 0)
    sodium = nutrients.get('NA', {}).get('quantity', 0) / 1000  # mg to g
    
    output = f"🥗 Nutrition Analysis: {food_text}\n"
    output += "=" * 40 + "\n"
    output += f"Calories: {calories:.0f} kcal\n"
    output += f"Protein: {protein:.1f}g\n"
    output += f"Carbs: {carbs:.1f}g\n"
    output += f"Fat: {fat:.1f}g\n"
    output += f"Fiber: {fiber:.1f}g\n"
    output += f"Sugar: {sugar:.1f}g\n"
    output += f"Sodium: {sodium:.1f}g\n"
    
    return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 edamam_nutrition.py 'food description'")
        print("Example: python3 edamam_nutrition.py '1 cup rice'")
        sys.exit(1)
    
    food_text = sys.argv[1]
    data = get_nutrition_data(food_text)
    
    if data:
        print(format_nutrition_output(data, food_text))
        # Also output JSON for further processing
        print("\n📊 Raw JSON:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed to get nutrition data for: {food_text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
