#!/usr/bin/env python3
"""
WHOOP API Poller
Fetches WHOOP data every hour via API (not webhooks)
Auto-refreshes tokens, saves to Airtable
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

# Add skills to path
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/scripts'))

from whoop_client import WhoopClient

def fetch_and_save_whoop_data():
    """Fetch WHOOP data and save to Airtable"""
    print(f"🔄 WHOOP API Poll - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize client (auto-refreshes tokens if needed)
    client = WhoopClient()
    
    # Check if we have valid tokens
    if not client.access_token:
        print("❌ No WHOOP tokens found. Run: python3 oauth_setup.py")
        return False
    
    print("✅ WHOOP client initialized (token auto-refreshed if needed)")
    
    # Fetch data
    print("📊 Fetching WHOOP data...")
    
    # Get latest sleep
    sleep_data = client.get_latest_sleep()
    if sleep_data and 'records' in sleep_data and sleep_data['records']:
        latest_sleep = sleep_data['records'][0]
        print(f"💤 Latest sleep: {latest_sleep.get('score', 'N/A')} score")
    else:
        print("⚠️ No sleep data found")
        latest_sleep = None
    
    # Get latest recovery
    recovery_data = client.get_latest_recovery()
    if recovery_data and 'records' in recovery_data and recovery_data['records']:
        latest_recovery = recovery_data['records'][0]
        recovery_score = latest_recovery.get('score', 'N/A')
        resting_hr = latest_recovery.get('resting_heart_rate', 'N/A')
        hrv = latest_recovery.get('hrv_rmssd_milli', 'N/A')
        print(f"💓 Recovery: {recovery_score}% | RHR: {resting_hr} | HRV: {hrv}")
    else:
        print("⚠️ No recovery data found")
        latest_recovery = None
    
    # Get latest cycle/workout
    cycles_data = client.get_cycles()
    if cycles_data and 'records' in cycles_data and cycles_data['records']:
        latest_cycle = cycles_data['records'][0]
        strain = latest_cycle.get('score', 'N/A')
        kilojoules = latest_cycle.get('kilojoule', 'N/A')
        print(f"🔥 Strain: {strain} | Energy: {kilojoules} kJ")
    else:
        print("⚠️ No cycle data found")
        latest_cycle = None
    
    # Save to Airtable
    if latest_recovery or latest_sleep:
        save_to_airtable(latest_recovery, latest_sleep, latest_cycle)
    
    print("✅ WHOOP poll complete!\n")
    return True

def save_to_airtable(recovery_data: Optional[Dict], sleep_data: Optional[Dict], cycle_data: Optional[Dict]):
    """Save WHOOP data to Airtable"""
    try:
        # Import Airtable helper
        sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/scripts'))
        from helpers import get_airtable_client
        
        airtable = get_airtable_client('Health')
        
        # Prepare record
        record = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Source': 'WHOOP API'
        }
        
        if recovery_data:
            record['Recovery Score'] = recovery_data.get('score')
            record['Resting Heart Rate'] = recovery_data.get('resting_heart_rate')
            record['HRV'] = recovery_data.get('hrv_rmssd_milli')
        
        if sleep_data:
            record['Sleep Score'] = sleep_data.get('score')
            record['Sleep Duration (hours)'] = sleep_data.get('total_in_bed_time_milli', 0) / 3600000  # ms to hours
        
        if cycle_data:
            record['Strain'] = cycle_data.get('score')
            record['Calories'] = cycle_data.get('kilojoule', 0) * 0.239  # kJ to kcal
        
        # Create or update record
        # Check if record exists for today
        formula = f"{{Date}} = '{datetime.now().strftime('%Y-%m-%d')}'"
        existing = airtable.get_all(formula=formula)
        
        if existing:
            # Update
            record_id = existing[0]['id']
            airtable.update(record_id, record)
            print(f"📤 Updated Airtable record: {record_id}")
        else:
            # Create
            result = airtable.insert(record)
            print(f"📤 Created Airtable record: {result['id']}")
            
    except Exception as e:
        print(f"⚠️ Could not save to Airtable: {e}")
        print("   Data logged locally only")

if __name__ == "__main__":
    print("=" * 50)
    print("🏃‍♂️ WHOOP API Poller")
    print("=" * 50)
    
    success = fetch_and_save_whoop_data()
    
    if not success:
        sys.exit(1)
