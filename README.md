# Obsidian AI Asset Tagger 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/Local--AI-VLM-green.svg)](https://lmstudio.ai/)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge--Base-purple.svg)](https://obsidian.md/)

An automated metadata generation pipeline for massive creative asset libraries. This tool leverages local Vision-Language Models (VLM) to categorize, tag, and rename thousands of images without breaking existing internal links in your knowledge base.

---

## 🌟 The "Rockstar" Edge: Development Support Engineering
This project demonstrates the core responsibilities of a **Development Support (Tools)** role:
- **Asset Pipeline Optimization**: Automating tedious manual tagging for 1,900+ creative files.
- **Hardware-Aware Engineering**: Solving VRAM exhaustion and GPU crashes on local hardware.
- **Remote Infrastructure**: Developed over a **Remote SSH tunnel from the UK to a GPU workstation in Japan**, showcasing ability to manage remote development environments.

---

## 🛠️ Key Features
- **Intelligent Sidecar Generation**: Creates `.md` files containing tags, categories, and AI descriptions compatible with Obsidian's Dataview.
- **Dynamic Renaming**: Automatically generates descriptive titles in Japanese (for searchability) while preserving the original technical filename to maintain data integrity.
- **VRAM Optimized**: Implements an in-memory image resizing pipeline (downscaling to 768px before inference) to prevent GPU TDR crashes and reduce latency.
- **Production-Ready Metadata**: Enforces English tags for standardized library indexing.

## 🏗️ Technical Challenges & Solutions

### 1. The "Model Crash" (VRAM Management)
**Problem**: Sending high-resolution 4K/8K images directly to the local 8B VLM caused consistent GPU out-of-memory (OOM) errors and API crashes.
**Solution**: Integrated `Pillow` to implement a real-time downsampling pipeline. By resizing images to a max dimension of 768px in-memory, processing stability was increased to **100%** with negligible impact on AI accuracy.

### 2. File Indexing Congestion
**Problem**: Rapid creation of 1,900 files in a synchronized vault (Syncthing/Obsidian Sync) caused UI freezing on the client machine.
**Solution**: Implemented a throttling mechanism (0.1s - 1.0s sleep cycles) to allow the filesystem indexer and network sync to breathe, ensuring a smooth background processing experience.

### 3. Data Integrity vs Searchability
**Problem**: "Pasted image 2022..." filenames are terrible for searching, but renaming them breaks thousands of existing Obsidian notes.
**Solution**: Developed a "Descriptive Sidecar" pattern. The image stays named as-is, but the accompanying Markdown file is named `OriginalName - DescriptiveTitle.md`, a format that solves searchability while keeping files grouped together in any file explorer.

---

## 🚀 Setup & Usage

1. **Load VLM**: Load a vision model (e.g., `Qwen3-VL`) in LM Studio and start the local server.
2. **Install Deps**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure**: Update `ASSETS_DIR` and `MODEL_ID` in `obsidian_asset_tagger.py`.
4. **Run**:
   ```bash
   python3 obsidian_asset_tagger.py
   ```

---

## 📈 Results (Before & After)

| Metric | Before | After |
| :--- | :--- | :--- |
| **Searchability** | Impossible (Timed filenames) | Instant (Natural Language) |
| **Organization** | Flat file list | Fully categorized (Art, Tech, Nature, etc.) |
| **Data Integrity** | Manual | Non-destructive automation |

---

## 👨‍💻 Developer Notes
This tool was built to solve a personal data management bottleneck, reflecting a passion for building robust pipelines that empower creators and maintain high data standards. Developed with a high-performance mindset, balancing speed with hardware constraints.
