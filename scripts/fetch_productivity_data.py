#!/usr/bin/env python3
"""Fetch productivity data (TAT tasks + habits) from Airtable for Mission Control"""

import requests
import json
from datetime import datetime, timedelta

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def fetch_productivity_data():
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # 1. Fetch TAT Tasks (non-complete)
    tat_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblkbuvkZUSpm1IgJ"
    tat_response = requests.get(
        f"{tat_url}?filterByFormula=Status!='Complete'&maxRecords=100",
        headers=headers,
        timeout=30
    )
    
    tat_tasks = []
    if tat_response.status_code == 200:
        for r in tat_response.json().get('records', []):
            f = r['fields']
            
            # Get days remaining safely - handle NaN dict
            days_remaining = f.get('Days Remaining')
            if isinstance(days_remaining, dict):
                days_remaining = 999
            elif days_remaining is None:
                days_remaining = 999
            else:
                days_remaining = int(days_remaining)
            
            # Determine due status
            if days_remaining < 0:
                due_status = 'overdue'
            elif days_remaining == 0:
                due_status = 'today'
            elif days_remaining <= 3:
                due_status = 'soon'
            else:
                due_status = 'later'
            
            tat_tasks.append({
                'id': r['id'],
                'name': f.get('Task Name', 'Unnamed Task'),
                'category': f.get('Category', '7'),
                'status': f.get('Status', 'Not Started'),
                'due_status': due_status,
                'days_remaining': days_remaining,
                'urgency': f.get('Urgency Level', 'Medium'),
                'due_date': f.get('Due Date', '')
            })
        
        # Sort by days remaining
        tat_tasks.sort(key=lambda x: x['days_remaining'])
    
    # 2. Fetch last 7 days of habits
    habits_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    habits_response = requests.get(
        f"{habits_url}?filterByFormula=IS_AFTER({{Date}}, '{week_ago}')&maxRecords=10",
        headers=headers,
        timeout=30
    )
    
    habit_days = []
    if habits_response.status_code == 200:
        records = habits_response.json().get('records', [])
        for r in records:
            f = r['fields']
            date_str = f.get('Date', '')
            if date_str:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                score = sum([
                    1 if f.get('Multivitamin') else 0,
                    1 if f.get('Fruit') else 0,
                    1 if f.get('Exercise') else 0,
                    1 if f.get('Creatine') else 0,
                    1 if f.get('Water', 0) >= 8 else 0
                ])
                
                habit_days.append({
                    'date': date_str,
                    'day_name': dt.strftime('%a'),
                    'day_num': dt.strftime('%d'),
                    'score': score,
                    'water': f.get('Water', 0),
                    'multivitamin': f.get('Multivitamin', False),
                    'fruit': f.get('Fruit', False),
                    'exercise': f.get('Exercise', False),
                    'creatine': f.get('Creatine', False)
                })
        
        # Sort by date
        habit_days.sort(key=lambda x: x['date'])
    
    # Save data
    data = {
        'generated_at': datetime.now().isoformat(),
        'tat_tasks': tat_tasks,
        'habit_days': habit_days,
        'stats': {
            'active': len(tat_tasks),
            'overdue': len([t for t in tat_tasks if t['due_status'] == 'overdue']),
            'today': len([t for t in tat_tasks if t['due_status'] == 'today']),
            'completed_7d': 0
        }
    }
    
    with open('/home/samsclaw/.openclaw/workspace/data/productivity_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Productivity data updated: {len(tat_tasks)} tasks, {len(habit_days)} habit days")
    return True

if __name__ == "__main__":
    fetch_productivity_data()
