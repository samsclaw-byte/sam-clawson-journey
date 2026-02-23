#!/usr/bin/env python3
"""Fetch productivity data from D1"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_productivity_data():
    """Fetch productivity metrics"""
    client = D1Client()
    
    # Last 7 days
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    daily_stats = []
    
    for date in dates:
        # Tasks completed
        try:
            tasks = client.get_tasks()
            tasks_completed = [t for t in tasks if t.get('status') == 'Completed' and t.get('date_completed') == date]
        except:
            tasks_completed = []
        
        # Exercise
        try:
            exercise = client.get_exercise(date)
            has_exercise = len(exercise) > 0
            total_mins = sum(e.get('duration_minutes', 0) or 0 for e in exercise)
        except:
            has_exercise = False
            total_mins = 0
        
        # Habits
        try:
            habits = client.get_habits(date)
            habits_done = sum(1 for h in habits if h.get('completed') == 1)
        except:
            habits_done = 0
        
        daily_stats.append({
            'date': date,
            'tasks_completed': len(tasks_completed),
            'exercise': has_exercise,
            'exercise_minutes': total_mins,
            'habits_done': habits_done
        })
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'daily': daily_stats
    }
    
    # Save
    output_file = Path(__file__).parent.parent / "data" / "productivity_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Productivity data saved")
    return data

if __name__ == "__main__":
    fetch_productivity_data()
