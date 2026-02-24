#!/usr/bin/env python3
"""Fetch exercise data from D1 - formatted for Mission Control"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_exercise_data():
    client = D1Client()
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    all_exercise = []
    exercise_types = {}
    total_minutes = 0
    total_strain = 0
    workout_count = 0
    
    for date in dates:
        try:
            exercises = client.get_exercise(date)
            for ex in exercises:
                workout_type = ex.get('workout_type', 'Unknown')
                duration = ex.get('duration_minutes', 0) or 0
                strain = ex.get('strain', 0) or 0
                
                # Add to main array (matches page's "workouts" key)
                all_exercise.append({
                    'date': ex.get('date'),
                    'type': workout_type,  # Page expects "type", not "workout_type"
                    'duration': duration,
                    'strain': strain,
                    'exercises': workout_type,  # Also needed
                    'notes': ex.get('notes')
                })
                
                # Build exercise_types (matches page's expected key)
                if workout_type not in exercise_types:
                    exercise_types[workout_type] = {'minutes': 0, 'count': 0}
                exercise_types[workout_type]['minutes'] += duration
                exercise_types[workout_type]['count'] += 1
                
                total_minutes += duration
                total_strain += strain
                workout_count += 1
        except Exception as e:
            pass
    
    # Calculate avg strain
    avg_strain = round(total_strain / workout_count, 1) if workout_count > 0 else 0
    
    # Format matches what health-nutrition.html expects
    data = {
        'generated_at': datetime.now().isoformat(),
        'exercise': all_exercise,  # Keep this too
        'workouts': all_exercise,  # Page expects "workouts"
        'total_minutes': total_minutes,
        'avg_strain': avg_strain,
        'workout_count': workout_count,
        'exercise_types': exercise_types,  # Page expects this key
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
    
    # Also copy to mission-control
    mc_file = Path(__file__).parent.parent / "mission-control" / "data" / "exercise_data.json"
    mc_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Exercise data saved: {workout_count} workouts, {total_minutes} min, strain {round(total_strain, 1)}")
    return data

if __name__ == "__main__":
    fetch_exercise_data()
