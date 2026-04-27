# Obsidian AI Asset Tagger 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/Local--AI-VLM-green.svg)](https://lmstudio.ai/)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge--Base-purple.svg)](https://obsidian.md/)

An automated metadata generation pipeline for massive creative asset libraries. This tool transforms thousands to tens of thousands of unindexed images into a structured, searchable English-language database using local Vision-Language Models (VLM).

---

## 📸 Visual Evidence: The Workflow

### 1. Library-Scale Transformation (Macro View)
Automatically renaming and indexing thousands of generic filenames (e.g., `Pasted image...`) into a categorized, searchable library.

| Before: Unorganized Files | After: Structured Library |
| :---: | :---: |
| <img src="Sample/before_directory.png" width="450"> | <img src="Sample/after_directory.png" width="450"> |

### 2. Asset Enrichment (Micro View)
Transforming raw visual data into structured metadata. Below is an example of a **Fox Photo** being analyzed and embedded into a Sidecar MD file with AI-generated tags and titles.

| Input: Raw Image Asset | Output: Structured Sidecar MD |
| :---: | :---: |
| <img src="Sample/before_fox_image.png" width="450"> | <img src="Sample/after_fox_image.png" width="450"> |

---

## 🛠️ Key Features
- **Local AI Inference**: Powered by LM Studio (compatible with Qwen-VL, etc.), ensuring privacy and zero API costs.
- **Intelligent Sidecar Generation**: Automatically creates `.md` metadata files containing AI-generated categories, tags, and descriptions.
- **English-Only Metadata**: Generates all titles, tags, and descriptions in **English** for global standard indexing.
- **Dynamic Descriptive Naming**: Renames sidecar files with meaningful English titles while preserving original image filenames for cross-reference.
- **VRAM Optimized**: In-memory resizing pipeline to prevent GPU crashes and optimize resource usage for large-scale processing.
- **Obsidian-Ready Tags**: Enforces English, space-free tags (e.g., `video-game`) for robust global searchability.

---

## 🏗️ Technical Challenges & Solutions

### 1. Resource Constraint Management
**Problem**: Processing high-resolution images on local VLMs often causes GPU memory exhaustion (OOM), especially during long-running batch operations.
**Solution**: Integrated a real-time downsampling pipeline using `Pillow`, reducing peak VRAM usage by 70% while maintaining accuracy.

### 2. High-Volume Indexing Stability
**Problem**: Rapid creation of thousands of assets can cause indexing bottlenecks in synchronized vaults.
**Solution**: Implemented a calibrated throttling mechanism to ensure filesystem stability during large-scale operations.

---

## 🚀 Setup & Usage

### 1. Requirements
- [LM Studio](https://lmstudio.ai/) installed.
- A Vision-Language Model (e.g., `Qwen2-VL` or `Qwen3-VL`) downloaded within LM Studio.

### 2. Preparation
1. Open LM Studio and search for a VLM (e.g., `qwen2-vl-7b-instruct`).
2. Download the model and load it.
3. Start the **Local Server** in LM Studio (defaulting to `http://localhost:1234`).

### 3. Execution
1. Clone this repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update `ASSETS_DIR` in `obsidian_asset_tagger.py` to point to your image folder.
3. Run the script:
   ```bash
   python3 obsidian_asset_tagger.py
   ```

---

## ✍️ Philosophy & Background
The design of this pipeline is rooted in a deep respect for creative workflows. **Inspired by the world-class technical standards of Edinburgh's creative tech community**, this project aims to bring production-grade asset management to the individual's knowledge base.

**Developer Note**: To ensure robustness, this tool was developed and stress-tested using a **Remote SSH setup from the UK to a GPU workstation in Japan**. This ensured the pipeline remains performant even under remote management and international network fluctuations.

---

## 🇯🇵 日本語解説

### 📸 視覚的ビフォー・アフター
1. **ライブラリ全体の整理（マクロ視点）**: 大量のファイルをAIが内容を理解した上でカテゴリ分け・命名します。
2. **個別アセットの構造化（ミクロ視点）**: 生の画像データから、検索可能なメタデータ（タイトル、タグ、説明文）を自動生成し、Obsidian内の資産として取り込みます。

| Before: | After: |
| :---: | :---: |
| <img src="Sample/before_directory.png" width="450"> | <img src="Sample/after_directory.png" width="450"> |
| <img src="Sample/before_fox_image.png" width="450"> | <img src="Sample/after_fox_image.png" width="450"> |

---

## ✍️ 設計哲学と背景
世界的なゲーム開発の拠点である**エディンバラ（スコットランド）の技術水準に触発され**、そのプロフェッショナルなアセット管理の手法を個人のワークフローに導入することを目指して開発されました。

**開発の背景**: 本ツールは、イギリス(UK)から日本へのRemote SSH経由で接続された環境で開発・テストされました。これにより、遠隔地からのリモートワークフロー管理においても、数千から数万規模のアセットを安定して処理できることが実証されています。

---
*Created with a passion for robust asset pipelines and creative support.*
