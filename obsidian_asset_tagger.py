"""
Obsidian AI Asset Tagger
========================
Automated metadata generation pipeline for creative asset libraries using Local Vision-Language Models (VLM).

Designed to transform thousands of unindexed images into a structured, searchable English-language database 
with intelligent backlink tracking across the entire Obsidian Vault.

Key Features:
- Local AI Inference: Powered by LM Studio for privacy and zero API costs.
- Intelligent Backlink Indexing: Scans the Vault to identify which notes reference each asset.
- All-English Metadata: Generates professional titles, tags, and descriptions in English.
- Resource Aware: Optimized in-memory resizing to handle massive high-res libraries.
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
VAULT_DIR = "/home/kz003/atelier/obsidian-vault"
MODEL_ID = "qwen/qwen3-vl-8b"
MAX_IMAGE_SIZE = 768
# ---------------------

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')
NOTE_EXTENSIONS = ('.md', '.canvas')

def build_backlink_index(vault_dir):
    """Scans the Vault and builds a reverse index of image references."""
    print("Building backlink index across Vault...")
    index = {}
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            if not any(fname.endswith(ext) for ext in NOTE_EXTENSIONS):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                links = re.findall(r'\[\[([^\]|#]+)', content)
                for link in links:
                    link_base = os.path.basename(link.strip())
                    if link_base not in index:
                        index[link_base] = []
                    note_name = os.path.splitext(fname)[0]
                    if note_name not in index[link_base]:
                        index[link_base].append(note_name)
            except:
                continue
    return index

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def sanitize_tags(tags):
    if isinstance(tags, list):
        return [tag.strip().replace(" ", "-").lower() for tag in tags if tag]
    return []

def encode_image_resized(image_path):
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
    base64_data = encode_image_resized(image_path)
    if not base64_data: return None

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
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}}
        ]}],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        content = response.json()['choices'][0]['message']['content']
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match: return json.loads(match.group())
    except:
        pass
    return None

def format_linked_notes(notes):
    if not notes: return "[]"
    items = "\n".join(f'  - "[[{n}]]"' for n in notes)
    return f"\n{items}"

def main():
    if not os.path.exists(ASSETS_DIR):
        print(f"Error: Directory {ASSETS_DIR} not found.")
        return

    backlink_index = build_backlink_index(VAULT_DIR)
    img_files = sorted([f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS)])
    
    print(f"Processing {len(img_files)} assets...")

    for filename in img_files:
        base_name = os.path.splitext(filename)[0]
        img_path = os.path.join(ASSETS_DIR, filename)
        
        # Filter out self-references (sidecar files) from linked notes
        linked = [n for n in backlink_index.get(filename, []) if not n.startswith(base_name)]

        # Check for existing sidecar with title
        existing = [f for f in os.listdir(ASSETS_DIR) if f.startswith(base_name) and " - " in f]
        if existing:
            # Check if linked_notes needs update
            md_path = os.path.join(ASSETS_DIR, existing[0])
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "linked_notes:" not in content:
                print(f"Updating backlinks: {existing[0]}")
                new_content = content.replace("---\n![[", f"linked_notes:{format_linked_notes(linked)}\n---\n![[", 1)
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
            continue
        
        print(f"Analyzing: {filename}")
        analysis = analyze_image(img_path)
        if not analysis: continue

        title = sanitize_filename(analysis.get('title', 'Untitled'))
        tags = sanitize_tags(analysis.get('tags', []))
        md_name = f"{base_name} - {title}.md"
        
        metadata = f"""---
title: {title}
category: {analysis.get('category', 'Unclassified')}
tags: {tags}
cover: "{filename}"
linked_notes:{format_linked_notes(linked)}
processed_at: {datetime.now().strftime("%Y-%m-%d %H:%M")}
---
![[{filename}]]

{analysis.get('description', '')}
"""
        with open(os.path.join(ASSETS_DIR, md_name), "w", encoding="utf-8") as f:
            f.write(metadata)
        print(f"  -> Created: {md_name}")

if __name__ == "__main__":
    main()
