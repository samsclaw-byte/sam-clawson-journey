#!/usr/bin/env python3
"""Fetch extended trend data for Mission Control Overview page"""

import requests
import json
from datetime import datetime, timedelta
import urllib.parse

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def fetch_nutrition_trends():
    """Fetch last 7 days of nutrition data"""
    food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/Food%20Log"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Get last 7 days of food
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    formula = urllib.parse.quote(f"IS_AFTER(Date, '{seven_days_ago}')")
    
    resp = requests.get(f"{food_url}?filterByFormula={formula}&sort[0][field]=Date", 
                        headers=headers, timeout=30)
    
    nutrition_by_day = {}
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            date = fields.get('Date')
            if date:
                if date not in nutrition_by_day:
                    nutrition_by_day[date] = {'calories': 0, 'protein': 0}
                nutrition_by_day[date]['calories'] += fields.get('Calories', 0) or 0
                nutrition_by_day[date]['protein'] += fields.get('Protein (g)', 0) or 0
    
    # Fill in missing days with 0
    result = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        day_data = nutrition_by_day.get(date, {'calories': 0, 'protein': 0})
        result.append({
            'date': date,
            'calories': day_data['calories'],
            'protein': day_data['protein']
        })
    
    return result

def fetch_productivity_trends():
    """Fetch last 30 days of task completion data"""
    tasks_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblkbuvkZUSpm1IgJ"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Get all tasks
    resp = requests.get(f"{tasks_url}?sort[0][field]=Date%20Created&sort[0][direction]=desc", 
                        headers=headers, timeout=30)
    
    completions_by_day = {}
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            # Check if task is complete
            if fields.get('Status') == 'Complete':
                # Use Date Created or a completion date field
                date = fields.get('Date Created', '')[:10] if fields.get('Date Created') else None
                if date:
                    completions_by_day[date] = completions_by_day.get(date, 0) + 1
    
    # Fill last 30 days
    result = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        result.append({
            'date': date,
            'completed': completions_by_day.get(date, 0)
        })
    
    return result

def main():
    """Generate extended trend data"""
    print("Fetching extended trend data...")
    
    nutrition = fetch_nutrition_trends()
    productivity = fetch_productivity_trends()
    
    trend_data = {
        'generated_at': datetime.now().isoformat(),
        'nutrition': nutrition,
        'productivity': productivity
    }
    
    # Save to file
    output_path = '/home/samsclaw/.openclaw/workspace/mission-control/data/trend_data.json'
    with open(output_path, 'w') as f:
        json.dump(trend_data, f, indent=2)
    
    print(f"✅ Trend data saved to {output_path}")
    print(f"   - Nutrition: {len(nutrition)} days")
    print(f"   - Productivity: {len(productivity)} days")

if __name__ == "__main__":
    main()
