#!/usr/bin/env python3
"""
D1 Sync - Replaces Airtable Sync
Fetches data from D1 and updates local JSON files for dashboard

Runs at: 3pm, 8pm, 11pm via cron
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def sync_d1_to_local():
    """Sync D1 data to local files for dashboard"""
    print("=" * 60)
    print("🔄 D1 Sync: Fetching data from Cloudflare D1")
    print("=" * 60)
    
    client = D1Client()
    results = {'nutrition': 0, 'exercise': 0, 'habits': 0, 'tasks': 0}
    
    # Fetch nutrition
    try:
        from datetime import datetime, timedelta
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        all_meals = []
        for date in dates:
            meals = client.get_nutrition(date)
            all_meals.extend(meals)
        
        output = {
            'generated_at': datetime.now().isoformat(),
            'meals': all_meals,
            'daily_totals': {}
        }
        
        # Calculate daily totals
        for meal in all_meals:
            date = meal.get('date')
            if date:
                if date not in output['daily_totals']:
                    output['daily_totals'][date] = 0
                output['daily_totals'][date] += meal.get('calories') or 0
        
        # Save
        output_file = Path(__file__).parent.parent / "data" / "nutrition_data.json"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(json.dumps(output, indent=2))
        results['nutrition'] = len(all_meals)
        print(f"✅ Nutrition: {len(all_meals)} meals synced")
    except Exception as e:
        print(f"❌ Nutrition sync failed: {e}")
    
    # Fetch exercise
    try:
        all_exercise = []
        for date in dates:
            exercises = client.get_exercise(date)
            all_exercise.extend(exercises)
        
        output = {
            'generated_at': datetime.now().isoformat(),
            'exercise': all_exercise,
            'summary': {
                'total_workouts': len(all_exercise),
                'total_minutes': sum(e.get('duration_minutes', 0) or 0 for e in all_exercise),
                'total_strain': sum(e.get('strain', 0) or 0 for e in all_exercise)
            }
        }
        
        output_file = Path(__file__).parent.parent / "data" / "exercise_data.json"
        output_file.write_text(json.dumps(output, indent=2))
        results['exercise'] = len(all_exercise)
        print(f"✅ Exercise: {len(all_exercise)} workouts synced")
    except Exception as e:
        print(f"❌ Exercise sync failed: {e}")
    
    # Fetch habits
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        habits = client.get_habits(today)
        
        output = {
            'generated_at': datetime.now().isoformat(),
            'date': today,
            'habits': {h.get('habit_name'): h.get('completed') == 1 for h in habits}
        }
        
        output_file = Path(__file__).parent.parent / "data" / "habit_tracker.json"
        output_file.write_text(json.dumps(output, indent=2))
        results['habits'] = len(habits)
        print(f"✅ Habits: {len(habits)} habits synced")
    except Exception as e:
        print(f"❌ Habits sync failed: {e}")
    
    # Fetch tasks
    try:
        tasks = client.get_tasks()
        pending = [t for t in tasks if t.get('status') != 'Completed']
        
        output = {
            'generated_at': datetime.now().isoformat(),
            'total_tasks': len(tasks),
            'pending_tasks': len(pending),
            'tasks': pending[:10]
        }
        
        output_file = Path(__file__).parent.parent / "data" / "tasks_data.json"
        output_file.write_text(json.dumps(output, indent=2))
        results['tasks'] = len(pending)
        print(f"✅ Tasks: {len(pending)} pending tasks synced")
    except Exception as e:
        print(f"❌ Tasks sync failed: {e}")
    
    print(f"\n✅ D1 Sync complete! {results}")
    return results

if __name__ == "__main__":
    sync_d1_to_local()
