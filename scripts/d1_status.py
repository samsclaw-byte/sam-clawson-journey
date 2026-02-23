#!/usr/bin/env python3
"""
Quick D1 Data Viewer
Usage: python3 d1_status.py [table]
Example: python3 d1_status.py tasks
"""

import sys
from scripts.d1_client import D1Client

def show_table(name, client):
    print(f"\n=== {name.upper()} ===")
    
    if name == 'tasks':
        data = client.get_tasks()
        print(f"Total: {len(data)} tasks\n")
        for t in data:
            status = t.get('status', 'N/A')
            name = t.get('task_name', 'Unnamed')
            due = t.get('due_date', 'N/A')
            cat = t.get('category', 'N/A')
            print(f"  [{status}] {name} (Due: {due}, Cat: {cat})")
            
    elif name == 'nutrition':
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
        data = client.get_nutrition(date)
        print(f"Today ({date}): {len(data)} meals\n")
        total_cals = 0
        for n in data:
            cals = n.get('calories') or 0
            total_cals += cals
            print(f"  {n.get('meal_type')}: {n.get('description')} ({cals} cal)")
        print(f"\n  Total: {total_cals} calories")
        
    elif name == 'exercise':
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
        data = client.get_exercise(date)
        print(f"Today ({date}): {len(data)} workouts\n")
        for e in data:
            print(f"  {e.get('workout_type')}: {e.get('duration_minutes')} min, strain {e.get('strain')}")
            
    elif name == 'habits':
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
        data = client.get_habits(date)
        print(f"Today ({date}): {len(data)} habits logged\n")
        for h in data:
            status = "✅" if h.get('completed') else "❌"
            print(f"  {status} {h.get('habit_name')}")
            
    else:
        print(f"Unknown table: {name}")
        print("Available: tasks, nutrition, exercise, habits")

if __name__ == "__main__":
    client = D1Client()
    
    if len(sys.argv) < 2:
        print("D1 Status Viewer")
        print("Usage: python3 d1_status.py [table]")
        print("Tables: tasks, nutrition, exercise, habits")
        print("\nShowing all...")
        show_table('tasks', client)
        show_table('nutrition', client)
        show_table('exercise', client)
        show_table('habits', client)
    else:
        show_table(sys.argv[1], client)
