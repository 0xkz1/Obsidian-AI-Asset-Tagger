"""
Obsidian AI Asset Tagger
========================
Automated metadata pipeline for creative assets using Local Vision-Language Models (VLM).

Developed to categorize and tag thousands of images in an Obsidian vault 
without breaking existing internal links.

Key Features:
- Local Inference: Uses LM Studio / OpenAI-compatible API for privacy and zero cost.
- Asset Pipeline: Resizes images in-memory to optimize VRAM usage and processing speed.
- Smart Renaming: Generates descriptive titles for sidecar files based on AI analysis.
- Remote Ready: Designed and tested over SSH from UK to a GPU-workstation in Japan.
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
# Default to LM Studio local server
API_URL = "http://localhost:1234/v1/chat/completions"
# Path to your Obsidian assets folder
ASSETS_DIR = "/home/kz003/atelier/obsidian-vault/11_assets_OB"
# VLM Model Identifier (Change based on your LM Studio settings)
MODEL_ID = "qwen/qwen3-vl-8b"
# Max dimension for image processing (smaller = faster / less VRAM)
MAX_IMAGE_SIZE = 768
# ---------------------

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')

def sanitize_filename(name):
    """Removes illegal characters for cross-platform filename safety."""
    name = re.sub(r'[\\/*?Internal:"<>|]', "", name)
    return name.strip()

def encode_image_resized(image_path):
    """Resizes image to target max dimension and encodes to Base64."""
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
        print(f"  [Error] Failed to process image {image_path}: {e}")
        return None

def analyze_image(image_path):
    """Sends image to VLM for categorization and tagging."""
    base64_data = encode_image_resized(image_path)
    if not base64_data:
        return None

    prompt = """
Analyze this image and provide a structured classification:
1. Short descriptive title in Japanese (max 15 chars).
2. Category: Photography, Art, Nature, Tech, Document, Finance, People, or Gaming.
3. Tags: 3-5 keywords in English only.
4. Description: One sentence in Japanese.

Output ONLY JSON format:
{
  "title": "Title",
  "category": "Category",
  "tags": ["tag1", "tag2"],
  "description": "Description"
}
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
        response.raise_for_status()
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
    print(f"Found {len(files)} creative assets. Starting pipeline...")

    for filename in files:
        base_name = os.path.splitext(filename)[0]
        img_path = os.path.join(ASSETS_DIR, filename)
        
        # Check if a sidecar file already exists for this image
        existing_md = [f for f in os.listdir(ASSETS_DIR) if f.startswith(base_name) and f.endswith(".md")]
        if existing_md:
            # Skip if already processed in latest Descriptive Format
            if " - " in existing_md[0]:
                continue
        
        print(f"Analyzing: {filename}...")
        analysis = analyze_image(img_path)
        
        if not analysis:
            print(f"  -> Skipping {filename}")
            continue

        title = sanitize_filename(analysis.get('title', 'Untitled'))
        md_filename = f"{base_name} - {title}.md"
        md_path = os.path.join(ASSETS_DIR, md_filename)

        metadata = f"""---
title: {title}
category: {analysis.get('category', 'Unclassified')}
tags: {analysis.get('tags', [])}
cover: "{filename}"
processed_at: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---
![[{filename}]]

{analysis.get('description', '')}
"""
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(metadata)
        
        print(f"  -> Created: {md_filename}")
        time.sleep(0.1)  # Throttling to prevent IO congestion

if __name__ == "__main__":
    main()
