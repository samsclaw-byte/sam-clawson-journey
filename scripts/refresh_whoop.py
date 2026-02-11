#!/usr/bin/env python3
"""
WHOOP Token Refresh Helper
Run this when you need to refresh your WHOOP token (expires every hour)
"""

import os
import sys

# Add scripts path
sys.path.append(os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/scripts'))

def refresh_whoop_token():
    """Guide user through token refresh"""
    print("🔄 WHOOP Token Refresh")
    print("=" * 40)
    print()
    print("Your WHOOP access token expires every hour.")
    print("Since WHOOP doesn't provide refresh tokens, you need to re-authorize.")
    print()
    print("Run this command:")
    print()
    print("  cd ~/.openclaw/workspace/skills/whoop-integration/scripts && python3 oauth_setup.py")
    print()
    print("Then open the URL in your browser and click 'Authorize'")
    print()
    
    # Check current token status
    try:
        from whoop_client import WhoopClient
        client = WhoopClient()
        if client.access_token:
            print("✅ Current token exists")
            print("   (Valid for ~1 hour from when you authorized)")
        else:
            print("❌ No valid token found")
            print("   Run the command above to get a new token")
    except Exception as e:
        print(f"⚠️  Could not check token status: {e}")
    
    print()
    print("💡 Tip: Authorize just before your morning brief (5:50am)")
    print("   for the freshest data!")

if __name__ == "__main__":
    refresh_whoop_token()
