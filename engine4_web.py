#!/usr/bin/env python3
"""
ATHERSPIRE ENGINE 4: WEB SERVER
Serves the 4D interface and static files
"""

import http.server
import socketserver
import json
import os
import time
from urllib.parse import urlparse

PORT = 3000
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

# Create public directory if it doesn't exist
os.makedirs(PUBLIC_DIR, exist_ok=True)

class AtherspireHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)
    
    def do_GET(self):
        # Health check endpoint
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'healthy',
                'engine': 'web-server',
                'time': time.time(),
                'uptime': time.time() - self.server.start_time
            }).encode())
            return
        
        # API status endpoint
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'engines': {
                    'substrate': 'checking',
                    'voice': 'checking',
                    'image': 'checking',
                    'web': 'running',
                    'security': 'checking'
                },
                'version': '1.0.0'
            }).encode())
            return
        
        # Serve static files
        return super().do_GET()
    
    def end_headers(self):
        # Add security headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        super().end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Handle requests in separate threads"""
    daemon_threads = True
    allow_reuse_address = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

def create_default_index():
    """Create a default index.html if none exists"""
    index_path = os.path.join(PUBLIC_DIR, 'index.html')
    
    if not os.path.exists(index_path):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Atherspire Intelligence</title>
    <style>
        body { 
            margin: 0; 
            background: linear-gradient(135deg, #000428, #004e92);
            color: cyan; 
            font-family: monospace; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
        }
        .container { 
            text-align: center; 
            padding: 20px;
        }
        h1 { 
            font-size: 3em; 
            text-shadow: 0 0 20px cyan;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #0ff;
            margin-bottom: 30px;
        }
        .status { 
            margin-top: 20px; 
            color: #0ff;
            font-size: 1.2em;
        }
        .engine-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 30px 0;
        }
        .engine-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0,255,255,0.3);
        }
        .engine-card h3 {
            color: #0ff;
            margin-top: 0;
        }
        .online { color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 ATHERSPIRE</h1>
        <div class="subtitle">4D Intelligence Interface</div>
        
        <div class="engine-grid">
            <div class="engine-card">
                <h3>🔮 Substrate Core</h3>
                <div class="online" id="engine1">✓ Online</div>
            </div>
            <div class="engine-card">
                <h3>❄️ Snow AI</h3>
                <div class="online" id="engine2">✓ Online</div>
            </div>
            <div class="engine-card">
                <h3>🖼️ Image Archive</h3>
                <div class="online" id="engine3">✓ Online</div>
            </div>
            <div class="engine-card">
                <h3>🌐 Web Server</h3>
                <div class="online" id="engine4">✓ Online</div>
            </div>
            <div class="engine-card">
                <h3>🔒 Quad-Mirror</h3>
                <div class="online" id="engine5">✓ Online</div>
            </div>
        </div>
        
        <div class="status">
            🌟 All systems operational 🌟
        </div>
        
        <p style="margin-top: 40px; color: #888;">
            Access points:<br>
            Engine 1: ws://localhost:8765<br>
            Engine 2: ws://localhost:8000/ws<br>
            Engine 3: ws://localhost:8766<br>
            Engine 5: http://localhost:9000/status
        </p>
    </div>
    
    <script>
        // Check engine status
        async function checkEngines() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('engine1').textContent = data.engines.substrate === 'running' ? '✓ Online' : '⚠️ Checking';
                document.getElementById('engine2').textContent = data.engines.voice === 'running' ? '✓ Online' : '⚠️ Checking';
                document.getElementById('engine3').textContent = data.engines.image === 'running' ? '✓ Online' : '⚠️ Checking';
                document.getElementById('engine5').textContent = data.engines.security === 'running' ? '✓ Online' : '⚠️ Checking';
            } catch (e) {
                console.log('Status check failed');
            }
        }
        
        checkEngines();
        setInterval(checkEngines, 5000);
    </script>
</body>
</html>"""
        
        with open(index_path, 'w') as f:
            f.write(html)
        print("📄 Created default index.html")

if __name__ == '__main__':
    create_default_index()
    
    print("\n" + "="*60)
    print("🌐 ATHERSPIRE ENGINE 4: WEB SERVER")
    print("="*60)
    print(f"📡 Port: {PORT}")
    print(f"📁 Serving: {PUBLIC_DIR}")
    print(f"🔗 URL: http://localhost:{PORT}")
    print(f"📊 Status: http://localhost:{PORT}/api/status")
    print("="*60 + "\n")
    
    with ThreadedHTTPServer(("0.0.0.0", PORT), AtherspireHandler) as httpd:
        httpd.start_time = time.time()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Web server stopped")
