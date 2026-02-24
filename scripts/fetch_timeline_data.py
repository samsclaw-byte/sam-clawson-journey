#!/usr/bin/env python3
"""Fetch 7-day timeline data from D1 for Mission Control dashboard"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_timeline_data():
    client = D1Client()
    
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    dates.reverse()  # Oldest first
    
    days_data = []
    
    for date in dates:
        day_data = {
            'date': date,
            'calories_burned': 0,
            'calories_consumed': 0,
            'strain': 0,
            'weight': None,
            'sleep': 0
        }
        
        # Get calories consumed from nutrition
        try:
            meals = client.get_nutrition(date)
            total_cals = sum(meal.get('calories', 0) or 0 for meal in meals)
            day_data['calories_consumed'] = total_cals
        except:
            pass
        
        # Get exercise/strain from exercise
        try:
            exercises = client.get_exercise(date)
            total_strain = sum(ex.get('strain', 0) or 0 for ex in exercises)
            day_data['strain'] = total_strain
        except:
            pass
        
        # Get weight
        try:
            import subprocess
            result = subprocess.run(
                f'wrangler d1 execute trak-db --command="SELECT weight_kg FROM weight WHERE date=\'{date}\'" --remote',
                shell=True, capture_output=True, text=True, timeout=10
            )
            if '"weight_kg":' in result.stdout:
                import re
                match = re.search(r'"weight_kg":\s*(\d+\.?\d*)', result.stdout)
                if match:
                    day_data['weight'] = float(match.group(1))
        except:
            pass
        
        days_data.append(day_data)
        print(f"{date}: {day_data['calories_consumed']} cal consumed, {day_data['strain']} strain")
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'days': days_data
    }
    
    output_file = Path(__file__).parent.parent / "data" / "timeline_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    # Also copy to mission-control
    mc_file = Path(__file__).parent.parent / "mission-control" / "data" / "timeline_data.json"
    mc_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Timeline data updated: {len(days_data)} days")
    return data

if __name__ == "__main__":
    fetch_timeline_data()
