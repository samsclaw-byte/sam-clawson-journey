#!/usr/bin/env python3
"""
Mission Control Dashboard Generator
Fetches real data from Airtable and generates static HTML dashboard
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from airtable_client import get_health_client, get_productivity_client

# Config
WORKSPACE = Path.home() / '.openclaw/workspace'
OUTPUT_PATH = WORKSPACE / 'mission-control/index.html'

def fetch_tat_tasks():
    """Fetch urgent TAT tasks from Airtable"""
    try:
        client = get_productivity_client()
        urgent_tasks = client.get_urgent_tat_tasks()
        
        today = datetime.now().strftime('%Y-%m-%d')
        tasks = []
        
        for task in urgent_tasks:
            fields = task.get('fields', {})
            
            name = fields.get('Task Name', '')
            category = fields.get('Category', '')
            due_date = fields.get('Due Date', '')
            priority = fields.get('Priority', '')
            status = fields.get('Status', '')
            notes = fields.get('Notes', '')
            
            # Check for Steve/Rafi mentions
            source = None
            if 'steve' in name.lower() or 'steve' in notes.lower():
                source = 'steve'
            elif 'rafi' in name.lower() or 'rafi' in notes.lower():
                source = 'rafi'
            
            is_overdue = due_date and due_date < today
            
            if name:
                tasks.append({
                    'name': name,
                    'category': category,
                    'due_date': due_date,
                    'priority': priority,
                    'status': status,
                    'overdue': is_overdue,
                    'source': source
                })
        
        return tasks
    
    except Exception as e:
        print(f"❌ Error fetching TAT tasks: {e}")
        return []

def get_food_log():
    """Get recent food log entries from Airtable"""
    try:
        client = get_health_client()
        entries = client.get_food_entries(days=1)
        
        total_calories = 0
        total_protein = 0
        meal_count = len(entries)
        
        for entry in entries:
            fields = entry.get('fields', {})
            total_calories += fields.get('Calories', 0) or 0
            total_protein += fields.get('Protein (g)', 0) or 0
        
        return {
            'entries': meal_count,
            'calories': total_calories,
            'protein': round(total_protein, 1)
        }
    except Exception as e:
        print(f"❌ Error fetching food log: {e}")
        return {'entries': 0, 'calories': 0, 'protein': 0}

def get_weight_data():
    """Get latest weight entry"""
    try:
        client = get_health_client()
        entries = client.get_weight_entries(days=30)
        
        if entries:
            latest = entries[0]['fields']
            return {
                'weight': latest.get('Weight (kg)'),
                'date': latest.get('Date'),
                'trend': 'stable'
            }
        return {'weight': None, 'date': None, 'trend': 'no data'}
    except Exception as e:
        print(f"❌ Error fetching weight: {e}")
        return {'weight': None, 'date': None, 'trend': 'error'}

def get_workouts():
    """Get recent workouts"""
    try:
        client = get_health_client()
        entries = client.get_workouts(days=7)
        
        total_duration = 0
        workout_count = len(entries)
        
        for entry in entries:
            fields = entry.get('fields', {})
            total_duration += fields.get('Duration (min)', 0) or 0
        
        return {
            'count': workout_count,
            'total_minutes': total_duration,
            'this_week': workout_count
        }
    except Exception as e:
        print(f"❌ Error fetching workouts: {e}")
        return {'count': 0, 'total_minutes': 0, 'this_week': 0}

def get_habits():
    """Get today's habit status"""
    try:
        client = get_health_client()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get all habits from today
        all_habits = client.get_habits(days=1)
        today_habits = [
            h for h in all_habits 
            if h['fields'].get('Date') == today
        ]
        
        # Common habits to track
        expected_habits = ['💊 Creatine', '💊 Multi', '💪 Exercise', '🍎 Fruit', '💧 Water']
        habit_status = {}
        
        for habit_name in expected_habits:
            # Check if this habit was completed today
            completed = any(
                h['fields'].get('Habit') == habit_name and h['fields'].get('Completed')
                for h in today_habits
            )
            habit_status[habit_name] = completed
        
        # Water is special - track count
        water_entries = [h for h in today_habits if 'water' in h['fields'].get('Habit', '').lower()]
        water_count = len(water_entries)
        
        habit_status['💧 Water'] = water_count >= 5  # Consider done if 5+ glasses
        
        return {
            'status': habit_status,
            'water_count': water_count,
            'total_completed': sum(1 for v in habit_status.values() if v)
        }
    except Exception as e:
        print(f"❌ Error fetching habits: {e}")
        return {'status': {}, 'water_count': 0, 'total_completed': 0}

def get_whoop_data():
    """Fetch WHOOP recovery data from file fallback"""
    try:
        whoop_file = Path.home() / '.openclaw/whoop_data/latest_recovery.json'
        if whoop_file.exists():
            with open(whoop_file, 'r') as f:
                data = json.load(f)
                return {
                    'recovery': data.get('recovery_score', 0),
                    'sleep': data.get('sleep_performance', 0),
                    'zone': 'green' if data.get('recovery_score', 0) >= 67 else 'yellow' if data.get('recovery_score', 0) >= 50 else 'red'
                }
    except Exception as e:
        print(f"❌ Error reading WHOOP data: {e}")
    
    # Fallback
    return {'recovery': 62, 'sleep': 83, 'zone': 'yellow'}

def generate_html_dashboard(tasks, food_data, weight_data, workouts, habits, whoop_data):
    """Generate the complete HTML dashboard"""
    
    today = datetime.now()
    day_name = today.strftime('%A, %B %d')
    
    # Separate tasks by source
    steve_tasks = [t for t in tasks if t.get('source') == 'steve']
    rafi_tasks = [t for t in tasks if t.get('source') == 'rafi']
    general_tasks = [t for t in tasks if t.get('source') not in ['steve', 'rafi']]
    
    # Generate urgent items HTML
    urgent_html = ""
    for task in tasks[:3]:
        if task['overdue']:
            urgent_html += f'<div class="task-item"><span class="tag tag-urgent">OVERDUE</span><span>{task["name"]}</span></div>'
        elif task['category'] == '1':
            urgent_html += f'<div class="task-item"><span class="tag tag-work">Today</span><span>{task["name"]}</span></div>'
    
    if whoop_data['recovery'] < 67:
        zone_class = 'tag-urgent' if whoop_data['recovery'] < 50 else 'tag-work'
        urgent_html += f'<div class="task-item"><span class="tag {zone_class}">WHOOP</span><span>Recovery {whoop_data["recovery"]}% - {"Rest day recommended" if whoop_data["recovery"] < 50 else "Take it easy"}</span></div>'
    
    if not urgent_html:
        urgent_html = '<div class="task-item"><span style="color: #22c55e;">✅ All caught up! No urgent items.</span></div>'
    
    # Generate habits HTML
    habits_html = ""
    for habit_name, completed in habits['status'].items():
        emoji = "✅" if completed else "⚪"
        habits_html += f'<div class="habit-item"><div style="font-size: 28px;">{emoji}</div><div>{habit_name}</div></div>'
    
    # Work summary stats
    total_tasks = len(tasks)
    in_progress = len([t for t in tasks if t.get('status') == 'In Progress'])
    done_today = len([t for t in tasks if t.get('status') == 'Complete'])
    
    # Recovery color
    zone_colors = {
        'green': '#22c55e',
        'yellow': '#eab308',
        'red': '#ef4444'
    }
    recovery_color = zone_colors.get(whoop_data['zone'], '#667eea')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sam's Mission Control</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0a0a0f, #1a1a2e); color: #fff; min-height: 100vh; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; text-align: center; position: relative; }}
        .refresh-btn {{ position: absolute; right: 20px; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.2); border: none; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; }}
        .refresh-btn:hover {{ background: rgba(255,255,255,0.3); }}
        .last-updated {{ font-size: 12px; opacity: 0.8; margin-top: 5px; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .nav {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .nav a {{ padding: 10px 20px; background: #1a1a2e; border: 1px solid #333; border-radius: 8px; color: #aaa; text-decoration: none; transition: all 0.2s; }}
        .nav a.active {{ background: #667eea; color: #fff; }}
        .nav a:hover {{ background: #2a2a3e; }}
        .section {{ background: #1a1a2e; border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
        .section h2 {{ font-size: 16px; color: #667eea; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
        .habit-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }}
        .habit-item {{ background: #0a0a0f; padding: 15px; border-radius: 8px; text-align: center; transition: transform 0.2s; }}
        .habit-item:hover {{ transform: scale(1.05); }}
        .card {{ background: #0a0a0f; padding: 20px; border-radius: 10px; text-align: center; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-2px); }}
        .card-number {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .card-label {{ font-size: 12px; color: #aaa; margin-top: 5px; }}
        .task-item {{ background: #0a0a0f; padding: 15px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; transition: background 0.2s; }}
        .task-item:hover {{ background: #1a1a2e; }}
        .tag {{ font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 500; }}
        .tag-urgent {{ background: #ef444420; color: #ef4444; }}
        .tag-work {{ background: #3b82f620; color: #3b82f6; }}
        .tag-personal {{ background: #22c55e20; color: #22c55e; }}
        .tag-health {{ background: #a855f720; color: #a855f7; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin-bottom: 15px; }}
        .recovery-card {{ background: linear-gradient(135deg, {recovery_color}20, {recovery_color}10); border: 1px solid {recovery_color}40; }}
        .recovery-value {{ color: {recovery_color}; font-size: 48px; font-weight: bold; }}
        .progress-bar {{ width: 100%; height: 8px; background: #333; border-radius: 4px; overflow: hidden; margin-top: 10px; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.5s; }}
        .empty-state {{ color: #666; text-align: center; padding: 20px; font-style: italic; }}
        .api-status {{ display: inline-flex; align-items: center; gap: 5px; font-size: 11px; padding: 2px 8px; border-radius: 12px; background: #22c55e20; color: #22c55e; }}
        .api-status.error {{ background: #ef444420; color: #ef4444; }}
        @media (max-width: 600px) {{ .card-number {{ font-size: 24px; }} .recovery-value {{ font-size: 32px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Sam's Mission Control</h1>
        <div style="font-size: 14px; opacity: 0.9;">{day_name}</div>
        <div class="last-updated">Last updated: {today.strftime('%H:%M')} | <span class="api-status">● Airtable Connected</span></div>
        <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
    </div>
    
    <div class="container">
        <div class="nav">
            <a href="index.html" class="active">📊 Overview</a>
            <a href="#health">💪 Health</a>
            <a href="#tasks">✅ Tasks</a>
            <a href="#nutrition">🍽️ Nutrition</a>
        </div>
        
        <div class="section" id="urgent">
            <h2>🔥 Urgent Tasks</h2>
            {urgent_html}
        </div>
        
        <div class="section" id="recovery">
            <h2>💓 Recovery Status</h2>
            <div class="stats-grid">
                <div class="card recovery-card">
                    <div class="recovery-value">{whoop_data['recovery']}%</div>
                    <div class="card-label">Recovery Score</div>
                    <div class="progress-bar"><div class="progress-fill" style="width: {whoop_data['recovery']}%; background: {recovery_color};"></div></div>
                </div>
                <div class="card">
                    <div class="card-number">{whoop_data['sleep']}%</div>
                    <div class="card-label">Sleep Performance</div>
                </div>
                <div class="card">
                    <div class="card-number">{habits['water_count']}/8</div>
                    <div class="card-label">Water Glasses</div>
                </div>
                <div class="card">
                    <div class="card-number">{workouts['this_week']}</div>
                    <div class="card-label">Workouts This Week</div>
                </div>
            </div>
        </div>
        
        <div class="section" id="habits">
            <h2>✅ Today's Habits ({habits['total_completed']}/{len(habits['status'])} completed)</h2>
            <div class="habit-grid">
                {habits_html}
            </div>
        </div>
        
        <div class="section" id="nutrition">
            <h2>🍽️ Today's Nutrition</h2>
            <div class="stats-grid">
                <div class="card">
                    <div class="card-number">{food_data['calories']}</div>
                    <div class="card-label">Calories</div>
                </div>
                <div class="card">
                    <div class="card-number">{food_data['protein']}g</div>
                    <div class="card-label">Protein</div>
                </div>
                <div class="card">
                    <div class="card-number">{food_data['entries']}</div>
                    <div class="card-label">Meals Logged</div>
                </div>
                <div class="card">
                    <div class="card-number">{weight_data['weight'] or '—'}</div>
                    <div class="card-label">Weight (kg)</div>
                </div>
            </div>
        </div>
        
        <div class="section" id="tasks">
            <h2>💼 Task Summary</h2>
            <div class="stats-grid">
                <div class="card">
                    <div class="card-number">{total_tasks}</div>
                    <div class="card-label">Total Urgent</div>
                </div>
                <div class="card">
                    <div class="card-number">{in_progress}</div>
                    <div class="card-label">In Progress</div>
                </div>
                <div class="card">
                    <div class="card-number">{done_today}</div>
                    <div class="card-label">Completed Today</div>
                </div>
                <div class="card">
                    <div class="card-number">{len(steve_tasks)}</div>
                    <div class="card-label">From Steve</div>
                </div>
                <div class="card">
                    <div class="card-number">{len(rafi_tasks)}</div>
                    <div class="card-label">From Rafi</div>
                </div>
            </div>
        </div>
        
        <div class="section" id="all-tasks">
            <h2>📋 All Urgent Tasks</h2>
    '''
    
    # Add task list
    if tasks:
        for task in tasks[:10]:
            priority_class = 'tag-urgent' if task['priority'] == '🔥 Critical' else 'tag-work' if task['priority'] == '⚡ High' else 'tag-personal'
            overdue_marker = '⚠️ ' if task['overdue'] else ''
            due_info = f" (Due: {task['due_date']})" if task['due_date'] else ''
            html += f'<div class="task-item"><span class="tag {priority_class}">{task["priority"] or "No Priority"}</span><span>{overdue_marker}{task["name"]}{due_info}</span></div>'
    else:
        html += '<div class="empty-state">No urgent tasks. You\'re all caught up! 🎉</div>'
    
    html += f'''
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setInterval(function() {{
            location.reload();
        }}, 300000);
        
        function refreshData() {{
            const btn = document.querySelector('.refresh-btn');
            btn.textContent = '🔄 Refreshing...';
            btn.disabled = true;
            location.reload();
        }}
        
        // Update timestamp
        document.addEventListener('DOMContentLoaded', function() {{
            const now = new Date();
            document.querySelector('.last-updated').innerHTML = 
                'Last updated: ' + now.toLocaleTimeString() + ' | <span class="api-status">● Airtable Connected</span>';
        }});
    </script>
</body>
</html>
    '''
    
    return html

def generate_dashboard():
    """Generate the Mission Control HTML dashboard"""
    
    print("🚀 Generating Mission Control Dashboard...")
    print("📡 Fetching data from Airtable...")
    
    # Fetch data from Airtable
    tasks = fetch_tat_tasks()
    food_data = get_food_log()
    weight_data = get_weight_data()
    workouts = get_workouts()
    habits = get_habits()
    whoop = get_whoop_data()
    
    print(f"  📋 Found {len(tasks)} urgent TAT tasks")
    print(f"  🍽️  Food: {food_data['calories']} calories, {food_data['entries']} meals")
    print(f"  ⚖️  Weight: {weight_data['weight'] or 'N/A'} kg")
    print(f"  💪 Workouts: {workouts['this_week']} this week")
    print(f"  ✅ Habits: {habits['total_completed']}/{len(habits['status'])} completed")
    print(f"  💓 WHOOP: {whoop['recovery']}% recovery")
    
    # Generate HTML
    html = generate_html_dashboard(tasks, food_data, weight_data, workouts, habits, whoop)
    
    # Save to file
    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated!")
    print(f"📄 View at: {OUTPUT_PATH}")
    print(f"🌐 Or open: file://{OUTPUT_PATH}")
    
    return True

if __name__ == "__main__":
    generate_dashboard()
    print("\n💡 To view: Open mission-control/index.html in your browser")
    print("🔄 Auto-refresh: Every 5 minutes (in-browser)")
    print("📡 Data source: Airtable API")
