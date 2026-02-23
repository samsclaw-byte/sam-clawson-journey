#!/usr/bin/env python3
"""Fetch extended trend data for Mission Control Overview page - D1 Version"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_nutrition_trends():
    """Fetch last 30 days of nutrition data from D1"""
    client = D1Client()
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    all_meals = []
    daily_totals = {}
    
    for date in dates:
        meals = client.get_nutrition(date)
        day_cals = 0
        for meal in meals:
            cals = meal.get('calories') or 0
            day_cals += cals
            all_meals.append({
                'date': date,
                'meal_type': meal.get('meal_type'),
                'description': meal.get('description'),
                'calories': cals
            })
        if day_cals > 0:
            daily_totals[date] = day_cals
    
    return {
        'meals': all_meals,
        'daily_totals': daily_totals,
        'avg_daily_cals': sum(daily_totals.values()) / max(len(daily_totals), 1)
    }

def fetch_exercise_trends():
    """Fetch exercise data from D1"""
    client = D1Client()
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    workouts = []
    total_strain = 0
    total_minutes = 0
    
    for date in dates:
        exercises = client.get_exercise(date)
        for ex in exercises:
            strain = ex.get('strain') or 0
            duration = ex.get('duration_minutes') or 0
            workouts.append({
                'date': date,
                'type': ex.get('workout_type'),
                'strain': strain,
                'duration': duration
            })
            total_strain += strain
            total_minutes += duration
    
    return {
        'workouts': workouts,
        'total_workouts': len(workouts),
        'total_minutes': total_minutes,
        'total_strain': round(total_strain, 1)
    }

def fetch_habit_trends():
    """Fetch habit data from D1"""
    client = D1Client()
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    habit_stats = {}
    for date in dates:
        habits = client.get_habits(date)
        completed = sum(1 for h in habits if h.get('completed') == 1)
        total = len(habits)
        if total > 0:
            habit_stats[date] = {'completed': completed, 'total': total, 'pct': round(completed/total*100)}
    
    return {'habit_stats': habit_stats}

def fetch_trend_data():
    """Main function to fetch all trend data"""
    print("Fetching trend data from D1...")
    
    nutrition = fetch_nutrition_trends()
    exercise = fetch_exercise_trends()
    habits = fetch_habit_trends()
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'nutrition': nutrition,
        'exercise': exercise,
        'habits': habits
    }
    
    output_file = Path(__file__).parent.parent / "mission-control" / "data" / "trend_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Trend data saved: {len(nutrition.get('meals', []))} meals, {exercise.get('total_workouts', 0)} workouts")
    return data

if __name__ == "__main__":
    fetch_trend_data()
