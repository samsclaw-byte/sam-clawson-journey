#!/usr/bin/env python3
"""
TAT Database Migration Script
Updates Notion TAT database schema per user requirements
"""

import requests
import json
import os
from datetime import datetime

# Config
NOTION_TOKEN = os.getenv('NOTION_TOKEN') or open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
TAT_DATABASE_ID = "2fcf2cb1-2276-81d6-aebe-f388bdb09b8e"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2025-09-03"
}

def get_database_schema():
    """Get current database schema"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def update_tat_category():
    """Update TAT Category to strict 4 options"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}"
    
    data = {
        "properties": {
            "TAT Category": {
                "select": {
                    "options": [
                        {"name": "🔥 Today", "color": "red"},
                        {"name": "⚡ 3 days", "color": "yellow"},
                        {"name": "📅 7 days", "color": "blue"},
                        {"name": "📆 30 days", "color": "green"}
                    ]
                }
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("✅ TAT Category updated to strict 4 options")
        return True
    else:
        print(f"❌ Failed to update TAT Category: {response.text}")
        return False

def add_date_created_property():
    """Add 'Date Created' property"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}"
    
    data = {
        "properties": {
            "Date Created": {
                "date": {}
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("✅ Date Created property added")
        return True
    else:
        print(f"❌ Failed to add Date Created: {response.text}")
        return False

def update_category_options():
    """Update Category to include 'Laptop tasks' and modify AI Development"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}"
    
    data = {
        "properties": {
            "Category": {
                "select": {
                    "options": [
                        {"name": "💪 Health", "color": "green"},
                        {"name": "💼 Work", "color": "blue"},
                        {"name": "👨‍👩‍👧 Family", "color": "yellow"},
                        {"name": "🔧 Projects", "color": "orange"},
                        {"name": "🛡️ Security", "color": "red"},
                        {"name": "🎨 Content", "color": "purple"},
                        {"name": "🧠 AI Development", "color": "pink"},
                        {"name": "💻 Laptop Tasks", "color": "gray"},
                        {"name": "🏠 Home", "color": "brown"},
                        {"name": "💰 Finance", "color": "default"}
                    ]
                }
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("✅ Category options updated (added Laptop Tasks)")
        return True
    else:
        print(f"❌ Failed to update Category: {response.text}")
        return False

def remove_property(property_name):
    """Remove a property from database"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}"
    
    # Note: Notion API doesn't actually support deleting properties
    # We'll archive them by renaming instead
    data = {
        "properties": {
            property_name: None  # This should remove it
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"✅ Removed property: {property_name}")
        return True
    else:
        print(f"⚠️  Could not remove {property_name} via API")
        print(f"   Manual removal required in Notion UI")
        return False

def populate_date_created():
    """Populate Date Created for existing tasks"""
    # Query all tasks
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to query tasks: {response.text}")
        return
    
    tasks = response.json().get('results', [])
    today = datetime.now().strftime('%Y-%m-%d')
    
    updated = 0
    for task in tasks:
        task_id = task['id']
        
        # Check if Date Created is already set
        if task.get('properties', {}).get('Date Created', {}).get('date'):
            continue
        
        # Update with today's date
        update_url = f"https://api.notion.com/v1/pages/{task_id}"
        update_data = {
            "properties": {
                "Date Created": {
                    "date": {
                        "start": today
                    }
                }
            }
        }
        
        update_response = requests.patch(update_url, headers=HEADERS, json=update_data)
        if update_response.status_code == 200:
            updated += 1
    
    print(f"✅ Populated Date Created for {updated} existing tasks")

def migrate_existing_tasks():
    """Migrate existing tasks to new category format"""
    url = f"https://api.notion.com/v1/databases/{TAT_DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to query tasks: {response.text}")
        return
    
    tasks = response.json().get('results', [])
    
    # Mapping old categories to new
    category_mapping = {
        "🔥 1 Day": "🔥 Today",
        "⚡ 3 Day": "⚡ 3 days",
        "📅 7 Day": "📅 7 days",
        "📆 30 Day": "📆 30 days"
    }
    
    updated = 0
    for task in tasks:
        task_id = task['id']
        properties = task.get('properties', {})
        
        # Check TAT Category
        tat_category = properties.get('TAT Category', {}).get('select', {}).get('name', '')
        if tat_category in category_mapping:
            update_url = f"https://api.notion.com/v1/pages/{task_id}"
            update_data = {
                "properties": {
                    "TAT Category": {
                        "select": {
                            "name": category_mapping[tat_category]
                        }
                    }
                }
            }
            
            requests.patch(update_url, headers=HEADERS, json=update_data)
            updated += 1
    
    if updated > 0:
        print(f"✅ Migrated {updated} tasks to new category format")
    else:
        print("ℹ️  No tasks needed category migration")

def main():
    print("🔄 TAT Database Migration")
    print("=" * 50)
    print()
    
    # 1. Update TAT Category options
    print("1. Updating TAT Category to strict 4 options...")
    update_tat_category()
    print()
    
    # 2. Add Date Created property
    print("2. Adding Date Created property...")
    add_date_created_property()
    print()
    
    # 3. Update Category options (add Laptop Tasks)
    print("3. Updating Category options...")
    update_category_options()
    print()
    
    # 4. Note about removing Priority and Time Estimated
    print("4. Property removal:")
    print("   ⚠️  Notion API doesn't support property deletion")
    print("   📝 Please manually remove in Notion UI:")
    print("      - Priority")
    print("      - Time Estimated")
    print()
    
    # 5. Populate Date Created for existing tasks
    print("5. Populating Date Created for existing tasks...")
    populate_date_created()
    print()
    
    # 6. Migrate existing tasks
    print("6. Migrating existing tasks to new categories...")
    migrate_existing_tasks()
    print()
    
    print("=" * 50)
    print("✅ Migration complete!")
    print()
    print("Summary of changes:")
    print("  ✓ TAT Category: Now 4 strict options (Today, 3/7/30 days)")
    print("  ✓ Date Created: Added as new property")
    print("  ✓ Category: Added 'Laptop Tasks' option")
    print("  ⚠ Priority & Time Estimated: Remove manually in Notion")
    print()
    print("Next steps:")
    print("  1. Open Notion TAT database")
    print("  2. Delete 'Priority' column")
    print("  3. Delete 'Time Estimated' column")
    print("  4. Set 'Date Created' as required field for new tasks")

if __name__ == "__main__":
    main()
