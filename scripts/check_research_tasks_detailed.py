#!/usr/bin/env python3
"""
Check Notion Overnight Research Tasks for any tasks needing research
"""

import requests
import os
from datetime import datetime

NOTION_TOKEN = os.environ.get('NOTION_TOKEN') or open(
    os.path.expanduser('~/.config/notion/api_key')
).read().strip()

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

OVERNIGHT_RESEARCH_TASKS_DB = "2fdf2cb1-2276-816f-bb5c-d9a812891de3"

def query_database(db_id):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    response = requests.post(url, headers=HEADERS, json={"page_size": 100})
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return []
    
    return response.json().get('results', [])

def extract_title(page):
    props = page.get('properties', {})
    for prop_name, prop_data in props.items():
        if prop_data.get('type') == 'title' and prop_data.get('title'):
            title_parts = [t.get('text', {}).get('content', '') for t in prop_data['title']]
            return ''.join(title_parts) or 'Untitled'
    return 'Untitled'

def extract_status(page):
    props = page.get('properties', {})
    for prop_name in ['Status', 'status', 'State', 'state']:
        if prop_name in props:
            prop_data = props[prop_name]
            if prop_data.get('type') == 'status' and prop_data.get('status'):
                return prop_data['status'].get('name', 'Unknown')
            elif prop_data.get('type') == 'select' and prop_data.get('select'):
                return prop_data['select'].get('name', 'Unknown')
    return 'Unknown'

def extract_description(page):
    """Extract description/notes from the page"""
    props = page.get('properties', {})
    # Check for description, notes, or rich_text properties
    for prop_name in ['Description', 'description', 'Notes', 'notes', 'Details', 'details']:
        if prop_name in props:
            prop_data = props[prop_name]
            if prop_data.get('type') == 'rich_text' and prop_data.get('rich_text'):
                parts = [t.get('text', {}).get('content', '') for t in prop_data['rich_text']]
                return ''.join(parts)
    return ''

def extract_priority(page):
    """Extract priority if available"""
    props = page.get('properties', {})
    for prop_name in ['Priority', 'priority', 'Urgency', 'urgency']:
        if prop_name in props:
            prop_data = props[prop_name]
            if prop_data.get('type') == 'select' and prop_data.get('select'):
                return prop_data['select'].get('name', '')
    return ''

def needs_research(status):
    """Check if task needs research based on status"""
    status_lower = status.lower()
    # Any status that indicates work still needed
    needs_research_keywords = [
        'pending', 'ready', 'todo', 'not started', 'backlog', 
        'queued', 'waiting', 'to do', 'in progress', 'started',
        'research needed', 'to research', 'planned'
    ]
    return any(k in status_lower for k in needs_research_keywords)

def is_complete(status):
    """Check if task is complete"""
    status_lower = status.lower()
    complete_keywords = ['complete', 'done', 'finished', '✅', 'archived', 'resolved', 'closed']
    return any(k in status_lower for k in complete_keywords)

def main():
    print(f"🔍 4AM RESEARCH TASK CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    tasks = query_database(OVERNIGHT_RESEARCH_TASKS_DB)
    print(f"\n📋 Found {len(tasks)} total research task(s):\n")
    
    needs_research_tasks = []
    complete_tasks = []
    other_tasks = []
    
    for task in tasks:
        title = extract_title(task)
        status = extract_status(task)
        description = extract_description(task)
        priority = extract_priority(task)
        task_id = task.get('id', 'N/A')
        url = task.get('url', '')
        
        if is_complete(status):
            complete_tasks.append({
                'id': task_id,
                'title': title,
                'status': status,
                'description': description,
                'priority': priority,
                'url': url
            })
        elif needs_research(status):
            needs_research_tasks.append({
                'id': task_id,
                'title': title,
                'status': status,
                'description': description,
                'priority': priority,
                'url': url
            })
        else:
            other_tasks.append({
                'id': task_id,
                'title': title,
                'status': status,
                'description': description,
                'priority': priority,
                'url': url
            })
    
    # Show all tasks
    print("\n📊 TASK BREAKDOWN:")
    print(f"   ✅ Complete: {len(complete_tasks)}")
    print(f"   🔍 Needs Research: {len(needs_research_tasks)}")
    print(f"   📝 Other Status: {len(other_tasks)}")
    
    if needs_research_tasks:
        print("\n" + "=" * 70)
        print("🔍 TASKS NEEDING RESEARCH:")
        print("=" * 70)
        for i, task in enumerate(needs_research_tasks, 1):
            print(f"\n   {i}. {task['title']}")
            print(f"      Status: {task['status']}")
            if task['priority']:
                print(f"      Priority: {task['priority']}")
            if task['description']:
                print(f"      Description: {task['description'][:100]}...")
            print(f"      ID: {task['id']}")
    
    if other_tasks:
        print("\n" + "-" * 70)
        print("📝 TASKS WITH OTHER STATUS:")
        print("-" * 70)
        for task in other_tasks:
            print(f"\n   • {task['title']}")
            print(f"     Status: {task['status']}")
    
    print("\n" + "=" * 70)
    
    # Return first task needing research
    if needs_research_tasks:
        # Sort by priority if available
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2, '': 3}
        needs_research_tasks.sort(key=lambda x: priority_order.get(x['priority'], 3))
        return needs_research_tasks[0]
    
    return None

if __name__ == "__main__":
    next_task = main()
    if next_task:
        print(f"\n🎯 NEXT TASK TO RESEARCH: {next_task['title']}")
    else:
        print("\n✅ No tasks currently need research - all complete!")
