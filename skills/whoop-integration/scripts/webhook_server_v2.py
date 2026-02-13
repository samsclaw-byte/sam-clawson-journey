#!/usr/bin/env python3
"""
WHOOP Webhook Server - Production Ready with Airtable Integration
Receives WHOOP webhooks and saves data to Airtable for historical analysis
"""

import os
import sys
import json
import hmac
import hashlib
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

# Add scripts directory to path for airtable_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'scripts'))

try:
    from airtable_client import get_health_client
    AIRTABLE_AVAILABLE = True
except ImportError:
    AIRTABLE_AVAILABLE = False
    print("⚠️ Airtable client not available, falling back to file storage only")

# Configuration
WEBHOOK_SECRET = os.getenv('WHOOP_WEBHOOK_SECRET', '')
DATA_DIR = Path.home() / '.openclaw' / 'whoop_data'
LOG_FILE = Path.home() / '.openclaw' / 'whoop_webhook.log'

# Create data directory
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

def log_event(message):
    """Log webhook events"""
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def verify_signature(payload, signature):
    """Verify HMAC-SHA256 signature from WHOOP"""
    if not WEBHOOK_SECRET:
        log_event("ERROR: WEBHOOK_SECRET not set")
        return False
    
    expected = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

def save_data_to_file(event_type, data):
    """Save WHOOP data to structured JSON files"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        date = datetime.now().strftime('%Y-%m-%d')
        
        # Create daily directory
        daily_dir = DATA_DIR / date
        daily_dir.mkdir(exist_ok=True)
        
        # Save individual event
        filename = f"{event_type}_{timestamp}.json"
        filepath = daily_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also update latest summary
        update_latest_summary(event_type, data)
        
        log_event(f"✅ Saved {event_type} data to {filepath}")
        return True
        
    except Exception as e:
        log_event(f"❌ Error saving data: {e}")
        return False

def update_latest_summary(event_type, data):
    """Update the latest summary file for quick access"""
    summary_file = DATA_DIR / 'latest_summary.json'
    
    try:
        # Load existing summary
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                summary = json.load(f)
        else:
            summary = {}
        
        # Update with new data
        summary[event_type] = {
            'data': data,
            'received_at': datetime.now().isoformat()
        }
        
        # Save updated summary
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
    except Exception as e:
        log_event(f"❌ Error updating summary: {e}")

def extract_recovery_metrics(data):
    """Extract key recovery metrics for easy access"""
    try:
        score = data.get('score', {})
        return {
            'recovery_score': score.get('recovery_score'),
            'hrv': score.get('hrv_rmssd_milli'),
            'resting_hr': score.get('resting_heart_rate'),
            'spo2': score.get('spo2_percentage'),
            'timestamp': data.get('updated_at'),
            'date': data.get('date')
        }
    except:
        return {}

def extract_sleep_metrics(data):
    """Extract key sleep metrics"""
    try:
        score = data.get('score', {})
        return {
            'sleep_performance': score.get('sleep_performance_percentage'),
            'sleep_efficiency': score.get('sleep_efficiency_percentage'),
            'duration_hours': score.get('stage_summary', {}).get('total_in_bed_time_milli', 0) / (1000 * 60 * 60),
            'respiratory_rate': score.get('respiratory_rate'),
            'timestamp': data.get('updated_at'),
            'date': data.get('date')
        }
    except:
        return {}

def extract_workout_metrics(data):
    """Extract key workout metrics"""
    try:
        score = data.get('score', {})
        return {
            'workout_id': data.get('id'),
            'sport_id': data.get('sport_id'),
            'sport_name': data.get('sport_name', 'Unknown'),
            'strain': score.get('strain'),
            'average_heart_rate': score.get('average_heart_rate'),
            'max_heart_rate': score.get('max_heart_rate'),
            'duration_minutes': data.get('duration', 0) / 60000,  # milliseconds to minutes
            'calories': score.get('kilojoule', 0) * 0.239,  # kJ to kcal
            'timestamp': data.get('updated_at'),
            'date': data.get('start')[:10] if data.get('start') else datetime.now().strftime('%Y-%m-%d')
        }
    except Exception as e:
        log_event(f"❌ Error extracting workout metrics: {e}")
        return {}

def extract_cycle_metrics(data):
    """Extract key cycle (daily) metrics"""
    try:
        score = data.get('score', {})
        return {
            'date': data.get('date'),
            'strain': score.get('strain'),
            'kilojoule': score.get('kilojoule'),
            'calories': score.get('kilojoule', 0) * 0.239,  # kJ to kcal
            'timestamp': data.get('updated_at')
        }
    except:
        return {}

def save_to_airtable_recovery(metrics):
    """Save recovery data to Airtable"""
    if not AIRTABLE_AVAILABLE:
        return False
    
    try:
        client = get_health_client()
        
        # Parse date from WHOOP data
        whoop_date = metrics.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        result = client.save_whoop_recovery(
            recovery_score=metrics.get('recovery_score', 0),
            hrv=metrics.get('hrv'),
            resting_hr=metrics.get('resting_hr'),
            date=whoop_date
        )
        
        log_event(f"✅ Saved recovery to Airtable: {metrics.get('recovery_score')}%")
        return True
        
    except Exception as e:
        log_event(f"⚠️ Failed to save recovery to Airtable: {e}")
        return False

def save_to_airtable_sleep(metrics):
    """Save sleep data to Airtable"""
    if not AIRTABLE_AVAILABLE:
        return False
    
    try:
        client = get_health_client()
        
        # Parse date from WHOOP data
        whoop_date = metrics.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        result = client.save_whoop_sleep(
            sleep_performance=metrics.get('sleep_performance', 0),
            duration_hours=metrics.get('duration_hours', 0),
            efficiency=metrics.get('sleep_efficiency'),
            date=whoop_date
        )
        
        log_event(f"✅ Saved sleep to Airtable: {metrics.get('sleep_performance')}%")
        return True
        
    except Exception as e:
        log_event(f"⚠️ Failed to save sleep to Airtable: {e}")
        return False

def save_to_airtable_workout(metrics):
    """Save workout data to Airtable Workouts table"""
    if not AIRTABLE_AVAILABLE:
        return False
    
    try:
        client = get_health_client()
        
        # Save to Workouts table
        result = client.save_workout(
            date=metrics.get('date'),
            workout_type=metrics.get('sport_name', 'Unknown'),
            duration=metrics.get('duration_minutes', 0),
            strain=metrics.get('strain', 0),
            calories=metrics.get('calories', 0),
            source='WHOOP'
        )
        
        log_event(f"✅ Saved workout to Airtable: {metrics.get('sport_name')} ({metrics.get('duration_minutes', 0):.0f} min)")
        return True
        
    except Exception as e:
        log_event(f"⚠️ Failed to save workout to Airtable: {e}")
        return False

def save_to_airtable_cycle(metrics):
    """Save cycle (daily strain/calories) to WHOOP Data table"""
    if not AIRTABLE_AVAILABLE:
        return False
    
    try:
        client = get_health_client()
        
        # Save to WHOOP Data table
        result = client.save_whoop_data(
            date=metrics.get('date'),
            strain=metrics.get('strain', 0),
            calories=metrics.get('calories', 0)
        )
        
        log_event(f"✅ Saved cycle to Airtable: {metrics.get('date')} - Strain {metrics.get('strain', 0):.1f}")
        return True
        
    except Exception as e:
        log_event(f"⚠️ Failed to save cycle to Airtable: {e}")
        return False

@app.route('/webhook/whoop', methods=['POST'])
def whoop_webhook():
    """Main webhook endpoint - receives all WHOOP data"""
    log_event("=" * 50)
    log_event("📥 Webhook received")
    
    # Get headers
    signature = request.headers.get('X-Whoop-Signature', '')
    
    # Get raw payload
    payload = request.get_data()
    
    # Verify signature
    if not verify_signature(payload, signature):
        log_event("❌ Invalid signature - rejecting")
        return jsonify({'error': 'Invalid signature'}), 401
    
    log_event("✅ Signature verified")
    
    # Parse JSON payload
    try:
        data = request.json
    except Exception as e:
        log_event(f"❌ Invalid JSON: {e}")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    # Get event type
    event_type = data.get('event_type', 'unknown')
    log_event(f"📊 Event type: {event_type}")
    
    # Save ALL data to file (always do this as backup)
    save_data_to_file(event_type, data)
    
    # Extract and save key metrics
    airtable_saved = False
    
    if event_type == 'recovery.updated':
        metrics = extract_recovery_metrics(data)
        if metrics:
            # Save to file
            metrics_file = DATA_DIR / 'latest_recovery.json'
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            log_event(f"💓 Recovery score: {metrics.get('recovery_score')}%")
            
            # Save to Airtable
            if save_to_airtable_recovery(metrics):
                airtable_saved = True
    
    elif event_type == 'sleep.updated':
        metrics = extract_sleep_metrics(data)
        if metrics:
            # Save to file
            metrics_file = DATA_DIR / 'latest_sleep.json'
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            log_event(f"😴 Sleep performance: {metrics.get('sleep_performance')}%")
            
            # Save to Airtable
            if save_to_airtable_sleep(metrics):
                airtable_saved = True
    
    elif event_type == 'workout.created' or event_type == 'workout.updated':
        log_event("🏋️ New workout recorded")
        # Extract workout metrics and save to Airtable
        workout_metrics = extract_workout_metrics(data)
        if workout_metrics:
            if save_to_airtable_workout(workout_metrics):
                airtable_saved = True
    
    elif event_type == 'cycles.updated':
        log_event("📅 Cycle data updated")
        # Cycle contains daily strain and calories
        cycle_metrics = extract_cycle_metrics(data)
        if cycle_metrics:
            if save_to_airtable_cycle(cycle_metrics):
                airtable_saved = True
    
    log_event("✅ Webhook processed successfully")
    
    return jsonify({
        'status': 'success', 
        'saved': True,
        'airtable_saved': airtable_saved
    }), 200

@app.route('/webhook/whoop/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'webhook_secret_set': bool(WEBHOOK_SECRET),
        'airtable_available': AIRTABLE_AVAILABLE,
        'data_directory': str(DATA_DIR),
        'version': '2.1'
    }), 200

@app.route('/webhook/whoop/data', methods=['GET'])
def get_latest_data():
    """Get latest WHOOP data summary"""
    try:
        summary_file = DATA_DIR / 'latest_summary.json'
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                return jsonify(json.load(f)), 200
        else:
            return jsonify({'error': 'No data available yet'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/whoop/recovery', methods=['GET'])
def get_latest_recovery():
    """Get latest recovery data"""
    try:
        recovery_file = DATA_DIR / 'latest_recovery.json'
        if recovery_file.exists():
            with open(recovery_file, 'r') as f:
                return jsonify(json.load(f)), 200
        else:
            return jsonify({'error': 'No recovery data yet'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/whoop/sleep', methods=['GET'])
def get_latest_sleep():
    """Get latest sleep data"""
    try:
        sleep_file = DATA_DIR / 'latest_sleep.json'
        if sleep_file.exists():
            with open(sleep_file, 'r') as f:
                return jsonify(json.load(f)), 200
        else:
            return jsonify({'error': 'No sleep data yet'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def initialize():
    """Initialize webhook server"""
    log_event("🚀 WHOOP Webhook Server v2.1 initialized")
    log_event(f"📁 Data directory: {DATA_DIR}")
    log_event(f"📝 Log file: {LOG_FILE}")
    log_event(f"📊 Airtable integration: {'✅ Available' if AIRTABLE_AVAILABLE else '⚠️ Not available'}")
    
    if not WEBHOOK_SECRET:
        log_event("⚠️ WARNING: WHOOP_WEBHOOK_SECRET not set!")
    
    if not AIRTABLE_AVAILABLE:
        log_event("⚠️ Airtable client not available - data will only be saved to files")

if __name__ == '__main__':
    initialize()
    
    print("\n🚀 Starting WHOOP Webhook Server with Airtable Integration...")
    print(f"📁 Saving data to: {DATA_DIR}")
    print(f"📊 Airtable: {'✅ Enabled' if AIRTABLE_AVAILABLE else '⚠️ Disabled'}")
    print("Listening on http://localhost:8080")
    print("\nEndpoints:")
    print("  POST /webhook/whoop       - Receive WHOOP webhooks")
    print("  GET  /webhook/whoop/health - Health check")
    print("  GET  /webhook/whoop/data   - Get all latest data")
    print("  GET  /webhook/whoop/recovery - Get latest recovery")
    print("  GET  /webhook/whoop/sleep  - Get latest sleep")
    print("")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
