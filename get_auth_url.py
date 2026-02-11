#!/usr/bin/env python3
"""
Google Calendar OAuth - Generate Authorization URL
"""

import json
import os

CLIENT_SECRETS_FILE = os.path.expanduser("~/.config/google-calendar/client_secret.json")

# Read client secrets
with open(CLIENT_SECRETS_FILE) as f:
    client_config = json.load(f)

client_id = client_config['installed']['client_id']
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"  # Manual copy-paste
scope = "https://www.googleapis.com/auth/calendar"

# Build auth URL
auth_url = (
    f"https://accounts.google.com/o/oauth2/v2/auth?"
    f"client_id={client_id}&"
    f"redirect_uri={redirect_uri}&"
    f"scope={scope}&"
    f"response_type=code&"
    f"access_type=offline&"
    f"prompt=consent"
)

print("🗓️  Google Calendar Authorization")
print("=" * 50)
print("\n📋 STEPS:")
print("1. Click this link (or copy-paste to browser):")
print(f"\n{auth_url}\n")
print("2. Sign in with your Google account")
print("3. Approve calendar access")
print("4. Copy the authorization code you receive")
print("5. Send me the code\n")
print("⚠️  Important: Make sure you're signing in with the account")
print("   that has access to 'Sam & Sophie Family Calendar'")
EOF