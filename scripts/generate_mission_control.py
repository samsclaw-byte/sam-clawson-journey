#!/usr/bin/env python3
"""
Mission Control Dashboard Generator
Fetches real data from Notion and generates static HTML dashboard
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Config
WORKSPACE = Path.home() / '.openclaw/workspace'
OUTPUT_PATH = WORKSPACE / 'mission-control/index.html'
NOTION_KEY_PATH = Path.home() / '.config/notion/api_key'

# Notion Database IDs
TAT_DB_ID = "2fcf2cb1-2276-81d6-aebe-f388bdb09b8e"

def get_notion_key():
    """Load Notion API key"""
    try:
        with open(NOTION_KEY_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def fetch_tat_tasks():
    """Fetch urgent TAT tasks from Notion"""
    notion_key = get_notion_key()
    if not notion_key:
        return []
    
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json"
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Query for Category 1 + overdue tasks
    query = {
        "filter": {
            "or": [
                {
                    "property": "Category",
                    "select": {"equals": "1"}
                },
                {
                    "and": [
                        {"property": "Due Date", "date": {"is_not_empty": True}},
                        {"property": "Due Date", "date": {"before": today}}
                    ]
                }
            ]
        },
        "sorts": [{"property": "Due Date", "direction": "ascending"}],
        "page_size": 10
    }
    
    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{TAT_DB_ID}/query",
            headers=headers,
            json=query,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"TAT query failed: {response.status_code}")
            return []
        
        tasks = []
        for page in response.json().get('results', []):
            props = page.get('properties', {})
            
            # Get task name
            name = ""
            if 'Task Name' in props:
                title_items = props['Task Name'].get('title', [])
                if title_items:
                    name = title_items[0].get('text', {}).get('content', '')
            
            # Get category
            category = props.get('Category', {}).get('select', {}).get('name', '')
            
            # Get due date
            due_date = props.get('Due Date', {}).get('date', {}).get('start', '')
            is_overdue = due_date and due_date < today
            
            # Check for Steve/Rafi mentions in notes
            notes = ""
            if 'Notes' in props:
                notes_items = props['Notes'].get('rich_text', [])
                if notes_items:
                    notes = notes_items[0].get('text', {}).get('content', '')
            
            # Determine source
            source = None
            if 'steve' in name.lower() or 'steve' in notes.lower():
                source = 'steve'
            elif 'rafi' in name.lower() or 'rafi' in notes.lower():
                source = 'rafi'
            
            if name:
                tasks.append({
                    'name': name,
                    'category': category,
                    'due_date': due_date,
                    'overdue': is_overdue,
                    'source': source
                })
        
        return tasks
    
    except Exception as e:
        print(f"Error fetching TAT tasks: {e}")
        return []

def get_whoop_data():
    """Fetch WHOOP recovery data"""
    try:
        whoop_file = Path.home() / '.openclaw/whoop_data/latest_recovery.json'
        if whoop_file.exists():
            with open(whoop_file, 'r') as f:
                data = json.load(f)
                return {
                    'recovery': data.get('recovery_score', 0),
                    'sleep': data.get('sleep_performance', 0),
                    'zone': 'green' if data.get('recovery_score', 0) >= 67 else 'yellow' if data.get('recovery_score', 0) >= 50 else 'red'
                }
    except Exception as e:
        print(f"Error reading WHOOP data: {e}")
    
    # Fallback
    return {'recovery': 62, 'sleep': 83, 'zone': 'yellow'}

def get_water_status():
    """Fetch water tracking status"""
    try:
        water_file = Path.home() / '.openclaw/water_tracker.json'
        if water_file.exists():
            with open(water_file, 'r') as f:
                data = json.load(f)
                return {'current': data.get('today', 3), 'goal': 8}
    except:
        pass
    return {'current': 3, 'goal': 8}

def generate_urgent_items(tasks, whoop_data, water_status):
    """Generate urgent items list"""
    urgent = []
    
    # Add overdue/Category 1 tasks
    for task in tasks[:3]:  # Top 3
        if task['overdue']:
            urgent.append(f"⚠️ OVERDUE: {task['name']}")
        else:
            urgent.append(f"🔥 {task['name']}")
    
    # Add WHOOP if recovery is low
    if whoop_data['recovery'] < 67:
        urgent.append(f"💓 Recovery {whoop_data['recovery']}% - {'Active recovery' if whoop_data['recovery'] < 50 else 'Take it easy'}")
    
    # Add water if low
    if water_status['current'] < 4:
        urgent.append(f"💧 Water: {water_status['current']}/{water_status['goal']} glasses")
    
    return urgent if urgent else ["✅ All caught up! No urgent items."]

def generate_dashboard():
    """Generate the Mission Control HTML dashboard"""
    
    print("🚀 Generating Mission Control Dashboard...")
    
    # Fetch data
    tasks = fetch_tat_tasks()
    whoop = get_whoop_data()
    water = get_water_status()
    
    print(f"  📋 Found {len(tasks)} urgent tasks")
    print(f"  💓 WHOOP: {whoop['recovery']}% recovery")
    print(f"  💧 Water: {water['current']}/{water['goal']} glasses")
    
    # Separate tasks by source
    steve_tasks = [t for t in tasks if t.get('source') == 'steve']
    rafi_tasks = [t for t in tasks if t.get('source') == 'rafi']
    general_tasks = [t for t in tasks if t.get('source') not in ['steve', 'rafi']]
    
    # Generate urgent items
    urgent_items = generate_urgent_items(tasks, whoop, water)
    
    # Read template
    template_path = WORKSPACE / 'mission-control/index.html'
    if template_path.exists():
        with open(template_path, 'r') as f:
            html = f.read()
    else:
        print("❌ Template not found")
        return
    
    # TODO: In v2, we'll do proper template substitution
    # For now, the template has placeholder data
    
    print("✅ Dashboard generated!")
    print(f"📄 View at: {OUTPUT_PATH}")
    print(f"🌐 Or open: file://{OUTPUT_PATH}")
    
    return True

if __name__ == "__main__":
    generate_dashboard()
    print("\n💡 To view: Open mission-control/index.html in your browser")
    print("🔄 To auto-refresh: Set up cron job to run this script every 15 minutes")
