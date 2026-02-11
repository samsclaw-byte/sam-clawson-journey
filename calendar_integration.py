#!/usr/bin/env python3
"""
Google Calendar Integration for Sam & Sophie
Adds events from Telegram (Sam) and WhatsApp (Sophie)
"""

import os
from datetime import datetime, timedelta

# Configuration
CALENDAR_ID_FILE = os.path.expanduser("~/.config/google-calendar/calendar_id")

def get_calendar_id():
    """Read the shared calendar ID"""
    try:
        with open(CALENDAR_ID_FILE, 'r') as f:
            return f.read().strip()
    except:
        return None

def add_event_from_text(text, source="Sam"):
    """
    Parse natural language and add to Google Calendar
    Examples:
    - "Dinner with Sophie Friday 7pm"
    - "Theo doctor appointment Tuesday 2pm"
    - "Noah playdate Saturday 10am"
    """
    calendar_id = get_calendar_id()
    if not calendar_id:
        return "❌ Calendar ID not found"
    
    # This is where we'd integrate with Google Calendar API
    # For now, return what we would add
    return f"📅 Would add to calendar: '{text}' from {source}"

# For future Google Calendar API integration
def setup_google_calendar_api():
    """
    Setup steps:
    1. Enable Google Calendar API in Google Cloud Console
    2. Create OAuth credentials
    3. Download client_secret.json
    4. Authenticate and store token
    """
    pass

if __name__ == "__main__":
    # Test
    print("🗓️  Sam & Sophie Calendar Integration")
    print(f"Calendar ID: {get_calendar_id()}")
    print("\nReady for WhatsApp integration setup...")
EOF