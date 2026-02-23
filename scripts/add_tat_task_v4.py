#!/usr/bin/env python3
"""
Add TAT Task v4 - D1 Database
Uses Cloudflare D1 instead of Airtable
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from d1_client import D1Client

# Laptop-related keywords
LAPTOP_KEYWORDS = [
    'laptop', 'computer', 'code', 'script', 'github', 'git', 'ssh',
    'push', 'commit', 'deploy', 'server', 'cron', 'workflow',
    'dashboard', 'update', 'fix code', 'debug', 'terminal', 'python',
    'javascript', 'html', 'css', 'server', 'cloudflare', 'tunnel'
]

# Priority keywords
PRIORITY_KEYWORDS = {
    'critical': 'High',
    'urgent': 'High',
    'high': 'High',
    'medium': 'Medium',
    'low': 'Low'
}

def determine_category(task_name):
    """Determine default category based on task content"""
    task_lower = task_name.lower()
    
    # Check if it's a laptop/computer task
    is_laptop_task = any(keyword in task_lower for keyword in LAPTOP_KEYWORDS)
    
    if is_laptop_task:
        return 1  # Today
    else:
        return 7  # 7 Days (default)

def determine_priority(task_name):
    """Determine priority based on task content"""
    task_lower = task_name.lower()
    
    for keyword, priority in PRIORITY_KEYWORDS.items():
        if keyword in task_lower:
            return priority
    
    return "Medium"

def extract_category(text):
    """Extract category if explicitly specified"""
    patterns = [
        r'\bcategory\s*(\d+)\b',
        r'\bcat\s*(\d+)\b',
        r'\b(\d+)\s*days?\b',
        r'#(\d+)\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            cat = int(match.group(1))
            if cat in [1, 3, 7, 30]:
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
    """Add TAT task to D1"""
    
    # Extract explicit category if mentioned
    explicit_category = extract_category(task_name + " " + notes)
    explicit_priority = extract_priority(task_name + " " + notes)
    
    if explicit_category:
        category = explicit_category
    else:
        category = determine_category(task_name)
    
    if explicit_priority:
        priority = explicit_priority
    else:
        priority = determine_priority(task_name)
    
    # Clean task name
    clean_name = clean_task_name(task_name)
    
    try:
        client = D1Client()
        result = client.create_task(
            task_name=clean_name,
            category=category,
            priority=priority,
            notes=notes
        )
        
        cat_name = {1: "Today", 3: "3 Days", 7: "7 Days", 30: "30 Days"}.get(category, category)
        print(f"✅ TAT Task created: {clean_name}")
        print(f"   Category: {cat_name}")
        print(f"   Priority: {priority}")
        print(f"   Status: Not Started")
        print(f"   Record ID: {result.get('id', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add TAT: {e}")
        return False

def show_pending_tasks(limit=10):
    """Show pending TAT tasks"""
    try:
        client = D1Client()
        tasks = client.get_tasks()
        
        # Filter pending
        pending = [t for t in tasks if t.get('status') != 'Completed']
        pending.sort(key=lambda x: x.get('due_date', ''))
        
        print(f"\n📋 Pending TAT Tasks:")
        print("-" * 60)
        
        for task in pending[:limit]:
            due = task.get('due_date', 'N/A')
            name = task.get('task_name', 'Untitled')
            cat = task.get('category')
            status = task.get('status', 'Not Started')
            print(f"  [{status}] {name} (Cat: {cat}, Due: {due})")
        
        if not pending:
            print("  No pending tasks!")
        
        return pending
        
    except Exception as e:
        print(f"❌ Failed to fetch tasks: {e}")
        return []

# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add_tat_task_v4.py <task_name> [category] [priority]")
        print("Example: add_tat_task_v4.py \"Talk to gardener\" 7")
        sys.exit(1)
    
    task_name = sys.argv[1]
    category = int(sys.argv[2]) if len(sys.argv) > 2 else None
    notes = sys.argv[3] if len(sys.argv) > 3 else ""
    
    # Override category if provided
    if not category:
        category = determine_category(task_name)
    
    # Clean name
    clean_name = clean_task_name(task_name)
    priority = determine_priority(task_name)
    
    # Add task
    client = D1Client()
    result = client.create_task(clean_name, category, priority, notes)
    
    cat_name = {1: "Today", 3: "3 Days", 7: "7 Days", 30: "30 Days"}.get(category, category)
    print(f"✅ TAT Task created: {clean_name}")
    print(f"   Category: {cat_name}")
    print(f"   Priority: {priority}")
    print(f"   Status: Not Started")
    print(f"   ID: {result.get('id')}")
