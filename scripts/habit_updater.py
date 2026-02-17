#!/usr/bin/env python3
"""
Robust Daily Habits Updater
Always checks for existing record before creating/updating
"""

import requests
from datetime import datetime

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
BASE_ID = 'appvUbV8IeGhxmcPn'
HABITS_TABLE = 'tblZSHA0bOZGNaRUm'

def update_daily_habit(field_name, value, date=None):
    """
    Update a single habit field for a given date
    Always checks for existing record first
    
    Args:
        field_name: 'Water', 'Multivitamin', 'Fruit', 'Exercise', 'Creatine'
        value: The value to set
        date: Date string (YYYY-MM-DD), defaults to today
    
    Returns:
        (success, message)
    """
    url = f'https://api.airtable.com/v0/{BASE_ID}/{HABITS_TABLE}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Check for existing record
    filter_formula = f"{{Date}}='{date}'"
    response = requests.get(
        f"{url}?filterByFormula={filter_formula}",
        headers=headers
    )
    
    if response.status_code != 200:
        return False, f"Error checking existing: {response.status_code}"
    
    records = response.json().get('records', [])
    
    # Handle multiple records (merge them)
    if len(records) > 1:
        # Keep first, delete others
        keep_id = records[0]['id']
        for r in records[1:]:
            requests.delete(f"{url}/{r['id']}", headers=headers)
        records = [records[0]]
    
    if records:
        # Update existing record
        record_id = records[0]['id']
        existing = records[0].get('fields', {})
        
        # For Water, add to existing; for booleans, OR with existing
        if field_name == 'Water':
            current = existing.get('Water', 0) or 0
            new_value = current + value if isinstance(value, (int, float)) else value
        else:
            current = existing.get(field_name, False)
            new_value = current or value if isinstance(value, bool) else value
        
        update_resp = requests.patch(
            f"{url}/{record_id}",
            headers=headers,
            json={'fields': {field_name: new_value}}
        )
        
        if update_resp.status_code == 200:
            return True, f"Updated {field_name} to {new_value}"
        else:
            return False, f"Update failed: {update_resp.status_code}"
    else:
        # Create new record
        create_resp = requests.post(
            url,
            headers=headers,
            json={
                'fields': {
                    'Date': date,
                    field_name: value
                }
            }
        )
        
        if create_resp.status_code == 200:
            return True, f"Created new record with {field_name}={value}"
        else:
            return False, f"Create failed: {create_resp.status_code}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        field = sys.argv[1]
        value = sys.argv[2]
        # Try to convert to int/float/bool
        if value.lower() in ['true', 'yes']:
            value = True
        elif value.lower() in ['false', 'no']:
            value = False
        elif value.isdigit():
            value = int(value)
        
        success, msg = update_daily_habit(field, value)
        print(f"{'✅' if success else '❌'} {msg}")
    else:
        print("Usage: python3 habit_updater.py <field> <value>")
        print("Examples:")
        print("  python3 habit_updater.py Water 1")
        print("  python3 habit_updater.py Exercise true")
        print("  python3 habit_updater.py Fruit True")
