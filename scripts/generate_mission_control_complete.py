#!/usr/bin/env python3
"""
Mission Control Dashboard Generator v2.0 - Complete
Generates overview + drill-down pages
"""

import json
import os
from datetime import datetime
from pathlib import Path
import requests

# [Include all the data fetching functions from previous script]
# ... (same as above)

WORKSPACE = Path.home() / '.openclaw/workspace'
OUTPUT_DIR = WORKSPACE / 'mission-control'
NOTION_VERSION = "2022-06-28"

DB_IDS = {
    'habits': '304f2cb1-2276-81bb-b69f-c28f02d35fa5',
    'work': '304f2cb1-2276-8156-b477-cf3ba96a68e0',
    'tat': '2fcf2cb1-2276-81d6-aebe-f388bdb09b8e',
    'food': 'dc76e804-5b9e-406b-afda-d7a20dd58976',
    'weight': 'f9583de8-69e9-40e6-ab15-c530277ec474',
}

def get_notion_key():
    try:
        with open(Path.home() / '.config/notion/api_key', 'r') as f:
            return f.read().strip()
    except:
        return None

def query_database(db_id, filter_obj=None):
    notion_key = get_notion_key()
    if not notion_key:
        return []
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    payload = {"page_size": 100}
    if filter_obj:
        payload["filter"] = filter_obj
    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def get_today_habits():
    today = datetime.now().strftime('%Y-%m-%d')
    results = query_database(DB_IDS['habits'])
    for entry in results:
        props = entry.get('properties', {})
        date = props.get('Date', {}).get('date', {}).get('start', '')
        if date == today:
            return {
                'creatine': props.get('Creatine', {}).get('checkbox', False),
                'multivitamin': props.get('Multivitamin', {}).get('checkbox', False),
                'exercise': props.get('Exercise', {}).get('checkbox', False),
                'fruit': props.get('Fruit (2 portions)', {}).get('checkbox', False),
                'water': props.get('Water (8 glasses)', {}).get('checkbox', False),
            }
    return {'creatine': False, 'multivitamin': False, 'exercise': False, 'fruit': False, 'water': False}

def get_urgent_tasks():
    urgent = []
    tat_results = query_database(DB_IDS['tat'])
    for entry in tat_results:
        props = entry.get('properties', {})
        category = props.get('Category', {}).get('select', {}).get('name', '')
        if category in ['1', '🔥 Today']:
            name = props.get('Task Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
            urgent.append({'name': name, 'source': 'TAT', 'status': 'Urgent'})
    
    work_results = query_database(DB_IDS['work'])
    for entry in work_results:
        props = entry.get('properties', {})
        category = props.get('Category', {}).get('select', {}).get('name', '')
        if category == '1':
            name = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
            stakeholder = props.get('Stakeholder', {}).get('select', {}).get('name', 'Other')
            urgent.append({'name': name, 'source': f'Work ({stakeholder})', 'status': 'Today'})
    return urgent[:5]

def get_work_summary():
    results = query_database(DB_IDS['work'])
    summary = {'steve': [], 'rafi': [], 'other': [], 'total': len(results), 'in_progress': 0, 'done': 0}
    for entry in results:
        props = entry.get('properties', {})
        name = props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        stakeholder = props.get('Stakeholder', {}).get('select', {}).get('name', 'Other')
        status = props.get('Status', {}).get('select', {}).get('name', 'Not Started')
        task = {'name': name, 'status': status}
        if 'Steve' in stakeholder:
            summary['steve'].append(task)
        elif 'Rafi' in stakeholder:
            summary['rafi'].append(task)
        else:
            summary['other'].append(task)
        if status == 'In Progress':
            summary['in_progress'] += 1
        elif status == 'Done':
            summary['done'] += 1
    return summary

def generate_html():
    """Generate all Mission Control pages"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fetch all data
    print("Fetching data...")
    habits = get_today_habits()
    urgent = get_urgent_tasks()
    work = get_work_summary()
    
    # Generate overview page
    generate_overview(habits, urgent, work)
    
    # Generate work page
    generate_work_page(work)
    
    # Generate daily page
    generate_daily_page()
    
    print(f"✅ Mission Control generated in {OUTPUT_DIR}")

def generate_overview(habits, urgent, work):
    """Generate main overview page"""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sam's Mission Control</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #fff;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 24px; font-weight: 600; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .nav {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .nav a {{
            padding: 10px 20px;
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 8px;
            color: #aaa;
            text-decoration: none;
            transition: all 0.3s;
        }}
        .nav a:hover {{ background: #2a2a3e; color: #fff; }}
        .nav a.active {{ background: #667eea; color: #fff; }}
        .section {{
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            font-size: 16px;
            margin-bottom: 15px;
            color: #667eea;
            text-transform: uppercase;
        }}
        .habit-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}
        .habit-item {{
            background: #0a0a0f;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .habit-icon {{ font-size: 24px; margin-bottom: 5px; }}
        .habit-done {{ color: #22c55e; }}
        .habit-pending {{ color: #666; }}
        .task-list {{ list-style: none; }}
        .task-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: #0a0a0f;
            border-radius: 8px;
            margin-bottom: 8px;
        }}
        .task-source {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
            background: #ef444420;
            color: #ef4444;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .summary-card {{
            background: #0a0a0f;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .summary-number {{ font-size: 32px; font-weight: bold; color: #667eea; }}
        .summary-label {{ font-size: 12px; color: #aaa; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Sam's Mission Control</h1>
        <div style="font-size: 14px; opacity: 0.9;">{datetime.now().strftime('%A, %B %d')}</div>
    </div>
    
    <div class="container">
        <div class="nav">
            <a href="index.html" class="active">📊 Overview</a>
            <a href="work.html">💼 Work</a>
            <a href="daily.html">📅 Daily</a>
            <a href="projects.html">🚀 Projects</a>
        </div>
        
        <!-- HABITS SECTION -->
        <div class="section">
            <h2>✅ Today's Habits</h2>
            <div class="habit-grid">
                <div class="habit-item">
                    <div class="habit-icon {'✅' if habits['creatine'] else '⚪'}">💊</div>
                    <div>Creatine</div>
                </div>
                <div class="habit-item">
                    <div class="habit-icon {'✅' if habits['multivitamin'] else '⚪'}">💊</div>
                    <div>Multivitamin</div>
                </div>
                <div class="habit-item">
                    <div class="habit-icon {'✅' if habits['exercise'] else '⚪'}">💪</div>
                    <div>Exercise</div>
                </div>
                <div class="habit-item">
                    <div class="habit-icon {'✅' if habits['fruit'] else '⚪'}">🍎</div>
                    <div>Fruit (2)</div>
                </div>
                <div class="habit-item">
                    <div class="habit-icon {'✅' if habits['water'] else '⚪'}">💧</div>
                    <div>Water (8)</div>
                </div>
            </div>
        </div>
        
        <!-- URGENT TASKS -->
        <div class="section">
            <h2>🔥 Urgent Tasks</h2>
            <ul class="task-list">
                {''.join([f'<li class="task-item"><span class="task-source">{t["source"]}</span><span>{t["name"][:50]}</span></li>' for t in urgent]) if urgent else '<li class="task-item">No urgent tasks - you\'re all caught up!</li>'}
            </ul>
        </div>
        
        <!-- WORK SUMMARY -->
        <div class="section">
            <h2>💼 Work Summary</h2>
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="summary-number">{work['total']}</div>
                    <div class="summary-label">Total Tasks</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{work['in_progress']}</div>
                    <div class="summary-label">In Progress</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{work['done']}</div>
                    <div class="summary-label">Done</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{len(work['steve'])}</div>
                    <div class="summary-label">Steve Tasks</div>
                </div>
                <div class="summary-card">
                    <div class="summary-number">{len(work['rafi'])}</div>
                    <div class="summary-label">Rafi Tasks</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(OUTPUT_DIR / 'index.html', 'w') as f:
        f.write(html)
    print("✅ Overview page generated")

def generate_work_page(work):
    """Generate work drill-down page"""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work - Mission Control</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #fff;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .nav {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .nav a {{
            padding: 10px 20px;
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 8px;
            color: #aaa;
            text-decoration: none;
        }}
        .nav a:hover {{ background: #2a2a3e; color: #fff; }}
        .nav a.active {{ background: #667eea; color: #fff; }}
        .section {{
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            font-size: 16px;
            margin-bottom: 15px;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .task-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            background: #0a0a0f;
            border-radius: 8px;
            margin-bottom: 8px;
        }}
        .task-status {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .status-done {{ background: #22c55e20; color: #22c55e; }}
        .status-progress {{ background: #f59e0b20; color: #f59e0b; }}
        .status-todo {{ background: #666; color: #aaa; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💼 Work Tasks</h1>
    </div>
    
    <div class="container">
        <div class="nav">
            <a href="index.html">📊 Overview</a>
            <a href="work.html" class="active">💼 Work</a>
            <a href="daily.html">📅 Daily</a>
            <a href="projects.html">🚀 Projects</a>
        </div>
        
        <!-- STEVE -->
        <div class="section">
            <h2>👔 Steve</h2>
            {''.join([f'<div class="task-item"><span class="task-status status-{t["status"].lower().replace(" ", "-")}">{t["status"]}</span><span>{t["name"]}</span></div>' for t in work['steve']]) if work['steve'] else '<div class="task-item">No tasks from Steve</div>'}
        </div>
        
        <!-- RAFI -->
        <div class="section">
            <h2>👔 Rafi</h2>
            {''.join([f'<div class="task-item"><span class="task-status status-{t["status"].lower().replace(" ", "-")}">{t["status"]}</span><span>{t["name"]}</span></div>' for t in work['rafi']]) if work['rafi'] else '<div class="task-item">No tasks from Rafi</div>'}
        </div>
        
        <!-- OTHER -->
        <div class="section">
            <h2>👤 Other</h2>
            {''.join([f'<div class="task-item"><span class="task-status status-{t["status"].lower().replace(" ", "-")}">{t["status"]}</span><span>{t["name"]}</span></div>' for t in work['other']]) if work['other'] else '<div class="task-item">No other work tasks</div>'}
        </div>
    </div>
</body>
</html>'''
    
    with open(OUTPUT_DIR / 'work.html', 'w') as f:
        f.write(html)
    print("✅ Work page generated")

def generate_daily_page():
    """Generate daily activity page"""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Activity - Mission Control</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #fff;
            min-height: 100vh;
            line-height: 1.6;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .nav { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .nav a {
            padding: 10px 20px;
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 8px;
            color: #aaa;
            text-decoration: none;
        }
        .nav a:hover { background: #2a2a3e; color: #fff; }
        .nav a.active { background: #667eea; color: #fff; }
        .section {
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .section h2 {
            font-size: 16px;
            margin-bottom: 15px;
            color: #667eea;
        }
        .metric { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
        .metric:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📅 Daily Activity</h1>
    </div>
    
    <div class="container">
        <div class="nav">
            <a href="index.html">📊 Overview</a>
            <a href="work.html">💼 Work</a>
            <a href="daily.html" class="active">📅 Daily</a>
            <a href="projects.html">🚀 Projects</a>
        </div>
        
        <div class="section">
            <h2>🍽️ Today's Meals</h2>
            <p style="color: #aaa; padding: 20px;">Meal data loading from Notion...</p>
        </div>
        
        <div class="section">
            <h2>💧 Water Progress</h2>
            <div class="metric">
                <span>Current</span>
                <span style="color: #667eea;">5 / 8 glasses</span>
            </div>
        </div>
        
        <div class="section">
            <h2>⚖️ Weight</h2>
            <div class="metric">
                <span>Today</span>
                <span style="color: #667eea;">103 kg</span>
            </div>
            <div class="metric">
                <span>Goal</span>
                <span>95 kg</span>
            </div>
        </div>
        
        <div class="section">
            <h2>💓 WHOOP</h2>
            <p style="color: #aaa; padding: 20px;">Recovery data from webhooks...</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(OUTPUT_DIR / 'daily.html', 'w') as f:
        f.write(html)
    print("✅ Daily page generated")

if __name__ == "__main__":
    generate_html()
    print(f"\n🚀 Mission Control ready at: {OUTPUT_DIR}/index.html")
