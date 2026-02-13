#!/usr/bin/env python3
"""
Fetch real data from Airtable for Mission Control
Queries: Food Log, Daily Habits, Weight, Workouts, WHOOP
"""

import requests
import json
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def fetch_airtable_data():
    """Fetch all data from Airtable"""
    data = {
        "today": {},
        "last_7_days": [],
        "generated_at": datetime.now().isoformat()
    }
    
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Calculate date range
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    print(f"Fetching data from {week_ago} to {today}")
    
    # 1. Fetch Food Log for today
    try:
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
        response = requests.get(
            f"{url}?filterByFormula=Date='{today}'",
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            meals = response.json().get('records', [])
            data['today']['meals'] = []
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fat = 0
            total_fiber = 0
            
            for meal in meals:
                f = meal['fields']
                data['today']['meals'].append({
                    'type': f.get('Meal Type', ''),
                    'items': f.get('Food Items', '')[:50],
                    'calories': f.get('Calories', 0),
                    'protein': f.get('Protein (g)', 0),
                    'carbs': f.get('Carbs (g)', 0),
                    'fat': f.get('Fat (g)', 0),
                    'fiber': f.get('Fiber (g)', 0)
                })
                total_calories += f.get('Calories', 0) or 0
                total_protein += f.get('Protein (g)', 0) or 0
                total_carbs += f.get('Carbs (g)', 0) or 0
                total_fat += f.get('Fat (g)', 0) or 0
                total_fiber += f.get('Fiber (g)', 0) or 0
            
            data['today']['total_calories'] = total_calories
            data['today']['macros'] = {
                'protein': round(total_protein, 1),
                'carbs': round(total_carbs, 1),
                'fat': round(total_fat, 1),
                'fiber': round(total_fiber, 1)
            }
            print(f"✅ Food Log: {len(meals)} meals, {total_calories} calories")
    except Exception as e:
        print(f"❌ Food Log error: {e}")
        data['today']['meals'] = []
        data['today']['total_calories'] = 0
        data['today']['macros'] = {'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
    
    # 2. Fetch Daily Habits for today
    try:
        url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
        response = requests.get(
            f"{url}?filterByFormula=Date='{today}'",
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            habits = response.json().get('records', [])
            if habits:
                f = habits[0]['fields']
                data['today']['habits'] = {
                    'multivitamin': f.get('Multivitamin', False),
                    'fruit': f.get('Fruit', False),
                    'water': f.get('Water', 0),
                    'exercise': f.get('Exercise', False),
                    'creatine': f.get('Creatine', False)
                }
                print(f"✅ Daily Habits: Water {f.get('Water', 0)}/8")
            else:
                data['today']['habits'] = {'multivitamin': False, 'fruit': False, 'water': 0, 'exercise': False, 'creatine': False}
    except Exception as e:
        print(f"❌ Daily Habits error: {e}")
        data['today']['habits'] = {'multivitamin': False, 'fruit': False, 'water': 0, 'exercise': False, 'creatine': False}
    
    # 3. Fetch last 7 days data
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        day_data = {'date': date, 'calories_burned': 0, 'calories_consumed': 0, 'strain': 0, 'weight': None, 'sleep': 0}
        
        # Food for this day
        try:
            url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                meals = response.json().get('records', [])
                day_data['calories_consumed'] = sum(m['fields'].get('Calories', 0) or 0 for m in meals)
        except:
            pass
        
        # WHOOP data for this day (from WHOOP table)
        try:
            url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblUpFFMXvJSHCKXk"
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                whoop = response.json().get('records', [])
                if whoop:
                    f = whoop[0]['fields']
                    day_data['calories_burned'] = f.get('Calories Burned', 0) or 0
                    day_data['strain'] = f.get('Strain', 0) or 0
                    day_data['sleep'] = f.get('Sleep Performance', 0) or 0
        except:
            pass
        
        # Weight for this day
        try:
            url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblD8WM0uTqIzFR7E"
            response = requests.get(
                f"{url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                weights = response.json().get('records', [])
                if weights:
                    day_data['weight'] = weights[0]['fields'].get('Weight (kg)', None)
        except:
            pass
        
        # Calculate net calories
        day_data['net_calories'] = day_data['calories_consumed'] - day_data['calories_burned']
        
        data['last_7_days'].append(day_data)
    
    print(f"✅ Last 7 days data fetched")
    
    # 4. Aggregate exercise data for last 7 days
    try:
        url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblB5xwGlKoaaq4qO"  # Workouts table
        response = requests.get(
            f"{url}?filterByFormula=AND(IS_AFTER(Date, '{week_ago}'), IS_BEFORE(Date, '{today}'))",
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            workouts = response.json().get('records', [])
            exercise_types = {}
            total_minutes = 0
            total_strain = 0
            
            for w in workouts:
                f = w['fields']
                workout_type = f.get('Type', 'Other')
                duration = f.get('Duration (min)', 0) or 0
                strain = f.get('Strain', 0) or 0
                
                if workout_type not in exercise_types:
                    exercise_types[workout_type] = {'minutes': 0, 'count': 0}
                exercise_types[workout_type]['minutes'] += duration
                exercise_types[workout_type]['count'] += 1
                
                total_minutes += duration
                total_strain += strain
            
            data['exercise_7_days'] = {
                'types': exercise_types,
                'total_minutes': total_minutes,
                'total_strain': round(total_strain, 1),
                'workout_count': len(workouts)
            }
            print(f"✅ Exercise: {len(workouts)} workouts, {total_minutes} minutes")
        else:
            data['exercise_7_days'] = {'types': {}, 'total_minutes': 0, 'total_strain': 0, 'workout_count': 0}
    except Exception as e:
        print(f"❌ Exercise error: {e}")
        data['exercise_7_days'] = {'types': {}, 'total_minutes': 0, 'total_strain': 0, 'workout_count': 0}
    
    return data

if __name__ == "__main__":
    data = fetch_airtable_data()
    
    # Save to JSON file for the HTML to use
    with open('/home/samsclaw/.openclaw/workspace/data/mission_control_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n✅ Data saved to mission_control_data.json")
    print(f"Total calories today: {data['today']['total_calories']}")
    print(f"Water today: {data['today']['habits']['water']}/8")
    print(f"Workouts (7 days): {data['exercise_7_days']['workout_count']}")
