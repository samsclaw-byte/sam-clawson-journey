# Cloudflare Tunnel SSH Setup Guide

This sets up a secure SSH tunnel through Cloudflare, giving you remote access to your WSL instance from anywhere.

## Overview

- **Tool:** cloudflared (Cloudflare Tunnel)
- **Access:** `ssh your-name@ssh.samsclaw.org` from anywhere
- **Security:** No open ports, encrypted tunnel through Cloudflare

---

## Step 1: Install cloudflared

```bash
# Download and install cloudflared
cd ~
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# Verify installation
cloudflared --version
```

---

## Step 2: Authenticate with Cloudflare

```bash
# Login to Cloudflare (opens browser)
cloudflared tunnel login
```

This will:
1. Open a browser
2. Ask you to select your Cloudflare account (samsclaw-498)
3. Authorize the tunnel
4. Download a certificate to `~/.cloudflared/cert.pem`

---

## Step 3: Create the Tunnel

```bash
# Create a named tunnel
cloudflared tunnel create samsclaw-ssh

# This outputs a tunnel ID like: 12345678-1234-1234-1234-123456789abc
# Note this ID - you'll need it
```

---

## Step 4: Configure the Tunnel

Create config file at `~/.cloudflared/config.yml`:

```yaml
tunnel: YOUR_TUNNEL_ID_HERE
credentials-file: /home/samsclaw/.cloudflared/YOUR_TUNNEL_ID_HERE.json

ingress:
  # SSH access
  - hostname: ssh.samsclaw.org
    service: ssh://localhost:22
  
  # Catch-all (required)
  - service: http_status:404
```

Replace `YOUR_TUNNEL_ID_HERE` with the actual ID from Step 3.

---

## Step 5: Set up SSH Server in WSL

```bash
# Install OpenSSH server
sudo apt update
sudo apt install -y openssh-server

# Configure SSH
sudo mkdir -p /var/run/sshd
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Start SSH service
sudo service ssh start

# Add to .bashrc to auto-start on WSL launch
echo 'sudo service ssh start 2>/dev/null || true' >> ~/.bashrc
```

---

## Step 6: Add SSH Key

Since we're disabling password auth, you need an SSH key:

```bash
# Generate key if you don't have one
ssh-keygen -t ed25519 -C "samsclaw@termius" -f ~/.ssh/id_ed25519

# Add to authorized_keys
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Copy the PRIVATE key for Termius
cat ~/.ssh/id_ed25519
# Copy this output and save it for Termius setup
```

---

## Step 7: Add DNS Record

In Cloudflare dashboard:

1. Go to your domain (samsclaw.org)
2. Click **DNS** tab
3. Add a **CNAME** record:
   - Name: `ssh`
   - Target: `YOUR_TUNNEL_ID_HERE.cfargotunnel.com`
   - Proxy status: ✅ Proxied (orange cloud)

---

## Step 8: Start the Tunnel

```bash
# Run tunnel (foreground for testing)
cloudflared tunnel run samsclaw-ssh
```

Test connection from another device:
```bash
ssh samsclaw@ssh.samsclaw.org
```

---

## Step 9: Auto-start Tunnel

Create systemd service or use tmux/screen:

```bash
# Option: Add to .bashrc with nohup
echo 'nohup cloudflared tunnel run samsclaw-ssh > ~/.cloudflared/tunnel.log 2>&1 &' >> ~/.bashrc
```

Or create a systemd service (if systemd works in your WSL):

```bash
sudo tee /etc/systemd/system/cloudflared.service > /dev/null << 'EOF'
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=samsclaw
WorkingDirectory=/home/samsclaw
ExecStart=/usr/local/bin/cloudflared tunnel run samsclaw-ssh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

---

## Step 10: Configure Termius

1. Open **Termius** app
2. Click **+ New Host**
3. Configure:
   - **Alias:** SamsClaw WSL
   - **Hostname:** `ssh.samsclaw.org`
   - **Username:** `samsclaw`
   - **Password:** (leave blank - using key)
4. Click **Key** → **+ New Key**
   - Paste your **private key** from Step 6
   - Save
5. Save the host
6. Connect!

---

## Troubleshooting

**Tunnel won't start:**
```bash
# Check logs
cloudflared tunnel logs samsclaw-ssh

# Verify config
cloudflared tunnel ingress validate ~/.cloudflared/config.yml
```

**SSH connection refused:**
```bash
# Check SSH is running
sudo service ssh status

# Check port 22 is listening
sudo ss -tlnp | grep 22
```

**DNS not resolving:**
- Wait 1-2 minutes for DNS propagation
- Verify CNAME points to tunnel
- Check Cloudflare dashboard → Tunnels for status

---

## Summary

Once complete, you'll have:
- ✅ Permanent SSH access via `ssh.samsclaw.org`
- ✅ No port forwarding required
- ✅ Encrypted tunnel through Cloudflare
- ✅ Termius app for mobile/remote access
- ✅ Auto-start on WSL boot
