# WHOOP Webhook Implementation Plan

## Overview
Replace polling-based WHOOP API calls with event-driven webhooks for automatic data push.

---

## 🎯 Benefits

1. **No Token Refresh** — Eliminates 1-hour token expiration issue
2. **Real-time Data** — Recovery data arrives when ready (after sleep)
3. **No Polling Waste** — Only receive data when events occur
4. **Better for 6am Brief** — Data already stored when cron runs

---

## 📋 Implementation Steps

### Step 1: Set Up Webhook Endpoint

**Create webhook receiver script:**
```python
# ~/.openclaw/workspace/skills/whoop-integration/scripts/webhook_server.py

from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)
WEBHOOK_SECRET = os.getenv('WHOOP_WEBHOOK_SECRET')

@app.route('/webhook/whoop', methods=['POST'])
def whoop_webhook():
    # Verify signature
    signature = request.headers.get('X-Whoop-Signature')
    payload = request.get_data()
    
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected:
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Process webhook data
    data = request.json
    event_type = data.get('event_type')
    
    if event_type == 'sleep.updated':
        save_sleep_data(data)
    elif event_type == 'recovery.updated':
        save_recovery_data(data)
    
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')
```

### Step 2: Security Hardening

**a) HTTPS Required**
- Use Let's Encrypt for free SSL certificate
- Webhook URL must be `https://`, not `http://`

**b) Signature Verification**
- WHOOP signs payloads with HMAC-SHA256
- Verify every request using shared secret
- Reject requests with invalid signatures

**c) IP Allowlisting**
```python
ALLOWED_IPS = ['52.XX.XX.XX', '54.XX.XX.XX']  # WHOOP's servers

@app.before_request
def check_ip():
    if request.remote_addr not in ALLOWED_IPS:
        return jsonify({'error': 'Unauthorized IP'}), 403
```

**d) Timestamp Validation**
```python
import time

timestamp = int(request.headers.get('X-Whoop-Timestamp'))
now = int(time.time())

# Reject requests older than 5 minutes
if abs(now - timestamp) > 300:
    return jsonify({'error': 'Request expired'}), 401
```

### Step 3: Register Webhook with WHOOP

**Via WHOOP Developer Dashboard:**
1. Go to developer.whoop.com
2. Find your app
3. Add webhook endpoint URL:
   ```
   https://your-domain.com/webhook/whoop
   ```
4. Select events to subscribe:
   - ☑️ sleep.updated
   - ☑️ recovery.updated
   - ☑️ workout.created

5. Copy webhook secret for signature verification

### Step 4: Data Storage

**Store webhook data locally:**
```python
def save_recovery_data(data):
    recovery = {
        'recovery_score': data['score']['recovery_score'],
        'hrv': data['score']['hrv_rmssd_milli'],
        'resting_hr': data['score']['resting_heart_rate'],
        'timestamp': data['updated_at'],
        'source': 'webhook'
    }
    
    with open('~/.openclaw/whoop_webhook_data.json', 'w') as f:
        json.dump(recovery, f)
```

### Step 5: Update Morning Brief

**Modify morning_brief.py to use webhook data:**
```python
def get_whoop_data():
    # Try webhook data first (always fresh)
    try:
        with open('~/.openclaw/whoop_webhook_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to API call
        return get_whoop_data_from_api()
```

---

## 🔒 Security Checklist

- [ ] HTTPS only (no HTTP)
- [ ] HMAC-SHA256 signature verification
- [ ] IP allowlisting (WHOOP's servers only)
- [ ] Timestamp validation (< 5 min old)
- [ ] Webhook secret stored securely (not in code)
- [ ] Request rate limiting (prevent spam)
- [ ] Logging all webhook events

---

## 📊 Expected Webhook Events

| Event | Frequency | Use Case |
|-------|-----------|----------|
| `sleep.updated` | Daily (after wake) | Sleep performance % |
| `recovery.updated` | Daily (after sleep) | Recovery score, HRV |
| `workout.created` | Per workout | Activity tracking |

---

## ⚠️ Challenges

1. **Public Endpoint** — Your server needs a public URL
   - Options: ngrok (dev), VPS, Cloudflare Tunnel
   
2. **SSL Certificate** — Must have valid HTTPS
   - Let's Encrypt (free)
   
3. **Server Always On** — Webhooks need 24/7 endpoint
   - Currently your setup is local only

---

## 🚀 Quick Start Options

### Option A: ngrok (Development)
```bash
# Expose local server temporarily
ngrok http 8080

# Use ngrok URL in WHOOP dashboard
# https://abc123.ngrok.io/webhook/whoop
```

### Option B: Cloudflare Tunnel (Permanent)
```bash
# Install cloudflared
# Persistent tunnel without opening ports
cloudflared tunnel --url http://localhost:8080
```

### Option C: VPS (Production)
- Rent small VPS ($5/month)
- Install webhook server
- Domain + SSL certificate
- 24/7 uptime

---

## 💡 Recommendation

**Start with Option B (Cloudflare Tunnel)** for testing:
- Free
- Secure (no open ports)
- Permanent URL
- Easy to set up

Once confirmed working, migrate to VPS for production.

---

## Next Steps

1. **Choose hosting option** (ngrok/Cloudflare/VPS)
2. **I'll create the webhook server code**
3. **Register endpoint in WHOOP dashboard**
4. **Test with sample data**
5. **Update morning brief to use webhook data**

Ready to proceed? 🦞
