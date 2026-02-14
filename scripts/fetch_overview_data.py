#!/usr/bin/env python3
"""Fetch data for Mission Control Overview page"""

import requests
import json
from datetime import datetime, timedelta
import urllib.parse

AIRTABLE_KEY = open('/home/samsclaw/.config/airtable/api_key').read().strip()

# Base IDs
HEALTH_BASE = "appnVeGSjwJgG2snS"
PRODUCTIVITY_BASE = "appvUbV8IeGhxmcPn"

def fetch_today_health():
    """Fetch today's health data"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get food log for today
    food_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/Food%20Log"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    formula = urllib.parse.quote(f"IS_SAME(Date, '{today}', 'day')")
    food_resp = requests.get(f"{food_url}?filterByFormula={formula}", headers=headers, timeout=30)
    
    total_calories = 0
    total_protein = 0
    if food_resp.status_code == 200:
        for record in food_resp.json().get('records', []):
            fields = record['fields']
            total_calories += fields.get('Calories', 0) or 0
            total_protein += fields.get('Protein (g)', 0) or 0
    
    # Get weight (most recent)
    weight_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblBXv1DfQWDZSbRc"
    weight_resp = requests.get(f"{weight_url}?sort[0][field]=Date&sort[0][direction]=desc&maxRecords=1", 
                               headers=headers, timeout=30)
    
    current_weight = None
    if weight_resp.status_code == 200:
        records = weight_resp.json().get('records', [])
        if records:
            current_weight = records[0]['fields'].get('Weight (kg)')
    
    # Get today's workout
    workout_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblZzvXBJoKcMtjZU"
    workout_resp = requests.get(f"{workout_url}?filterByFormula={formula}", 
                                headers=headers, timeout=30)
    
    activity_minutes = 0
    if workout_resp.status_code == 200:
        for record in workout_resp.json().get('records', []):
            activity_minutes += record['fields'].get('Duration (min)', 0) or 0
    
    return {
        'today_calories': total_calories,
        'today_protein': total_protein,
        'current_weight': current_weight,
        'today_activity': activity_minutes
    }

def fetch_today_habits():
    """Fetch today's habit data"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    habits_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    formula = urllib.parse.quote(f"IS_SAME(Date, '{today}', 'day')")
    resp = requests.get(f"{habits_url}?filterByFormula={formula}", headers=headers, timeout=30)
    
    if resp.status_code == 200 and resp.json().get('records'):
        fields = resp.json()['records'][0]['fields']
        return {
            'multivitamin': fields.get('Multivitamin', False),
            'fruit': fields.get('Fruit', False),
            'water': fields.get('Water', 0) or 0,
            'exercise': fields.get('Exercise', False),
            'creatine': fields.get('Creatine', False)
        }
    
    return {'multivitamin': False, 'fruit': False, 'water': 0, 'exercise': False, 'creatine': False}

def fetch_priority_tasks():
    """Fetch priority TAT tasks (today + overdue)"""
    tasks_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblkbuvkZUSpm1IgJ"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Get non-complete tasks
    formula = urllib.parse.quote("Status!='Complete'")
    resp = requests.get(f"{tasks_url}?filterByFormula={formula}&sort[0][field]=Days%20Remaining&sort[0][direction]=asc", 
                        headers=headers, timeout=30)
    
    priority_tasks = []
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            days_remaining = fields.get('Days Remaining')
            
            # Determine due status (handle dict or number)
            if isinstance(days_remaining, dict):
                days_remaining = days_remaining.get('Days Remaining')
            if days_remaining is None or (isinstance(days_remaining, (int, float)) and days_remaining > 30):
                continue
            elif isinstance(days_remaining, (int, float)) and days_remaining < 0:
                due_status = 'overdue'
            elif isinstance(days_remaining, (int, float)) and days_remaining == 0:
                due_status = 'today'
            else:
                continue  # Skip non-priority
            
            priority_tasks.append({
                'id': record['id'],
                'name': fields.get('Task Name', 'Unnamed Task'),
                'category': fields.get('Category', 'Uncategorized'),
                'due_status': due_status,
                'days_remaining': days_remaining,
                'status': fields.get('Status', 'Not Started')
            })
            
            if len(priority_tasks) >= 5:
                break
    
    return priority_tasks

def fetch_habit_history():
    """Fetch last 7 days of habit data"""
    habits_url = f"https://api.airtable.com/v0/{PRODUCTIVITY_BASE}/tblZSHA0bOZGNaRUm"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Get last 7 days
    resp = requests.get(f"{habits_url}?sort[0][field]=Date&sort[0][direction]=desc&maxRecords=7", 
                        headers=headers, timeout=30)
    
    habit_days = []
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            habit_days.append({
                'date': fields.get('Date'),
                'multivitamin': fields.get('Multivitamin', False),
                'fruit': fields.get('Fruit', False),
                'water': fields.get('Water', 0) or 0,
                'exercise': fields.get('Exercise', False),
                'creatine': fields.get('Creatine', False)
            })
    
    return habit_days

def fetch_weight_history():
    """Fetch last 30 days of weight data"""
    weight_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblBXv1DfQWDZSbRc"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    resp = requests.get(f"{weight_url}?sort[0][field]=Date&sort[0][direction]=desc&maxRecords=30", 
                        headers=headers, timeout=30)
    
    weights = []
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            weights.append({
                'date': fields.get('Date'),
                'weight': fields.get('Weight (kg)')
            })
    
    return weights

def fetch_workout_history():
    """Fetch last 7 days of workouts"""
    workout_url = f"https://api.airtable.com/v0/{HEALTH_BASE}/tblZzvXBJoKcMtjZU"
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    
    # Get last 7 days
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    formula = urllib.parse.quote(f"IS_AFTER(Date, '{seven_days_ago}')")
    
    resp = requests.get(f"{workout_url}?filterByFormula={formula}&sort[0][field]=Date", 
                        headers=headers, timeout=30)
    
    workouts = []
    if resp.status_code == 200:
        for record in resp.json().get('records', []):
            fields = record['fields']
            workouts.append({
                'date': fields.get('Date'),
                'duration': fields.get('Duration (min)', 0) or 0,
                'strain': fields.get('Strain', 0) or 0,
                'name': fields.get('Workout Name', 'Workout')
            })
    
    return workouts

def main():
    """Generate overview data file"""
    print("Fetching data for Overview page...")
    
    # Fetch all data
    health_data = fetch_today_health()
    today_habits = fetch_today_habits()
    priority_tasks = fetch_priority_tasks()
    habit_days = fetch_habit_history()
    weight_history = fetch_weight_history()
    workouts = fetch_workout_history()
    
    # Combine into overview data
    overview_data = {
        'generated_at': datetime.now().isoformat(),
        'today': {
            'health': health_data,
            'habits': today_habits,
            'priority_tasks': priority_tasks
        },
        'trends': {
            'habit_days': habit_days,
            'weight_history': weight_history,
            'workouts': workouts
        }
    }
    
    # Save to file
    output_path = '/home/samsclaw/.openclaw/workspace/mission-control/data/overview_data.json'
    with open(output_path, 'w') as f:
        json.dump(overview_data, f, indent=2)
    
    print(f"✅ Overview data saved to {output_path}")
    print(f"   - Today: {health_data.get('today_calories', 0)} cal")
    print(f"   - Habits: {len(habit_days)} days history")
    print(f"   - Priority tasks: {len(priority_tasks)} tasks")
    print(f"   - Weight history: {len(weight_history)} records")

if __name__ == "__main__":
    main()
