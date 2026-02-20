import os
import sys
import hmac
import hashlib

# Load .env
env_path = os.path.expanduser('~/.openclaw/workspace/skills/whoop-integration/.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

secret = os.getenv('WHOOP_WEBHOOK_SECRET', '')
print(f"Secret loaded: {'Yes' if secret else 'No'}")
print(f"Secret length: {len(secret)}")
print(f"Secret (first 10 chars): {secret[:10]}...")

# Test signature verification
test_payload = b'{"test": "data"}'
test_sig = hmac.new(secret.encode('utf-8'), test_payload, hashlib.sha256).hexdigest()
print(f"\nTest signature generation works: {'Yes' if test_sig else 'No'}")
print(f"Sample signature: {test_sig[:20]}...")
