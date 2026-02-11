#!/usr/bin/env python3
"""
Quick WHOOP token refresh - manual version
"""

import requests
import json
import os

CLIENT_ID = "074bb494-e088-4510-b83f-399d5a588efe"
CLIENT_SECRET = "01760749cc5eb0d061319dabf56582d675f974f7753d0182811d62f363b016af"

print("WHOOP Quick Token Test")
print("=" * 40)

# Check current token
tokens_path = os.path.expanduser("~/.openclaw/whoop_tokens.json")
try:
    with open(tokens_path, 'r') as f:
        tokens = json.load(f)
    print(f"Current token expires in: {tokens.get('expires_in', 'unknown')} seconds")
    print(f"Has refresh_token: {'Yes' if tokens.get('refresh_token') else 'No'}")
except:
    print("No token file found")

print()
print("To get a new token:")
print("1. Visit this URL in your browser:")
print()
auth_url = f"https://api.prod.whoop.com/oauth/oauth2/auth?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:18790/oauth/callback&scope=read:sleep%20read:recovery%20read:cycles"
print(auth_url)
print()
print("2. Click 'Authorize'")
print("3. The browser will show 'Authorization successful'")
print("4. Run this script again to verify")
