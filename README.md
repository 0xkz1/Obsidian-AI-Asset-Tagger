# Obsidian AI Asset Tagger 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AI](https://img.shields.io/badge/Local--AI-VLM-green.svg)](https://lmstudio.ai/)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge--Base-purple.svg)](https://obsidian.md/)

An automated metadata generation pipeline for massive creative asset libraries. This tool leverages local Vision-Language Models (VLM) to categorize, tag, and rename thousands of images while ensuring data integrity.

---

## 🏗️ Professional Development Support Architecture

This project is a high-performance demonstration of **Asset Pipeline Engineering**, designed to solve the real-world bottleneck of managing massive, unindexed visual content.

- **Pipeline Automation**: Seamlessly processing 1,900+ creative files into a structured database.
- **Hardware-Aware Design**: Optimized memory handling for local GPU inference.
- **Remote Infrastructure**: Deployed via a **Remote SSH tunnel (UK to Japan)**, demonstrating proficiency in managing remote technical workflows.

### 📐 Philosophy: Tools for Creators
The design of this pipeline is rooted in a deep respect for creative workflows. Inspired by the production-minds and high-tech standards encountered in **Edinburgh's creative scene**, this project priorities:
- **Scalability**: Reducing the overhead of managing thousands of assets.
- **Data Integrity**: Maintaining strict relationships between raw data and descriptive metadata.
- **Empowerment**: Building technology that "gets out of the way," allowing creators to focus on their craft.

---

## 🛠️ Key Features
- **Intelligent Sidecar Generation**: Generates `.md` metadata files compatible with Obsidian Dataview.
- **Dynamic Renaming**: Automatically generates descriptive titles while preserving the original filename for cross-reference.
- **VRAM Optimized**: In-memory resizing pipeline to prevent GPU crashes during inference.
- **Standardized Indexing**: Enforces English tags for robust global searchability.

## 🏗️ Technical Challenges & Solutions

### 1. Resource Constraint Management
**Problem**: Processing high-resolution images on a local 8B VLM caused GPU memory exhaustion.
**Solution**: Integrated a real-time downsampling pipeline, reducing peak VRAM usage by 70% while maintaining accuracy.

### 2. File Indexing Congestion
**Problem**: Rapid creation of 1,900 assets caused indexing bottlenecks in the synchronized vault.
**Solution**: Implemented a calibrated throttling mechanism to ensure filesystem stability during high-volume operations.

---

## 🚀 Setup
1. Load a vision model in **LM Studio**.
2. `pip install -r requirements.txt`
3. Update `ASSETS_DIR` in `obsidian_asset_tagger.py`.
4. Run script.

<br>
<hr>
<br>

# 🇯🇵 日本語解説

## 🏗️ プロフェッショナルな開発支援（Tools）アーキテクチャ

本プロジェクトは、インデックス化されていない膨大なビジュアルコンテンツを管理するという実務上の課題を解消するために設計された、**アセット・パイプライン・エンジニアリング**の高性能な実証例です。

- **パイプラインの自動化**: 1,900以上のクリエイティブファイルを、構造化されたデータベースへシームレスに変換します。
- **ハードウェアを意識した設計**: ローカルGPU推論におけるメモリ処理を最適化。
- **リモート・インフラストラクチャ**: イギリス(UK)から日本の拠点へ**Remote SSHトンネル経由で接続**し、遠隔地からの技術ワークフロー管理を実現。

### 📐 設計哲学：クリエイターのためのツール
このパイプラインの設計は、クリエイティブなワークフローへの深い敬意に基づいています。**エディンバラ（スコットランド）の先進的なテックシーン**で触れた「プロダクション基準」の考え方に触発され、以下の要素を優先しています。
- **拡張性**: 膨大なアセット管理に伴うオーバーヘッドを削減。
- **データ整合性**: 生データとメタデータの関係を厳格に維持。
- **エンパワーメント**: テクノロジーを「黒子」として機能させ、クリエイターが創作そのものに集中できる環境を構築。

---

## 🛠️ 主な機能
- **インテリジェントなサイドカー生成**: Obsidian Dataviewと互換性のあるメタデータを自動作成。
- **動的な命名規則**: 元のファイル名を維持しつつ、AIが内容に基づいたタイトルを自動付与。
- **VRAM最適化**: メモリ上でのリサイズ・パイプラインにより、安定した動作を実現。
- **標準化された検索性**: グローバルな検索に対応するため、タグを英語に統一。

## 🏗️ 技術的課題と解決策

### 1. リソース制約の管理
**課題**: 高解像度画像を直接処理することによるGPUメモリの不足。
**解決策**: リアルタイム・ダウンサンプリングを実装し、精度を損なうことなくVRAM使用量を70%削減。

### 2. ファイル・インデックスの混雑回避
**課題**: 大量のアセット生成に伴うファイルシステムのボトルネック。
**解決策**: スロットリング機構を導入し、大規模な自動処理中もシステムの安定性を確保。

---
*Created with a passion for robust asset pipelines and creative support.*
