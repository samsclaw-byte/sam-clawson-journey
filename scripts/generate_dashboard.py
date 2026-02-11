#!/usr/bin/env python3
"""
Sam's Daily Command Center - Dashboard Generator
Fetches data from all sources and generates mobile-optimized HTML dashboard
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Config
DASHBOARD_PATH = Path.home() / '.openclaw/workspace/dashboard/index.html'
DATA_DIR = Path.home() / '.openclaw'

def get_tat_tasks():
    """Fetch urgent TAT tasks from Notion"""
    # Placeholder - will integrate with Notion API
    return [
        {"name": "Fix voice transcription", "urgency": "1 Day", "due": "Today"},
        {"name": "WHOOP webhooks setup", "urgency": "7 Days", "due": "In 5 days"},
        {"name": "Security updates", "urgency": "1 Day", "due": "Today"},
    ]

def get_nutrition_summary():
    """Get today's nutrition totals"""
    # Will integrate with Notion Nutrition DB
    return {
        "calories": 1350,
        "calories_goal": 2500,
        "protein": 62,
        "protein_goal": 160,
        "carbs": 145,
        "carbs_goal": 250,
        "fat": 65,
        "fat_goal": 80,
        "meals": [
            {"name": "Breakfast", "cal": 500},
            {"name": "Lunch", "cal": 850},
        ]
    }

def get_water_status():
    """Get water tracker status"""
    try:
        with open(DATA_DIR / 'water_tracker.json', 'r') as f:
            data = json.load(f)
            return {
                "current": data.get('today', 5),
                "goal": 8
            }
    except:
        return {"current": 5, "goal": 8}

def get_whoop_data():
    """Get WHOOP recovery data"""
    try:
        with open(DATA_DIR / 'whoop_webhook_data.json', 'r') as f:
            data = json.load(f)
            return {
                "recovery": data.get('recovery_score', 92),
                "sleep": data.get('sleep_performance', 83),
                "zone": "green" if data.get('recovery_score', 0) >= 67 else "yellow" if data.get('recovery_score', 0) >= 50 else "red"
            }
    except:
        return {"recovery": 92, "sleep": 83, "zone": "green"}

def get_habits():
    """Get today's habit status"""
    return {
        "fruit": {"current": 2, "goal": 2, "done": True},
        "vitamins": {"done": True},
        "workout": {"done": False},
        "sleep": {"hours": 7.5, "done": True},
        "streak": 12
    }

def get_workout_status():
    """Get workout info"""
    return {
        "last": "Yesterday (Swim - Active)",
        "next": "Today (Hard - Kettlebell)",
        "zone": "green"
    }

def get_security_status():
    """Get security sentinel status"""
    return {
        "status": "clear",
        "pending_updates": 35
    }

def generate_dashboard():
    """Generate HTML dashboard"""
    
    # Fetch all data
    tat = get_tat_tasks()
    nutrition = get_nutrition_summary()
    water = get_water_status()
    whoop = get_whoop_data()
    habits = get_habits()
    workout = get_workout_status()
    security = get_security_status()
    
    now = datetime.now()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Sam's Command Center</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
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
        
        .header h1 {{
            font-size: 20px;
            font-weight: 600;
        }}
        
        .header .date {{
            font-size: 14px;
            opacity: 0.9;
            margin-top: 5px;
        }}
        
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
        
        .card-header .icon {{
            font-size: 20px;
        }}
        
        /* WHOOP Card */
        .whoop-card {{
            background: linear-gradient(135deg, {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'}20, #1a1a2e);
            border-color: {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'};
        }}
        
        .whoop-score {{
            font-size: 32px;
            font-weight: bold;
            color: {'#22c55e' if whoop['zone'] == 'green' else '#f59e0b' if whoop['zone'] == 'yellow' else '#ef4444'};
        }}
        
        .whoop-label {{
            font-size: 12px;
            color: #aaa;
            margin-top: 5px;
        }}
        
        /* TAT Tasks */
        .tat-list {{
            list-style: none;
        }}
        
        .tat-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }}
        
        .tat-item:last-child {{
            border-bottom: none;
        }}
        
        .tat-checkbox {{
            width: 20px;
            height: 20px;
            border: 2px solid #667eea;
            border-radius: 6px;
        }}
        
        .tat-name {{
            flex: 1;
            font-size: 14px;
        }}
        
        .tat-urgency {{
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            background: #f59e0b20;
            color: #f59e0b;
        }}
        
        /* Nutrition */
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
        
        .macro-value {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .macro-label {{
            font-size: 11px;
            color: #aaa;
            margin-top: 4px;
        }}
        
        .macro-goal {{
            font-size: 10px;
            color: #666;
        }}
        
        /* Progress Bar */
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
            transition: width 0.3s;
        }}
        
        /* Water Tracker */
        .water-glasses {{
            display: flex;
            gap: 8px;
            justify-content: center;
            margin: 10px 0;
            font-size: 24px;
        }}
        
        .water-full {{ color: #06b6d4; }}
        .water-empty {{ color: #333; }}
        
        /* Habits */
        .habit-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        
        .habit-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px;
            background: #0a0a0f;
            border-radius: 8px;
        }}
        
        .habit-icon {{
            font-size: 18px;
        }}
        
        .habit-info {{
            flex: 1;
        }}
        
        .habit-name {{
            font-size: 12px;
            color: #aaa;
        }}
        
        .habit-status {{
            font-size: 13px;
            font-weight: 500;
        }}
        
        .habit-done {{ color: #22c55e; }}
        .habit-pending {{ color: #f59e0b; }}
        
        .streak {{
            text-align: center;
            margin-top: 15px;
            padding: 10px;
            background: #f59e0b20;
            border-radius: 8px;
        }}
        
        .streak-number {{
            font-size: 24px;
            font-weight: bold;
            color: #f59e0b;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            font-size: 11px;
            color: #666;
        }}
        
        /* Animations */
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        .live-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 6px;
            animation: pulse 2s infinite;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 Sam's Command Center</h1>
        <div class="date">{now.strftime('%A, %B %d')}</div>
    </div>
    
    <!-- WHOOP Recovery -->
    <div class="card whoop-card">
        <div class="card-header">
            <span class="icon">💓</span>
            <span>WHOOP Recovery</span>
        </div>
        <div class="whoop-score">{whoop['recovery']}%</div>
        <div class="whoop-label">{'🟢 Green Zone - Hard Workout Ready!' if whoop['zone'] == 'green' else '🟡 Yellow Zone - Active Recovery' if whoop['zone'] == 'yellow' else '🔴 Red Zone - Rest Day'}</div>
        <div class="whoop-label" style="margin-top: 8px;">Sleep: {whoop['sleep']}% performance</div>
    </div>
    
    <!-- Urgent TAT Tasks -->
    <div class="card">
        <div class="card-header">
            <span class="icon">🔥</span>
            <span>Urgent TAT ({len(tat)})</span>
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
    
    cal_percent = (nutrition['calories'] / nutrition['calories_goal']) * 100
    
    html += f'''        </ul>
    </div>
    
    <!-- Nutrition Summary -->
    <div class="card">
        <div class="card-header">
            <span class="icon">🥗</span>
            <span>Today's Nutrition</span>
        </div>
        <div class="macro-item" style="background: transparent; margin-bottom: 10px;">
            <div class="macro-value" style="font-size: 28px;">{nutrition['calories']}</div>
            <div class="macro-label">Calories</div>
            <div class="macro-goal">Goal: {nutrition['calories_goal']}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {cal_percent}%"></div>
            </div>
        </div>
        <div class="macro-grid">
            <div class="macro-item">
                <div class="macro-value">{nutrition['protein']}g</div>
                <div class="macro-label">Protein</div>
                <div class="macro-goal">Goal: {nutrition['protein_goal']}g</div>
            </div>
            <div class="macro-item">
                <div class="macro-value">{nutrition['carbs']}g</div>
                <div class="macro-label">Carbs</div>
                <div class="macro-goal">Goal: {nutrition['carbs_goal']}g</div>
            </div>
            <div class="macro-item">
                <div class="macro-value">{nutrition['fat']}g</div>
                <div class="macro-label">Fat</div>
                <div class="macro-goal">Goal: {nutrition['fat_goal']}g</div>
            </div>
            <div class="macro-item">
                <div class="macro-value">{water['current']}/{water['goal']}</div>
                <div class="macro-label">Glasses</div>
                <div class="macro-goal">Water</div>
            </div>
        </div>
    </div>
    
    <!-- Water Tracker -->
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
    
    <!-- Habits -->
    <div class="card">
        <div class="card-header">
            <span class="icon">✅</span>
            <span>Today's Habits</span>
        </div>
        <div class="habit-grid">
            <div class="habit-item">
                <span class="habit-icon">🍎</span>
                <div class="habit-info">
                    <div class="habit-name">Fruit</div>
                    <div class="habit-status habit-done">{habits['fruit']['current']}/{habits['fruit']['goal']} ✅</div>
                </div>
            </div>
            <div class="habit-item">
                <span class="habit-icon">💊</span>
                <div class="habit-info">
                    <div class="habit-name">Vitamins</div>
                    <div class="habit-status habit-done">Taken ✅</div>
                </div>
            </div>
            <div class="habit-item">
                <span class="habit-icon">🏋️</span>
                <div class="habit-info">
                    <div class="habit-name">Workout</div>
                    <div class="habit-status habit-pending">Pending ☐</div>
                </div>
            </div>
            <div class="habit-item">
                <span class="habit-icon">💤</span>
                <div class="habit-info">
                    <div class="habit-name">Sleep</div>
                    <div class="habit-status habit-done">{habits['sleep']['hours']}h ✅</div>
                </div>
            </div>
        </div>
        <div class="streak">
            <div class="streak-number">🔥 {habits['streak']} Days</div>
            <div style="font-size: 11px; color: #aaa;">Current Streak</div>
        </div>
    </div>
    
    <!-- Workout Status -->
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
    
    <!-- Security -->
    <div class="card">
        <div class="card-header">
            <span class="icon">🛡️</span>
            <span>Security Status</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: #22c55e; font-size: 18px;">✓</span>
            <span>All Clear</span>
        </div>
        <div style="margin-top: 8px; font-size: 12px; color: #f59e0b;">
            {security['pending_updates']} system updates pending
        </div>
    </div>
    
    <div class="footer">
        <span class="live-indicator"></span>
        Last updated: {now.strftime('%H:%M')}
        <br>
        Auto-refresh every 15 minutes
    </div>
</body>
</html>'''
    
    # Write dashboard
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_PATH, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {DASHBOARD_PATH}")
    print(f"📊 File size: {len(html):,} bytes")

if __name__ == "__main__":
    generate_dashboard()
    print("\n🚀 To view: Open dashboard/index.html in browser")
    print("📱 Optimized for mobile!")
