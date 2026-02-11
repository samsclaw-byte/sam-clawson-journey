#!/usr/bin/env python3
"""
Rebuild Habit Tracker Database with Individual Streak Tracking
Each habit has its own Current Streak and Longest Streak properties
"""

import os
import requests
from datetime import datetime, timedelta

# Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = "2fdf2cb12276818f8845ed296b42d781"
PARENT_PAGE_ID = "2fcf2cb1-2276-8021-a8a9-ce059efecbf6"

if not NOTION_TOKEN:
    print("❌ NOTION_TOKEN not found in environment variables")
    exit(1)

# API Headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def delete_database_entries(database_id):
    """Delete all existing entries in the database"""
    print("🗑️  Checking for existing entries to delete...")
    
    try:
        # Query all entries
        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=headers,
            json={"page_size": 100}
        )
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            print(f"📋 Found {len(results)} existing entries")
            
            for entry in results:
                entry_id = entry['id']
                archive_response = requests.patch(
                    f"https://api.notion.com/v1/pages/{entry_id}",
                    headers=headers,
                    json={"archived": True}
                )
                if archive_response.status_code == 200:
                    print(f"  ✅ Archived entry: {entry_id}")
                else:
                    print(f"  ⚠️  Could not archive entry: {entry_id}")
        else:
            print(f"⚠️  Could not query database: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Error deleting entries: {e}")

def update_database_schema(database_id):
    """Update database schema with individual streak properties for each habit"""
    print("📊 Updating database schema with individual streak tracking...")
    
    schema_updates = {
        "properties": {
            # Date property
            "Date": {
                "date": {}
            },
            # Fruit habit with streaks
            "Fruit": {
                "checkbox": {}
            },
            "Fruit Current Streak": {
                "number": {
                    "format": "number"
                }
            },
            "Fruit Longest Streak": {
                "number": {
                    "format": "number"
                }
            },
            # Multivitamin habit with streaks
            "Multivitamin": {
                "checkbox": {}
            },
            "Multi Current Streak": {
                "number": {
                    "format": "number"
                }
            },
            "Multi Longest Streak": {
                "number": {
                    "format": "number"
                }
            },
            # Exercise habit with streaks
            "Exercise": {
                "checkbox": {}
            },
            "Exercise Current Streak": {
                "number": {
                    "format": "number"
                }
            },
            "Exercise Longest Streak": {
                "number": {
                    "format": "number"
                }
            },
            # Water habit with streaks
            "Water": {
                "number": {
                    "format": "number"
                }
            },
            "Water Current Streak": {
                "number": {
                    "format": "number"
                }
            },
            "Water Longest Streak": {
                "number": {
                    "format": "number"
                }
            }
        }
    }
    
    try:
        response = requests.patch(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers,
            json=schema_updates
        )
        
        if response.status_code == 200:
            print("✅ Database schema updated successfully!")
            return True
        else:
            print(f"❌ Error updating schema: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception updating schema: {e}")
        return False

def add_habit_entry(database_id, date_str, fruit, fruit_streak, fruit_longest,
                   multivitamin, multi_streak, multi_longest,
                   exercise, exercise_streak, exercise_longest,
                   water, water_streak, water_longest):
    """Add a habit tracking entry"""
    
    entry = {
        "parent": {"database_id": database_id},
        "properties": {
            "Date": {"date": {"start": date_str}},
            "Fruit": {"checkbox": fruit},
            "Fruit Current Streak": {"number": fruit_streak},
            "Fruit Longest Streak": {"number": fruit_longest},
            "Multivitamin": {"checkbox": multivitamin},
            "Multi Current Streak": {"number": multi_streak},
            "Multi Longest Streak": {"number": multi_longest},
            "Exercise": {"checkbox": exercise},
            "Exercise Current Streak": {"number": exercise_streak},
            "Exercise Longest Streak": {"number": exercise_longest},
            "Water": {"number": water},
            "Water Current Streak": {"number": water_streak},
            "Water Longest Streak": {"number": water_longest}
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=entry
        )
        
        if response.status_code == 200:
            print(f"✅ Entry added for {date_str}")
            return True
        else:
            print(f"❌ Error adding entry for {date_str}: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception adding entry: {e}")
        return False

def main():
    """Main execution function"""
    print("🦞 Rebuilding Habit Tracker Database with Individual Streak Tracking")
    print("=" * 70)
    
    # Step 1: Delete existing entries
    delete_database_entries(DATABASE_ID)
    
    print()
    
    # Step 2: Update database schema
    if not update_database_schema(DATABASE_ID):
        print("❌ Failed to update database schema. Exiting.")
        return
    
    print()
    
    # Step 3: Add Feb 3 entry (Yesterday)
    print("📅 Adding February 3rd entry (Yesterday)...")
    add_habit_entry(
        DATABASE_ID,
        "2026-02-03",
        fruit=True,           # Checked
        fruit_streak=1,       # Streak 1
        fruit_longest=1,
        multivitamin=True,    # Checked
        multi_streak=1,       # Streak 1
        multi_longest=1,
        exercise=False,       # Not checked
        exercise_streak=0,    # Broken streak
        exercise_longest=0,
        water=1,              # Water count
        water_streak=1,       # Streak 1
        water_longest=1
    )
    
    print()
    
    # Step 4: Add Feb 4 entry (Today)
    print("📅 Adding February 4th entry (Today)...")
    add_habit_entry(
        DATABASE_ID,
        "2026-02-04",
        fruit=True,           # Continuing
        fruit_streak=2,       # Now streak 2
        fruit_longest=2,
        multivitamin=True,    # Checked
        multi_streak=2,       # Streak 2
        multi_longest=2,
        exercise=True,        # Checked today
        exercise_streak=1,    # New streak started
        exercise_longest=1,
        water=1,              # Water count
        water_streak=2,       # Streak 2
        water_longest=2
    )
    
    print()
    print("=" * 70)
    print("🎉 Habit Tracker Database Rebuilt Successfully!")
    print()
    print("📊 Database Structure:")
    print("  • Date - Entry date")
    print("  • Fruit (checkbox) + Fruit Current/Longest Streak")
    print("  • Multivitamin (checkbox) + Multi Current/Longest Streak")
    print("  • Exercise (checkbox) + Exercise Current/Longest Streak")
    print("  • Water (number) + Water Current/Longest Streak")
    print()
    print("📋 Populated with:")
    print("  • Feb 3: Fruit✅(1), Multi✅(1), Exercise❌(0), Water✅(1)")
    print("  • Feb 4: Fruit✅(2), Multi✅(2), Exercise✅(1), Water✅(2)")
    print()
    print(f"🔗 Database ID: {DATABASE_ID}")
    print("✨ Ready for daily habit tracking!")

if __name__ == "__main__":
    main()
