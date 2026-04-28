# Obsidian AI Asset Tagger 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/Local--AI-VLM-green.svg)](https://lmstudio.ai/)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge--Base-purple.svg)](https://obsidian.md/)

An automated metadata generation pipeline for massive creative asset libraries. This tool transforms thousands to tens of thousands of unindexed images into a structured, searchable English-language database using local Vision-Language Models (VLM).

---

## 📸 Visual Evidence: The Workflow

### 1. Library-Scale Transformation (Macro View)
Automatically renaming and indexing thousands of generic filenames (e.g., `Pasted image...`) into a categorized, searchable library.

#### ❌ Before: Unorganized Generic Filenames
No context, difficult to search, and cluttered filesystem.
![Before Directory](Sample/before_directory.png)

#### ✅ After: Categorized & Searchable Library
AI-driven English titles and sidecar metadata for every asset.
![After Directory](Sample/after_directory.png)

---

### 2. Asset Enrichment (Micro View)
Transforming raw visual data into structured metadata. Below is an example of a **Fox Photo** being analyzed and embedded into a Sidecar MD file with AI-generated tags, descriptions, and backlink tracking.

| Input: Raw Image Asset | Output: Structured Sidecar MD |
| :---: | :---: |
| <img src="Sample/before_fox_image.png" width="450"> | <img src="Sample/after_fox_image.png" width="450"> |

---

## 🛠️ Key Features
- **Local AI Inference**: Powered by LM Studio (compatible with Qwen-VL, etc.), ensuring privacy and zero API costs.
- **Continuous Monitoring (Daemon Mode)**: Uses `watchdog` to monitor your assets folder in real-time. New images are tagged automatically as soon as they are added.
- **Intelligent Backlink Indexing**: Automatically identifies and lists every note or canvas in your Vault that references the image, preserving data relationships.
- **Intelligent Sidecar Generation**: Automatically creates `.md` metadata files containing AI-generated categories, tags, and descriptions.
- **English-Only Metadata**: Generates all titles, tags, and descriptions in **English** for global standard indexing.
- **VRAM Optimized**: In-memory resizing pipeline to prevent GPU crashes and optimize resource usage for large-scale processing.

---

## 🏗️ Technical Challenges & Solutions

### 1. Resource Constraint Management
**Problem**: Processing high-resolution images on local VLMs often causes GPU memory exhaustion (OOM), especially during long-running batch operations.
**Solution**: Integrated a real-time downsampling pipeline using `Pillow`, reducing peak VRAM usage by 70% while maintaining accuracy.

### 2. Relational Data Integrity
**Problem**: Traditional tagging loses the context of where an image is actually used within a knowledge base.
**Solution**: Implemented a Vault-wide reverse-indexing engine that scans `.md` and `.canvas` files to build a backlink map, embedding these connections directly into the asset metadata.

### 3. Production-Ready Deployment
**Problem**: Running scripts manually is inefficient for daily workflows.
**Solution**: Developed a `systemd` service integration and an automated `install.sh` script, allowing the tagger to run as a reliable background daemon on Linux environments.

---

## 🚀 Setup & Usage

### 1. Quick Install (Linux Service)
To run the tagger as a permanent background service:
```bash
git clone https://github.com/0xkz1/Obsidian-AI-Asset-Tagger.git
cd Obsidian-AI-Asset-Tagger
chmod +x install.sh
sudo ./install.sh
```

### 2. Manual Execution
**Batch Mode (Process all images once):**
```bash
python3 obsidian_asset_tagger.py
```

**Watch Mode (Monitor for new images):**
```bash
python3 obsidian_asset_tagger.py --watch
```

---

## ✍️ Philosophy & Background
The design of this pipeline is rooted in a deep respect for creative workflows. **Inspired by the world-class technical standards of Edinburgh's creative tech community**, this project aims to bring production-grade asset management to the individual's knowledge base.

**Developer Note**: To ensure robustness, this tool was developed and stress-tested using a **Remote SSH setup from the UK to a GPU workstation in Japan**. This ensured the pipeline remains performant even under remote management and international network fluctuations.

---

## 🇯🇵 日本語解説

### 📸 視覚的ビフォー・アフター
1. **ライブラリ全体の整理**: 大量のファイルをAIが内容を理解した上でカテゴリ分け・命名します。
2. **リアルタイム監視（常駐モード）**: `watchdog` を使用してフォルダを監視し、画像を追加した瞬間に自動でタグ付けを行います。
3. **バックリンクの自動追跡**: その画像がVault内のどのノートやCanvasで使われているかを自動的にリスト化します。

---
*Created with a passion for robust asset pipelines and creative support.*
