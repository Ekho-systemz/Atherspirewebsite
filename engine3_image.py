
#!/usr/bin/env python3
"""
ATHERSPIRE ENGINE 3: IMAGE ARCHIVE
Serves 4D images and galleries
"""

import asyncio
import websockets
import json
import base64
import os
from pathlib import Path
import mimetypes
from datetime import datetime

class ImageArchive:
    def __init__(self):
        self.images = {}
        self.galleries = {
            'neuromodulation': [],
            'intelligence': [],
            'robotics': [],
            'architecture': [],
            'systems': [],
            'founder': [],
            'quantum': []
        }
        self.base_path = Path('./images')
        self.load_images()
    
    def load_images(self):
        """Scan images directory and load metadata"""
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True)
            print("📁 Created images directory")
            
            # Create category folders
            for category in self.galleries.keys():
                cat_path = self.base_path / category
                cat_path.mkdir(exist_ok=True)
        
        # Load all images
        for img_path in self.base_path.glob('**/*'):
            if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
                rel_path = str(img_path.relative_to(self.base_path))
                category = img_path.parent.name
                
                # Generate image ID
                img_id = f"{category}_{img_path.stem}".replace(' ', '_').lower()
                
                self.images[img_id] = {
                    'id': img_id,
                    'path': rel_path,
                    'category': category,
                    'name': img_path.stem,
                    'type': mimetypes.guess_type(img_path)[0] or 'image/jpeg',
                    'size': img_path.stat().st_size,
                    'created': datetime.fromtimestamp(img_path.stat().st_ctime).isoformat()
                }
                
                if category in self.galleries:
                    self.galleries[category].append(img_id)
        
        print(f"📸 Loaded {len(self.images)} images")
        for category, imgs in self.galleries.items():
            if imgs:
                print(f"  • {category}: {len(imgs)} images")
    
    async def get_image(self, image_id):
        """Retrieve and encode an image"""
        if image_id not in self.images:
            return None
        
        img_info = self.images[image_id]
        img_path = self.base_path / img_info['path']
        
        if not img_path.exists():
            return None
        
        with open(img_path, 'rb') as f:
            img_data = f.read()
        
        return {
            'id': image_id,
            'name': img_info['name'],
            'category': img_info['category'],
            'data': base64.b64encode(img_data).decode('utf-8'),
            'type': img_info['type'],
            'size': len(img_data)
        }
    
    async def get_gallery(self, category):
        """Get all images in a gallery"""
        if category not in self.galleries:
            return []
        
        gallery = []
        for img_id in self.galleries[category]:
            img_info = self.images.get(img_id)
            if img_info:
                gallery.append({
                    'id': img_id,
                    'name': img_info['name'],
                    'category': img_info['category'],
                    'type': img_info['type']
                })
        
        return gallery
    
    async def search_images(self, query):
        """Search images by name or category"""
        query = query.lower()
        results = []
        
        for img_id, info in self.images.items():
            if query in info['name'].lower() or query in info['category'].lower():
                results.append({
                    'id': img_id,
                    'name': info['name'],
                    'category': info['category']
                })
        
        return results

# Create archive instance
archive = ImageArchive()

async def handler(websocket):
    print("📡 Image Archive client connected")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'get_image':
                img = await archive.get_image(data['id'])
                if img:
                    await websocket.send(json.dumps({
                        'type': 'image_data',
                        'data': img
                    }))
                else:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Image not found'
                    }))
            
            elif data['type'] == 'get_gallery':
                gallery = await archive.get_gallery(data['category'])
                await websocket.send(json.dumps({
                    'type': 'gallery_data',
                    'category': data['category'],
                    'images': gallery
                }))
            
            elif data['type'] == 'search':
                results = await archive.search_images(data['query'])
                await websocket.send(json.dumps({
                    'type': 'search_results',
                    'query': data['query'],
                    'results': results
                }))
            
            elif data['type'] == 'list_categories':
                await websocket.send(json.dumps({
                    'type': 'categories',
                    'categories': list(archive.galleries.keys())
                }))
            
            elif data['type'] == 'ping':
                await websocket.send(json.dumps({'type': 'pong'}))
    
    except websockets.exceptions.ConnectionClosed:
        print("📡 Image Archive client disconnected")

async def main():
    print("\n" + "="*60)
    print("🖼️ ATHERSPIRE ENGINE 3: IMAGE ARCHIVE")
    print("="*60)
    print(f"📡 WebSocket: ws://localhost:8766")
    print(f"📸 Serving images from ./images directory")
    print("="*60 + "\n")
    
    async with websockets.serve(handler, "0.0.0.0", 8766):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
