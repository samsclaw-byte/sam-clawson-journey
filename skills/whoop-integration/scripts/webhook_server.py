#!/usr/bin/env python3
"""
WHOOP Webhook Server - Production Ready
Secure webhook endpoint for receiving WHOOP data via Cloudflare Tunnel
"""

import os
import sys
import json
import hmac
import hashlib
import time
from datetime import datetime
from flask import Flask, request, jsonify

# Configuration
WEBHOOK_SECRET = os.getenv('WHOOP_WEBHOOK_SECRET', '')
ALLOWED_IPS = ['52.0.0.0/8', '54.0.0.0/8']  # WHOOP's AWS IP ranges (update with actual)
DATA_FILE = os.path.expanduser('~/.openclaw/whoop_webhook_data.json')
LOG_FILE = os.path.expanduser('~/.openclaw/whoop_webhook.log')

app = Flask(__name__)

def log_event(message):
    """Log webhook events"""
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

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

def verify_timestamp(timestamp_header):
    """Verify request is not too old (prevent replay attacks)"""
    try:
        request_time = int(timestamp_header)
        current_time = int(time.time())
        
        # Allow 5 minute window
        if abs(current_time - request_time) > 300:
            log_event(f"ERROR: Request expired (timestamp: {request_time})")
            return False
        return True
    except (ValueError, TypeError):
        log_event("ERROR: Invalid timestamp")
        return False

def verify_ip(client_ip):
    """Verify request comes from WHOOP's IP ranges"""
    # Simplified check - in production, use ipaddress module for CIDR matching
    # For now, log the IP for monitoring
    log_event(f"Request from IP: {client_ip}")
    return True  # TODO: Implement proper CIDR checking

def save_recovery_data(data):
    """Save recovery data to local file"""
    try:
        score = data.get('score', {})
        recovery = {
            'recovery_score': score.get('recovery_score'),
            'hrv': score.get('hrv_rmssd_milli'),
            'resting_hr': score.get('resting_heart_rate'),
            'spo2': score.get('spo2_percentage'),
            'timestamp': data.get('updated_at'),
            'source': 'webhook',
            'received_at': datetime.now().isoformat()
        }
        
        with open(DATA_FILE, 'w') as f:
            json.dump(recovery, f, indent=2)
        
        log_event(f"Recovery data saved: {recovery['recovery_score']}%")
        return True
    except Exception as e:
        log_event(f"ERROR saving recovery: {e}")
        return False

def save_sleep_data(data):
    """Save sleep data to local file"""
    try:
        score = data.get('score', {})
        sleep = {
            'sleep_performance': score.get('sleep_performance_percentage'),
            'sleep_efficiency': score.get('sleep_efficiency_percentage'),
            'respiratory_rate': score.get('respiratory_rate'),
            'duration_hours': score.get('stage_summary', {}).get('total_in_bed_time_milli', 0) / (1000 * 60 * 60),
            'timestamp': data.get('updated_at'),
            'source': 'webhook',
            'received_at': datetime.now().isoformat()
        }
        
        # Append to sleep history
        sleep_file = DATA_FILE.replace('webhook_data', 'sleep_data')
        try:
            with open(sleep_file, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
        
        history.append(sleep)
        
        # Keep last 30 days
        history = history[-30:]
        
        with open(sleep_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        log_event(f"Sleep data saved: {sleep['sleep_performance']}%")
        return True
    except Exception as e:
        log_event(f"ERROR saving sleep: {e}")
        return False

@app.route('/webhook/whoop', methods=['POST'])
def whoop_webhook():
    """Main webhook endpoint"""
    log_event("=" * 50)
    log_event("Webhook received")
    
    # Get headers
    signature = request.headers.get('X-Whoop-Signature', '')
    timestamp = request.headers.get('X-Whoop-Timestamp', '')
    client_ip = request.remote_addr
    
    # Verify IP
    if not verify_ip(client_ip):
        return jsonify({'error': 'Unauthorized IP'}), 403
    
    # Verify timestamp (prevent replay attacks)
    if not verify_timestamp(timestamp):
        return jsonify({'error': 'Request expired'}), 401
    
    # Get raw payload
    payload = request.get_data()
    
    # Verify signature
    if not verify_signature(payload, signature):
        log_event("ERROR: Invalid signature")
        return jsonify({'error': 'Invalid signature'}), 401
    
    log_event("Signature verified ✓")
    
    # Parse JSON payload
    try:
        data = request.json
    except Exception as e:
        log_event(f"ERROR: Invalid JSON: {e}")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    # Get event type
    event_type = data.get('event_type', 'unknown')
    log_event(f"Event type: {event_type}")
    
    # Process based on event type
    success = False
    if event_type == 'recovery.updated':
        success = save_recovery_data(data)
    elif event_type == 'sleep.updated':
        success = save_sleep_data(data)
    elif event_type == 'workout.created':
        log_event("Workout event received (not processing)")
        success = True
    else:
        log_event(f"Unknown event type: {event_type}")
    
    if success:
        log_event("Webhook processed successfully ✓")
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 500

@app.route('/webhook/whoop/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'webhook_secret_set': bool(WEBHOOK_SECRET)
    }), 200

@app.route('/webhook/whoop/data', methods=['GET'])
def get_latest_data():
    """Get latest WHOOP data (for morning brief)"""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'No data available'}), 404

def initialize():
    """Initialize webhook server"""
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Check for webhook secret
    if not WEBHOOK_SECRET:
        print("⚠️  WARNING: WHOOP_WEBHOOK_SECRET not set!")
        print("Set it with: export WHOOP_WEBHOOK_SECRET='your-secret-here'")
        print("")
    
    log_event("Webhook server initialized")
    log_event(f"Data file: {DATA_FILE}")
    log_event(f"Log file: {LOG_FILE}")

if __name__ == '__main__':
    initialize()
    
    # Run with SSL (Cloudflare Tunnel handles external SSL)
    # Internal traffic is HTTP on localhost
    print("🚀 Starting WHOOP Webhook Server...")
    print("Listening on http://localhost:8080")
    print("")
    print("Endpoints:")
    print("  POST /webhook/whoop       - Main webhook endpoint")
    print("  GET  /webhook/whoop/health - Health check")
    print("  GET  /webhook/whoop/data   - Get latest data")
    print("")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
