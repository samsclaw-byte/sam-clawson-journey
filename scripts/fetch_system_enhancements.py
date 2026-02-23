#!/usr/bin/env python3
"""
Fetch System Enhancement tasks from D1 for Mission Control architecture page.
Updated to use Cloudflare D1 instead of Airtable
"""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_system_enhancements():
    """Fetch tasks from D1 for system enhancements"""
    client = D1Client()
    
    try:
        tasks = client.get_tasks()
        
        # Filter for system-related tasks
        system_keywords = ['system', 'automation', 'cron', 'workflow', 'setup', 'configure', 'deploy', 'worker', 'infrastructure']
        
        enhancements = []
        for task in tasks:
            task_name = task.get('task_name', '').lower()
            if any(kw in task_name for kw in system_keywords):
                enhancements.append({
                    'id': task.get('id'),
                    'name': task.get('task_name'),
                    'status': task.get('status', 'Not Started'),
                    'priority': task.get('priority', 'Medium'),
                    'category': task.get('category'),
                    'due_date': task.get('due_date')
                })
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'enhancements': enhancements,
            'total': len(enhancements)
        }
        
        output_file = Path(__file__).parent.parent / "mission-control" / "data" / "system_enhancements.json"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(json.dumps(data, indent=2))
        
        print(f"✅ System enhancements saved: {len(enhancements)} tasks")
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'enhancements': [], 'total': 0}

if __name__ == "__main__":
    fetch_system_enhancements()
