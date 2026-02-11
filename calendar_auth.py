#!/usr/bin/env python3
"""
Google Calendar OAuth Authorization
One-time setup for Sam's calendar integration
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes needed
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Paths
CLIENT_SECRETS_FILE = os.path.expanduser("~/.config/google-calendar/client_secret.json")
TOKEN_FILE = os.path.expanduser("~/.config/google-calendar/token.json")

def authorize():
    """Run OAuth flow to get authorization"""
    creds = None
    
    # Check if token already exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print("✅ Authorization complete!")
        print(f"Token saved to: {TOKEN_FILE}")
        return True
    
    print("✅ Already authorized!")
    return True

if __name__ == "__main__":
    print("🗓️  Google Calendar Authorization")
    print("=" * 40)
    print("\nThis will open a browser window.")
    print("Please sign in with your Google account and approve access.\n")
    
    if authorize():
        print("\n🎉 Ready to add events to your calendar!")
    else:
        print("\n❌ Authorization failed")
EOF