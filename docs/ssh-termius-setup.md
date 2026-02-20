# SSH Termius Setup Guide

## Current Status
- ✅ OpenSSH server running in WSL (port 22)
- ✅ Key-based authentication configured
- ❌ Port forwarding from Windows to WSL needed

## Option 1: Automated Setup (Recommended)

1. Open **PowerShell as Administrator**
2. Run this script:
```powershell
cd $env:USERPROFILE\.openclaw\workspace\scripts
.\setup-termius-ssh.ps1
```
3. Note the **Windows IP** and **Port 2222**

## Option 2: Manual Setup

### Step 1: Get WSL IP
In WSL, run:
```bash
hostname -I
```
Note the IP (e.g., 172.18.106.51)

### Step 2: Add Port Forwarding
In PowerShell (Admin):
```powershell
netsh interface portproxy add v4tov4 listenport=2222 listenaddress=0.0.0.0 connectport=22 connectaddress=<WSL_IP>
```

### Step 3: Allow Firewall
In PowerShell (Admin):
```powershell
New-NetFirewallRule -DisplayName "WSL SSH" -Direction Inbound -LocalPort 2222 -Protocol TCP -Action Allow
```

### Step 4: Get Windows IP
```powershell
(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' }).IPAddress
```

## Termius Configuration

**Host:** Your Windows IP  
**Port:** 2222  
**Username:** samsclaw  
**Authentication:** SSH Key

### Add SSH Key to Termius:

1. In WSL, copy your public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

2. In Termius:
   - Go to Keychain
   - Add Key
   - Paste the public key
   - Or import private key from `~/.ssh/id_ed25519`

## Troubleshooting

**Connection refused?**
- Check Windows Firewall allows port 2222
- Verify port forwarding: `netsh interface portproxy show all`

**Authentication failed?**
- Ensure SSH key is added to `~/.ssh/authorized_keys` in WSL
- Check key permissions: `chmod 600 ~/.ssh/authorized_keys`

**WSL IP changed?**
- WSL IP changes on restart
- Re-run the PowerShell script or update port forwarding with new IP

## Verification

Test from Termius or another terminal:
```bash
ssh -p 2222 samsclaw@<WINDOWS_IP>
```
