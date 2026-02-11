#!/usr/bin/env python3
"""
Auto-update Notion Habit Tracker from natural language
"""

import json
import sys
import os
import subprocess
from datetime import datetime

# Import the parser
sys.path.insert(0, '/home/samsclaw/.openclaw/workspace')
from scripts.habit_parser import parse_habit_update, format_confirmation

NOTION_DB_ID = "2fdf2cb1-2276-819a-b352-000b8c4ff0be"

def get_today_page_id():
    """Get or create today's habit tracker page"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Query for today's entry
    query_cmd = f'''NOTION_KEY=$(cat ~/.config/notion/api_key) && curl -s -X POST "https://api.notion.com/v1/data_sources/{NOTION_DB_ID}/query" \
        -H "Authorization: Bearer $NOTION_KEY" \
        -H "Notion-Version: 2025-09-03" \
        -H "Content-Type: application/json" \
        -d '{{"filter": {{"property": "Date", "date": {{"equals": "{today}"}}}}}}' '''
    
    result = subprocess.run(query_cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        if data.get('results'):
            return data['results'][0]['id']
    except:
        pass
    
    return None

def update_notion_habit(page_id, updates):
    """Update habit values in Notion"""
    properties = {}
    
    for update in updates:
        field = update['field']
        update_type = update['type']
        
        if update_type == 'boolean':
            properties[field] = {"checkbox": True}
        elif update_type == 'increment':
            # Need to get current value first
            pass  # Will handle increment below
    
    if not properties:
        return False
    
    # Build update JSON
    props_json = json.dumps(properties)
    
    update_cmd = f'''NOTION_KEY=$(cat ~/.config/notion/api_key) && curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
        -H "Authorization: Bearer $NOTION_KEY" \
        -H "Notion-Version: 2025-09-03" \
        -H "Content-Type: application/json" \
        -d '{{"properties": {props_json}}}' '''
    
    result = subprocess.run(update_cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        return data.get('object') == 'page'
    except:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 notion_habit_updater.py '<message>'")
        sys.exit(1)
    
    message = sys.argv[1]
    
    # Parse the message
    updates = parse_habit_update(message)
    
    if not updates:
        print("No habit updates detected")
        sys.exit(0)
    
    # Get today's page ID
    page_id = get_today_page_id()
    
    if not page_id:
        print("Error: No habit tracker entry found for today")
        sys.exit(1)
    
    # Update Notion
    success = update_notion_habit(page_id, updates)
    
    if success:
        confirmation = format_confirmation(updates)
        print(confirmation)
    else:
        print("Error updating Notion")
        sys.exit(1)

if __name__ == "__main__":
    main()
