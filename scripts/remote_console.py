#!/usr/bin/env python3
"""
Remote Command Center - Web interface for phone access
Run commands from mobile browser without SSH
"""

import http.server
import socketserver
import subprocess
import json
import urllib.parse
from pathlib import Path

PORT = 8765

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sam's Remote Console</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0f;
            color: #fff;
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        h1 { color: #667eea; margin-bottom: 20px; font-size: 24px; }
        .section { margin-bottom: 25px; }
        .section h2 {
            font-size: 14px;
            color: #aaa;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            margin: 8px 0;
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
            text-align: left;
        }
        .btn:active { background: #667eea; }
        .btn-green { border-color: #22c55e; }
        .btn-yellow { border-color: #f59e0b; }
        .btn-red { border-color: #ef4444; }
        .output {
            background: #0a0a0f;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
            display: none;
        }
        .output.show { display: block; }
        .status {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #22c55e;
            color: #000;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            display: none;
        }
        .status.show { display: block; }
        .status.error { background: #ef4444; color: #fff; }
    </style>
</head>
<body>
    <div id="status" class="status"></div>
    <h1>🦞 Remote Console</h1>
    
    <div class="section">
        <h2>GitHub</h2>
        <button class="btn btn-green" onclick="run('git_push')">⬆️ Push to GitHub</button>
        <button class="btn" onclick="run('git_status')">📋 Git Status</button>
        <button class="btn" onclick="run('git_log')">📜 Recent Commits</button>
    </div>
    
    <div class="section">
        <h2>Dashboard</h2>
        <button class="btn btn-green" onclick="run('gen_dashboard')">🔄 Regenerate Dashboard</button>
        <button class="btn" onclick="run('check_dashboard')">👁️ Check Dashboard Status</button>
    </div>
    
    <div class="section">
        <h2>System</h2>
        <button class="btn" onclick="run('check_whoop')">💓 WHOOP Status</button>
        <button class="btn" onclick="run('check_tat')">📋 TAT Tasks</button>
        <button class="btn" onclick="run('list_cron')">⏰ Cron Jobs</button>
        <button class="btn btn-yellow" onclick="run('security_audit')">🔒 Security Audit</button>
    </div>
    
    <div class="section">
        <h2>Quick Info</h2>
        <button class="btn" onclick="run('disk_space')">💾 Disk Space</button>
        <button class="btn" onclick="run('memory_usage')">🧠 Memory Usage</button>
    </div>
    
    <div id="output" class="output"></div>
    
    <script>
        async function run(command) {
            const status = document.getElementById('status');
            const output = document.getElementById('output');
            
            status.textContent = 'Running...';
            status.className = 'status show';
            output.className = 'output';
            
            try {
                const response = await fetch('/run?cmd=' + encodeURIComponent(command));
                const data = await response.json();
                
                if (data.success) {
                    status.textContent = '✅ Done';
                    status.className = 'status show';
                    output.textContent = data.output || 'Command completed successfully';
                    output.className = 'output show';
                } else {
                    status.textContent = '❌ Error';
                    status.className = 'status show error';
                    output.textContent = data.error || 'Command failed';
                    output.className = 'output show';
                }
            } catch (e) {
                status.textContent = '❌ Error';
                status.className = 'status show error';
                output.textContent = 'Failed to run command: ' + e.message;
                output.className = 'output show';
            }
            
            setTimeout(() => {
                status.className = 'status';
            }, 3000);
        }
    </script>
</body>
</html>'''

COMMANDS = {
    'git_push': ['git', '-C', '/home/samsclaw/.openclaw/workspace', 'push', 'origin', 'master'],
    'git_status': ['git', '-C', '/home/samsclaw/.openclaw/workspace', 'status', '-sb'],
    'git_log': ['git', '-C', '/home/samsclaw/.openclaw/workspace', 'log', '--oneline', '-10'],
    'gen_dashboard': ['python3', '/home/samsclaw/.openclaw/workspace/scripts/generate_dashboard_v2.py'],
    'check_dashboard': ['ls', '-la', '/home/samsclaw/.openclaw/workspace/dashboard/'],
    'check_whoop': ['ls', '-la', '/home/samsclaw/.openclaw/whoop_data/'],
    'check_tat': ['python3', '/home/samsclaw/.openclaw/workspace/scripts/add_tat_task.py', 'list'],
    'list_cron': ['crontab', '-l'],
    'security_audit': ['python3', '/home/samsclaw/.openclaw/workspace/scripts/security_sentinel.py'],
    'disk_space': ['df', '-h'],
    'memory_usage': ['free', '-h'],
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path.startswith('/run'):
            self.handle_command()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_command(self):
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        cmd_key = params.get('cmd', [''])[0]
        
        if cmd_key not in COMMANDS:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': 'Unknown command'}).encode())
            return
        
        try:
            result = subprocess.run(
                COMMANDS[cmd_key],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout
            if result.stderr:
                output += '\n\n[Errors]:\n' + result.stderr
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': result.returncode == 0,
                'output': output,
                'error': result.stderr if result.returncode != 0 else None
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        # Suppress logs
        pass

if __name__ == '__main__':
    import socket
    
    # Get IP address
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = 'localhost'
    
    print(f"🚀 Remote Console starting...")
    print(f"📱 Access from your phone: http://{ip}:{PORT}")
    print(f"💻 Or locally: http://localhost:{PORT}")
    print(f"🛑 Press Ctrl+C to stop")
    print()
    
    with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
