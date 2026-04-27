"""
Obsidian AI Asset Tagger
========================
Automated metadata generation pipeline for creative asset libraries using Local Vision-Language Models (VLM).

Designed to transform thousands of unindexed images into a structured, searchable English-language database.

Key Features:
- Local Inference: Uses LM Studio (compatible with Qwen-VL) for privacy and speed.
- All-English Metadata: Generates titles, tags, and descriptions exclusively in English.
- Asset Pipeline: High-performance in-memory processing to handle massive libraries.
- Remote Ready: Developed via SSH from UK to Japan, optimized for remote management.
"""

import os
import requests
import json
import re
import time
import io
import base64
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

# --- CONFIGURATION ---
API_URL = "http://localhost:1234/v1/chat/completions"
ASSETS_DIR = "/home/kz003/atelier/obsidian-vault/11_assets_OB"
MODEL_ID = "qwen/qwen3-vl-8b"
MAX_IMAGE_SIZE = 768
# ---------------------

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')

def sanitize_filename(name):
    """Clean filename for cross-platform compatibility."""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip()

def sanitize_tags(tags):
    """Format tags for Obsidian (lowercase, no spaces, use hyphens)."""
    if isinstance(tags, list):
        return [tag.strip().replace(" ", "-").lower() for tag in tags if tag]
    return []

def encode_image_resized(image_path):
    """Resize image and convert to Base64."""
    if not HAS_PILLOW:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    try:
        with Image.open(image_path) as img:
            img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            return base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"  [Error] {e}")
        return None

def analyze_image(image_path):
    """Analyze image using local VLM API."""
    base64_data = encode_image_resized(image_path)
    if not base64_data:
        return None

    prompt = """
Analyze this image and provide a structured English classification:
1. title: Short English title (max 5 words).
2. category: Photography, Art, Nature, Tech, Document, Finance, People, or Gaming.
3. tags: 3-5 keywords in English (use hyphens for spaces).
4. description: One sentence English description.

Output ONLY JSON format. All values must be in English.
"""
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}}
                ]
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        content = response.json()['choices'][0]['message']['content']
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"  [API Error] {e}")
    return None

def main():
    if not os.path.exists(ASSETS_DIR):
        print(f"Error: Directory {ASSETS_DIR} not found.")
        return

    files = sorted([f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS)])
    print(f"Syncing {len(files)} assets (English Pipeline)...")

    for filename in files:
        base_name = os.path.splitext(filename)[0]
        img_path = os.path.join(ASSETS_DIR, filename)
        
        # Check if MD file exists
        existing_md = [f for f in os.listdir(ASSETS_DIR) if f.startswith(base_name) and f.endswith(".md")]
        if existing_md:
            # For brevity, this version skips existing titled files.
            # In your local scratch script, we added logic to 'fix' Japanese.
            if " - " in existing_md[0]:
                continue
        
        print(f"Analyzing: {filename}...")
        analysis = analyze_image(img_path)
        if not analysis: continue

        title = sanitize_filename(analysis.get('title', 'Untitled'))
        tags = sanitize_tags(analysis.get('tags', []))
        md_filename = f"{base_name} - {title}.md"
        
        metadata = f"""---
title: {title}
category: {analysis.get('category', 'Unclassified')}
tags: {tags}
cover: "{filename}"
processed_at: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---
![[{filename}]]

{analysis.get('description', '')}
"""
        with open(os.path.join(ASSETS_DIR, md_filename), "w", encoding="utf-8") as f:
            f.write(metadata)
        
        print(f"  -> Created: {md_filename}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
