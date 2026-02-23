#!/usr/bin/env python3
"""Check habits from D1"""

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

HABITS = ['Water', 'Multivitamin', 'Fruit', 'Exercise', 'Sleep']

def check_habits(date=None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    client = D1Client()
    
    try:
        habits = client.get_habits(date)
    except Exception as e:
        print(f"Error fetching habits: {e}")
        habits = []
    
    completed = {}
    for habit in HABITS:
        completed[habit] = any(
            h.get('habit_name') == habit and h.get('completed') == 1 
            for h in habits
        )
    
    return {
        'date': date,
        'habits': completed,
        'all_complete': all(completed.values())
    }

def log_habit(habit_name, date=None, completed=True):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Logged: {habit_name} ({date}) - {'✅' if completed else '❌'}")

if __name__ == "__main__":
    result = check_habits()
    print(f"\n📋 Habits for {result['date']}:")
    for habit, done in result['habits'].items():
        status = "✅" if done else "❌"
        print(f"  {status} {habit}")
