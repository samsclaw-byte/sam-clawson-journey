#!/usr/bin/env python3
"""Fetch daily nutrition data (meals + macros) for last 7 days"""

import requests
import json
import urllib.parse
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"

def fetch_daily_nutrition():
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
    
    # Calculate last 7 days
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    for date in dates:
        data = {
            'date': date,
            'meals': [],
            'total_calories': 0,
            'macros': {'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
        }
        
        try:
            # Fetch meals for this date
            formula = urllib.parse.quote(f"IS_SAME(Date, '{date}', 'day')")
            resp = requests.get(
                f"{food_url}?filterByFormula={formula}&sort[0][field]=Meal Type",
                headers=headers,
                timeout=30
            )
            
            if resp.status_code == 200:
                records = resp.json().get('records', [])
                
                for r in records:
                    f = r['fields']
                    meal = {
                        'type': f.get('Meal Type', 'Snack'),
                        'items': f.get('Food Items', '')[:60] + ('...' if len(f.get('Food Items', '')) > 60 else ''),
                        'calories': f.get('Calories', 0) or 0
                    }
                    data['meals'].append(meal)
                    data['total_calories'] += meal['calories']
                    
                    # Accumulate macros
                    data['macros']['protein'] += f.get('Protein (g)', 0) or 0
                    data['macros']['carbs'] += f.get('Carbs (g)', 0) or 0
                    data['macros']['fat'] += f.get('Fat (g)', 0) or 0
                    data['macros']['fiber'] += f.get('Fiber (g)', 0) or 0
                
                # Round macros
                data['macros'] = {k: round(v, 1) for k, v in data['macros'].items()}
                
                print(f"  {date}: {len(data['meals'])} meals, {data['total_calories']} calories")
            else:
                print(f"  {date}: Error {resp.status_code}")
                
        except Exception as e:
            print(f"  {date}: Error - {e}")
        
        # Save to file
        with open(f'/home/samsclaw/.openclaw/workspace/data/daily_nutrition_{date}.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    print(f"\n✅ Daily nutrition data saved for {len(dates)} days")
    return True

if __name__ == "__main__":
    fetch_daily_nutrition()
