#!/usr/bin/env python3
"""
Fetch Work Tasks data from D1 for Mission Control
Updated to use Cloudflare D1 instead of Airtable
"""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from d1_client import D1Client

def fetch_work_data():
    """Fetch tasks from D1 and format for Mission Control"""
    client = D1Client()
    
    try:
        # Get all tasks from D1
        tasks = client.get_tasks()
        
        work_tasks = []
        
        for task in tasks:
            # Map D1 task to work_data format
            work_tasks.append({
                "id": task.get("id", ""),
                "name": task.get("task_name", ""),
                "detail": task.get("notes", ""),
                "type": "Task",
                "tat": task.get("category", 7),
                "due_date": task.get("due_date", ""),
                "category": "General",
                "source": "D1",
                "project": "N/A",
                "stakeholder": "Me",
                "assigned": "Me",
                "status": task.get("status", "Not Started"),
                "priority": task.get("priority", "Medium"),
                "effort": "Small",
                "blocked_reason": "",
                "created": task.get("date_created", "")
            })
        
        # Structure matches work_data.json
        data = {
            "generated_at": datetime.now().isoformat(),
            "tasks": work_tasks,
            "projects": [],
            "deliverables": [],
            "total_tasks": len(work_tasks)
        }
        
        # Save to file
        output_file = Path(__file__).parent.parent / "mission-control" / "data" / "work_data.json"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(json.dumps(data, indent=2))
        
        print(f"✅ Work data saved: {len(work_tasks)} tasks")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching work data: {e}")
        return {"tasks": [], "projects": [], "deliverables": []}

if __name__ == "__main__":
    fetch_work_data()
