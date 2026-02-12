#!/usr/bin/env python3
"""
Add TAT Task - Natural Language to Airtable
With smart defaults: Laptop=1, Other=7
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from airtable_client import get_productivity_client

# Laptop-related keywords
LAPTOP_KEYWORDS = [
    'laptop', 'computer', 'code', 'script', 'github', 'git', 'ssh',
    'database', 'notion', 'airtable', 'api', 'config', 'setup', 'install',
    'push', 'commit', 'deploy', 'server', 'cron', 'workflow',
    'dashboard', 'update', 'fix code', 'debug', 'terminal', 'python',
    'javascript', 'html', 'css', 'server', 'cloudflare', 'tunnel'
]

# Priority keywords
PRIORITY_KEYWORDS = {
    'critical': '🔥 Critical',
    'urgent': '🔥 Critical',
    'high': '⚡ High',
    'medium': '📋 Medium',
    'low': '💤 Low'
}

def determine_category(task_name):
    """Determine default category based on task content"""
    task_lower = task_name.lower()
    
    # Check if it's a laptop/computer task
    is_laptop_task = any(keyword in task_lower for keyword in LAPTOP_KEYWORDS)
    
    if is_laptop_task:
        return "1"  # Today
    else:
        return "7"  # 7 Days (default for non-laptop)

def determine_priority(task_name):
    """Determine priority based on task content"""
    task_lower = task_name.lower()
    
    for keyword, priority in PRIORITY_KEYWORDS.items():
        if keyword in task_lower:
            return priority
    
    return "📋 Medium"  # Default

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

def extract_priority(text):
    """Extract priority if explicitly specified"""
    text_lower = text.lower()
    
    for keyword, priority in PRIORITY_KEYWORDS.items():
        if keyword in text_lower:
            return priority
    
    return None

def clean_task_name(task_name):
    """Remove category and priority keywords from task name"""
    # Remove category mentions
    task_name = re.sub(r'\s*\(?\b(cat|category)\s*\d+\)?\b', '', task_name, flags=re.IGNORECASE).strip()
    
    # Remove priority keywords
    for keyword in PRIORITY_KEYWORDS.keys():
        task_name = re.sub(rf'\b{keyword}\b', '', task_name, flags=re.IGNORECASE).strip()
    
    # Clean up extra whitespace
    task_name = ' '.join(task_name.split())
    
    return task_name

def add_tat_task(task_name, notes=""):
    """Add TAT task to Airtable with smart defaults"""
    
    # Extract explicit category if mentioned
    explicit_category = extract_category(task_name + " " + notes)
    explicit_priority = extract_priority(task_name + " " + notes)
    
    if explicit_category:
        category = explicit_category
    else:
        # Use smart defaults
        category = determine_category(task_name)
    
    if explicit_priority:
        priority = explicit_priority
    else:
        priority = determine_priority(task_name)
    
    # Clean task name
    clean_name = clean_task_name(task_name)
    
    # Calculate due date
    days = int(category) if category.isdigit() else 7
    due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    
    try:
        client = get_productivity_client()
        result = client.add_tat_task(
            task_name=clean_name,
            category=category,
            priority=priority,
            notes=notes,
            due_date=due_date
        )
        
        cat_name = {"1": "Today", "3": "3 Days", "7": "7 Days", "30": "30 Days"}.get(category, category)
        print(f"✅ Added TAT to Airtable: {clean_name}")
        print(f"   Category: {cat_name} (auto-determined)")
        print(f"   Priority: {priority}")
        print(f"   Due: {due_date}")
        print(f"   Record ID: {result.get('id', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add TAT: {e}")
        return False

def parse_natural_language(text):
    """Parse natural language TAT creation"""
    text_lower = text.lower()
    
    # Check if this is a TAT creation message
    tat_keywords = ['add tat', 'new tat', 'tat:', 'create tat', 'tat for', 'tat task']
    
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

def show_recent_tasks(limit=5):
    """Show recent TAT tasks from Airtable"""
    try:
        client = get_productivity_client()
        tasks = client.get_tat_tasks()
        
        print(f"\n📋 Recent TAT Tasks (last {limit}):")
        print("-" * 50)
        
        for task in tasks[:limit]:
            fields = task.get('fields', {})
            name = fields.get('Task Name', 'Unnamed')
            category = fields.get('Category', 'N/A')
            status = fields.get('Status', 'N/A')
            due = fields.get('Due Date', 'No date')
            
            cat_display = {"1": "🔴 Today", "3": "🟠 3-Day", "7": "🟡 7-Day", "30": "🟢 30-Day"}.get(category, category)
            print(f"  {cat_display} | {name} ({status})")
        
        print()
        
    except Exception as e:
        print(f"⚠️ Could not fetch recent tasks: {e}")

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
        print("       python3 add_tat_task.py 'Research flights category 3 priority high'")
        print("       python3 add_tat_task.py 'Update laptop script'  # Auto: Category 1")
        print("       python3 add_tat_task.py 'Buy groceries'  # Auto: Category 7")
        print("")
        print("Auto-categories:")
        print("  Laptop/Computer tasks → Category 1 (Today)")
        print("  Everything else → Category 7 (7 Days)")
        print("")
        print("Auto-priorities:")
        print("  'critical', 'urgent' → 🔥 Critical")
        print("  'high' → ⚡ High")
        print("  'low' → 💤 Low")
        print("  Everything else → 📋 Medium")
        print("")
        
        # Show recent tasks
        show_recent_tasks()
