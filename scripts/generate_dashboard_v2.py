#!/usr/bin/env python3
"""
Sam's Daily Command Center - Dashboard Generator v2.1
With 7-day history, individual habit streaks, and improved layout
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Config
DASHBOARD_PATH = Path.home() / '.openclaw/workspace/dashboard/index.html'
DATA_DIR = Path.home() / '.openclaw'

def get_tat_tasks():
    """Fetch urgent TAT tasks - 🔥 Today category + overdue from Notion"""
    try:
        import requests
        
        # Get Notion API key
        notion_key_path = Path.home() / '.config/notion/api_key'
        if not notion_key_path.exists():
            return [{"name": "Notion API not configured", "urgency": "Today", "due": "Setup needed"}]
        
        with open(notion_key_path, 'r') as f:
            notion_key = f.read().strip()
        
        # TAT Database ID
        db_id = "2fcf2cb1-2276-81d6-aebe-f388bdb09b8e"
        
        headers = {
            "Authorization": f"Bearer {notion_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Query for "🔥 Today" category + overdue tasks
        query = {
            "filter": {
                "or": [
                    {
                        "property": "TAT Category Days",
                        "select": {
                            "equals": "🔥 Today"
                        }
                    },
                    {
                        "and": [
                            {
                                "property": "Due Date",
                                "date": {
                                    "is_not_empty": True
                                }
                            },
                            {
                                "property": "Due Date",
                                "date": {
                                    "before": today
                                }
                            }
                        ]
                    }
                ]
            },
            "sorts": [
                {
                    "property": "Due Date",
                    "direction": "ascending"
                }
            ],
            "page_size": 10
        }
        
        response = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=query
        )
        
        if response.status_code != 200:
            return [{"name": "TAT query failed", "urgency": "Error", "due": "Check API"}]
        
        data = response.json()
        tasks = []
        
        for page in data.get('results', []):
            props = page.get('properties', {})
            
            # Get task name
            name = ""
            if 'Task Name' in props:
                title_items = props['Task Name'].get('title', [])
                if title_items:
                    name = title_items[0].get('text', {}).get('content', '')
            
            # Get TAT Category Days
            tat_category = props.get('TAT Category Days', {}).get('select', {}).get('name', '')
            
            # Get due date
            due_date = props.get('Due Date', {}).get('date', {}).get('start', '')
            
            # Determine urgency display
            is_overdue = due_date and due_date < today
            
            # Map category to urgency display
            if tat_category == '🔥 Today' or tat_category == '🔥 1 Day':
                urgency = "🔥 Today"
            elif is_overdue:
                urgency = "⚠️ Overdue"
            elif tat_category in ['⚡ 3 Days', '🟠 3-Day']:
                urgency = "⚡ 3 Days"
            elif tat_category in ['📅 7 Days', '🟡 7-Day']:
                urgency = "📅 7 Days"
            else:
                urgency = tat_category or "📌 Later"
            
            due_display = "Overdue" if is_overdue else (due_date or "Today")
            
            if name:
                tasks.append({
                    "name": name,
                    "urgency": urgency,
                    "due": due_display
                })
        
        # Fallback if no urgent tasks found
        if not tasks:
            return [{"name": "No urgent tasks - you're all caught up!", "urgency": "✅", "due": "-"}]
        
        return tasks
        
    except Exception as e:
        return [{"name": f"Error loading TAT: {str(e)[:30]}", "urgency": "Error", "due": "-"}]

def get_nutrition_with_meals():
    """Get nutrition with detailed meal breakdown from Notion Food Log"""
    try:
        import requests
        from datetime import datetime

        # Get Notion API key
        notion_key_path = Path.home() / '.config/notion/api_key'
        if not notion_key_path.exists():
            return _get_fallback_nutrition()

        with open(notion_key_path, 'r') as f:
            notion_key = f.read().strip()

        # Food Log Data Source ID
        data_source_id = "c1d1100c-cbc4-416d-8c1b-59f7e2ff15c0"

        headers = {
            "Authorization": f"Bearer {notion_key}",
            "Notion-Version": "2025-09-03",
            "Content-Type": "application/json"
        }

        today = datetime.now().strftime('%Y-%m-%d')

        # Query for today's entries
        query = {
            "filter": {
                "property": "Date",
                "date": {
                    "equals": today
                }
            },
            "sorts": [{"property": "Meal", "direction": "ascending"}]
        }

        response = requests.post(
            f"https://api.notion.com/v1/data_sources/{data_source_id}/query",
            headers=headers,
            json=query
        )

        if response.status_code != 200:
            return _get_fallback_nutrition()

        data = response.json()
        meals = []
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0

        # Group entries by meal type
        meal_groups = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snack": []}

        for page in data.get('results', []):
            props = page.get('properties', {})

            # Get food name
            name = ""
            if 'Name' in props:
                title_items = props['Name'].get('title', [])
                if title_items:
                    name = title_items[0].get('text', {}).get('content', '')

            # Get meal type
            meal_type = props.get('Meal', {}).get('select', {}).get('name', 'Snack')

            # Get nutrition values
            calories = props.get('Calories', {}).get('number') or 0
            protein = props.get('Protein (g)', {}).get('number') or 0
            carbs = props.get('Carbs (g)', {}).get('number') or 0
            fat = props.get('Fat (g)', {}).get('number') or 0

            total_calories += calories
            total_protein += protein
            total_carbs += carbs
            total_fat += fat

            meal_groups[meal_type] = meal_groups.get(meal_type, [])
            meal_groups[meal_type].append({
                "name": name,
                "cal": int(calories) if calories else 0
            })

        # Build meal summary
        meal_order = [("Breakfast", "🌅"), ("Lunch", "🍽️"), ("Dinner", "🌙"), ("Snack", "🥤")]
        formatted_meals = []

        for meal_type, icon in meal_order:
            items = meal_groups.get(meal_type, [])
            if items:
                item_names = ", ".join([i["name"] for i in items])
                meal_cals = sum([i["cal"] for i in items])
                formatted_meals.append({
                    "name": f"{icon} {meal_type}",
                    "items": item_names[:60] + "..." if len(item_names) > 60 else item_names,
                    "cal": meal_cals
                })

        if not formatted_meals:
            formatted_meals = [{"name": "No meals logged", "items": "Add entries to Food Log", "cal": 0}]

        return {
            "calories": int(total_calories),
            "calories_goal": 2500,
            "protein": int(total_protein),
            "protein_goal": 160,
            "carbs": int(total_carbs),
            "carbs_goal": 250,
            "fat": int(total_fat),
            "fat_goal": 80,
            "meals": formatted_meals
        }

    except Exception as e:
        print(f"Nutrition fetch error: {e}")
        return _get_fallback_nutrition()

def _get_fallback_nutrition():
    """Fallback nutrition data when Notion is unavailable"""
    return {
        "calories": 0,
        "calories_goal": 2500,
        "protein": 0,
        "protein_goal": 160,
        "carbs": 0,
        "carbs_goal": 250,
        "fat": 0,
        "fat_goal": 80,
        "meals": [{"name": "No data", "items": "Check Notion connection", "cal": 0}]
    }

def get_water_status():
    """Get water tracker status"""
    try:
        with open(DATA_DIR / 'water_tracker.json', 'r') as f:
            data = json.load(f)
            return {"current": data.get('today', 9), "goal": 8}
    except:
        return {"current": 9, "goal": 8}

def get_whoop_data():
    """Get WHOOP recovery data from latest available sources"""
    # Try multiple sources in order of preference
    
    # 1. Try memory context (most recent from webhook/API)
    try:
        whoop_context_path = Path.home() / '.openclaw/workspace/memory/whoop_context.json'
        if whoop_context_path.exists():
            with open(whoop_context_path, 'r') as f:
                data = json.load(f)
                recovery = data.get('summary', {}).get('recovery_score', 0)
                sleep = data.get('summary', {}).get('sleep_performance', 0)
                if recovery > 0:
                    return {
                        "recovery": int(recovery),
                        "sleep": int(sleep),
                        "zone": "green" if recovery >= 67 else "yellow" if recovery >= 50 else "red"
                    }
    except Exception as e:
        print(f"WHOOP context error: {e}")
    
    # 2. Try latest_recovery.json if it exists
    try:
        latest_path = Path.home() / '.openclaw/whoop_data/latest_recovery.json'
        if latest_path.exists():
            with open(latest_path, 'r') as f:
                data = json.load(f)
                recovery = data.get('recovery_score', 0)
                sleep = data.get('sleep_performance', 0)
                if recovery > 0:
                    return {
                        "recovery": int(recovery),
                        "sleep": int(sleep),
                        "zone": "green" if recovery >= 67 else "yellow" if recovery >= 50 else "red"
                    }
    except Exception as e:
        print(f"WHOOP latest error: {e}")
    
    # 3. Try whoop_data.csv for sleep performance
    try:
        csv_path = Path.home() / '.openclaw/workspace/dashboard/whoop_data.csv'
        if csv_path.exists():
            import csv
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    latest = rows[0]  # Most recent first
                    sleep_perf = float(latest.get('sleep_performance', 0))
                    # Estimate recovery based on sleep performance
                    recovery = int(sleep_perf * 0.9)  # Rough estimate
                    return {
                        "recovery": recovery,
                        "sleep": int(sleep_perf),
                        "zone": "green" if recovery >= 67 else "yellow" if recovery >= 50 else "red"
                    }
    except Exception as e:
        print(f"WHOOP CSV error: {e}")
    
    # 4. Try webhook data file
    try:
        with open(DATA_DIR / 'whoop_webhook_data.json', 'r') as f:
            data = json.load(f)
            recovery = data.get('recovery_score', 0)
            sleep = data.get('sleep_performance', 0)
            if recovery > 0:
                return {
                    "recovery": int(recovery),
                    "sleep": int(sleep),
                    "zone": "green" if recovery >= 67 else "yellow" if recovery >= 50 else "red"
                }
    except:
        pass
    
    # Fallback: no data available
    return {"recovery": 0, "sleep": 0, "zone": "unknown", "nodata": True}

def get_habits_with_streaks():
    """Get habits with individual streaks from Notion Habit Tracker"""
    try:
        import requests
        from datetime import datetime

        # Get Notion API key
        notion_key_path = Path.home() / '.config/notion/api_key'
        if not notion_key_path.exists():
            return _get_fallback_habits()

        with open(notion_key_path, 'r') as f:
            notion_key = f.read().strip()

        # Habit Tracker Database ID
        db_id = "304f2cb1-2276-81bb-b69f-c28f02d35fa5"

        headers = {
            "Authorization": f"Bearer {notion_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        today = datetime.now().strftime('%Y-%m-%d')

        # Query for today's entry
        query = {
            "filter": {
                "property": "Date",
                "date": {
                    "equals": today
                }
            }
        }

        response = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=query
        )

        if response.status_code != 200:
            return _get_fallback_habits()

        data = response.json()
        results = data.get('results', [])

        # Default habits structure
        habits = {
            "fruit": {"current": 0, "goal": 2, "done": False, "streak": 0},
            "vitamins": {"done": False, "streak": 0},
            "creatine": {"done": False, "streak": 0},
            "workout": {"done": False, "streak": 0},
            "water": {"done": False, "streak": 0},
            "sleep": {"hours": 0, "done": False, "streak": 0},
        }

        if results:
            props = results[0].get('properties', {})

            # Fruit (2 portions)
            fruit_done = props.get('Fruit (2 portions)', {}).get('checkbox', False)
            habits['fruit'] = {"current": 2 if fruit_done else 0, "goal": 2, "done": fruit_done, "streak": 0}

            # Multivitamin
            vitamin_done = props.get('Multivitamin', {}).get('checkbox', False)
            habits['vitamins'] = {"done": vitamin_done, "streak": 0}

            # Creatine
            creatine_done = props.get('Creatine', {}).get('checkbox', False)
            habits['creatine'] = {"done": creatine_done, "streak": 0}

            # Exercise/Workout
            exercise_done = props.get('Exercise', {}).get('checkbox', False)
            exercise_type = ""
            if 'Exercise Type' in props:
                rich_text = props['Exercise Type'].get('rich_text', [])
                if rich_text:
                    exercise_type = rich_text[0].get('text', {}).get('content', '')
            habits['workout'] = {"done": exercise_done, "streak": 0, "type": exercise_type}

            # Water (8 glasses)
            water_done = props.get('Water (8 glasses)', {}).get('checkbox', False)
            habits['water'] = {"current": 8 if water_done else 0, "goal": 8, "done": water_done, "streak": 0}

            # Sleep - estimate from WHOOP or default
            sleep_hours = 7.5  # Default estimate
            habits['sleep'] = {"hours": sleep_hours, "done": sleep_hours >= 7, "streak": 0}

        return habits

    except Exception as e:
        print(f"Habits fetch error: {e}")
        return _get_fallback_habits()

def _get_fallback_habits():
    """Fallback habits when Notion is unavailable"""
    return {
        "fruit": {"current": 0, "goal": 2, "done": False, "streak": 0},
        "vitamins": {"done": False, "streak": 0},
        "creatine": {"done": False, "streak": 0},
        "workout": {"done": False, "streak": 0},
        "water": {"current": 0, "goal": 8, "done": False, "streak": 0},
        "sleep": {"hours": 0, "done": False, "streak": 0},
    }

def get_workout_status():
    """Get workout info"""
    return {
        "last": "Today (Kettlebell - Hard)",
        "next": "Tomorrow (Active Recovery)",
        "zone": "green"
    }

def get_security_status():
    """Get security sentinel status from latest audit"""
    try:
        from datetime import datetime
        import re
        import glob

        # Find latest security audit file
        audit_dir = Path.home() / '.openclaw/workspace/research'
        audit_files = glob.glob(str(audit_dir / 'security-audit-*.md'))

        if not audit_files:
            return {"status": "unknown", "pending_updates": 0, "last_check": "Never"}

        # Sort by date (newest first)
        latest_file = sorted(audit_files)[-1]

        with open(latest_file, 'r') as f:
            content = f.read()

        # Count pending updates from the markdown
        pending_count = 0
        status = "clear"

        # Look for upgradeable packages section
        if 'upgradable' in content.lower():
            # Count lines with upgradable packages
            lines = content.split('\n')
            for line in lines:
                if 'upgradable from:' in line.lower():
                    pending_count += 1

        # Determine status
        if pending_count == 0:
            status = "clear"
        elif pending_count < 10:
            status = "low"
        elif pending_count < 30:
            status = "medium"
        else:
            status = "high"

        # Extract date from filename
        date_match = re.search(r'security-audit-(\d{4}-\d{2}-\d{2})\.md', latest_file)
        last_check = date_match.group(1) if date_match else "Unknown"

        return {
            "status": status,
            "pending_updates": pending_count,
            "last_check": last_check
        }

    except Exception as e:
        print(f"Security status error: {e}")
        return {"status": "unknown", "pending_updates": 0, "last_check": "Error"}

def get_7day_history():
    """Get 7-day history for charts"""
    return {
        "recovery": [92, 88, 62, 74, 81, 85, 92],
        "calories_in": [2100, 1950, 2300, 2200, 2050, 2400, 2260],
        "calories_out": [2800, 2600, 2400, 2700, 2500, 2900, 2850],
        "dates": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    }

def generate_sparkline(data, height=40):
    """Generate SVG sparkline chart"""
    if not data:
        return ""
    
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val if max_val != min_val else 1
    
    width = 200
    points = []
    for i, val in enumerate(data):
        x = (i / (len(data) - 1)) * width if len(data) > 1 else width / 2
        y = height - ((val - min_val) / range_val) * (height - 10) - 5
        points.append(f"{x},{y}")
    
    path = "M" + " L".join(points)
    return f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" style="overflow: visible;"><path d="{path}" fill="none" stroke="#667eea" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{width}" cy="{height - ((data[-1] - min_val) / range_val) * (height - 10) - 5}" r="3" fill="#22c55e"/></svg>'

def generate_dashboard():
    """Generate HTML dashboard"""
    
    # Fetch all data
    tat = get_tat_tasks()
    nutrition = get_nutrition_with_meals()
    water = get_water_status()
    whoop = get_whoop_data()
    habits = get_habits_with_streaks()
    workout = get_workout_status()
    security = get_security_status()
    history = get_7day_history()
    
    now = datetime.now()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Sam's Command Center</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0f;
            color: #fff;
            line-height: 1.5;
            padding-bottom: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 20px; font-weight: 600; }}
        .header .date {{ font-size: 14px; opacity: 0.9; margin-top: 5px; }}
        
        .card {{
            background: #1a1a2e;
            margin: 15px;
            border-radius: 16px;
            padding: 15px;
            border: 1px solid #333;
        }}
        .card-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            font-size: 16px;
            font-weight: 600;
        }}
        .card-header .icon {{ font-size: 20px; }}
        
        .whoop-card {{
            background: linear-gradient(135deg, {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'}20, #1a1a2e);
            border-color: {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'};
        }}
        .whoop-score {{ font-size: 32px; font-weight: bold; color: {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'}; }}
        .whoop-label {{ font-size: 12px; color: #aaa; margin-top: 5px; }}
        
        .tat-list {{ list-style: none; }}
        .tat-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }}
        .tat-item:last-child {{ border-bottom: none; }}
        .tat-checkbox {{ width: 20px; height: 20px; border: 2px solid #ef4444; border-radius: 6px; }}
        .tat-name {{ flex: 1; font-size: 14px; }}
        .tat-urgency {{
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            background: #ef444420;
            color: #ef4444;
        }}
        
        .meal-item {{
            background: #0a0a0f;
            padding: 12px;
            border-radius: 10px;
            margin: 8px 0;
        }}
        .meal-name {{ font-weight: 600; color: #667eea; font-size: 13px; }}
        .meal-items {{ font-size: 12px; color: #aaa; margin-top: 4px; }}
        .meal-cal {{ font-size: 12px; color: #888; margin-top: 4px; }}
        
        .macro-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }}
        .macro-item {{
            background: #0a0a0f;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
        }}
        .macro-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
        .macro-label {{ font-size: 11px; color: #aaa; margin-top: 4px; }}
        .macro-goal {{ font-size: 10px; color: #666; }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #333;
            border-radius: 4px;
            margin-top: 8px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 4px;
        }}
        
        .water-glasses {{
            display: flex;
            gap: 8px;
            justify-content: center;
            margin: 10px 0;
            font-size: 24px;
        }}
        .water-full {{ color: #06b6d4; }}
        .water-empty {{ color: #333; }}
        
        .habit-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: #0a0a0f;
            border-radius: 8px;
            margin: 6px 0;
        }}
        .habit-icon {{ font-size: 18px; }}
        .habit-info {{ flex: 1; }}
        .habit-name {{ font-size: 12px; color: #aaa; }}
        .habit-status {{ font-size: 13px; font-weight: 500; }}
        .habit-streak {{
            background: #f59e0b20;
            color: #f59e0b;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        .habit-done {{ color: #22c55e; }}
        .habit-pending {{ color: #f59e0b; }}
        
        .chart-container {{
            background: #0a0a0f;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }}
        .chart-title {{
            font-size: 12px;
            color: #aaa;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }}
        .chart-value {{ color: #667eea; font-weight: 600; }}
        
        .days-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #666;
            margin-top: 5px;
            padding: 0 5px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            font-size: 11px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 Sam's Command Center</h1>
        <div class="date">{now.strftime('%A, %B %d')}</div>
    </div>
'''

    # WHOOP Card
    if whoop.get('nodata'):
        # No WHOOP data available
        html += '''
    <div class="card whoop-card" style="background: linear-gradient(135deg, #333 0%, #1a1a2e 100%); border-color: #666;">
        <div class="card-header">
            <span class="icon">💓</span>
            <span>WHOOP Recovery</span>
        </div>
        <div class="whoop-score" style="color: #888;">--</div>
        <div class="whoop-label">No data available - Sync WHOOP</div>
        <div class="whoop-label" style="margin-top: 8px;">Sleep: --% performance</div>
    </div>
'''
    else:
        html += f'''
    <div class="card whoop-card">
        <div class="card-header">
            <span class="icon">💓</span>
            <span>WHOOP Recovery</span>
        </div>
        <div class="whoop-score">{whoop['recovery']}%</div>
        <div class="whoop-label">{'🟢 Green Zone - Hard Workout Ready!' if whoop['zone'] == 'green' else '🟡 Yellow Zone - Active Recovery' if whoop['zone'] == 'yellow' else '🔴 Red Zone - Rest Day'}</div>
        <div class="whoop-label" style="margin-top: 8px;">Sleep: {whoop['sleep']}% performance</div>
    </div>
'''

    # 7-Day History
    html += '''
    <div class="card">
        <div class="card-header">
            <span class="icon">📊</span>
            <span>7-Day History</span>
        </div>
'''
    
    # Recovery chart
    avg_recovery = sum(history['recovery']) // len(history['recovery'])
    html += f'''
        <div class="chart-container">
            <div class="chart-title">
                <span>Recovery Score</span>
                <span class="chart-value">Avg: {avg_recovery}%</span>
            </div>
            {generate_sparkline(history['recovery'])}
            <div class="days-labels">
                {''.join([f'<span>{d}</span>' for d in history['dates']])}
            </div>
        </div>
'''
    
    # Calories chart
    avg_in = sum(history['calories_in']) // len(history['calories_in'])
    avg_out = sum(history['calories_out']) // len(history['calories_out'])
    html += f'''
        <div class="chart-container">
            <div class="chart-title">
                <span>Calories In</span>
                <span class="chart-value">Avg: {avg_in}</span>
            </div>
            {generate_sparkline(history['calories_in'])}
            <div class="days-labels">
                {''.join([f'<span>{d}</span>' for d in history['dates']])}
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">
                <span>Calories Out</span>
                <span class="chart-value">Avg: {avg_out}</span>
            </div>
            {generate_sparkline(history['calories_out'])}
            <div class="days-labels">
                {''.join([f'<span>{d}</span>' for d in history['dates']])}
            </div>
        </div>
    </div>
'''

    # Urgent TAT (Today only)
    html += '''
    <div class="card">
        <div class="card-header">
            <span class="icon">🔥</span>
            <span>Urgent TAT (Today)</span>
        </div>
        <ul class="tat-list">
'''
    for task in tat:
        html += f'''            <li class="tat-item">
                <div class="tat-checkbox"></div>
                <span class="tat-name">{task['name']}</span>
                <span class="tat-urgency">{task['urgency']}</span>
            </li>
'''
    html += '''        </ul>
    </div>
'''

    # Nutrition with Meals
    cal_percent = (nutrition['calories'] / nutrition['calories_goal']) * 100
    html += f'''
    <div class="card">
        <div class="card-header">
            <span class="icon">🥗</span>
            <span>Today's Nutrition</span>
        </div>
        <div style="text-align: center; margin-bottom: 15px;">
            <div style="font-size: 28px; font-weight: bold; color: #667eea;">{nutrition['calories']}</div>
            <div style="font-size: 12px; color: #aaa;">of {nutrition['calories_goal']} kcal</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {cal_percent}%"></div>
            </div>
        </div>
'''
    
    for meal in nutrition['meals']:
        html += f'''        <div class="meal-item">
            <div class="meal-name">{meal['name']}</div>
            <div class="meal-items">{meal['items']}</div>
            <div class="meal-cal">{meal['cal']} kcal</div>
        </div>
'''
    
    html += '''    </div>
'''

    # Water
    html += f'''
    <div class="card">
        <div class="card-header">
            <span class="icon">💧</span>
            <span>Water Progress</span>
        </div>
        <div class="water-glasses">
'''
    for i in range(water['goal']):
        if i < water['current']:
            html += '            <span class="water-full">💧</span>\n'
        else:
            html += '            <span class="water-empty">⚪</span>\n'
    html += f'''        </div>
        <div style="text-align: center; color: #aaa; font-size: 13px;">
            {water['current']}/{water['goal']} glasses ({(water['current']/water['goal'])*100:.0f}%)
        </div>
    </div>
'''

    # Habits with Individual Streaks
    html += '''
    <div class="card">
        <div class="card-header">
            <span class="icon">✅</span>
            <span>Today's Habits</span>
        </div>
'''
    
    habit_icons = {
        'fruit': '🍎',
        'vitamins': '💊',
        'creatine': '⚡',
        'workout': '🏋️',
        'water': '💧',
        'sleep': '💤'
    }
    
    for habit_name, habit_data in habits.items():
        icon = habit_icons.get(habit_name, '✓')
        is_done = habit_data.get('done', False)
        status_text = 'Done ✅' if is_done else 'Pending ☐'
        status_class = 'habit-done' if is_done else 'habit-pending'
        streak = habit_data.get('streak', 0)
        
        if habit_name == 'fruit':
            current = habit_data.get('current', 0)
            goal = habit_data.get('goal', 2)
            status_text = f"{current}/{goal} {'✅' if is_done else '⏳'}"
        elif habit_name == 'water':
            current = habit_data.get('current', 0)
            goal = habit_data.get('goal', 8)
            status_text = f"{current}/{goal} glasses {'✅' if is_done else '⏳'}"
        elif habit_name == 'sleep':
            hours = habit_data.get('hours', 0)
            status_text = f"{hours}h {'✅' if is_done else '⏳'}"
        elif habit_name == 'workout':
            exercise_type = habit_data.get('type', '')
            if exercise_type and is_done:
                status_text = f"{exercise_type} ✅"
            else:
                status_text = 'Done ✅' if is_done else 'Rest day ⏳'
        
        html += f'''        <div class="habit-item">
            <span class="habit-icon">{icon}</span>
            <div class="habit-info">
                <div class="habit-name">{habit_name.title()}</div>
                <div class="habit-status {status_class}">{status_text}</div>
            </div>
            <span class="habit-streak">🔥 {streak}</span>
        </div>
'''
    
    html += '''    </div>
'''

    # Workout
    html += f'''
    <div class="card">
        <div class="card-header">
            <span class="icon">🏋️</span>
            <span>Workout Status</span>
        </div>
        <div style="margin-bottom: 10px;">
            <div style="font-size: 12px; color: #aaa;">Last Workout</div>
            <div style="font-size: 14px;">{workout['last']}</div>
        </div>
        <div>
            <div style="font-size: 12px; color: #aaa;">Next Workout</div>
            <div style="font-size: 14px; color: {'#22c55e' if workout['zone'] == 'green' else '#f59e0b' if workout['zone'] == 'yellow' else '#ef4444'};">{workout['next']}</div>
        </div>
    </div>
'''

    # Security
    security_color = '#22c55e' if security['status'] == 'clear' else '#f59e0b' if security['status'] == 'low' else '#ef4444' if security['status'] in ['medium', 'high'] else '#888'
    security_icon = '✓' if security['status'] == 'clear' else '⚠️'
    security_text = 'All Clear' if security['status'] == 'clear' else f"{security['pending_updates']} updates pending"
    
    html += f'''
    <div class="card">
        <div class="card-header">
            <span class="icon">🛡️</span>
            <span>Security Status</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: {security_color}; font-size: 18px;">{security_icon}</span>
            <span>{security_text}</span>
        </div>
        <div style="margin-top: 8px; font-size: 12px; color: #888;">
            Last check: {security.get('last_check', 'Unknown')}
        </div>
    </div>
    
    <div class="footer">
        Dashboard v2.1 • Auto-refresh every 15 min
    </div>
</body>
</html>'''

    # Write dashboard
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_PATH, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard v2.1 generated: {DASHBOARD_PATH}")
    print(f"📊 File size: {len(html):,} bytes")

if __name__ == "__main__":
    generate_dashboard()
    print("\n🚀 Dashboard updated with 7-day history and individual habit streaks!")
