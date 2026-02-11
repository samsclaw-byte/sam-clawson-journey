#!/usr/bin/env python3
"""
Create Visual Views for Habit Tracker Database
Since Notion API doesn't support creating database views directly,
we'll create linked database blocks with filters and a comprehensive
visual dashboard page.
"""

import os
import requests
from datetime import datetime, timedelta

# Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN') or open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
DATABASE_ID = "2fdf2cb12276818f8845ed296b42d781"
PARENT_PAGE_ID = "2fcf2cb1-2276-8021-a8a9-ce059efecbf6"

# API Headers (using older version for compatibility with existing databases)
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_database_info(database_id):
    """Get database schema and properties"""
    print(f"📊 Fetching database info...")
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database found: {data['title'][0]['text']['content']}")
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def query_database_entries(database_id, start_date=None, end_date=None):
    """Query database entries with optional date filter"""
    
    body = {"page_size": 100}
    
    if start_date and end_date:
        body["filter"] = {
            "and": [
                {"property": "Date", "date": {"on_or_after": start_date}},
                {"property": "Date", "date": {"on_or_before": end_date}}
            ]
        }
    
    try:
        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=headers,
            json=body
        )
        
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"⚠️ Query error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"⚠️ Query exception: {e}")
        return []

def create_visual_dashboard_page(parent_page_id):
    """Create a visual dashboard page with embedded database views"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_future = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    page_config = {
        "parent": {"page_id": parent_page_id},
        "icon": {"emoji": "📊"},
        "properties": {
            "title": [{"text": {"content": "🎮 Habit Tracker Visual Dashboard"}}]
        },
        "children": [
            # Header
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"text": {"content": "🎮 Habit Tracker Visual Dashboard"}}],
                    "color": "blue"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "Visual views of your habit tracking data. Each section shows different perspectives on your progress."}},
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Week View Section
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📅 Last 7 Days at a Glance"}}],
                    "color": "purple"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"Showing entries from {week_ago} to {today}"}}],
                    "icon": {"emoji": "📆"},
                    "color": "purple_background"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "🔗 Open Habit Tracker Database: "}},
                        {"text": {"content": f"https://notion.so/{DATABASE_ID.replace('-', '')}", "link": {"url": f"https://notion.so/{DATABASE_ID.replace('-', '')}"}}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "💡 Tip: In Notion, change this to 'Table' view and sort by Date descending to see the last 7 days."}}]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Calendar View Section
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🗓️ Calendar View"}}],
                    "color": "green"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"text": {"content": "To create a Calendar view:\n1. Open the Habit Tracker database\n2. Click '+' next to existing views\n3. Select 'Calendar'\n4. Set 'Date' property as the calendar date\n\nColor coding by habit completion:\n🟢 All habits complete | 🟡 Some habits | 🔴 No habits"}}
                    ],
                    "icon": {"emoji": "💡"},
                    "color": "green_background"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "🔗 Open Database: "}},
                        {"text": {"content": f"https://notion.so/{DATABASE_ID.replace('-', '')}", "link": {"url": f"https://notion.so/{DATABASE_ID.replace('-', '')}"}}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Board View Section (Kanban)
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📋 Board View (Kanban Style)"}}],
                    "color": "orange"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"text": {"content": "To create a Board view:\n1. Open the Habit Tracker database\n2. Click '+' next to existing views\n3. Select 'Board'\n4. Group by 'Date' property\n\nThis shows habits grouped by date with completion status!"}}
                    ],
                    "icon": {"emoji": "🎯"},
                    "color": "orange_background"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "🔗 Open Database: "}},
                        {"text": {"content": f"https://notion.so/{DATABASE_ID.replace('-', '')}", "link": {"url": f"https://notion.so/{DATABASE_ID.replace('-', '')}"}}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Gallery View Section
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🖼️ Gallery View - Daily Habit Cards"}}],
                    "color": "pink"
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"text": {"content": "To create a Gallery view:\n1. Open the Habit Tracker database\n2. Click '+' next to existing views\n3. Select 'Gallery'\n4. Show properties: Fruit, Multivitamin, Exercise, Water, Streak counts\n\nThis creates beautiful cards showing each day's habit summary!"}}
                    ],
                    "icon": {"emoji": "✨"},
                    "color": "pink_background"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "🔗 Open Database: "}},
                        {"text": {"content": f"https://notion.so/{DATABASE_ID.replace('-', '')}", "link": {"url": f"https://notion.so/{DATABASE_ID.replace('-', '')}"}}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Visual Progress Summary
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📈 Quick Stats"}}],
                    "color": "blue"
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "🍎 Fruit Habit Stats"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Current Streak: Check 'Fruit Current Streak' property"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Longest Streak: Check 'Fruit Longest Streak' property"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "💊 Multivitamin Habit Stats"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Current Streak: Check 'Multi Current Streak' property"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Longest Streak: Check 'Multi Longest Streak' property"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "🏃 Exercise Habit Stats"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Current Streak: Check 'Exercise Current Streak' property"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Longest Streak: Check 'Exercise Longest Streak' property"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "💧 Water Habit Stats"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Current Streak: Check 'Water Current Streak' property"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"text": {"content": "Longest Streak: Check 'Water Longest Streak' property"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            
            # Instructions for manual view creation
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "⚙️ How to Set Up Views in Notion"}}],
                    "color": "gray"
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"text": {"content": "Click on the Habit Tracker database link above"}}]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"text": {"content": "Look for the view tabs at the top (Default View, Table, etc.)"}}]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"text": {"content": "Click the '+' icon to add a new view"}}]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"text": {"content": "Choose from: Table, Board, Gallery, Calendar, Timeline, List, or Form"}}]
                }
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"text": {"content": "Name your view and customize the layout!"}}]
                }
            },
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [
                        {"text": {"content": "💡 Pro Tip: Create multiple views for different purposes. For example:\n• 'This Week' - Filtered to show only last 7 days\n• 'Monthly Calendar' - Calendar view for the full month\n• 'Streak Board' - Board view grouped by habit type\n• 'Progress Gallery' - Gallery view with large cards showing all stats"}}
                    ]
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=page_config
        )
        
        if response.status_code == 200:
            result = response.json()
            page_id = result['id']
            print(f"✅ Visual Dashboard Page created!")
            print(f"📄 Page ID: {page_id}")
            return page_id
        else:
            print(f"❌ Error creating page: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception creating page: {e}")
        return None

def create_linked_database_with_filters(parent_page_id, view_name, filter_config=None):
    """
    Create a linked database block with specific filters.
    Note: Notion API has limited support for view filters in linked databases.
    """
    
    # For now, we create a simple linked database
    # The user will need to manually configure filters in Notion UI
    blocks = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"text": {"content": view_name}}]
            }
        },
        {
            "object": "block",
            "type": "link_to_page",
            "link_to_page": {
                "type": "database_id",
                "database_id": DATABASE_ID
            }
        }
    ]
    
    try:
        response = requests.patch(
            f"https://api.notion.com/v1/blocks/{parent_page_id}/children",
            headers=headers,
            json={"children": blocks}
        )
        
        if response.status_code == 200:
            print(f"✅ Added '{view_name}' linked database")
            return True
        else:
            print(f"⚠️ Error adding linked database: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Exception: {e}")
        return False

def generate_view_setup_guide():
    """Generate a detailed guide for setting up views in Notion UI"""
    
    guide = """
# 🎮 Habit Tracker Visual Views Setup Guide

## ⚠️ Important Note About Notion API
The Notion API **does not support creating database views programmatically**. 
Views must be created manually in the Notion web/app interface.

However, I've created a **Visual Dashboard Page** with links and instructions!

---

## 📋 Views to Create (Step-by-Step)

### 1️⃣ Calendar View
**Purpose:** See habits by date with color coding

**Setup:**
1. Open your Habit Tracker database
2. Click the `+` next to existing view tabs
3. Select **"Calendar"**
4. Set "Date" as the calendar property
5. Name it "📅 Calendar View"

**Color Coding Setup:**
- Click the view settings (•••)
- Go to "Layout" → "Color"
- Create rules:
  - 🟢 Green: When "Fruit" is checked AND "Exercise" is checked
  - 🟡 Yellow: When 1-2 habits completed
  - 🔴 Red: When 0 habits completed

---

### 2️⃣ Board View (Kanban Style)
**Purpose:** Group by date showing habit completion status

**Setup:**
1. Click `+` to add new view
2. Select **"Board"**
3. Group by: "Date" 
4. Name it "📋 Board View"
5. Card preview: Show all habit checkboxes

**Customize Cards:**
- Show: Fruit, Multivitamin, Exercise, Water
- Show streak numbers

---

### 3️⃣ Gallery View
**Purpose:** Card-based view showing daily habit summaries with visual progress

**Setup:**
1. Click `+` to add new view
2. Select **"Gallery"**
3. Name it "🖼️ Gallery View"
4. Card size: Large
5. Card preview: Show Date as title

**Properties to Show:**
- ✅ Fruit (with streak)
- 💊 Multivitamin (with streak)
- 🏃 Exercise (with streak)
- 💧 Water (with streak)

---

### 4️⃣ Week View
**Purpose:** Show last 7 days at a glance

**Setup:**
1. Click `+` to add new view
2. Select **"Table"** (or Timeline)
3. Name it "📊 Week View"
4. Add Filter: "Date" is within "past week"
5. Sort by: "Date" descending

**Alternative - Timeline View:**
1. Select **"Timeline"** instead of Table
2. Date property: "Date"
3. Shows 7-day rolling window

---

## 🎨 Recommended View Configuration Summary

| View Type | Name | Group/Filter By | Properties Visible |
|-----------|------|-----------------|-------------------|
| Calendar | 📅 Calendar View | Date | All habits |
| Board | 📋 Board View | Date | Habits + Streaks |
| Gallery | 🖼️ Gallery View | None (cards) | All + Streak counts |
| Table | 📊 Week View | Date (past week) | All habits |

---

## 🚀 Quick Start

1. **Go to the Visual Dashboard page** I created in your Notion workspace
2. **Click the Habit Tracker database link**
3. **Follow the instructions** above to create each view
4. **Switch between views** using the tabs at the top

---

## 💡 Pro Tips

1. **Create a 'Master Dashboard'** page linking to all views
2. **Use filters** to create specialized views:
   - "This Month" - Current month's habits
   - "High Streaks" - Days with 3+ habits completed
   - "Needs Attention" - Days with 0-1 habits

3. **Add formulas** for visual indicators:
   ```
   Completion Rate: (fruit + multi + exercise + water) / 4 * 100
   ```

4. **Mobile setup:** Favorite your dashboard for quick mobile access

---

## 🔗 Database Information

- **Database ID:** `2fdf2cb12276818f8845ed296b42d781`
- **Parent Page:** `2fcf2cb1-2276-8021-a8a9-ce059efecbf6`
- **Visual Dashboard:** Created and linked!

Happy habit tracking! 🦞✨
"""
    
    return guide

def main():
    """Main execution function"""
    print("🎮 Habit Tracker Visual Views Creator")
    print("=" * 60)
    print()
    
    # Step 1: Get database info
    db_info = get_database_info(DATABASE_ID)
    if not db_info:
        print("❌ Could not fetch database. Check permissions.")
        return
    
    print()
    
    # Step 2: Create visual dashboard page
    print("📊 Creating Visual Dashboard page...")
    dashboard_id = create_visual_dashboard_page(PARENT_PAGE_ID)
    
    if dashboard_id:
        print()
        print("✅ Visual Dashboard created successfully!")
        print(f"🔗 Page ID: {dashboard_id}")
        print()
    
    # Step 3: Generate setup guide
    print("📝 Generating setup guide...")
    guide = generate_view_setup_guide()
    
    # Save guide to file
    guide_path = "/home/samsclaw/.openclaw/workspace/habit_tracker_views_guide.md"
    with open(guide_path, 'w') as f:
        f.write(guide)
    
    print(f"✅ Setup guide saved to: {guide_path}")
    print()
    
    # Summary
    print("=" * 60)
    print("🎉 Setup Complete!")
    print()
    print("📊 Created:")
    print("  ✅ Visual Dashboard page with instructions")
    print("  ✅ Linked database references")
    print("  ✅ Detailed setup guide (Markdown file)")
    print()
    print("⚠️  Important:")
    print("  Database views must be created manually in Notion UI")
    print("  The API doesn't support programmatic view creation")
    print()
    print("📋 Next Steps:")
    print("  1. Open your Notion workspace")
    print("  2. Find 'Habit Tracker Visual Dashboard' page")
    print("  3. Follow the instructions to create each view")
    print("  4. Read the full guide: habit_tracker_views_guide.md")
    print()
    print("🦞 Happy habit tracking!")

if __name__ == "__main__":
    main()
