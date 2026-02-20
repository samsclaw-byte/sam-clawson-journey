import os
import sys
import json
import hmac
import hashlib
from datetime import datetime

# Load .env
env_path = os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

WEBHOOK_SECRET = os.getenv('WHOOP_WEBHOOK_SECRET', '')
LOG_FILE = os.path.expanduser('~/.openclaw/whoop_signature_debug.log')

def log_debug(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

# Simulate the verification function
def verify_signature_debug(payload, signature_header):
    """Debug version that shows what's happening"""
    log_debug(f"Payload length: {len(payload)} bytes")
    log_debug(f"Signature header received: '{signature_header[:50]}...' (len={len(signature_header)})")
    log_debug(f"Secret configured: '{WEBHOOK_SECRET[:20]}...' (len={len(WEBHOOK_SECRET)})")
    
    if not WEBHOOK_SECRET:
        log_debug("ERROR: WEBHOOK_SECRET not set")
        return False
    
    if not signature_header:
        log_debug("ERROR: No signature header provided")
        return False
    
    # Try different signature formats
    formats_to_try = [
        signature_header,  # As-is
        signature_header.replace('sha256=', ''),  # Remove prefix if present
        signature_header.lower(),  # Lowercase
    ]
    
    expected = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    log_debug(f"Expected signature: {expected}")
    
    for i, sig_format in enumerate(formats_to_try):
        log_debug(f"  Trying format {i+1}: '{sig_format[:50]}...'")
        if hmac.compare_digest(sig_format, expected):
            log_debug("  ✓ MATCH!")
            return True
        else:
            log_debug(f"  ✗ No match (len: {len(sig_format)} vs {len(expected)})")
    
    return False

# Test with sample data
test_payload = b'{"event_type": "recovery.updated", "test": true}'
test_sig = hmac.new(WEBHOOK_SECRET.encode('utf-8'), test_payload, hashlib.sha256).hexdigest()

log_debug("="*60)
log_debug("TESTING SIGNATURE VERIFICATION")
log_debug("="*60)
log_debug(f"Test payload: {test_payload}")
log_debug(f"Generated test signature: {test_sig}")
log_debug(f"Verification result: {verify_signature_debug(test_payload, test_sig)}")

log_debug("\n" + "="*60)
log_debug("Now waiting for next webhook to log details...")
log_debug("="*60)
