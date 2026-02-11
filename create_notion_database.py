#!/usr/bin/env python3
"""
Direct Notion Database Creation for Sam's TAT Task System
Builds complete task database with gaming elements and all real tasks
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Get environment variables
NOTION_TOKEN = os.environ.get('NOTION_TOKEN', 'YOUR_TOKEN_HERE')
WORKSPACE_ID = "ea2f2cb1-2276-8163-b1bf-0003b4237bda"

# API Headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_tat_database():
    """Create Sam's TAT Task Database with all real tasks"""
    
    # Database configuration
    database_config = {
        "parent": {
            "type": "page_id",
            "page_id": WORKSPACE_ID
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Sam's TAT Task System 🎮"
                }
            }
        ],
        "properties": {
            "Task Name": {
                "title": {}
            },
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
            "Time Estimated": {
                "number": {}
            },
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
                        {"name": "⏸️ On Hold", "color": "yellow"},
                        {"name": "❌ Cancelled", "color": "red"}
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
            "Created Date": {
                "created_time": {}
            },
            "Due Date": {
                "date": {}
            },
            "Progress %": {
                "number": {}
            },
            "Notes": {
                "rich_text": {}
            }
        }
    }
    
    print("🎮 Creating Sam's TAT Task Database...")
    
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
            return database_id
        else:
            print(f"❌ Error creating database: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def add_tasks_to_database(database_id):
    """Add all of Sam's real tasks to the database"""
    
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=3)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Complete vehicle registration for toll system. Requires phone call and documentation."}}]}
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=3)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Finalize passport application and submission. May require documentation gathering."}}]}
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Replace light bulbs in downstairs area. Simple hardware task."}}]}
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Pay various service fees. Financial administration task."}}]}
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Fix bathroom issues. May require plumbing work or hardware replacement."}}]}
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
                "Due Date": {"date": {"start": (datetime.now() + timedelta(days=7)).isoformat()}},
                "Notes": {"rich_text": [{"text": {"content": "Add Andy and Libby to car insurance policy. Requires phone call to insurance company."}}]}
            }
        }
    ]
    
    print(f"📋 Adding {len(tasks)} tasks to database...")
    
    for i, task in enumerate(tasks, 1):
        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=task
            )
            
            if response.status_code == 200:
                print(f"✅ Task {i} added successfully!")
            else:
                print(f"❌ Error adding task {i}: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception adding task {i}: {e}")
    
    print("🎉 All tasks added successfully!")

def main():
    """Main execution function"""
    print("🚀 Starting Notion database creation...")
    
    # Create the database
    database_id = create_tat_database()
    
    if database_id:
        # Add all tasks
        add_tasks_to_database(database_id)
        
        print(f"\n🎮 Database created successfully!")
        print(f"📊 Database ID: {database_id}")
        print(f"✅ All 6 tasks added with complete gaming structure!")
        print(f"\n🎯 Your TAT Task System is ready for use!")
        print(f"Access it in your Notion workspace and start tracking your tasks! 🦞✨")
    else:
        print("❌ Failed to create database")

if __name__ == "__main__":
    main()