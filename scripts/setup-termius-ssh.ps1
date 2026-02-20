# SSH Termius Setup Script for Windows
# Run this in PowerShell as Administrator

Write-Host "=== SSH Termius Port Forwarding Setup ===" -ForegroundColor Cyan

# Get WSL IP
$wslIp = wsl hostname -I | ForEach-Object { $_.Trim().Split(' ')[0] }
Write-Host "WSL IP: $wslIp" -ForegroundColor Yellow

# Get Windows IP
$windowsIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike '127.*' -and 
    $_.IPAddress -notlike '169.254.*' -and
    $_.InterfaceAlias -notlike '*Loopback*'
} | Select-Object -First 1).IPAddress

Write-Host "Windows IP: $windowsIp" -ForegroundColor Green

# Add port forwarding rule (port 2222 on Windows → port 22 on WSL)
Write-Host "`nAdding port forwarding rule..." -ForegroundColor Cyan
netsh interface portproxy add v4tov4 listenport=2222 listenaddress=0.0.0.0 connectport=22 connectaddress=$wslIp

# Verify rule
Write-Host "`nCurrent port forwarding rules:" -ForegroundColor Cyan
netsh interface portproxy show all

# Add Windows Firewall rule
Write-Host "`nAdding firewall rule..." -ForegroundColor Cyan
New-NetFirewallRule -DisplayName "WSL SSH" -Direction Inbound -LocalPort 2222 -Protocol TCP -Action Allow -Enabled True

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nIn Termius, connect to:" -ForegroundColor Yellow
Write-Host "  Host: $windowsIp" -ForegroundColor White
Write-Host "  Port: 2222" -ForegroundColor White
Write-Host "  Username: samsclaw" -ForegroundColor White
Write-Host "  Auth: SSH Key" -ForegroundColor White

# Export SSH key for Termius
Write-Host "`nExporting SSH public key for Termius..." -ForegroundColor Cyan
$pubKey = Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" -ErrorAction SilentlyContinue
if ($pubKey) {
    Write-Host "Public key (copy to Termius):" -ForegroundColor Green
    Write-Host $pubKey
} else {
    Write-Host "No SSH key found at ~/.ssh/id_ed25519.pub" -ForegroundColor Red
    Write-Host "Generate one with: ssh-keygen -t ed25519" -ForegroundColor Yellow
}

Write-Host "`nTo remove this forwarding later, run:" -ForegroundColor Gray
Write-Host "  netsh interface portproxy delete v4tov4 listenport=2222 listenaddress=0.0.0.0" -ForegroundColor Gray
