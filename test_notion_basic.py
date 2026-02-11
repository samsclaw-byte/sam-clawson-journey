#!/usr/bin/env python3
"""
Basic Notion Test - Immediate Database Creation
Creates simple test database so Sam can verify API works
"""

import os
import requests
import json
from datetime import datetime, timedelta

# Environment setup
NOTION_TOKEN = os.environ.get('NOTION_TOKEN', 'YOUR_TOKEN_HERE')
WORKSPACE_ID = "2fcf2cb122768021a8a9ce059efecbf6"

# API Headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_test_database():
    """Create a simple test database"""
    
    print("🧪 Creating basic test database...")
    
    # Simple test database
    test_config = {
        "parent": {
            "type": "page_id", 
            "page_id": WORKSPACE_ID
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "API Test 🧪"
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Testing", "color": "blue"},
                        {"name": "Working", "color": "green"},
                        {"name": "Issue", "color": "red"}
                    ]
                }
            },
            "Notes": {
                "rich_text": {}
            }
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=test_config
        )
        
        if response.status_code == 200:
            result = response.json()
            database_id = result['id']
            print(f"✅ Test database created successfully!")
            print(f"📊 Database ID: {database_id}")
            return database_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def add_test_task(database_id):
    """Add a simple test task"""
    
    test_task = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": "API Connection Test"}}]},
            "Status": {"select": {"name": "Testing"}},
            "Notes": {"rich_text": [{"text": {"content": "Testing Notion API connection. If you can see this, the API is working! 🎉"}}]}
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=test_task
        )
        
        if response.status_code == 200:
            print(f"✅ Test task added successfully!")
            return True
        else:
            print(f"❌ Error adding task: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception adding task: {e}")
        return False

def test_api_connection():
    """Test basic API connectivity"""
    print("🔍 Testing API connection...")
    
    try:
        # Test basic connectivity
        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ API connection working!")
            print(f"👤 User: {user_data.get('name', 'Unknown')}")
            print(f"🏢 Workspace: {user_data.get('bot', {}).get('workspace_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Connection test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    print("🚀 Starting basic Notion test...")
    
    # Test connection first
    if test_api_connection():
        # Create database
        database_id = create_test_database()
        
        if database_id:
            # Add test task
            if add_test_task(database_id):
                print(f"\n🎉 SUCCESS! Your Notion API is working perfectly!")
                print(f"📊 Database ID: {database_id}")
                print(f"✨ Go to your Notion workspace and look for 'API Test 🧪'")
                print(f"✨ You should see the test task there!")
                print(f"\n🦞 Ready to build the full TAT system tomorrow!")
            else:
                print("❌ Failed to add test task")
        else:
            print("❌ Failed to create database")
    else:
        print("❌ API connection not working")

if __name__ == "__main__":
    main()
