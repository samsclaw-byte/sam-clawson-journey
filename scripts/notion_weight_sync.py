#!/usr/bin/env python3
"""
Weight Tracker - Notion Sync
Logs weight to Notion database
"""

import json
import os
import subprocess
from datetime import datetime, date

NOTION_DB_ID = "f9583de8-69e9-40e6-ab15-c530277ec474"
DATA_SOURCE_ID = "700f937f-6509-4db6-9408-2bd9d281da72"

def notion_api(method, endpoint, data=None):
    """Make Notion API call."""
    notion_key = os.getenv('NOTION_KEY') or subprocess.getoutput('cat ~/.config/notion/api_key').strip()
    
    cmd_parts = [
        'curl', '-s', '-X', method,
        f'https://api.notion.com/v1{endpoint}',
        '-H', f'Authorization: Bearer {notion_key}',
        '-H', 'Notion-Version: 2025-09-03',
        '-H', 'Content-Type: application/json'
    ]
    
    if data:
        cmd_parts.extend(['-d', json.dumps(data)])
    
    result = subprocess.run(cmd_parts, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"error": result.stdout or result.stderr}

def get_last_entry():
    """Get the most recent weight entry from Notion."""
    data = notion_api('POST', f'/data_sources/{DATA_SOURCE_ID}/query', {
        "sorts": [{"property": "Date", "direction": "descending"}],
        "page_size": 1
    })
    
    results = data.get('results', [])
    if results:
        props = results[0].get('properties', {})
        date_prop = props.get('Date', {})
        weight_prop = props.get('Weight (kg)', {})
        
        date_val = None
        if date_prop and date_prop.get('date'):
            date_val = date_prop['date'].get('start')
        
        weight_val = None
        if weight_prop:
            weight_val = weight_prop.get('number')
            
        return {
            'date': date_val,
            'weight_kg': weight_val
        }
    return None

def log_weight_to_notion(weight_kg, notes=""):
    """Log weight to Notion database."""
    weight_lbs = round(weight_kg * 2.20462, 1)
    today = str(date.today())
    
    # Calculate change from last entry
    last = get_last_entry()
    change = None
    if last and last.get('weight_kg'):
        change = round(weight_kg - last['weight_kg'], 1)
    
    properties = {
        "Date": {"date": {"start": today}},
        "Weight (kg)": {"number": weight_kg},
        "Weight (lbs)": {"number": weight_lbs},
        "Notes": {"rich_text": [{"text": {"content": notes}}]}
    }
    
    if change is not None:
        properties["Change (kg)"] = {"number": change}
    
    data = notion_api('POST', '/pages', {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": properties
    })
    
    return data

def get_all_entries():
    """Get all weight entries from Notion."""
    data = notion_api('POST', f'/data_sources/{DATA_SOURCE_ID}/query', {
        "sorts": [{"property": "Date", "direction": "ascending"}]
    })
    return data.get('results', [])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'log':
        weight = float(sys.argv[2])
        notes = sys.argv[3] if len(sys.argv) > 3 else ""
        result = log_weight_to_notion(weight, notes)
        
        if result.get('object') == 'page':
            print(f"✅ Logged {weight} kg to Notion")
        else:
            print(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'list':
        entries = get_all_entries()
        print(f"Found {len(entries)} entries:")
        for e in entries:
            props = e.get('properties', {})
            date_prop = props.get('Date', {})
            date_val = date_prop.get('date', {}).get('start', '?') if date_prop and date_prop.get('date') else '?'
            weight_prop = props.get('Weight (kg)', {})
            weight = weight_prop.get('number', '?') if weight_prop else '?'
            change_prop = props.get('Change (kg)', {})
            change = change_prop.get('number') if change_prop else None
            change_str = f" ({change:+.1f})" if change else ""
            print(f"  {date_val}: {weight} kg{change_str}")
    
    else:
        print("Usage:")
        print("  python3 notion_weight_sync.py log 104 'Morning weigh-in'")
        print("  python3 notion_weight_sync.py list")
