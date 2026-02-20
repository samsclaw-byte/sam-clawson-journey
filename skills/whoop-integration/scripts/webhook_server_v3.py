#!/usr/bin/env python3
"""
WHOOP Webhook Server - Full Data Capture
Receives WHOOP webhooks, saves ALL data to Airtable, sends notifications
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'scripts'))

from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
DATA_DIR = Path.home() / '.openclaw' / 'whoop_data'
LOG_FILE = Path.home() / '.openclaw' / 'whoop_webhook.log'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Telegram config for notifications
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '8210116595')

def log_event(message):
    """Log event with timestamp"""
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def send_telegram_notification(title, details):
    """Send notification to Telegram"""
    if not TELEGRAM_BOT_TOKEN:
        log_event("⚠️ No Telegram bot token configured")
        return False
    
    try:
        message = f"🏃‍♂️ *{title}*\n\n{details}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        log_event(f"⚠️ Failed to send Telegram notification: {e}")
        return False

def save_raw_data(event_type, data):
    """Save complete raw webhook data"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    date = datetime.now().strftime('%Y-%m-%d')
    
    daily_dir = DATA_DIR / date
    daily_dir.mkdir(exist_ok=True)
    
    filename = f"{event_type}_{timestamp}.json"
    filepath = daily_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    log_event(f"💾 Raw data saved: {filepath}")
    return filepath

# ========== COMPREHENSIVE DATA EXTRACTION ==========

def extract_full_workout(data):
    """Extract ALL workout data from WHOOP"""
    score = data.get('score', {})
    zone_durations = score.get('zone_durations', {})
    
    return {
        # Core IDs
        'workout_id': data.get('id'),
        'sport_id': data.get('sport_id'),
        'user_id': data.get('user_id'),
        
        # Activity Info
        'sport_name': data.get('sport_name', 'Unknown'),
        'start_time': data.get('start'),
        'end_time': data.get('end'),
        'duration_ms': data.get('duration'),
        'duration_minutes': data.get('duration', 0) / 60000 if data.get('duration') else None,
        'timezone_offset': data.get('timezone_offset'),
        
        # Scores
        'strain': score.get('strain'),
        'average_heart_rate': score.get('average_heart_rate'),
        'max_heart_rate': score.get('max_heart_rate'),
        'kilojoule': score.get('kilojoule'),
        'calories': score.get('kilojoule', 0) * 0.239 if score.get('kilojoule') else None,
        'percent_recorded': score.get('percent_recorded'),
        
        # Distance & Altitude
        'distance_meters': score.get('distance_meter'),
        'altitude_gain_meters': score.get('altitude_gain_meter'),
        'altitude_change_meters': score.get('altitude_change_meter'),
        
        # HR Zones (in milliseconds)
        'zone_0_ms': zone_durations.get('zone_zero_milli'),
        'zone_1_ms': zone_durations.get('zone_one_milli'),
        'zone_2_ms': zone_durations.get('zone_two_milli'),
        'zone_3_ms': zone_durations.get('zone_three_milli'),
        'zone_4_ms': zone_durations.get('zone_four_milli'),
        'zone_5_ms': zone_durations.get('zone_five_milli'),
        
        # HR Zones (in minutes)
        'zone_0_min': zone_durations.get('zone_zero_milli', 0) / 60000 if zone_durations.get('zone_zero_milli') else 0,
        'zone_1_min': zone_durations.get('zone_one_milli', 0) / 60000 if zone_durations.get('zone_one_milli') else 0,
        'zone_2_min': zone_durations.get('zone_two_milli', 0) / 60000 if zone_durations.get('zone_two_milli') else 0,
        'zone_3_min': zone_durations.get('zone_three_milli', 0) / 60000 if zone_durations.get('zone_three_milli') else 0,
        'zone_4_min': zone_durations.get('zone_four_milli', 0) / 60000 if zone_durations.get('zone_four_milli') else 0,
        'zone_5_min': zone_durations.get('zone_five_milli', 0) / 60000 if zone_durations.get('zone_five_milli') else 0,
        
        # Metadata
        'score_state': data.get('score_state'),
        'created_at': data.get('created_at'),
        'updated_at': data.get('updated_at'),
        'date': data.get('start')[:10] if data.get('start') else datetime.now().strftime('%Y-%m-%d')
    }

def extract_full_sleep(data):
    """Extract ALL sleep data from WHOOP"""
    score = data.get('score', {})
    stage_summary = score.get('stage_summary', {})
    sleep_needed = score.get('sleep_needed', {})
    
    return {
        # Core IDs
        'sleep_id': data.get('id'),
        'cycle_id': data.get('cycle_id'),
        'user_id': data.get('user_id'),
        
        # Timing
        'start_time': data.get('start'),
        'end_time': data.get('end'),
        'timezone_offset': data.get('timezone_offset'),
        'is_nap': data.get('nap', False),
        
        # Performance Metrics
        'sleep_performance_pct': score.get('sleep_performance_percentage'),
        'sleep_consistency_pct': score.get('sleep_consistency_percentage'),
        'sleep_efficiency_pct': score.get('sleep_efficiency_percentage'),
        'respiratory_rate': score.get('respiratory_rate'),
        
        # Stage Summary
        'total_in_bed_ms': stage_summary.get('total_in_bed_time_milli'),
        'total_awake_ms': stage_summary.get('total_awake_time_milli'),
        'total_light_sleep_ms': stage_summary.get('total_light_sleep_time_milli'),
        'total_slow_wave_sleep_ms': stage_summary.get('total_slow_wave_sleep_time_milli'),
        'total_rem_sleep_ms': stage_summary.get('total_rem_sleep_time_milli'),
        'sleep_cycle_count': stage_summary.get('sleep_cycle_count'),
        'disturbance_count': stage_summary.get('disturbance_count'),
        
        # Stage Summary (hours)
        'total_in_bed_hours': stage_summary.get('total_in_bed_time_milli', 0) / (3600000) if stage_summary.get('total_in_bed_time_milli') else 0,
        'total_awake_hours': stage_summary.get('total_awake_time_milli', 0) / (3600000) if stage_summary.get('total_awake_time_milli') else 0,
        'total_light_sleep_hours': stage_summary.get('total_light_sleep_time_milli', 0) / (3600000) if stage_summary.get('total_light_sleep_time_milli') else 0,
        'total_slow_wave_sleep_hours': stage_summary.get('total_slow_wave_sleep_time_milli', 0) / (3600000) if stage_summary.get('total_slow_wave_sleep_time_milli') else 0,
        'total_rem_sleep_hours': stage_summary.get('total_rem_sleep_time_milli', 0) / (3600000) if stage_summary.get('total_rem_sleep_time_milli') else 0,
        
        # Sleep Needed
        'baseline_sleep_needed_ms': sleep_needed.get('baseline_milli'),
        'sleep_debt_ms': sleep_needed.get('need_from_sleep_debt_milli'),
        'strain_sleep_need_ms': sleep_needed.get('need_from_recent_strain_milli'),
        'nap_adjustment_ms': sleep_needed.get('need_from_recent_nap_milli'),
        
        # Metadata
        'score_state': data.get('score_state'),
        'created_at': data.get('created_at'),
        'updated_at': data.get('updated_at'),
        'date': data.get('start')[:10] if data.get('start') else datetime.now().strftime('%Y-%m-%d')
    }

def extract_full_recovery_from_sleep(sleep_data):
    """Extract recovery data from sleep record (v2 API links recovery to sleep)"""
    # In WHOOP v2, recovery is often embedded in or linked to sleep data
    # Try to find recovery data in the sleep record
    recovery = sleep_data.get('recovery', {})
    score = recovery.get('score', {})
    
    if not score:
        # If no recovery in sleep, return minimal data
        return {
            'recovery_id': sleep_data.get('id'),
            'sleep_id': sleep_data.get('id'),
            'user_id': sleep_data.get('user_id'),
            'recovery_score': None,
            'resting_heart_rate': None,
            'hrv_rmssd': None,
            'date': sleep_data.get('created_at', '')[:10] if sleep_data.get('created_at') else None
        }
    
    return {
        'recovery_id': recovery.get('id'),
        'sleep_id': sleep_data.get('id'),
        'cycle_id': recovery.get('cycle_id'),
        'user_id': sleep_data.get('user_id'),
        'recovery_score': score.get('recovery_score'),
        'resting_heart_rate': score.get('resting_heart_rate'),
        'hrv_rmssd': score.get('hrv_rmssd_milli'),
        'spo2_percentage': score.get('spo2_percentage'),
        'skin_temp_celsius': score.get('skin_temp_celsius'),
        'date': sleep_data.get('created_at', '')[:10] if sleep_data.get('created_at') else None
    }

def extract_full_recovery(data):
    """Extract ALL recovery data from WHOOP"""
    score = data.get('score', {})
    
    return {
        # Core IDs
        'recovery_id': data.get('id'),
        'cycle_id': data.get('cycle_id'),
        'sleep_id': data.get('sleep_id'),
        'user_id': data.get('user_id'),
        
        # Recovery Metrics
        'recovery_score': score.get('recovery_score'),
        'resting_heart_rate': score.get('resting_heart_rate'),
        'hrv_rmssd': score.get('hrv_rmssd_milli'),
        'spo2_percentage': score.get('spo2_percentage'),
        'skin_temp_celsius': score.get('skin_temp_celsius'),
        'user_calibrating': score.get('user_calibrating'),
        
        # Metadata
        'score_state': data.get('score_state'),
        'created_at': data.get('created_at'),
        'updated_at': data.get('updated_at'),
        'date': data.get('date') or datetime.now().strftime('%Y-%m-%d')
    }

def extract_full_cycle(data):
    """Extract ALL cycle (daily) data from WHOOP"""
    score = data.get('score', {})
    
    return {
        # Core IDs
        'cycle_id': data.get('id'),
        'user_id': data.get('user_id'),
        
        # Daily Metrics
        'date': data.get('date'),
        'strain': score.get('strain'),
        'kilojoule': score.get('kilojoule'),
        'calories': score.get('kilojoule', 0) * 0.239 if score.get('kilojoule') else None,
        'average_heart_rate': score.get('average_heart_rate'),
        'max_heart_rate': score.get('max_heart_rate'),
        
        # Timing
        'start_time': data.get('start'),
        'end_time': data.get('end'),
        'timezone_offset': data.get('timezone_offset'),
        
        # Metadata
        'score_state': data.get('score_state'),
        'created_at': data.get('created_at'),
        'updated_at': data.get('updated_at')
    }

# ========== WHOOP API FETCHING (v2) ==========

def refresh_whoop_token():
    """Refresh WHOOP access token using refresh token"""
    try:
        token_file = Path.home() / '.openclaw' / 'whoop_tokens.json'
        with open(token_file) as f:
            tokens = json.load(f)
        
        refresh_token = tokens.get('refresh_token')
        client_id = os.getenv('WHOOP_CLIENT_ID')
        client_secret = os.getenv('WHOOP_CLIENT_SECRET')
        
        if not refresh_token:
            log_event("⚠️ No refresh token available")
            return None
        
        # Refresh token request
        url = 'https://api.prod.whoop.com/oauth/oauth2/token'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(url, data=payload, timeout=30)
        
        if response.status_code == 200:
            new_tokens = response.json()
            # Save new tokens
            with open(token_file, 'w') as f:
                json.dump(new_tokens, f, indent=2)
            log_event("✅ WHOOP token refreshed successfully")
            return new_tokens.get('access_token')
        else:
            log_event(f"⚠️ Token refresh failed: {response.status_code}")
            return None
            
    except Exception as e:
        log_event(f"❌ Error refreshing token: {e}")
        return None

def fetch_whoop_data_v2(endpoint, record_id):
    """Fetch full data from WHOOP API v2 using the record ID"""
    try:
        # Load tokens
        token_file = Path.home() / '.openclaw' / 'whoop_tokens.json'
        if not token_file.exists():
            log_event("⚠️ WHOOP tokens not found")
            return None
        
        with open(token_file) as f:
            tokens = json.load(f)
        
        access_token = tokens.get('access_token')
        if not access_token:
            log_event("⚠️ No access token available")
            return None
        
        # Make API request to v2 endpoint
        url = f'https://api.prod.whoop.com/v2/{endpoint}/{record_id}'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            log_event(f"✅ Fetched full data from WHOOP v2 API: {endpoint}/{record_id}")
            return response.json()
        elif response.status_code == 401:
            log_event("⚠️ Token expired, attempting refresh...")
            # Try to refresh token and retry
            new_token = refresh_whoop_token()
            if new_token:
                headers = {'Authorization': f'Bearer {new_token}'}
                response = requests.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    log_event(f"✅ Fetched data after token refresh: {endpoint}/{record_id}")
                    return response.json()
            return None
        else:
            log_event(f"⚠️ API error: {response.status_code} - {response.text[:100]}")
            return None
            
    except Exception as e:
        log_event(f"❌ Error fetching WHOOP data: {e}")
        return None

# ========== WEBHOOK ENDPOINT ==========

@app.route('/webhook/whoop', methods=['POST'])
def whoop_webhook():
    """Main webhook endpoint"""
    log_event("=" * 60)
    log_event("📥 WHOOP Webhook Received")
    
    try:
        data = request.json
        # WHOOP sends event type as 'type', not 'event_type'
        event_type = data.get('event_type') or data.get('type', 'unknown')
        log_event(f"📊 Event Type: {event_type}")
        
        # Step 1: Save raw data locally
        raw_file = save_raw_data(event_type, data)
        
        # Step 2: Fetch full data from WHOOP API v2 using the record ID from webhook
        record_id = data.get('id')
        full_data = None
        
        if event_type in ['workout.created', 'workout.updated']:
            log_event(f"🔍 Fetching workout data from WHOOP v2 API for ID: {record_id}")
            # v2 endpoint: GET /v2/activity/workout/{workoutId}
            full_data = fetch_whoop_data_v2('activity/workout', record_id)
            processed_data = extract_full_workout(full_data or data)
            table_name = "WHOOP Workouts"
            notification_title = "🏋️ Workout Recorded"
            duration = processed_data.get('duration_minutes') or 0
            strain = processed_data.get('strain') or 0
            calories = processed_data.get('calories') or 0
            avg_hr = processed_data.get('average_heart_rate') or 0
            notification_details = f"*{processed_data.get('sport_name', 'Unknown')}*\n" \
                                 f"Duration: {duration:.0f} min\n" \
                                 f"Strain: {strain:.1f}\n" \
                                 f"Calories: {calories:.0f}\n" \
                                 f"Avg HR: {avg_hr} bpm"
        
        elif event_type in ['sleep.created', 'sleep.updated']:
            log_event(f"🔍 Fetching sleep data from WHOOP v2 API for ID: {record_id}")
            # v2 endpoint: GET /v2/activity/sleep/{sleepId}
            full_data = fetch_whoop_data_v2('activity/sleep', record_id)
            processed_data = extract_full_sleep(full_data or data)
            table_name = "WHOOP Sleep"
            notification_title = "😴 Sleep Recorded"
            bed_hours = processed_data.get('total_in_bed_hours') or 0
            performance = processed_data.get('sleep_performance_pct') or 0
            efficiency = processed_data.get('sleep_efficiency_pct') or 0
            rem_hours = processed_data.get('total_rem_sleep_hours') or 0
            notification_details = f"Duration: {bed_hours:.1f} hours\n" \
                                 f"Performance: {performance:.0f}%\n" \
                                 f"Efficiency: {efficiency:.0f}%\n" \
                                 f"REM: {rem_hours:.1f} hrs"
        
        elif event_type in ['recovery.created', 'recovery.updated']:
            log_event(f"🔍 Fetching recovery data from WHOOP v2 API for ID: {record_id}")
            # Recovery in v2: GET /v2/cycle/{cycleId}/recovery
            # Or fetch via sleep ID if that's what the webhook provides
            # Try fetching sleep first (recovery is linked to sleep in v2)
            full_data = fetch_whoop_data_v2('activity/sleep', record_id)
            if full_data:
                # Extract recovery from sleep data if available
                processed_data = extract_full_recovery_from_sleep(full_data)
            else:
                # Try cycle-based recovery
                full_data = fetch_whoop_data_v2(f'cycle/{record_id}/recovery', '')
                processed_data = extract_full_recovery(full_data or data)
            table_name = "WHOOP Recovery"
            notification_title = "💓 Recovery Updated"
            score = processed_data.get('recovery_score') or 0
            rhr = processed_data.get('resting_heart_rate') or 0
            hrv = processed_data.get('hrv_rmssd') or 0
            notification_details = f"Score: {score:.0f}%\n" \
                                 f"RHR: {rhr} bpm\n" \
                                 f"HRV: {hrv:.1f} ms"
        
        elif event_type == 'cycles.updated':
            log_event(f"🔍 Fetching cycle data from WHOOP v2 API for ID: {record_id}")
            # v2 endpoint: GET /v2/cycle/{cycleId}
            full_data = fetch_whoop_data_v2('cycle', record_id)
            processed_data = extract_full_cycle(full_data or data)
            table_name = "WHOOP Daily"
            notification_title = "📅 Daily Data Updated"
            date = processed_data.get('date') or 'Unknown'
            strain = processed_data.get('strain') or 0
            calories = processed_data.get('calories') or 0
            notification_details = f"Date: {date}\n" \
                                 f"Strain: {strain:.1f}\n" \
                                 f"Calories: {calories:.0f}"
        
        else:
            log_event(f"⚠️ Unknown event type: {event_type}")
            return jsonify({'status': 'received', 'processed': False}), 200
        
        # Step 3: Save to Airtable (if available)
        airtable_saved = False
        try:
            from airtable_client import get_health_client
            client = get_health_client()
            
            # Save to appropriate table
            result = client.create_record(client.base_id, table_name, processed_data)
            airtable_saved = True
            log_event(f"✅ Saved to Airtable: {table_name} (ID: {result['id'][:10]}...)")
            
        except Exception as e:
            log_event(f"⚠️ Airtable save failed: {e}")
        
        # Step 4: Send notification
        notification_sent = send_telegram_notification(notification_title, notification_details)
        if notification_sent:
            log_event("✅ Telegram notification sent")
        
        # Step 5: Return confirmation
        log_event("✅ Webhook processing complete")
        return jsonify({
            'status': 'success',
            'event_type': event_type,
            'raw_saved': True,
            'raw_file': str(raw_file),
            'airtable_saved': airtable_saved,
            'table': table_name if airtable_saved else None,
            'notification_sent': notification_sent
        }), 200
        
    except Exception as e:
        log_event(f"❌ Error processing webhook: {e}")
        import traceback
        log_event(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/webhook/whoop/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0 - Full Data Capture'
    }), 200

if __name__ == '__main__':
    log_event("🚀 WHOOP Webhook Server v3.0 - Full Data Capture")
    log_event(f"📁 Data directory: {DATA_DIR}")
    app.run(host='0.0.0.0', port=8080)
