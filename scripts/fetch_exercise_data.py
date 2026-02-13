#!/usr/bin/env python3
"""Fetch exercise data from Airtable for Mission Control dashboard"""

import requests
import json
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
WORKOUTS_TABLE = "tblZzvXBJoKcMtjZU"

def fetch_exercise_data():
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    url = f"https://api.airtable.com/v0/{HEALTH_BASE}/{WORKOUTS_TABLE}"
    
    # Get workouts from last 7 days
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    resp = requests.get(
        f"{url}?filterByFormula=IS_AFTER({{Date}}, '{week_ago}')&maxRecords=50",
        headers=headers,
        timeout=30
    )
    
    if resp.status_code == 200:
        records = resp.json().get('records', [])
        
        exercise_types = {}
        total_minutes = 0
        total_strain = 0
        
        for r in records:
            f = r['fields']
            # Use Exercises field for the workout description
            exercises = f.get('Exercises', f.get('Workout Name', 'Unnamed'))
            workout_type = f.get('Type', 'Other')
            duration = f.get('Duration (min)', 0) or 0
            strain = f.get('Strain', 0) or 0
            
            # Group by exercises (actual workout description)
            if exercises not in exercise_types:
                exercise_types[exercises] = {'minutes': 0, 'count': 0, 'type': workout_type}
            exercise_types[exercises]['minutes'] += duration
            exercise_types[exercises]['count'] += 1
            
            total_minutes += duration
            total_strain += strain
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'workout_count': len(records),
            'total_minutes': total_minutes,
            'avg_strain': round(total_strain / len(records), 1) if records else 0,
            'exercise_types': exercise_types,
            'workouts': [
                {
                    'date': r['fields'].get('Date'),
                    'type': r['fields'].get('Type', 'Other'),
                    'exercises': r['fields'].get('Exercises', r['fields'].get('Workout Name', 'Unnamed')),
                    'duration': r['fields'].get('Duration (min)', 0) or 0,
                    'strain': r['fields'].get('Strain', 0) or 0
                }
                for r in records
            ]
        }
        
        with open('/home/samsclaw/.openclaw/workspace/data/exercise_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Exercise data updated: {len(records)} workouts, {total_minutes} minutes")
        return True
    else:
        print(f"❌ Error fetching exercise data: {resp.status_code}")
        return False

if __name__ == "__main__":
    fetch_exercise_data()
