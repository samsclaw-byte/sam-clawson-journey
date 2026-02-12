#!/usr/bin/env python3
"""
Check pending nutrition updates and retry Edamam API
Runs at 12pm, 3pm, 8pm via cron
"""

import sys
sys.path.insert(0, '/home/samsclaw/.openclaw/workspace/scripts')

from log_food_meal_robust import check_pending_nutrition_updates

def main():
    print("🔍 Checking for pending nutrition updates...")
    print("=" * 50)
    
    updated = check_pending_nutrition_updates()
    
    print("\n" + "=" * 50)
    if updated:
        print(f"✅ Successfully updated {len(updated)} meals:")
        for meal in updated:
            print(f"  • {meal}")
        
        # Send notification
        try:
            from telegram_notify import send_message
            send_message(f"🍽️ Updated {len(updated)} meals with complete nutrition data!")
        except:
            pass
    else:
        print("⏳ No meals ready for update (API still failing or no pending meals)")
    
    print("\nNext check in 3 hours...")

if __name__ == "__main__":
    main()
