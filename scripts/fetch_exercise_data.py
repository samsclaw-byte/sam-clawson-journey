#!/usr/bin/env python3
"""Fetch exercise data from D1"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_exercise_data():
    client = D1Client()
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    all_exercise = []
    exercise_types = {}
    total_minutes = 0
    total_strain = 0
    workout_count = 0
    
    for date in dates:
        try:
            exercises = client.get_exercise(date)
            for ex in exercises:
                workout_type = ex.get('workout_type', 'Other')
                duration = ex.get('duration_minutes', 0) or 0
                strain = ex.get('strain', 0) or 0
                
                all_exercise.append({
                    'date': ex.get('date'),
                    'workout_type': workout_type,
                    'duration': duration,
                    'strain': strain,
                    'notes': ex.get('notes')
                })
                
                if workout_type not in exercise_types:
                    exercise_types[workout_type] = {'minutes': 0, 'count': 0}
                exercise_types[workout_type]['minutes'] += duration
                exercise_types[workout_type]['count'] += 1
                
                total_minutes += duration
                total_strain += strain
                workout_count += 1
        except Exception as e:
            print(f"Error fetching {date}: {e}")
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'exercise': all_exercise,
        'summary': {
            'total_workouts': workout_count,
            'total_minutes': total_minutes,
            'total_strain': round(total_strain, 1),
            'by_type': exercise_types
        }
    }
    
    output_file = Path(__file__).parent.parent / "data" / "exercise_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Exercise data saved: {workout_count} workouts, {total_minutes} min, strain {round(total_strain, 1)}")
    return data

if __name__ == "__main__":
    fetch_exercise_data()
