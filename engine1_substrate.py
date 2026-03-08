#!/usr/bin/env python3
"""
ATHERSPIRE ENGINE 1: SUBSTRATE CORE
The 4D intelligence heart - stability, signatures, core logic
"""

import asyncio
import websockets
import json
import uuid
import time
from datetime import datetime

class SubstrateCore:
    def __init__(self):
        self.stability = 0.0
        self.coherence = 0.95
        self.visitor_signature = None
        self.active_chambers = []
        self.clients = set()
        self.start_time = datetime.now()

    async def initialize(self):
        print("\n" + "="*60)
        print("🧠 ATHERSPIRE ENGINE 1: SUBSTRATE CORE")
        print("="*60)
        print("🔮 Initializing 4D intelligence core...")
        
        # The 0.3s stabilization sequence
        self.stability = 0.92
        print(f"▓ 92% stabilized")
        await asyncio.sleep(0.1)
        
        self.stability = 0.97
        print(f"▓▓ 97% stabilized")
        await asyncio.sleep(0.1)
        
        self.stability = 0.99
        print(f"▓▓▓ 99% stabilized")
        await asyncio.sleep(0.1)
        
        self.stability = 1.0
        print(f"✅ Substrate stabilized at 100%")
        print(f"📡 WebSocket: ws://localhost:8765")
        print("="*60 + "\n")

    def get_state(self):
        return {
            'stability': self.stability,
            'coherence': self.coherence,
            'visitor_signature': self.visitor_signature,
            'active_chambers': self.active_chambers,
            'uptime': (datetime.now() - self.start_time).seconds,
            'dimension': 4,
            'particles': 10000
        }

    async def scan_visitor(self):
        signature = str(uuid.uuid4())[:8].upper() + "-" + str(uuid.uuid4())[:4].upper()
        self.visitor_signature = signature
        self.stability = 0.95
        await asyncio.sleep(0.2)
        self.stability = 1.0
        return signature

    async def navigate_chamber(self, chamber):
        if chamber not in self.active_chambers:
            self.active_chambers.append(chamber)
        return {'chamber': chamber, 'status': 'entered', 'timestamp': datetime.now().isoformat()}

# Create global instance
core = SubstrateCore()

async def handler(websocket):
    client_id = str(uuid.uuid4())[:8]
    print(f"🌐 Client {client_id} connected to Substrate")
    core.clients.add(websocket)
    
    try:
        # Send initial state
        await websocket.send(json.dumps({
            'type': 'state',
            'data': core.get_state()
        }))
        
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'ping':
                await websocket.send(json.dumps({'type': 'pong', 'timestamp': time.time()}))
                
            elif data['type'] == 'scan':
                sig = await core.scan_visitor()
                await websocket.send(json.dumps({
                    'type': 'signature',
                    'signature': sig
                }))
                
            elif data['type'] == 'navigate':
                result = await core.navigate_chamber(data['chamber'])
                await websocket.send(json.dumps({
                    'type': 'navigation',
                    'data': result
                }))
                
            elif data['type'] == 'stabilize':
                core.stability = 1.0
                await websocket.send(json.dumps({
                    'type': 'stabilized',
                    'stability': 1.0
                }))
                
            elif data['type'] == 'get_state':
                await websocket.send(json.dumps({
                    'type': 'state',
                    'data': core.get_state()
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Client {client_id} disconnected")
    finally:
        core.clients.remove(websocket)

async def broadcast_state():
    """Send state to all connected clients"""
    while True:
        if core.clients:
            message = json.dumps({
                'type': 'state_update',
                'data': core.get_state()
            })
            await asyncio.gather(
                *[client.send(message) for client in core.clients],
                return_exceptions=True
            )
        await asyncio.sleep(1)  # Update every second

async def main():
    await core.initialize()
    
    # Start broadcast task
    asyncio.create_task(broadcast_state())
    
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
