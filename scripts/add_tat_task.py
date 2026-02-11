#!/usr/bin/env python3
"""
Add TAT Task - Natural Language to Notion
With smart defaults: Laptop=1, Other=7
"""

import os
import re
import requests
from datetime import datetime

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
if not NOTION_API_KEY:
    try:
        with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
            NOTION_API_KEY = f.read().strip()
    except FileNotFoundError:
        print("❌ Notion API key not found")
        exit(1)

# TAT Database ID
TAT_DB_ID = "2fcf2cb1-2276-81d6-aebe-f388bdb09b8e"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

# Laptop-related keywords
LAPTOP_KEYWORDS = [
    'laptop', 'computer', 'code', 'script', 'github', 'git', 'ssh',
    'database', 'notion', 'api', 'config', 'setup', 'install',
    'push', 'commit', 'deploy', 'server', 'cron', 'workflow',
    'dashboard', 'update', 'fix code', 'debug', 'terminal'
]

def determine_category(task_name):
    """Determine default category based on task content"""
    task_lower = task_name.lower()
    
    # Check if it's a laptop/computer task
    is_laptop_task = any(keyword in task_lower for keyword in LAPTOP_KEYWORDS)
    
    if is_laptop_task:
        return "1"  # Today
    else:
        return "7"  # 7 Days (default for non-laptop)

def extract_category(text):
    """Extract category if explicitly specified"""
    # Look for explicit category mentions
    patterns = [
        r'\bcategory\s*(\d+)\b',
        r'\bcat\s*(\d+)\b',
        r'\b(\d+)\s*days?\b',
        r'#(\d+)\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            cat = match.group(1)
            if cat in ['1', '3', '7', '30']:
                return cat
    
    return None

def add_tat_task(task_name, notes=""):
    """Add TAT task to Notion with smart defaults"""
    
    # Extract explicit category if mentioned
    explicit_category = extract_category(task_name + " " + notes)
    
    if explicit_category:
        category = explicit_category
        # Remove category mention from task name
        task_name = re.sub(r'\s*\(?\b(cat|category)\s*\d+\)?\b', '', task_name, flags=re.IGNORECASE).strip()
    else:
        # Use smart defaults
        category = determine_category(task_name)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    properties = {
        "Task Name": {
            "title": [{"text": {"content": task_name}}]
        },
        "Category": {
            "select": {"name": category}
        },
        "Status": {
            "select": {"name": "Not Started"}
        },
        "Date Created": {
            "date": {"start": today}
        }
    }
    
    if notes:
        properties["Notes"] = {
            "rich_text": [{"text": {"content": notes}}]
        }
    
    payload = {
        "parent": {"database_id": TAT_DB_ID},
        "properties": properties
    }
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        cat_name = {"1": "Today", "3": "3 Days", "7": "7 Days", "30": "30 Days"}.get(category, category)
        print(f"✅ Added TAT: {task_name}")
        print(f"   Category: {cat_name} (auto-determined)")
        print(f"   Due: {today} + {category} days")
        return True
    else:
        print(f"❌ Failed to add TAT: {response.text}")
        return False

def parse_natural_language(text):
    """Parse natural language TAT creation"""
    text_lower = text.lower()
    
    # Check if this is a TAT creation message
    tat_keywords = ['add tat', 'new tat', 'tat:', 'create tat', 'tat for']
    
    is_tat = any(kw in text_lower for kw in tat_keywords)
    
    if not is_tat:
        return None
    
    # Extract task name
    # Remove TAT keywords
    task_name = text
    for kw in tat_keywords:
        task_name = re.sub(kw, '', task_name, flags=re.IGNORECASE)
    
    task_name = task_name.strip(' :,-')
    
    # Split task name from notes if there's a separator
    parts = re.split(r'[.!?]\s+', task_name, maxsplit=1)
    
    if len(parts) > 1:
        task_name = parts[0].strip()
        notes = parts[1].strip()
    else:
        notes = ""
    
    return task_name, notes

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        parsed = parse_natural_language(text)
        
        if parsed:
            task_name, notes = parsed
            add_tat_task(task_name, notes)
        else:
            # Direct task name (no "add tat" prefix)
            add_tat_task(text)
    else:
        print("Usage: python3 add_tat_task.py 'Add TAT: Fix the printer'")
        print("       python3 add_tat_task.py 'Research flights category 3'")
        print("")
        print("Auto-categories:")
        print("  Laptop/Computer tasks → Category 1 (Today)")
        print("  Everything else → Category 7 (7 Days)")
