#!/usr/bin/env python3
"""
Fetch Google Calendar data via Maton API
Caches results for Mission Control calendar view
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Maton API configuration
MATON_API_KEY = "x694-xnB7_-PnARWe5A4WZVtCXT2D-cVLvHqvI_FQ4zZYX1Zg7FeuihrNhJ9LwP8b1EDbcx57-OioO2_NSyca1bygTwSlbGqNa6GbKqFHg"
BASE_URL = "https://gateway.maton.ai/google-calendar"

def fetch_calendar_events():
    """Fetch upcoming events from Google Calendar"""
    headers = {"Authorization": f"Bearer {MATON_API_KEY}"}
    
    # Get events from today to 30 days ahead
    today = datetime.now()
    time_min = today.strftime("%Y-%m-%dT00:00:00Z")
    time_max = (today + timedelta(days=30)).strftime("%Y-%m-%dT23:59:59Z")
    
    url = f"{BASE_URL}/calendar/v3/calendars/primary/events"
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        events = []
        for item in data.get("items", []):
            event = {
                "id": item.get("id"),
                "summary": item.get("summary", "No Title"),
                "description": item.get("description", ""),
                "start": item.get("start", {}),
                "end": item.get("end", {}),
                "location": item.get("location", ""),
                "htmlLink": item.get("htmlLink", "")
            }
            events.append(event)
        
        print(f"✅ Fetched {len(events)} events from Google Calendar")
        return events
        
    except Exception as e:
        print(f"❌ Error fetching calendar events: {e}")
        return []

def save_calendar_data(events):
    """Save calendar data to JSON file"""
    data = {
        "generated_at": datetime.now().isoformat(),
        "events": events
    }
    
    output_path = os.path.expanduser("~/.openclaw/workspace/mission-control/data/calendar_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Calendar data saved to {output_path}")

def main():
    print(f"📅 Fetching Google Calendar data...")
    print(f"   Time range: {datetime.now().strftime('%Y-%m-%d')} to {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}")
    
    events = fetch_calendar_events()
    save_calendar_data(events)
    
    # Print upcoming events
    if events:
        print(f"\n📋 Upcoming events:")
        for event in events[:5]:
            start = event['start'].get('dateTime', event['start'].get('date', 'Unknown'))
            print(f"   {start[:10]}: {event['summary']}")

if __name__ == "__main__":
    main()
