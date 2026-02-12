#!/usr/bin/env python3
"""
WHOOP Data Sync - Export WHOOP data to CSV for dashboard
Run this daily to update dashboard data
"""

import sys
import os
import json
import csv
from datetime import datetime, timedelta

sys.path.append(os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/scripts'))
from whoop_client import WhoopClient

def sync_whoop_data():
    """Sync WHOOP data to CSV"""
    
    client = WhoopClient()
    
    # Get last 30 days of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    print("🔄 Syncing WHOOP data...")
    
    # Fetch data using API endpoints directly
    end_time = end_date.isoformat() + 'Z'
    start_time = start_date.isoformat() + 'Z'
    
    # Get recovery data
    recovery_params = {'start': start_time, 'end': end_time, 'limit': 25}
    recovery_data = client._make_request('/v2/recovery', recovery_params) or {'records': []}
    
    # Get sleep data  
    sleep_params = {'start': start_time, 'end': end_time, 'limit': 25}
    sleep_data = client._make_request('/v2/activity/sleep', sleep_params) or {'records': []}
    
    # Get cycles (strain) data
    cycle_params = {'start': start_time, 'end': end_time, 'limit': 25}
    cycles_data = client._make_request('/v2/cycle', cycle_params) or {'records': []}
    
    # Merge data by date
    data_by_date = {}
    
    # Process recovery data
    for rec in recovery_data.get('records', []):
        date = rec.get('date', '')[:10] if rec.get('date') else ''
        if not date:
            continue
        score = rec.get('score', {})
        data_by_date[date] = {
            'date': date,
            'recovery_score': score.get('recovery_score', 0) or 0,
            'resting_hr': score.get('resting_heart_rate', 0) or 0,
            'hrv': (score.get('hrv_rmssd_milli', 0) or 0) / 1000,  # Convert to ms
            'spo2': score.get('spo2_percentage', 0) or 0,
            'skin_temp': score.get('skin_temp_celsius', 0) or 0,
        }
    
    # Process sleep data
    for sleep in sleep_data.get('records', []):
        date = sleep.get('start', '')[:10] if sleep.get('start') else ''
        if not date:
            continue
        score = sleep.get('score', {})
        stage_summary = score.get('stage_summary', {}) if score else {}
        
        if date not in data_by_date:
            data_by_date[date] = {'date': date}
        
        # Convert milliseconds to hours (with fallbacks)
        in_bed_ms = stage_summary.get('total_in_bed_time_milli', 0) or 0
        awake_ms = stage_summary.get('total_awake_time_milli', 0) or 0
        light_ms = stage_summary.get('total_light_sleep_time_milli', 0) or 0
        deep_ms = stage_summary.get('total_slow_wave_sleep_time_milli', 0) or 0
        rem_ms = stage_summary.get('total_rem_sleep_time_milli', 0) or 0
        
        data_by_date[date].update({
            'sleep_performance': score.get('sleep_performance_percentage', 0) or 0,
            'sleep_efficiency': score.get('sleep_efficiency_percentage', 0) or 0,
            'sleep_consistency': score.get('sleep_consistency_percentage', 0) or 0,
            'sleep_duration_hours': round((in_bed_ms - awake_ms) / 3600000, 2) if in_bed_ms else 0,
            'time_in_bed_hours': round(in_bed_ms / 3600000, 2) if in_bed_ms else 0,
            'awake_hours': round(awake_ms / 3600000, 2) if awake_ms else 0,
            'light_sleep_hours': round(light_ms / 3600000, 2) if light_ms else 0,
            'deep_sleep_hours': round(deep_ms / 3600000, 2) if deep_ms else 0,
            'rem_sleep_hours': round(rem_ms / 3600000, 2) if rem_ms else 0,
            'sleep_cycles': stage_summary.get('sleep_cycle_count', 0) or 0,
            'disturbances': stage_summary.get('disturbance_count', 0) or 0,
            'respiratory_rate': score.get('respiratory_rate', 0) or 0,
        })
    
    # Process cycles (strain) data
    for cycle in cycles_data.get('records', []):
        date = cycle.get('date', '')[:10] if cycle.get('date') else ''
        if not date:
            continue
        
        if date not in data_by_date:
            data_by_date[date] = {'date': date}
        
        kilojoules = cycle.get('kilojoules', 0) or 0
        data_by_date[date].update({
            'strain': cycle.get('strain', 0) or 0,
            'kilojoules': kilojoules,
            'calories_burned': round(kilojoules * 0.239006, 0),
        })
    
    # Save to CSV
    csv_path = os.path.expanduser('~/.openclaw/workspace/dashboard/whoop_data.csv')
    
    if data_by_date:
        # Get all fieldnames
        all_fields = set()
        for row in data_by_date.values():
            all_fields.update(row.keys())
        
        fieldnames = ['date'] + sorted([f for f in all_fields if f != 'date'])
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for date in sorted(data_by_date.keys(), reverse=True):
                writer.writerow(data_by_date[date])
        
        print(f"✅ Synced {len(data_by_date)} days to {csv_path}")
        return True
    else:
        print("❌ No data retrieved")
        return False

if __name__ == "__main__":
    sync_whoop_data()
