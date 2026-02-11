#!/usr/bin/env python3
"""
Update Notion TAT System from natural language
Parses TAT updates and updates Notion database
"""

import os
import re
import requests
from datetime import datetime

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
if not NOTION_API_KEY:
    try:
        with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
            NOTION_API_KEY = f.read().strip()
    except FileNotFoundError:
        print("❌ Notion API key not found")
        exit(1)

# TAT Database ID (corrected)
TAT_DB_ID = "2fcf2cb1-2276-8111-9bdc-000b11c351d8"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

def search_tat_task(task_name):
    """Search for TAT task by name"""
    url = f"https://api.notion.com/v1/data_sources/{TAT_DB_ID}/query"
    
    # Try exact match first
    payload = {
        "filter": {
            "property": "Task Name",
            "title": {
                "contains": task_name
            }
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['id']
    
    return None

def complete_tat_task(page_id):
    """Mark TAT task as complete"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    properties = {
        "Status": {"select": {"name": "Done"}},
        "Completed": {"date": {"start": today}}
    }
    
    response = requests.patch(url, headers=HEADERS, json={"properties": properties})
    
    return response.status_code == 200

def parse_and_update(text):
    """Parse natural language and complete TAT tasks"""
    text_lower = text.lower()
    
    # Keywords indicating completion
    complete_keywords = ['complete', 'done', 'finished', 'did', 'completed']
    
    # Check if this is a completion message
    if not any(kw in text_lower for kw in complete_keywords):
        return False
    
    # Known TAT tasks to look for
    task_mappings = {
        'sunvisor': 'Sunvisor for Theo',
        'theo': 'Sunvisor for Theo',
        'aster': 'Withdraw aster cash',
        'cash': 'Withdraw aster cash',
        'atm': 'Withdraw aster cash',
        'research': 'Push research repo to GitHub',
        'github': 'Push research repo to GitHub',
        'repo': 'Push research repo to GitHub',
        'bath': 'Fix bath',
        'bathroom': 'Fix bath',
    }
    
    completed = []
    
    for keyword, task_name in task_mappings.items():
        if keyword in text_lower:
            page_id = search_tat_task(task_name)
            if page_id:
                if complete_tat_task(page_id):
                    completed.append(task_name)
    
    if completed:
        print("✅ Completed TAT Tasks:")
        for task in completed:
            print(f"  ✅ {task}")
        return True
    else:
        print("⚠️ No matching TAT tasks found")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        parse_and_update(text)
    else:
        print("Usage: python3 update_tat.py 'Completed sunvisor for Theo'")
