#!/usr/bin/env python3
"""
Habit & Exercise Tracker Sync - Export Notion data to CSV
This syncs the main tracking database (water, exercise, fruit, multivitamin, creatine)
"""

import os
import json
import csv
import requests
from datetime import datetime, timedelta

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
if not NOTION_API_KEY:
    try:
        with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
            NOTION_API_KEY = f.read().strip()
    except FileNotFoundError:
        print("❌ Notion API key not found")
        exit(1)

# Main Tracker Database ID
TRACKER_DB_ID = "2fdf2cb1-2276-819a-b352-000b8c4ff0be"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

def get_tracker_data():
    """Query tracker database"""
    url = f"https://api.notion.com/v1/data_sources/{TRACKER_DB_ID}/query"
    
    all_records = []
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {
            "page_size": 100,
            "sorts": [{"property": "Date", "direction": "descending"}]
        }
        
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            print(response.text)
            break
        
        data = response.json()
        all_records.extend(data.get('results', []))
        
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
    
    return all_records

def parse_tracker_record(record):
    """Parse a Notion tracker record into dict"""
    props = record.get('properties', {})
    
    def get_number(prop_name):
        prop = props.get(prop_name, {})
        return prop.get('number', 0) or 0
    
    def get_checkbox(prop_name):
        prop = props.get(prop_name, {})
        return prop.get('checkbox', False)
    
    def get_date(prop_name):
        prop = props.get(prop_name, {})
        date_prop = prop.get('date', {})
        return date_prop.get('start', '') if date_prop else ''
    
    def get_text(prop_name):
        prop = props.get(prop_name, {})
        title = prop.get('title', [])
        return title[0]['text']['content'] if title else ''
    
    return {
        'date': get_date('Date'),
        'name': get_text('Name'),
        'water': get_number('Water'),
        'exercise': get_checkbox('Exercise'),
        'exercise_minutes': get_number('Exercise Duration (min)'),
        'multivitamin': get_checkbox('Multivitamin'),
        'fruit': get_checkbox('Fruit'),
        'creatine': get_checkbox('Creatine'),
        'zone_1': get_number('Zone 1 (Easy)'),
        'zone_2': get_number('Zone 2 (Aerobic)'),
        'zone_3': get_number('Zone 3 (Threshold)'),
        'zone_4': get_number('Zone 4 (Anaerobic)'),
        'zone_5': get_number('Zone 5 (Max)'),
        'water_streak': get_number('Water Current Streak'),
        'exercise_streak': get_number('Exercise Current Streak'),
        'multi_streak': get_number('Multi Current Streak'),
        'fruit_streak': get_number('Fruit Current Streak'),
    }

def sync_tracker():
    """Sync tracker data to CSV"""
    print("🔄 Syncing habit & exercise data from Notion...")
    
    records = get_tracker_data()
    
    if not records:
        print("❌ No records found")
        return False
    
    # Parse records
    tracker_data = [parse_tracker_record(r) for r in records]
    
    # Save to CSV
    csv_path = os.path.expanduser('~/.openclaw/workspace/dashboard/habit_data.csv')
    
    fieldnames = ['date', 'name', 'water', 'exercise', 'exercise_minutes', 
                  'multivitamin', 'fruit', 'creatine',
                  'zone_1', 'zone_2', 'zone_3', 'zone_4', 'zone_5',
                  'water_streak', 'exercise_streak', 'multi_streak', 'fruit_streak']
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tracker_data)
    
    print(f"✅ Synced {len(tracker_data)} records to {csv_path}")
    
    # Show latest data
    if tracker_data:
        show_latest(tracker_data[0])
    
    return True

def show_latest(latest):
    """Display latest day's data"""
    print(f"\n📊 Latest Entry ({latest['date']}):")
    print("-" * 40)
    print(f"Water: {latest['water']}/8 glasses")
    print(f"Exercise: {'✅' if latest['exercise'] else '❌'} ({latest['exercise_minutes']} min)")
    print(f"Multivitamin: {'✅' if latest['multivitamin'] else '❌'}")
    print(f"Fruit: {'✅' if latest['fruit'] else '❌'}")
    print(f"Creatine: {'✅' if latest['creatine'] else '❌'}")
    print("\n🔥 Current Streaks:")
    print(f"Water: {int(latest['water_streak'])} days")
    print(f"Exercise: {int(latest['exercise_streak'])} days")
    print(f"Multivitamin: {int(latest['multi_streak'])} days")
    print(f"Fruit: {int(latest['fruit_streak'])} days")

if __name__ == "__main__":
    sync_tracker()
