#!/usr/bin/env python3
"""Fetch mission control data from D1"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_mission_control_data():
    """Fetch all data for Mission Control dashboard"""
    client = D1Client()
    
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Get tasks
    try:
        all_tasks = client.get_tasks()
        pending_tasks = [t for t in all_tasks if t.get('status') != 'Completed']
        pending_tasks.sort(key=lambda x: x.get('due_date', ''))
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        pending_tasks = []
    
    # Get nutrition
    try:
        nutrition = client.get_nutrition(today)
        today_cals = sum(n.get('calories', 0) or 0 for n in nutrition)
    except:
        today_cals = 0
    
    # Get exercise
    try:
        exercise = client.get_exercise(today)
        today_exercise = exercise[0] if exercise else None
    except:
        today_exercise = None
    
    # Get habits
    try:
        habits = client.get_habits(today)
        habits_completed = sum(1 for h in habits if h.get('completed') == 1)
    except:
        habits_completed = 0
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'date': today,
        'tasks': {
            'pending': len(pending_tasks),
            'next_due': pending_tasks[0]['task_name'] if pending_tasks else None
        },
        'nutrition': {
            'today_calories': today_cals
        },
        'exercise': today_exercise,
        'habits': {
            'completed': habits_completed,
            'total': 5
        }
    }
    
    # Save
    output_file = Path(__file__).parent.parent / "data" / "mission_control_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Mission Control data saved")
    return data

if __name__ == "__main__":
    fetch_mission_control_data()
