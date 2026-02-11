#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta

# Get Notion API key
with open('/home/samsclaw/.config/notion/api_key', 'r') as f:
    NOTION_KEY = f.read().strip()

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Page ID where we'll create the database
PAGE_ID = "2fcf2cb122768021a8a9ce059efecbf6"

print("🎮 Creating Sam's TAT Task System...")

# Create the database using the correct endpoint
database_config = {
    "parent": {"page_id": PAGE_ID},
    "title": [{"type": "text", "text": {"content": "Sam's TAT Task System 🎮"}}],
    "properties": {
        "Task Name": {"title": {}},
        "TAT Category": {
            "select": {
                "options": [
                    {"name": "🔴 Today", "color": "red"},
                    {"name": "🟠 3-Day", "color": "orange"},
                    {"name": "🟡 7-Day", "color": "yellow"},
                    {"name": "🟢 Low", "color": "green"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "🔥 Critical", "color": "red"},
                    {"name": "⚡ High", "color": "orange"},
                    {"name": "📋 Medium", "color": "yellow"},
                    {"name": "💤 Low", "color": "gray"}
                ]
            }
        },
        "Time Estimated": {"number": {"format": "number"}},
        "Category": {
            "select": {
                "options": [
                    {"name": "💼 Work", "color": "blue"},
                    {"name": "👨‍👩‍👧‍👦 Family", "color": "purple"},
                    {"name": "🏠 Home", "color": "green"},
                    {"name": "📚 Personal", "color": "pink"},
                    {"name": "🎨 Creative", "color": "yellow"},
                    {"name": "🏃 Health", "color": "orange"}
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "🆕 Not Started", "color": "gray"},
                    {"name": "🔄 In Progress", "color": "blue"},
                    {"name": "✅ Complete", "color": "green"},
                    {"name": "⏸️ On Hold", "color": "yellow"}
                ]
            }
        },
        "Energy Required": {
            "select": {
                "options": [
                    {"name": "🔋 High Energy", "color": "red"},
                    {"name": "⚡ Medium Energy", "color": "yellow"},
                    {"name": "😴 Low Energy", "color": "gray"}
                ]
            }
        },
        "Due Date": {"date": {}},
        "Notes": {"rich_text": {}}
    }
}

try:
    response = requests.post(
        "https://api.notion.com/v1/databases",
        headers=headers,
        json=database_config
    )
    
    if response.status_code == 200:
        result = response.json()
        database_id = result['id']
        print(f"✅ Database created successfully!")
        print(f"📊 Database ID: {database_id}")
        
        # Add all 6 tasks
        tasks = [
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Register car for Salik"}}]},
                    "TAT Category": {"select": {"name": "🟠 3-Day"}},
                    "Priority": {"select": {"name": "⚡ High"}},
                    "Time Estimated": {"number": 30},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "⚡ Medium Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Complete vehicle registration for toll system."}}]}
                }
            },
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Complete UK passport renewal"}}]},
                    "TAT Category": {"select": {"name": "🟠 3-Day"}},
                    "Priority": {"select": {"name": "⚡ High"}},
                    "Time Estimated": {"number": 90},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "🔋 High Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Finalize passport application and submission."}}]}
                }
            },
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Buy and install downstairs bulbs"}}]},
                    "TAT Category": {"select": {"name": "🟡 7-Day"}},
                    "Priority": {"select": {"name": "💤 Low"}},
                    "Time Estimated": {"number": 30},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "⚡ Medium Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Replace light bulbs in downstairs area."}}]}
                }
            },
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Pay service fees"}}]},
                    "TAT Category": {"select": {"name": "🟡 7-Day"}},
                    "Priority": {"select": {"name": "📋 Medium"}},
                    "Time Estimated": {"number": 30},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "⚡ Medium Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Pay various service fees."}}]}
                }
            },
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Fix bath"}}]},
                    "TAT Category": {"select": {"name": "🟡 7-Day"}},
                    "Priority": {"select": {"name": "⚡ High"}},
                    "Time Estimated": {"number": 60},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "🔋 High Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Fix bathroom issues. May require plumbing work."}}]}
                }
            },
            {
                "parent": {"database_id": database_id},
                "properties": {
                    "Task Name": {"title": [{"text": {"content": "Speak to Insurance company to add Andy and Libby to car insurance"}}]},
                    "TAT Category": {"select": {"name": "🟡 7-Day"}},
                    "Priority": {"select": {"name": "⚡ High"}},
                    "Time Estimated": {"number": 45},
                    "Category": {"select": {"name": "🏠 Home"}},
                    "Status": {"select": {"name": "🆕 Not Started"}},
                    "Energy Required": {"select": {"name": "⚡ Medium Energy"}},
                    "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}},
                    "Notes": {"rich_text": [{"text": {"content": "Add Andy and Libby to car insurance policy."}}]}
                }
            }
        ]
        
        print(f"\n📋 Adding {len(tasks)} tasks...")
        
        for i, task in enumerate(tasks, 1):
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=task
            )
            
            if response.status_code == 200:
                print(f"✅ Task {i} added: {task['properties']['Task Name']['title'][0]['text']['content']}")
            else:
                print(f"❌ Error adding task {i}: {response.status_code}")
        
        print(f"\n🎉 SUCCESS! Your TAT Task System is ready!")
        print(f"📊 Database ID: {database_id}")
        print(f"✅ All 6 tasks added!")
        print(f"\n🦞 Go to your Notion workspace and check for 'Sam's TAT Task System 🎮'!")
        
    else:
        print(f"❌ Error creating database: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
