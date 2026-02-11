#!/usr/bin/env python3
"""
Update Notion Habit Tracker from natural language
Parses habit updates and updates Notion database
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

# Tracker Database ID
TRACKER_DB_ID = "2fdf2cb1-2276-819a-b352-000b8c4ff0be"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

def get_or_create_todays_entry():
    """Get today's entry or create if not exists"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Search for today's entry
    url = f"https://api.notion.com/v1/data_sources/{TRACKER_DB_ID}/query"
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "equals": today
            }
        }
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        if results:
            return results[0]['id']
        else:
            # Create new entry for today
            create_url = "https://api.notion.com/v1/pages"
            create_payload = {
                "parent": {"database_id": TRACKER_DB_ID},
                "properties": {
                    "Name": {"title": [{"text": {"content": f"Day Entry - {today}"}}]},
                    "Date": {"date": {"start": today}}
                }
            }
            
            create_response = requests.post(create_url, headers=HEADERS, json=create_payload)
            if create_response.status_code == 200:
                return create_response.json()['id']
    
    return None

def update_habit(page_id, habit_type, value=None):
    """Update a specific habit"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    properties = {}
    
    if habit_type == 'water':
        properties['Water'] = {"number": value}
    elif habit_type == 'exercise':
        properties['Exercise'] = {"checkbox": True}
        if value:
            properties['Exercise Duration (min)'] = {"number": value}
    elif habit_type == 'multivitamin':
        properties['Multivitamin'] = {"checkbox": True}
    elif habit_type == 'fruit':
        properties['Fruit'] = {"checkbox": True}
    elif habit_type == 'creatine':
        properties['Creatine'] = {"checkbox": True}
    
    response = requests.patch(url, headers=HEADERS, json={"properties": properties})
    
    return response.status_code == 200

def parse_and_update(text):
    """Parse natural language and update Notion"""
    text_lower = text.lower()
    page_id = get_or_create_todays_entry()
    
    if not page_id:
        print("❌ Could not get/create today's entry")
        return False
    
    updates = []
    
    # Parse water
    water_match = re.search(r'(\d+)\s*(?:glasses?|cups?)?\s*(?:of\s*)?water', text_lower)
    if water_match:
        water_count = int(water_match.group(1))
        if update_habit(page_id, 'water', water_count):
            updates.append(f"💧 Water: {water_count}/8")
    
    # Check for water at X/8 format
    water_status_match = re.search(r'water\s*(?:at\s*)?(\d+)[\/\\]8', text_lower)
    if water_status_match:
        water_count = int(water_status_match.group(1))
        if update_habit(page_id, 'water', water_count):
            updates.append(f"💧 Water: {water_count}/8")
    
    # Parse exercise
    if any(word in text_lower for word in ['exercise', 'workout', 'run', 'swim', 'training']):
        # Try to extract minutes
        min_match = re.search(r'(\d+)\s*(?:min|minutes?)', text_lower)
        duration = int(min_match.group(1)) if min_match else None
        
        if update_habit(page_id, 'exercise', duration):
            updates.append(f"🏃 Exercise: {'✅' + (f' ({duration} min)' if duration else '')}")
    
    # Parse multivitamin
    if any(word in text_lower for word in ['multivitamin', 'multi', 'vitamin']):
        if update_habit(page_id, 'multivitamin'):
            updates.append("💊 Multivitamin: ✅")
    
    # Parse fruit
    if any(word in text_lower for word in ['fruit', 'apple', 'banana', 'dates', 'pineapple']):
        if update_habit(page_id, 'fruit'):
            updates.append("🍎 Fruit: ✅")
    
    # Parse creatine
    if 'creatine' in text_lower:
        if update_habit(page_id, 'creatine'):
            updates.append("💊 Creatine: ✅")
    
    if updates:
        print("✅ Updated Notion Habit Tracker:")
        for update in updates:
            print(f"  {update}")
        return True
    else:
        print("⚠️ No habit updates detected")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        parse_and_update(text)
    else:
        print("Usage: python3 update_habits.py 'Drank 2 glasses of water and took multivitamin'")
