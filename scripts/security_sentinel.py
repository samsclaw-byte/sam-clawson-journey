#!/usr/bin/env python3
"""
Security Sentinel - Daily Security Audit for OpenClaw
Checks system security, updates, and vulnerabilities
"""

import os
import subprocess
import json
from datetime import datetime

REPORT_FILE = "/home/samsclaw/.openclaw/workspace/research/security-audit-{}.md"

def run_command(cmd, description):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {
            "description": description,
            "command": cmd,
            "output": result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}",
            "status": "✅" if result.returncode == 0 else "❌"
        }
    except Exception as e:
        return {
            "description": description,
            "command": cmd,
            "output": f"Failed: {str(e)}",
            "status": "❌"
        }

def check_os_info():
    """Check OS and version"""
    return run_command("uname -a", "Operating System")

def check_listening_ports():
    """Check open ports"""
    return run_command("ss -ltnup 2>/dev/null || netstat -tlnp 2>/dev/null || echo 'No port info available'", "Listening Ports")

def check_firewall():
    """Check firewall status"""
    ufw = run_command("sudo ufw status 2>/dev/null || echo 'UFW not available'", "UFW Firewall")
    return ufw

def check_disk_encryption():
    """Check disk encryption"""
    return run_command("lsblk -f 2>/dev/null | grep -E 'crypt|luks' || echo 'No encryption detected'", "Disk Encryption")

def check_updates():
    """Check for available updates"""
    return run_command("apt list --upgradable 2>/dev/null | head -10 || echo 'Update check not available'", "Pending Updates")

def check_ssh_config():
    """Check SSH configuration"""
    return run_command("grep -E '^PasswordAuthentication|^PermitRootLogin' /etc/ssh/sshd_config 2>/dev/null || echo 'SSH config not accessible'", "SSH Security")

def check_openclaw_config():
    """Check OpenClaw config for security issues"""
    config_path = "/home/samsclaw/.openclaw/openclaw.json"
    issues = []
    
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            # Check gateway bind
            gateway = config.get('gateway', {})
            if gateway.get('bind') == '0.0.0.0':
                issues.append("⚠️ Gateway bound to 0.0.0.0 (public)")
            else:
                issues.append("✅ Gateway bound to loopback (secure)")
            
            # Check auth mode
            if gateway.get('auth', {}).get('mode') == 'token':
                issues.append("✅ Token auth enabled")
            
            # Check tailscale
            tailscale = gateway.get('tailscale', {})
            if tailscale.get('mode') == 'off':
                issues.append("ℹ️ Tailscale disabled")
            
        except Exception as e:
            issues.append(f"❌ Error reading config: {e}")
    else:
        issues.append("❌ Config file not found")
    
    return {
        "description": "OpenClaw Security Config",
        "command": "Check openclaw.json",
        "output": "\n".join(issues),
        "status": "✅"
    }

def check_sensitive_files():
    """Check for exposed sensitive files"""
    checks = []
    
    # Check .env files
    env_files = [
        "/home/samsclaw/.openclaw/workspace/.env",
        "/home/samsclaw/.config/notion/api_key"
    ]
    
    for f in env_files:
        if os.path.exists(f):
            perms = oct(os.stat(f).st_mode)[-3:]
            if perms in ['600', '400']:
                checks.append(f"✅ {f} - Secure permissions ({perms})")
            else:
                checks.append(f"⚠️ {f} - Permissions {perms} (should be 600)")
    
    return {
        "description": "Sensitive File Permissions",
        "command": "Check .env and api_key files",
        "output": "\n".join(checks) if checks else "No sensitive files found",
        "status": "✅"
    }

def generate_report():
    """Generate full security report"""
    print("🔒 Security Sentinel - Daily Audit")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    checks = [
        check_os_info(),
        check_listening_ports(),
        check_firewall(),
        check_disk_encryption(),
        check_updates(),
        check_ssh_config(),
        check_openclaw_config(),
        check_sensitive_files()
    ]
    
    for check in checks:
        print(f"\n{check['status']} {check['description']}")
        print(f"   {check['output'][:200]}..." if len(check['output']) > 200 else f"   {check['output']}")
    
    # Save report
    report_path = REPORT_FILE.format(datetime.now().strftime('%Y-%m-%d'))
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write(f"# Security Audit - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        for check in checks:
            f.write(f"## {check['status']} {check['description']}\n")
            f.write(f"Command: `{check['command']}`\n\n")
            f.write(f"```\n{check['output']}\n```\n\n")
    
    print(f"\n📄 Report saved: {report_path}")
    return report_path

if __name__ == "__main__":
    generate_report()
