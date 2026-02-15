#!/usr/bin/env python3
"""
List all research tasks with full details
"""

import requests
import os
import json
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

def extract_all_properties(page):
    """Extract all properties for display"""
    props = page.get('properties', {})
    result = {}
    for name, data in props.items():
        prop_type = data.get('type', '')
        if prop_type == 'title' and data.get('title'):
            result[name] = ''.join([t.get('text', {}).get('content', '') for t in data['title']])
        elif prop_type == 'rich_text' and data.get('rich_text'):
            result[name] = ''.join([t.get('text', {}).get('content', '') for t in data['rich_text']])
        elif prop_type == 'status' and data.get('status'):
            result[name] = data['status'].get('name', '')
        elif prop_type == 'select' and data.get('select'):
            result[name] = data['select'].get('name', '')
        elif prop_type == 'multi_select' and data.get('multi_select'):
            result[name] = [s.get('name', '') for s in data['multi_select']]
        elif prop_type == 'date' and data.get('date'):
            result[name] = data['date'].get('start', '')
        elif prop_type == 'checkbox':
            result[name] = data.get('checkbox', False)
    return result

def main():
    print(f"🔍 ALL RESEARCH TASKS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    tasks = query_database(OVERNIGHT_RESEARCH_TASKS_DB)
    
    for i, task in enumerate(tasks, 1):
        title = extract_title(task)
        status = extract_status(task)
        task_id = task.get('id', 'N/A')
        url = task.get('url', '')
        created = task.get('created_time', '')
        last_edited = task.get('last_edited_time', '')
        
        print(f"\n{i}. {title}")
        print(f"   Status: {status}")
        print(f"   ID: {task_id}")
        print(f"   Created: {created}")
        print(f"   Last Edited: {last_edited}")
        
        # Show all properties
        props = extract_all_properties(task)
        for name, value in props.items():
            if name not in ['Name', 'Status'] and value:
                print(f"   {name}: {value}")
        
        print(f"   URL: {url}")
        print("-" * 50)
    
    print(f"\n📊 Total tasks: {len(tasks)}")

if __name__ == "__main__":
    main()
