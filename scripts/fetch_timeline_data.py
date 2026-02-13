#!/usr/bin/env python3
"""Fetch 7-day timeline data from Airtable for Mission Control dashboard"""

import requests
import json
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"

def fetch_timeline_data():
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Calculate date range
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    dates.reverse()  # Oldest first
    
    days_data = []
    
    for date in dates:
        day_data = {
            'date': date,
            'calories_burned': 0,
            'calories_consumed': 0,
            'strain': 0,
            'weight': None,
            'sleep': 0
        }
        
        # 1. Get calories consumed from Food Log
        try:
            food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblsoErCMSBtzBZKB"
            food_resp = requests.get(
                f"{food_url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if food_resp.status_code == 200:
                meals = food_resp.json().get('records', [])
                day_data['calories_consumed'] = sum(
                    m['fields'].get('Calories', 0) or 0 for m in meals
                )
        except:
            pass
        
        # 2. Get calories burned, strain, sleep from WHOOP
        try:
            whoop_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblUpFFMXvJSHCKXk"
            whoop_resp = requests.get(
                f"{whoop_url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if whoop_resp.status_code == 200:
                whoop_records = whoop_resp.json().get('records', [])
                if whoop_records:
                    f = whoop_records[0]['fields']
                    day_data['calories_burned'] = f.get('Calories Burned', 0) or 0
                    day_data['strain'] = f.get('Strain', 0) or 0
                    day_data['sleep'] = f.get('Sleep Performance', 0) or 0
        except:
            pass
        
        # 3. Get weight from Weight Tracker
        try:
            weight_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblBXv1DfQWDZSbRc"
            weight_resp = requests.get(
                f"{weight_url}?filterByFormula=Date='{date}'",
                headers=headers,
                timeout=10
            )
            if weight_resp.status_code == 200:
                weight_records = weight_resp.json().get('records', [])
                if weight_records:
                    day_data['weight'] = weight_records[0]['fields'].get('Weight (kg)')
        except:
            pass
        
        days_data.append(day_data)
    
    # Save data
    data = {
        'generated_at': datetime.now().isoformat(),
        'days': days_data
    }
    
    with open('/home/samsclaw/.openclaw/workspace/data/timeline_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Timeline data updated: {len(days_data)} days")
    for d in days_data:
        print(f"  {d['date']}: {d['calories_consumed']} cal, strain {d['strain']}")
    
    return True

if __name__ == "__main__":
    fetch_timeline_data()
