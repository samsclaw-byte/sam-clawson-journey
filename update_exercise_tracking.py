import requests
import json

NOTION_KEY = open('/home/samsclaw/.config/notion/api_key').read().strip()
headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

DATABASE_ID = "2fdf2cb12276818f8845ed296b42d781"

print("🏃 Upgrading Habit Tracker with detailed exercise fields...")

# Add exercise detail properties
properties_to_add = {
    "Exercise Activity": {
        "select": {
            "options": [
                {"name": "🏃 Run", "color": "blue"},
                {"name": "🏊 Swim", "color": "cyan"},
                {"name": "🚴 Cycle", "color": "green"},
                {"name": "🚶 Walk", "color": "yellow"},
                {"name": "🏋️ Gym", "color": "red"},
                {"name": "🧘 Yoga", "color": "purple"},
                {"name": "⚽ Sport", "color": "orange"},
                {"name": "🎯 Other", "color": "gray"}
            ]
        }
    },
    "Exercise Duration (min)": {
        "number": {"format": "number"}
    },
    "Zone 1 (Easy)": {
        "number": {"format": "number"}
    },
    "Zone 2 (Aerobic)": {
        "number": {"format": "number"}
    },
    "Zone 3 (Threshold)": {
        "number": {"format": "number"}
    },
    "Zone 4 (Anaerobic)": {
        "number": {"format": "number"}
    },
    "Zone 5 (Max)": {
        "number": {"format": "number"}
    },
    "Exercise Notes": {
        "rich_text": {}
    }
}

for prop_name, prop_config in properties_to_add.items():
    try:
        response = requests.patch(
            f"https://api.notion.com/v1/databases/{DATABASE_ID}",
            headers=headers,
            json={"properties": {prop_name: prop_config}}
        )
        if response.status_code == 200:
            print(f"✅ Added: {prop_name}")
        else:
            print(f"⚠️  {prop_name}: {response.status_code}")
    except Exception as e:
        print(f"❌ {prop_name}: {e}")

print("\n🎉 Exercise tracking upgraded!")
print("📊 New fields: Activity, Duration, Zone 1-5 times, Notes")
