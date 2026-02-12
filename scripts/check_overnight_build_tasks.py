#!/usr/bin/env python3
"""
5am Build Task Check - Query Notion Overnight Build Tasks
Fixed version with better property detection
"""

import requests
import os
from datetime import datetime, date

# Notion API Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN') or open(
    os.path.expanduser('~/.config/notion/api_key')
).read().strip()

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Database IDs from system architect review
OVERNIGHT_BUILD_TASKS_DB = "2fdf2cb1-2276-81cc-99c6-df60e7a1600e"
OVERNIGHT_RESEARCH_TASKS_DB = "2fdf2cb1-2276-816f-bb5c-d9a812891de3"
MASTER_CRON_SCHEDULE_DB = "2fdf2cb1-2276-81a5-84e9-d60295943cd6"

def get_database_schema(database_id):
    """Get the schema of a Notion database to understand property names"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Error fetching database schema: {response.status_code}")
        return None
    
    return response.json()

def query_notion_database(database_id, filter_payload=None):
    """Query a Notion database and return results"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    payload = filter_payload or {}
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Error querying database {database_id}: {response.status_code}")
        print(f"   Response: {response.text}")
        return []
    
    return response.json().get('results', [])

def extract_title(page):
    """Extract the title from a Notion page"""
    props = page.get('properties', {})
    
    # Try to find the title property
    for prop_name, prop_data in props.items():
        if prop_data.get('type') == 'title' and prop_data.get('title'):
            title_parts = []
            for text_obj in prop_data['title']:
                content = text_obj.get('text', {}).get('content', '')
                if content:
                    title_parts.append(content)
            return ' '.join(title_parts) if title_parts else 'Untitled'
    
    # Fallback: check page title directly
    if 'title' in page:
        if isinstance(page['title'], list) and page['title']:
            return page['title'][0].get('text', {}).get('content', 'Untitled')
        elif isinstance(page['title'], str):
            return page['title']
    
    return 'Untitled'

def extract_status(page):
    """Extract the status from a Notion page"""
    props = page.get('properties', {})
    
    # Try common status property names
    for prop_name in ['Status', 'status', 'State', 'state', 'Progress', 'progress']:
        if prop_name in props:
            prop_data = props[prop_name]
            prop_type = prop_data.get('type', '')
            
            if prop_type == 'status' and prop_data.get('status'):
                return prop_data['status'].get('name', 'Unknown')
            elif prop_type == 'select' and prop_data.get('select'):
                return prop_data['select'].get('name', 'Unknown')
    
    return 'Unknown'

def is_task_complete(page):
    """Check if a task is complete based on its status"""
    status = extract_status(page).lower()
    complete_keywords = ['complete', 'done', 'finished', '✅', 'closed', 'archived', 'resolved']
    return any(keyword in status for keyword in complete_keywords)

def check_database(database_id, database_name):
    """Check a database for pending tasks"""
    print(f"\n{database_name}")
    print("-" * 50)
    
    results = query_notion_database(database_id)
    
    if not results:
        print("✅ Database is empty - no pending tasks")
        return []
    
    pending_tasks = []
    
    for result in results:
        task_name = extract_title(result)
        status = extract_status(result)
        
        if not is_task_complete(result):
            pending_tasks.append({
                'id': result.get('id'),
                'name': task_name,
                'status': status,
                'url': result.get('url', '')
            })
    
    if pending_tasks:
        print(f"⚠️  Found {len(pending_tasks)} pending task(s):")
        for i, task in enumerate(pending_tasks, 1):
            print(f"   {i}. {task['name']}")
            if task['status'] != 'Unknown':
                print(f"      Status: {task['status']}")
    else:
        print(f"✅ All {len(results)} task(s) complete")
    
    return pending_tasks

def main():
    """Main function to check all overnight databases"""
    print("\n" + "=" * 60)
    print(f"🌅 5AM BUILD TASK CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Check all databases
    build_tasks = check_database(OVERNIGHT_BUILD_TASKS_DB, "🔨 OVERNIGHT BUILD TASKS")
    research_tasks = check_database(OVERNIGHT_RESEARCH_TASKS_DB, "🔍 OVERNIGHT RESEARCH TASKS")
    cron_jobs = check_database(MASTER_CRON_SCHEDULE_DB, "📋 MASTER CRON SCHEDULE")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    total_pending = len(build_tasks) + len(research_tasks) + len(cron_jobs)
    
    if total_pending == 0:
        print("✅ ALL CLEAR - No pending tasks to execute")
        print("   - Build Tasks: 0 pending")
        print("   - Research Tasks: 0 pending")
        print("   - Cron Jobs: 0 pending")
    else:
        print(f"⚠️  TOTAL PENDING: {total_pending} task(s)")
        print(f"   - Build Tasks: {len(build_tasks)} pending")
        print(f"   - Research Tasks: {len(research_tasks)} pending")
        print(f"   - Cron Jobs: {len(cron_jobs)} pending")
        
        print("\n📝 PENDING TASKS:")
        all_tasks = []
        if build_tasks:
            print("\n   🔨 Build Tasks:")
            for task in build_tasks:
                print(f"      • {task['name']}")
                all_tasks.append(('build', task))
        if research_tasks:
            print("\n   🔍 Research Tasks:")
            for task in research_tasks:
                print(f"      • {task['name']}")
                all_tasks.append(('research', task))
        if cron_jobs:
            print("\n   📋 Cron Jobs:")
            for job in cron_jobs:
                print(f"      • {job['name']}")
                all_tasks.append(('cron', job))
    
    print("=" * 60)
    
    return {
        'build_tasks': build_tasks,
        'research_tasks': research_tasks,
        'cron_jobs': cron_jobs
    }

if __name__ == "__main__":
    result = main()
    
    # Exit with appropriate code
    total_pending = len(result['build_tasks']) + len(result['research_tasks']) + len(result['cron_jobs'])
    exit(total_pending)  # Return number of pending tasks as exit code
