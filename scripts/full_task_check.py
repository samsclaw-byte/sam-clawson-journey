#!/usr/bin/env python3
"""
Check all Notion databases for pending tasks
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

# Database IDs
OVERNIGHT_BUILD_TASKS_DB = "2fdf2cb1-2276-81cc-99c6-df60e7a1600e"
OVERNIGHT_RESEARCH_TASKS_DB = "2fdf2cb1-2276-816f-bb5c-d9a812891de3"
MASTER_CRON_SCHEDULE_DB = "2fdf2cb1-2276-81a5-84e9-d60295943cd6"

def query_database(db_id, db_name):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    response = requests.post(url, headers=HEADERS, json={"page_size": 100})
    
    if response.status_code != 200:
        print(f"❌ Error querying {db_name}: {response.status_code}")
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
    for prop_name in ['Status', 'status', 'State', 'state', 'Progress', 'progress']:
        if prop_name in props:
            prop_data = props[prop_name]
            if prop_data.get('type') == 'status' and prop_data.get('status'):
                return prop_data['status'].get('name', 'Unknown')
            elif prop_data.get('type') == 'select' and prop_data.get('select'):
                return prop_data['select'].get('name', 'Unknown')
    return 'Unknown'

def is_pending(status):
    status_lower = status.lower()
    pending_keywords = ['pending', 'ready', 'todo', 'not started', 'backlog', 'queued', 'waiting']
    return any(k in status_lower for k in pending_keywords)

def is_in_progress(status):
    status_lower = status.lower()
    progress_keywords = ['in progress', 'started', 'working', 'doing', 'active']
    return any(k in status_lower for k in progress_keywords)

def main():
    print(f"🌙 3AM BUILD TASK CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    all_pending = []
    
    # Check Build Tasks
    print("\n🔨 OVERNIGHT BUILD TASKS")
    print("-" * 50)
    build_tasks = query_database(OVERNIGHT_BUILD_TASKS_DB, "Build Tasks")
    for task in build_tasks:
        title = extract_title(task)
        status = extract_status(task)
        pending = is_pending(status)
        in_progress = is_in_progress(status)
        icon = "⏳" if pending else "🔄" if in_progress else "✅"
        print(f"   {icon} {title} [{status}]")
        if pending:
            all_pending.append(('build', task, title, status))
    
    # Check Research Tasks  
    print("\n🔍 OVERNIGHT RESEARCH TASKS")
    print("-" * 50)
    research_tasks = query_database(OVERNIGHT_RESEARCH_TASKS_DB, "Research Tasks")
    for task in research_tasks:
        title = extract_title(task)
        status = extract_status(task)
        pending = is_pending(status)
        in_progress = is_in_progress(status)
        icon = "⏳" if pending else "🔄" if in_progress else "✅"
        print(f"   {icon} {title} [{status}]")
        if pending:
            all_pending.append(('research', task, title, status))
    
    # Check Master Cron Schedule
    print("\n📋 MASTER CRON SCHEDULE")
    print("-" * 50)
    cron_tasks = query_database(MASTER_CRON_SCHEDULE_DB, "Cron Schedule")
    for task in cron_tasks:
        title = extract_title(task)
        status = extract_status(task)
        pending = is_pending(status)
        in_progress = is_in_progress(status)
        icon = "⏳" if pending else "🔄" if in_progress else "✅"
        print(f"   {icon} {title} [{status}]")
        if pending:
            all_pending.append(('cron', task, title, status))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if all_pending:
        print(f"\n✅ Found {len(all_pending)} PENDING task(s) to execute:\n")
        for task_type, task_data, title, status in all_pending:
            print(f"   🔹 {title}")
            print(f"      Type: {task_type.upper()}")
            print(f"      Status: {status}")
            print(f"      ID: {task_data.get('id')}")
            print()
    else:
        print("\n   ✅ No pending tasks found.")
        print("   All tasks are either complete or in progress.")
    
    return all_pending

if __name__ == "__main__":
    pending = main()
