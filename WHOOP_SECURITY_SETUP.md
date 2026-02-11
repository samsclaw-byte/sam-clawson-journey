# WHOOP Integration - Security Setup Complete ✅

## 🔒 What's Been Done (By Clawson)

### ✅ Secure Directory Structure
```
~/.config/whoop/           (drwx------ 700)
├── credentials            (-rw------- 600)
└── tokens.json            (-rw------- 600)
```

### ✅ Git Protection
- Added to `.gitignore`:
  - `.config/whoop/`
  - `**/whoop_tokens.json`
  - `whoop/`
  - `.env`

### ✅ File Permissions
- Directory: `700` (owner only)
- Files: `600` (owner read/write only)
- No group/other access

---

## 📋 What YOU Need to Do (At Laptop)

### Step 1: Create WHOOP Developer Account
1. Go to: https://developer.whoop.com/
2. Sign in with your WHOOP account
3. Create "New App"
4. Name it: "Sam-Clawson-Assistant"
5. Set Redirect URL: `https://localhost:3000/callback`
6. Save the credentials shown

### Step 2: Add Credentials
```bash
# Edit the credentials file
nano ~/.config/whoop/credentials

# Replace placeholders with your actual credentials:
export WHOOP_CLIENT_ID="your_actual_client_id_here"
export WHOOP_CLIENT_SECRET="your_actual_client_secret_here"
```

### Step 3: Auto-load on Shell Start
```bash
echo 'source ~/.config/whoop/credentials' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: OAuth Authorization (One-Time)
```bash
cd ~/.openclaw/workspace/skills/whoop
node bin/whoop-auth --redirect-uri https://localhost:3000/callback
```

**What happens:**
1. Script prints a URL
2. Open URL on your phone/browser
3. Click "Allow" to authorize
4. You'll be redirected to localhost (will show error — that's OK)
5. Copy the `code=...` from the URL
6. Paste it back in terminal
7. Script saves refresh token securely

### Step 5: Verify Security
```bash
ls -la ~/.config/whoop/
# Should see:
# drwx------ for directory
# -rw------- for files
```

---

## 🔐 Security Features Implemented

| Feature | Status | Notes |
|---------|--------|-------|
| Secure directory (700) | ✅ Done | Owner only |
| File permissions (600) | ✅ Done | Owner read/write only |
| Git exclusion | ✅ Done | Never committed |
| Cloud backup exclusion | ⚠️ Manual | Add to Dropbox/OneDrive exclusions |
| Token rotation | ✅ Automatic | Handled by skill |
| Session isolation | ✅ Enabled | `sessionTarget: isolated` |
| Encrypted at rest | ⬜ Optional | Can add GPG if desired |

---

## 🚨 Security Checklist

Before going live:
- [ ] Created WHOOP developer account
- [ ] Added CLIENT_ID to credentials file
- [ ] Added CLIENT_SECRET to credentials file
- [ ] Ran OAuth authorization
- [ ] Verified tokens saved with 600 permissions
- [ ] Added `.config/whoop/` to cloud backup exclusions
- [ ] Set calendar reminder: Monthly permission audit

---

## 🎯 What Happens Next

Once setup complete:
1. Cron job runs every morning at 6am
2. Fetches WHOOP data (recovery, sleep, strain)
3. Sends you Telegram report with:
   - Recovery score + color-coded recommendation
   - Sleep quality breakdown
   - Resting HR, HRV metrics
   - Calories burned yesterday
4. Integrates with food tracking for net calorie calculation

---

## 🛡️ Ongoing Security

**Monthly (Set Calendar Reminder):**
```bash
# Check permissions
ls -la ~/.config/whoop/

# Check for token leaks in logs
grep -r "WHOOP" ~/.openclaw/logs/ 2>/dev/null | grep -i "token\|secret" || echo "No leaks found"

# Check WHOOP dashboard
# https://developer.whoop.com/ → Review active tokens
```

**If Compromised:**
1. Revoke tokens in WHOOP dashboard immediately
2. Delete `~/.config/whoop/tokens.json`
3. Re-run OAuth authorization
4. Check logs for unauthorized access

---

## 📊 Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Token theft | Medium | 600 permissions, isolated sessions |
| Data breach (WHOOP) | Low | WHOOP's security, HTTPS only |
| Local file exposure | Low | 700/600 permissions, git excluded |
| Man-in-the-middle | Low | HTTPS, certificate pinning |
| Social engineering | Medium | User awareness, no credential sharing |

**Overall Risk: LOW** (with implemented mitigations)

---

*Setup script: `/home/samsclaw/.openclaw/workspace/scripts/setup-whoop-secure.sh`*
*Last updated: 2026-02-06*
