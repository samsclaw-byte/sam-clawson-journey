#!/usr/bin/env python3
"""
Add event to Google Calendar
"""

import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Paths
TOKEN_FILE = os.path.expanduser("~/.config/google-calendar/token.json")
CLIENT_SECRETS_FILE = os.path.expanduser("~/.config/google-calendar/client_secret.json")
CALENDAR_ID_FILE = os.path.expanduser("~/.config/google-calendar/calendar_id")

def get_calendar_id():
    """Read the calendar ID"""
    try:
        with open(CALENDAR_ID_FILE, 'r') as f:
            return f.read().strip()
    except:
        return "primary"

def add_event(summary, start_time, end_time, description="", timezone="Asia/Dubai"):
    """Add event to Google Calendar"""
    
    # Check for token
    if not os.path.exists(TOKEN_FILE):
        print("❌ No authentication token found")
        print("Please run: python3 calendar_auth.py")
        return False
    
    # Load credentials
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, ['https://www.googleapis.com/auth/calendar'])
    
    # Refresh if needed
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Build service
    service = build('calendar', 'v3', credentials=creds)
    calendar_id = get_calendar_id()
    
    # Create event
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': timezone,
        },
    }
    
    # Insert event
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 add_calendar_event.py 'Event Title' '2026-02-23T10:00:00' [duration_hours]")
        sys.exit(1)
    
    summary = sys.argv[1]
    start = sys.argv[2]
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    
    # Calculate end time
    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
    end_dt = start_dt + timedelta(hours=duration)
    end = end_dt.isoformat()
    
    add_event(summary, start, end)
