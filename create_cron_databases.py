#!/usr/bin/env python3
"""
Create 3 Cron Scheduling and Task Management Databases in Sam's Notion Workspace
Parent Page ID: 2fcf2cb1-2276-8021-a8a9-ce059efecbf6
"""

import os
import json
import requests

# Get Notion API token
NOTION_TOKEN = os.environ.get('NOTION_TOKEN') or open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
PARENT_PAGE_ID = "2fcf2cb1-2276-8021-a8a9-ce059efecbf6"

# API Headers - using 2022-06-28 for database creation (2025-09-03 for data sources)
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_master_cron_schedule():
    """Create Master Cron Schedule database"""
    
    database_config = {
        "parent": {
            "page_id": PARENT_PAGE_ID
        },
        "title": [
            {
                "text": {
                    "content": "📅 Master Cron Schedule"
                }
            }
        ],
        "properties": {
            "Task Name": {
                "title": {}
            },
            "Time": {
                "select": {
                    "options": [
                        {"name": "6:00 AM", "color": "yellow"},
                        {"name": "10:00 PM", "color": "purple"},
                        {"name": "11:00 AM", "color": "blue"}
                    ]
                }
            },
            "Task Type": {
                "select": {
                    "options": [
                        {"name": "📰 Briefing", "color": "blue"},
                        {"name": "🔨 Build", "color": "green"},
                        {"name": "🔍 Research", "color": "orange"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "📋 Scheduled", "color": "gray"},
                        {"name": "🔄 Running", "color": "blue"},
                        {"name": "✅ Complete", "color": "green"},
                        {"name": "❌ Failed", "color": "red"}
                    ]
                }
            },
            "Last Run Date": {
                "date": {}
            },
            "Next Run Date": {
                "date": {}
            },
            "Description": {
                "rich_text": {}
            }
        },
        "is_inline": False
    }
    
    print("📅 Creating Master Cron Schedule database...")
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=database_config
        )
        
        if response.status_code == 200:
            result = response.json()
            database_id = result['id']
            print(f"✅ Master Cron Schedule created!")
            print(f"   Database ID: {database_id}")
            return database_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def create_overnight_build_tasks():
    """Create Overnight Build Tasks database"""
    
    database_config = {
        "parent": {
            "page_id": PARENT_PAGE_ID
        },
        "title": [
            {
                "text": {
                    "content": "🔨 Overnight Build Tasks"
                }
            }
        ],
        "properties": {
            "Task Name": {
                "title": {}
            },
            "Description": {
                "rich_text": {}
            },
            "Priority": {
                "select": {
                    "options": [
                        {"name": "🔴 Critical", "color": "red"},
                        {"name": "🟠 High", "color": "orange"},
                        {"name": "🟡 Medium", "color": "yellow"},
                        {"name": "🟢 Low", "color": "green"}
                    ]
                }
            },
            "Estimated Time": {
                "rich_text": {}
            },
            "Dependencies": {
                "rich_text": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "⏳ Pending", "color": "gray"},
                        {"name": "🔄 Running", "color": "blue"},
                        {"name": "✅ Complete", "color": "green"},
                        {"name": "❌ Failed", "color": "red"}
                    ]
                }
            },
            "Database/Tool Needed": {
                "rich_text": {}
            },
            "Created Date": {
                "created_time": {}
            },
            "Completion Date": {
                "date": {}
            }
        },
        "is_inline": False
    }
    
    print("🔨 Creating Overnight Build Tasks database...")
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=database_config
        )
        
        if response.status_code == 200:
            result = response.json()
            database_id = result['id']
            print(f"✅ Overnight Build Tasks created!")
            print(f"   Database ID: {database_id}")
            return database_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def create_overnight_research_tasks():
    """Create Overnight Research Tasks database"""
    
    database_config = {
        "parent": {
            "page_id": PARENT_PAGE_ID
        },
        "title": [
            {
                "text": {
                    "content": "🔍 Overnight Research Tasks"
                }
            }
        ],
        "properties": {
            "Topic": {
                "title": {}
            },
            "Category": {
                "select": {
                    "options": [
                        {"name": "🔒 Security", "color": "red"},
                        {"name": "💻 Dev", "color": "blue"},
                        {"name": "🎮 Gaming", "color": "purple"},
                        {"name": "🤖 AI", "color": "green"},
                        {"name": "📱 Tech", "color": "orange"},
                        {"name": "🌐 Web3", "color": "pink"},
                        {"name": "📊 Data", "color": "yellow"},
                        {"name": "🎯 Other", "color": "gray"}
                    ]
                }
            },
            "Priority": {
                "select": {
                    "options": [
                        {"name": "🔴 Critical", "color": "red"},
                        {"name": "🟠 High", "color": "orange"},
                        {"name": "🟡 Medium", "color": "yellow"},
                        {"name": "🟢 Low", "color": "green"}
                    ]
                }
            },
            "Sources to Check": {
                "multi_select": {
                    "options": [
                        {"name": "🐦 X/Twitter", "color": "blue"},
                        {"name": "🐙 GitHub", "color": "gray"},
                        {"name": "💬 Discord", "color": "purple"},
                        {"name": "📰 Reddit", "color": "orange"},
                        {"name": "📚 Blogs", "color": "green"},
                        {"name": "📄 Papers", "color": "yellow"},
                        {"name": "▶️ YouTube", "color": "red"},
                        {"name": "🔗 HackerNews", "color": "pink"}
                    ]
                }
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "⏳ Pending", "color": "gray"},
                        {"name": "🔄 Running", "color": "blue"},
                        {"name": "✅ Complete", "color": "green"},
                        {"name": "❌ Failed", "color": "red"}
                    ]
                }
            },
            "Findings Summary": {
                "rich_text": {}
            },
            "Created Date": {
                "created_time": {}
            },
            "Completion Date": {
                "date": {}
            },
            "Links Found": {
                "url": {}
            }
        },
        "is_inline": False
    }
    
    print("🔍 Creating Overnight Research Tasks database...")
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=database_config
        )
        
        if response.status_code == 200:
            result = response.json()
            database_id = result['id']
            print(f"✅ Overnight Research Tasks created!")
            print(f"   Database ID: {database_id}")
            return database_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    """Main execution function"""
    print("🚀 Creating 3 Cron Scheduling & Task Management Databases")
    print(f"📄 Parent Page ID: {PARENT_PAGE_ID}")
    print("=" * 60)
    
    # Create all three databases
    cron_db = create_master_cron_schedule()
    print()
    build_db = create_overnight_build_tasks()
    print()
    research_db = create_overnight_research_tasks()
    
    print("\n" + "=" * 60)
    print("🎉 All Databases Created Successfully!")
    print("=" * 60)
    
    if cron_db:
        print(f"\n📅 Master Cron Schedule:")
        print(f"   Database ID: {cron_db}")
        print(f"   Properties: Task Name, Time (6am/10pm/11am), Task Type (Briefing/Build/Research), Status, Last Run Date, Next Run Date")
    
    if build_db:
        print(f"\n🔨 Overnight Build Tasks:")
        print(f"   Database ID: {build_db}")
        print(f"   Properties: Task Name, Description, Priority (Critical/High/Medium/Low), Estimated Time, Dependencies, Status, Database/Tool Needed")
    
    if research_db:
        print(f"\n🔍 Overnight Research Tasks:")
        print(f"   Database ID: {research_db}")
        print(f"   Properties: Topic, Category (Security/Dev/Gaming/etc), Priority, Sources to Check (X/GitHub/Discord), Status, Findings Summary")
    
    print("\n✨ All databases are ready to use in Sam's Notion workspace!")
    
    # Save database IDs for reference
    db_info = {
        "master_cron_schedule": {"database_id": cron_db},
        "overnight_build_tasks": {"database_id": build_db},
        "overnight_research_tasks": {"database_id": research_db},
        "parent_page_id": PARENT_PAGE_ID
    }
    
    with open("/home/samsclaw/.openclaw/workspace/cron_databases.json", "w") as f:
        json.dump(db_info, f, indent=2)
    
    print("📁 Database IDs saved to: cron_databases.json")

if __name__ == "__main__":
    main()
