#!/usr/bin/env python3
"""
Check Daily Habits in Airtable
Returns water count and habit status for today
"""

import requests
import json
from datetime import datetime

def get_today_habits():
    """Get today's habit data from Airtable"""
    try:
        with open('/home/samsclaw/.config/airtable/api_key', 'r') as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        return {"error": "Airtable API key not found"}
    
    # Productivity base - Daily Habits table
    base_id = "appvUbV8IeGhxmcPn"
    table_id = "tblZSHA0bOZGNaRUm"
    
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Query for today's record
    import urllib.parse
    formula = urllib.parse.quote(f"IS_SAME(Date, '{today}', 'day')")
    
    resp = requests.get(f"{url}?filterByFormula={formula}", headers=headers, timeout=30)
    
    if resp.status_code == 200:
        records = resp.json().get('records', [])
        if records:
            fields = records[0]['fields']
            return {
                "date": today,
                "water": fields.get('Water', 0) or 0,
                "fruit": fields.get('Fruit', False),
                "multivitamin": fields.get('Multivitamin', False),
                "exercise": fields.get('Exercise', False),
                "creatine": fields.get('Creatine', False),
                "found": True
            }
        else:
            return {
                "date": today,
                "water": 0,
                "fruit": False,
                "multivitamin": False,
                "exercise": False,
                "creatine": False,
                "found": False
            }
    else:
        return {"error": f"API error: {resp.status_code}"}

if __name__ == "__main__":
    result = get_today_habits()
    print(json.dumps(result, indent=2))
