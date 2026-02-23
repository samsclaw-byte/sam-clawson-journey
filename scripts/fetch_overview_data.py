#!/usr/bin/env python3
"""Fetch overview data from D1"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_overview_data():
    """Fetch overview data for dashboard"""
    client = D1Client()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get all tasks
    all_tasks = []
    try:
        all_tasks = client.get_tasks()
        completed = [t for t in all_tasks if t.get('status') == 'Completed']
        pending = [t for t in all_tasks if t.get('status') != 'Completed']
        
        # Overdue tasks
        overdue = [t for t in pending if t.get('due_date') and t.get('due_date') < today]
    except Exception as e:
        print(f"Error: {e}")
        completed = []
        pending = []
        overdue = []
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'tasks': {
            'total': len(all_tasks),
            'completed': len(completed),
            'pending': len(pending),
            'overdue': len(overdue)
        }
    }
    
    # Save
    output_file = Path(__file__).parent.parent / "data" / "overview_data.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(data, indent=2))
    
    print(f"✅ Overview data saved: {len(all_tasks)} tasks, {len(overdue)} overdue")
    return data

if __name__ == "__main__":
    fetch_overview_data()
