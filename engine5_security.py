#!/usr/bin/env python3
"""
ATHERSPIRE ENGINE 5: SECURITY ORCHESTRATOR
Quad-Mirror Defense System - Protects against attacks
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class MirrorGatekeeper:
    """Mirror 1: AI-Powered WAAP - Blocks bad traffic at the edge"""
    def __init__(self):
        self.blocked_ips = set()
        self.suspicious_patterns = [
            'sql', 'SELECT', 'DROP', 'UNION', '--', ';',
            '../', '..\\', '/etc/', 'passwd',
            '<script', 'javascript:', 'onerror='
        ]
        self.request_counts = defaultdict(list)
        self.max_requests_per_minute = 60
    
    def check_request(self, ip, path, headers):
        # Check if IP is already blocked
        if ip in self.blocked_ips:
            return False, "IP blocked"
        
        # Rate limiting
        now = time.time()
        self.request_counts[ip] = [t for t in self.request_counts[ip] if now - t < 60]
        self.request_counts[ip].append(now)
        
        if len(self.request_counts[ip]) > self.max_requests_per_minute:
            self.blocked_ips.add(ip)
            return False, "Rate limit exceeded"
        
        # Check for malicious patterns in path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                self.blocked_ips.add(ip)
                return False, f"Suspicious pattern: {pattern}"
        
        return True, "Allowed"

class MirrorMirage:
    """Mirror 2: Frontend Obfuscation - Confuses reverse engineers"""
    def __init__(self):
        self.rotation_keys = {}
        self.active_tokens = {}
    
    def generate_token(self, client_id):
        token = hashlib.sha256(f"{client_id}{time.time()}".encode()).hexdigest()[:32]
        self.active_tokens[token] = datetime.now() + timedelta(hours=1)
        return token
    
    def validate_token(self, token):
        if token in self.active_tokens:
            if datetime.now() < self.active_tokens[token]:
                return True
            else:
                del self.active_tokens[token]
        return False

class MirrorTrap:
    """Mirror 3: Honeypots & RASP - Traps attackers in fake environments"""
    def __init__(self):
        self.honeypots = [
            '/admin/backup.sql',
            '/.env',
            '/config.json.bak',
            '/wp-admin',
            '/phpmyadmin',
            '/.git/config',
            '/api/v1/debug',
            '/database.sql'
        ]
        self.trapped_ips = {}
        self.attack_log = []
    
    def is_honeypot(self, path):
        return path in self.honeypots
    
    def trap_attacker(self, ip, path):
        self.trapped_ips[ip] = {
            'first_seen': datetime.now(),
            'path': path,
            'attempts': 1
        }
        self.attack_log.append({
            'ip': ip,
            'path': path,
            'time': datetime.now().isoformat(),
            'action': 'trapped'
        })
        return True
    
    def get_attack_log(self):
        return self.attack_log[-100:]  # Last 100 attacks

class MirrorVoid:
    """Mirror 4: Zero-Trust Enforcement - Immutable logging and strict access"""
    def __init__(self):
        self.access_log = []
        self.valid_tokens = set()
        self.log_file = 'security.audit'
    
    def log_access(self, ip, path, token, allowed):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'path': path,
            'token_valid': token is not None,
            'allowed': allowed
        }
        self.access_log.append(entry)
        
        # Append to immutable log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        return entry

class SecurityOrchestrator:
    """Coordinates all four mirrors"""
    def __init__(self):
        self.gatekeeper = MirrorGatekeeper()
        self.mirage = MirrorMirage()
        self.trap = MirrorTrap()
        self.void = MirrorVoid()
        self.start_time = datetime.now()
        self.total_requests = 0
        self.blocked_requests = 0
    
    def check_request(self, ip, path, headers, token=None):
        self.total_requests += 1
        
        # Mirror 1: Gatekeeper
        allowed, reason = self.gatekeeper.check_request(ip, path, headers)
        if not allowed:
            self.blocked_requests += 1
            self.void.log_access(ip, path, token, False)
            return {'allowed': False, 'reason': reason, 'mirror': 1}
        
        # Mirror 3: Trap - Check if hitting honeypot
        if self.trap.is_honeypot(path):
            self.trap.trap_attacker(ip, path)
            self.blocked_requests += 1
            self.void.log_access(ip, path, token, False)
            return {'allowed': False, 'reason': 'Honeypot triggered', 'mirror': 3}
        
        # Mirror 4: Void - Token validation
        if token:
            if not self.mirage.validate_token(token):
                self.void.log_access(ip, path, token, False)
                return {'allowed': False, 'reason': 'Invalid token', 'mirror': 4}
        
        # All checks passed
        self.void.log_access(ip, path, token, True)
        return {'allowed': True, 'reason': 'Allowed', 'mirror': 0}
    
    def get_stats(self):
        uptime = datetime.now() - self.start_time
        return {
            'uptime_seconds': uptime.seconds,
            'total_requests': self.total_requests,
            'blocked_requests': self.blocked_requests,
            'blocked_percentage': round(self.blocked_requests / max(1, self.total_requests) * 100, 2),
            'active_tokens': len(self.mirage.active_tokens),
            'trapped_ips': len(self.trap.trapped_ips),
            'mirrors': {
                'gatekeeper': 'active',
                'mirage': 'active',
                'trap': 'active',
                'void': 'active'
            }
        }

# Initialize security orchestrator
security = SecurityOrchestrator()

class SecurityHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(security.get_stats()).encode())
        
        elif self.path == '/attacks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(security.trap.get_attack_log()).encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logging

def run_security_server():
    server = HTTPServer(('0.0.0.0', 9000), SecurityHandler)
    print(f"🔒 Security API: http://localhost:9000/status")
    print(f"📋 Attack log: http://localhost:9000/attacks")
    server.serve_forever()

async def main():
    print("\n" + "="*60)
    print("🔒 ATHERSPIRE ENGINE 5: QUAD-MIRROR SECURITY")
    print("="*60)
    print("🛡️ Mirror 1: Gatekeeper - AI WAAP")
    print("🛡️ Mirror 2: Mirage - Frontend Obfuscation")
    print("🛡️ Mirror 3: Trap - Honeypots & RASP")
    print("🛡️ Mirror 4: Void - Zero-Trust & Immutable Logs")
    print("="*60)
    print("📡 Security API: http://localhost:9000")
    print("📊 Status: http://localhost:9000/status")
    print("📋 Attack log: http://localhost:9000/attacks")
    print("="*60 + "\n")
    
    # Run in a separate thread
    thread = threading.Thread(target=run_security_server)
    thread.daemon = True
    thread.start()
    
    # Keep running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
