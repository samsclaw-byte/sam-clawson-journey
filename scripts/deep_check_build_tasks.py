#!/usr/bin/env python3
"""
Deep check of Notion Overnight Build Tasks - find next pending task
"""

import requests
import os
from datetime import datetime

# Notion API Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN') or open(
    os.path.expanduser('~/.config/notion/api_key')
).read().strip()

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

OVERNIGHT_BUILD_TASKS_DB = "2fdf2cb1-2276-81cc-99c6-df60e7a1600e"

def query_all_tasks():
    """Query all tasks and show their status"""
    url = f"https://api.notion.com/v1/databases/{OVERNIGHT_BUILD_TASKS_DB}/query"
    
    response = requests.post(url, headers=HEADERS, json={"page_size": 100})
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return []
    
    return response.json().get('results', [])

def extract_title(page):
    """Extract title from page"""
    props = page.get('properties', {})
    for prop_name, prop_data in props.items():
        if prop_data.get('type') == 'title' and prop_data.get('title'):
            title_parts = [t.get('text', {}).get('content', '') for t in prop_data['title']]
            return ''.join(title_parts) or 'Untitled'
    return 'Untitled'

def extract_status(page):
    """Extract status from page"""
    props = page.get('properties', {})
    for prop_name in ['Status', 'status', 'State', 'state']:
        if prop_name in props:
            prop_data = props[prop_name]
            if prop_data.get('type') == 'status' and prop_data.get('status'):
                return prop_data['status'].get('name', 'Unknown')
            elif prop_data.get('type') == 'select' and prop_data.get('select'):
                return prop_data['select'].get('name', 'Unknown')
    return 'Unknown'

def main():
    print(f"🔍 Checking Notion Overnight Build Tasks at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    tasks = query_all_tasks()
    print(f"\n📋 Found {len(tasks)} total task(s):\n")
    
    pending_tasks = []
    
    for task in tasks:
        title = extract_title(task)
        status = extract_status(task)
        task_id = task.get('id', 'N/A')
        
        print(f"  • {title}")
        print(f"    Status: {status}")
        print(f"    ID: {task_id}")
        print()
        
        # Check if pending
        status_lower = status.lower()
        if any(k in status_lower for k in ['pending', 'ready', 'todo', 'not started', 'backlog']):
            pending_tasks.append({
                'id': task_id,
                'title': title,
                'status': status,
                'full_data': task
            })
    
    print("=" * 60)
    if pending_tasks:
        print(f"\n✅ Found {len(pending_tasks)} PENDING task(s):")
        for task in pending_tasks:
            print(f"   • {task['title']} ({task['status']})")
    else:
        print("\n📝 No tasks with 'pending' status found.")
        print("   All tasks appear to be complete or in progress.")
    
    return pending_tasks

if __name__ == "__main__":
    pending = main()
