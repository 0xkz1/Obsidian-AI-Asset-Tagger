"""
Obsidian AI Asset Tagger
========================
Automated metadata generation pipeline for creative asset libraries using Local Vision-Language Models (VLM).
Supports both Batch Processing and Real-time Monitoring (Daemon Mode).
"""

import os
import requests
import json
import re
import time
import io
import base64
import argparse
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

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

def process_single_asset(filename, backlink_index):
    """Processes a single image asset and creates its sidecar MD."""
    base_name = os.path.splitext(filename)[0]
    img_path = os.path.join(ASSETS_DIR, filename)
    
    # Filter out self-references (sidecar files) from linked notes
    linked = [n for n in backlink_index.get(filename, []) if not n.startswith(base_name)]

    # Strict matching to avoid collisions (e.g. image-1 vs image-11)
    existing = [f for f in os.listdir(ASSETS_DIR) if f == f"{base_name}.md" or f.startswith(f"{base_name} - ")]
    
    if existing:
        try:
            md_path = os.path.join(ASSETS_DIR, existing[0])
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check if linked_notes needs an update (relational integrity)
            new_linked_block = f"linked_notes:{format_linked_notes(linked)}"
            if "linked_notes:" in content:
                match = re.search(r'linked_notes:\s*(.*?)(?=\n---|\n[a-z_]+:)', content, re.DOTALL)
                if match and match.group(0).strip() != new_linked_block.strip():
                    updated = content.replace(match.group(0), new_linked_block)
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(updated)
                    print(f"  -> Updated backlinks: {existing[0]}")
            elif linked:
                updated = content.replace("---\n![[", f"{new_linked_block}\n---\n![[", 1)
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(updated)
                print(f"  -> Added backlinks: {existing[0]}")
            return
        except:
            pass
    
    # If no valid English sidecar exists, perform AI analysis
    print(f"Analyzing: {filename}")
    analysis = analyze_image(img_path)
    if not analysis: return

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

class AssetHandler(FileSystemEventHandler):
    """Watches for new image files and triggers processing."""
    def __init__(self, backlink_index):
        self.backlink_index = backlink_index

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(IMAGE_EXTENSIONS):
            filename = os.path.basename(event.src_path)
            print(f"\n[Detected New Asset] {filename}")
            time.sleep(2)  # Wait for file to be fully written
            process_single_asset(filename, self.backlink_index)

def main():
    parser = argparse.ArgumentParser(description="Obsidian AI Asset Tagger")
    parser.add_argument("--watch", action="store_true", help="Run in Daemon mode (continuous monitoring)")
    args = parser.parse_args()

    if not os.path.exists(ASSETS_DIR):
        print(f"Error: Directory {ASSETS_DIR} not found.")
        return

    # Build index once at startup
    backlink_index = build_backlink_index(VAULT_DIR)

    if args.watch:
        if not HAS_WATCHDOG:
            print("Error: 'watchdog' library not found. Install it with: pip install watchdog")
            return
        print(f"\n--- Entering Daemon Mode ---")
        print(f"Monitoring: {ASSETS_DIR}")
        event_handler = AssetHandler(backlink_index)
        observer = Observer()
        observer.schedule(event_handler, ASSETS_DIR, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        # Standard Batch Mode
        img_files = sorted([f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(IMAGE_EXTENSIONS)])
        print(f"Processing {len(img_files)} assets in Batch Mode...")
        for filename in img_files:
            process_single_asset(filename, backlink_index)
        print("\nBatch Processing Complete.")

if __name__ == "__main__":
    main()
