#!/usr/bin/env python3
"""
Fetch Google Calendar data via Maton API and save to JSON.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta, timezone

# Configuration
MATON_API_KEY = os.environ.get("MATON_API_KEY")
OUTPUT_PATH = os.path.expanduser("~/.openclaw/workspace/mission-control/data/calendar_data.json")
GATEWAY_URL = "https://gateway.maton.ai"

def fetch_calendar_data():
    """Fetch calendar events from Google Calendar via Maton API."""
    
    if not MATON_API_KEY:
        print("Error: MATON_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    headers = {
        "Authorization": f"Bearer {MATON_API_KEY}"
    }
    
    # Calculate time range: now to 30 days ahead
    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=30)).isoformat()
    
    print(f"Fetching calendar events from {time_min} to {time_max}...")
    
    # Fetch events from Sam & Sophie Family Calendar
    family_calendar_id = "5b69bf4aee3985fe14303dc0e733d51cca028bde7dfe73437678829cf52acafe@group.calendar.google.com"
    events_url = f"{GATEWAY_URL}/google-calendar/calendar/v3/calendars/{family_calendar_id}/events"
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": 100
    }
    
    response = requests.get(events_url, headers=headers, params=params)
    
    if response.status_code == 401:
        print("Error: Invalid or missing Maton API key", file=sys.stderr)
        sys.exit(1)
    elif response.status_code == 400:
        print("Error: No Google Calendar connection found. Please connect at https://ctrl.maton.ai", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: Failed to fetch events (HTTP {response.status_code})", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)
    
    events_data = response.json()
    
    # Fetch calendar list for additional context
    calendars_url = f"{GATEWAY_URL}/google-calendar/calendar/v3/users/me/calendarList"
    calendars_response = requests.get(calendars_url, headers=headers)
    
    calendars_data = {}
    if calendars_response.status_code == 200:
        calendars_data = calendars_response.json()
    
    # Compile data
    calendar_data = {
        "metadata": {
            "fetched_at": now.isoformat(),
            "time_range": {
                "start": time_min,
                "end": time_max
            }
        },
        "calendars": calendars_data.get("items", []),
        "events": events_data.get("items", [])
    }
    
    return calendar_data

def save_data(data):
    """Save calendar data to JSON file."""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(data['events'])} events to {OUTPUT_PATH}")

def main():
    data = fetch_calendar_data()
    save_data(data)
    
    # Print summary
    print(f"\nSummary:")
    print(f"  - Fetched at: {data['metadata']['fetched_at']}")
    print(f"  - Time range: {data['metadata']['time_range']['start'][:10]} to {data['metadata']['time_range']['end'][:10]}")
    print(f"  - Events: {len(data['events'])}")
    print(f"  - Calendars: {len(data['calendars'])}")

if __name__ == "__main__":
    main()
