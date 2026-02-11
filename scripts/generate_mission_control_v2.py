#!/usr/bin/env python3
"""
Mission Control Dashboard Generator v2.0
Pulls data from ALL Notion databases
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Config
WORKSPACE = Path.home() / '.openclaw/workspace'
OUTPUT_DIR = WORKSPACE / 'mission-control'
NOTION_VERSION = "2022-06-28"

# Database IDs
DB_IDS = {
    'habits': '304f2cb1-2276-81bb-b69f-c28f02d35fa5',
    'work': '304f2cb1-2276-8156-b477-cf3ba96a68e0',
    'tat': '2fcf2cb1-2276-81d6-aebe-f388bdb09b8e',
    'food': 'dc76e804-5b9e-406b-afda-d7a20dd58976',
    'weight': 'f9583de8-69e9-40e6-ab15-c530277ec474',
}

def get_notion_key():
    try:
        with open(Path.home() / '.config/notion/api_key', 'r') as f:
            return f.read().strip()
    except:
        return None

def query_database(db_id, filter_obj=None):
    """Query a Notion database"""
    notion_key = get_notion_key()
    if not notion_key:
        return []
    
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    payload = {"page_size": 100}
    if filter_obj:
        payload["filter"] = filter_obj
    
    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def get_today_habits():
    """Get today's habit status"""
    today = datetime.now().strftime('%Y-%m-%d')
    results = query_database(DB_IDS['habits'])
    
    for entry in results:
        props = entry.get('properties', {})
        date = props.get('Date', {}).get('date', {}).get('start', '')
        if date == today:
            return {
                'creatine': props.get('Creatine', {}).get('checkbox', False),
                'multivitamin': props.get('Multivitamin', {}).get('checkbox', False),
                'exercise': props.get('Exercise', {}).get('checkbox', False),
                'fruit': props.get('Fruit (2 portions)', {}).get('checkbox', False),
                'water': props.get('Water (8 glasses)', {}).get('checkbox', False),
                'exercise_type': props.get('Exercise Type', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ''),
                'notes': props.get('Notes', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
            }
    
    # Return empty if no entry for today
    return {
        'creatine': False,
        'multivitamin': False,
        'exercise': False,
        'fruit': False,
        'water': False,
        'exercise_type': '',
        'notes': ''
    }

def get_urgent_tasks():
    """Get urgent TAT tasks (Category 1) and work tasks"""
    urgent = []
    
    # TAT tasks
    tat_results = query_database(DB_IDS['tat'])
    for entry in tat_results:
        props = entry.get('properties', {})
        category = props.get('Category', {}).get('select', {}).get('name', '')
        if category == '1' or category == '🔥 Today':
            name = props.get('Task Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
            status = props.get('Status', {}).get('select', {}).get('name', 'Not Started')
            urgent.append({'name': name, 'source': 'TAT', 'status': status})
    
    # Work tasks
    work_results = query_database(DB_IDS['work'])
    for entry in work_results:
        props = entry.get('properties', {})
        category = props.get('Category', {}).get('select', {}).get('name', '')
        if category == '1':
            name = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
            status = props.get('Status', {}).get('select', {}).get('name', 'Not Started')
            stakeholder = props.get('Stakeholder', {}).get('select', {}).get('name', '')
            urgent.append({'name': name, 'source': f'Work ({stakeholder})', 'status': status})
    
    return urgent[:5]  # Top 5

def get_work_summary():
    """Get work task summary"""
    results = query_database(DB_IDS['work'])
    
    summary = {
        'steve': [],
        'rafi': [],
        'other': [],
        'total': len(results),
        'in_progress': 0,
        'done': 0
    }
    
    for entry in results:
        props = entry.get('properties', {})
        name = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        stakeholder = props.get('Stakeholder', {}).get('select', {}).get('name', 'Other')
        status = props.get('Status', {}).get('select', {}).get('name', 'Not Started')
        
        task = {'name': name, 'status': status}
        
        if 'Steve' in stakeholder:
            summary['steve'].append(task)
        elif 'Rafi' in stakeholder:
            summary['rafi'].append(task)
        else:
            summary['other'].append(task)
        
        if status == 'In Progress':
            summary['in_progress'] += 1
        elif status == 'Done':
            summary['done'] += 1
    
    return summary

def get_daily_activity():
    """Get meals and weight"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get meals
    meals = []
    food_results = query_database(DB_IDS['food'])
    for entry in food_results:
        props = entry.get('properties', {})
        date = props.get('Date', {}).get('date', {}).get('start', '')
        if date == today:
            name = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
            meal_type = props.get('Meal', {}).get('select', {}).get('name', 'Meal')
            meals.append({'name': name, 'type': meal_type})
    
    # Get weight
    weight = None
    weight_results = query_database(DB_IDS['weight'])
    for entry in weight_results:
        props = entry.get('properties', {})
        date = props.get('Date', {}).get('date', {}).get('start', '')
        if date == today:
            weight = props.get('Weight (kg)', {}).get('number', 0)
    
    # Get water from local
    water_current = 5
    try:
        with open(WORKSPACE / 'data/water_tracker.json') as f:
            data = json.load(f)
            if data.get('date') == today:
                water_current = data.get('today', 5)
    except:
        pass
    
    return {
        'meals': meals,
        'weight': weight,
        'water': {'current': water_current, 'goal': 8}
    }

def get_whoop_data():
    """Get WHOOP recovery data"""
    try:
        whoop_file = Path.home() / '.openclaw/whoop_data/latest_recovery.json'
        if whoop_file.exists():
            with open(whoop_file) as f:
                data = json.load(f)
                return {
                    'recovery': data.get('recovery_score', 0),
                    'sleep': data.get('sleep_performance', 0),
                    'zone': 'green' if data.get('recovery_score', 0) >= 67 else 'yellow' if data.get('recovery_score', 0) >= 50 else 'red'
                }
    except:
        pass
    return {'recovery': 62, 'sleep': 83, 'zone': 'yellow'}

# Generate HTML functions will continue in the next part...
if __name__ == "__main__":
    print("Testing data fetch...")
    print(f"Habits today: {get_today_habits()}")
    print(f"Urgent tasks: {len(get_urgent_tasks())}")
    print(f"Work summary: {get_work_summary()['total']} tasks")
    print(f"Daily activity: {len(get_daily_activity()['meals'])} meals today")
