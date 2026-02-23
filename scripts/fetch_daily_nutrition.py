#!/usr/bin/env python3
"""Fetch daily nutrition data from D1"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_daily_nutrition():
    """Fetch nutrition data from D1 for last 7 days"""
    client = D1Client()
    
    # Get last 7 days
    dates = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
    
    all_meals = []
    daily_totals = {}
    
    for date in dates:
        try:
            meals = client.get_nutrition(date)
            day_calories = 0
            for meal in meals:
                calories = meal.get('calories') or 0
                day_calories += calories
                all_meals.append({
                    'date': meal.get('date'),
                    'meal_type': meal.get('meal_type'),
                    'description': meal.get('description'),
                    'calories': calories
                })
            daily_totals[date] = day_calories
        except Exception as e:
            print(f"Error fetching {date}: {e}")
            daily_totals[date] = 0
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'meals': all_meals,
        'daily_totals': daily_totals
    }
    
    # Save to file
    output_file = Path(__file__).parent.parent / "data" / "nutrition_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    total_meals = len(all_meals)
    total_cals = sum(daily_totals.values())
    print(f"✅ Daily nutrition data saved: {total_meals} meals, {total_cals} calories")
    return data

if __name__ == "__main__":
    fetch_daily_nutrition()
