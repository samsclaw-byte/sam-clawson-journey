# WHOOP Webhook Implementation - Step by Step

## Prerequisites
- Cloudflare account (free)
- Domain managed by Cloudflare
- Python 3.8+ with pip

---

## Step 1: Install Cloudflared

```bash
# Download and install
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared --version
```

---

## Step 2: Authenticate with Cloudflare

```bash
# This opens browser for login
cloudflared tunnel login

# Select the domain you want to use
# (e.g., yourdomain.com)
```

A certificate will be saved to `~/.cloudflared/cert.pem`

---

## Step 3: Create the Tunnel

```bash
# Create tunnel
cloudflared tunnel create whoop-webhook

# Note the Tunnel ID displayed (looks like: abc123-def456-ghi789)
```

---

## Step 4: Configure the Tunnel

```bash
# Create config file
nano ~/.cloudflared/config.yml
```

**Paste this (replace with your actual tunnel ID and domain):**

```yaml
tunnel: YOUR-TUNNEL-ID-HERE
credentials-file: /home/YOUR-USERNAME/.cloudflared/YOUR-TUNNEL-ID-HERE.json

ingress:
  - hostname: whoop.YOUR-DOMAIN.com
    service: http://localhost:8080
    originRequest:
      noTLSVerify: true
  - service: http_status:404
```

**Example:**
```yaml
tunnel: abc123-def456-ghi789
credentials-file: /home/samsclaw/.cloudflared/abc123-def456-ghi789.json

ingress:
  - hostname: whoop.samsclaw.com
    service: http://localhost:8080
  - service: http_status:404
```

---

## Step 5: Create DNS Record

```bash
# Create CNAME record automatically
cloudflared tunnel route dns whoop-webhook whoop.YOUR-DOMAIN.com

# Example:
cloudflared tunnel route dns whoop-webhook whoop.samsclaw.com
```

**Or manually in Cloudflare dashboard:**
- Type: CNAME
- Name: whoop
- Target: YOUR-TUNNEL-ID.cfargotunnel.com
- Proxy status: Enabled (orange cloud)

---

## Step 6: Install Webhook Server Dependencies

```bash
# Install Flask
pip3 install flask --user

# Or if using conda
conda install flask
```

---

## Step 7: Configure Webhook Secret

```bash
# Generate a random secret
export WHOOP_WEBHOOK_SECRET=$(openssl rand -hex 32)
echo $WHOOP_WEBHOOK_SECRET

# Save it for persistence
echo "export WHOOP_WEBHOOK_SECRET='$WHOOP_WEBHOOK_SECRET'" >> ~/.bashrc
```

**Copy this secret** — you'll need it for WHOOP dashboard

---

## Step 8: Start the Webhook Server

```bash
cd ~/.openclaw/workspace/skills/whoop-integration/scripts

# Run the server
python3 webhook_server.py
```

You should see:
```
🚀 Starting WHOOP Webhook Server...
Listening on http://localhost:8080

Endpoints:
  POST /webhook/whoop       - Main webhook endpoint
  GET  /webhook/whoop/health - Health check
  GET  /webhook/whoop/data   - Get latest data
```

**Test it:**
```bash
curl http://localhost:8080/webhook/whoop/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T...",
  "webhook_secret_set": true
}
```

---

## Step 9: Start Cloudflare Tunnel

**In a new terminal window:**

```bash
cloudflared tunnel run whoop-webhook
```

You should see:
```
INF Connected to WHOOP
INF Registered tunnel connection
INF Your Tunnel ID: abc123-def456-ghi789
```

**Test the public URL:**
```bash
curl https://whoop.YOUR-DOMAIN.com/webhook/whoop/health
```

Should return the same health check response.

---

## Step 10: Register Webhook in WHOOP Dashboard

1. Go to https://developer.whoop.com
2. Click on your app
3. Go to "Webhooks" section
4. Add webhook endpoint:
   - **URL:** `https://whoop.YOUR-DOMAIN.com/webhook/whoop`
   - **Secret:** Paste the secret from Step 7
5. Select events to subscribe:
   - ☑️ `recovery.updated`
   - ☑️ `sleep.updated`
   - ☐ `workout.created` (optional)
6. Click "Save"

---

## Step 11: Test the Webhook

**Option A: Wait for natural event**
- Go to sleep tonight
- Wake up tomorrow
- WHOOP will push data automatically

**Option B: Manual test (if WHOOP supports it)**
- Some platforms allow "Test webhook" button in dashboard

**Check logs:**
```bash
tail -f ~/.openclaw/whoop_webhook.log
```

You should see:
```
[2026-02-10T...] Webhook received
[2026-02-10T...] Signature verified ✓
[2026-02-10T...] Event type: recovery.updated
[2026-02-10T...] Recovery data saved: 92%
```

---

## Step 12: Update Morning Brief

Edit `~/.openclaw/workspace/scripts/morning_brief.py`:

Replace the WHOOP data retrieval section:

```python
def get_whoop_data():
    """Get WHOOP data from webhook storage"""
    import json
    
    # Try webhook data first (always fresh)
    webhook_file = os.path.expanduser('~/.openclaw/whoop_webhook_data.json')
    
    try:
        with open(webhook_file, 'r') as f:
            data = json.load(f)
            
            # Check if data is recent (< 24 hours old)
            received = datetime.fromisoformat(data.get('received_at', '2000-01-01'))
            age_hours = (datetime.now() - received).total_seconds() / 3600
            
            if age_hours < 24:
                return {
                    'status': 'success',
                    'recovery_score': data.get('recovery_score'),
                    'sleep_performance': data.get('sleep_performance'),
                    'hrv': data.get('hrv'),
                    'resting_hr': data.get('resting_hr'),
                    'source': 'webhook'
                }
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    # Fallback to API if no recent webhook data
    return get_whoop_data_from_api()  # Original API method
```

---

## Step 13: Set Up as Systemd Service (Optional but Recommended)

**Create service file:**

```bash
sudo nano /etc/systemd/system/whoop-webhook.service
```

**Paste:**

```ini
[Unit]
Description=WHOOP Webhook Server
After=network.target

[Service]
Type=simple
User=samsclaw
WorkingDirectory=/home/samsclaw/.openclaw/workspace/skills/whoop-integration/scripts
Environment="WHOOP_WEBHOOK_SECRET=YOUR-SECRET-HERE"
ExecStart=/usr/bin/python3 /home/samsclaw/.openclaw/workspace/skills/whoop-integration/scripts/webhook_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable whoop-webhook
sudo systemctl start whoop-webhook
sudo systemctl status whoop-webhook
```

---

## Step 14: Set Up Cloudflare Tunnel as Service

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

---

## ✅ Verification Checklist

- [ ] `curl https://whoop.YOUR-DOMAIN.com/webhook/whoop/health` returns healthy
- [ ] WHOOP dashboard shows webhook as "Active"
- [ ] `whoop_webhook.log` shows incoming requests
- [ ] `whoop_webhook_data.json` contains latest recovery data
- [ ] Morning brief reads from webhook data
- [ ] Both services auto-start on boot

---

## 🚨 Troubleshooting

### "Invalid signature" errors
- Double-check WHOOP_WEBHOOK_SECRET matches dashboard
- Ensure no extra whitespace

### Tunnel not connecting
- Check Cloudflare dashboard for tunnel status
- Verify DNS CNAME record exists

### Webhook server not receiving requests
- Check firewall: `sudo ufw allow 8080`
- Verify server is running: `curl localhost:8080/webhook/whoop/health`

### Data not saving
- Check file permissions: `ls -la ~/.openclaw/whoop_webhook_data.json`
- Ensure directory exists: `mkdir -p ~/.openclaw`

---

## 📊 What You Get

Once set up:
- ✅ Recovery data pushed automatically after sleep
- ✅ No more token expiration issues
- ✅ Morning brief uses fresh data
- ✅ Full audit log of all webhooks
- ✅ Secure with HMAC signatures

**Ready to start?** Begin with Step 1! 🦞
