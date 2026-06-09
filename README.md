# 🧩 PuzzleEvo

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Repo](https://img.shields.io/badge/GitHub-Jimmi1e%2FPuzzleEvo-black)](https://github.com/Jimmi1e/PuzzleEvo)

> **🌍 Language:** [English](#-english-version) | [中文](#-中文版)

---

## 🇬🇧 English Version

### 📖 Introduction

Welcome to **PuzzleEvo**! This project is a Python-based framework designed for algorithmically solving, analyzing, and visualizing puzzles. Inspired by evolutionary computation and advanced search algorithms, PuzzleEvo provides a modular approach to puzzle-solving, combining robust backend logic with intuitive visual feedback.

### ✨ Key Features

* **Modular Algorithm Design:** Easily swap or upgrade solving algorithms without altering the core pipeline.
* **Rich Visualization:** Watch the puzzle-solving process in real-time or analyze the final results step-by-step.
* **Data-Driven:** Structured data handling makes it easy to import new puzzles or export solution metrics.
* **Clean Architecture:** Highly organized codebase separating logic, data, and presentation.

### 📂 Repository Structure

Based on our clean separation of concerns, here is how the project is organized:

| Directory/File | Description |
| :--- | :--- |
| 📁 `algorithm/` | Contains the core puzzle-solving algorithms (e.g., evolutionary, search). |
| 📁 `data/` | Stores input puzzle datasets, configurations, and saved output files. |
| 📁 `utils/` | Helper functions, constants, and shared utilities used across the project. |
| 📁 `visualization/` | Code responsible for rendering graphics and plotting the solving process. |
| 📄 `run.py` | The main entry point to execute the puzzle solver pipeline. |
| 📄 `puzzle_viewer.py` | A dedicated standalone script to inspect and view puzzles/results visually. |

### 🚀 Quick Start

**1. Clone the repository:**

    git clone https://github.com/Jimmi1e/PuzzleEvo.git
    cd PuzzleEvo

**2. Run the main algorithm:**

    python run.py

**3. View the puzzle visualization:**

    python puzzle_viewer.py

---

## 🇨🇳 中文版

### 📖 项目简介

欢迎来到 **PuzzleEvo**！本项目是一个基于 Python 开发的框架，致力于通过算法来求解、分析和可视化各类拼图/谜题。受进化计算和高级搜索算法的启发，PuzzleEvo 提供了一套高度模块化的解决方案，将强大的底层算法逻辑与直观的视觉反馈完美结合。

### ✨ 核心特性

* **模块化算法设计：** 算法与核心流程解耦，方便随时替换、升级或测试不同的求解算法。
* **丰富的可视化：** 实时动态展示拼图求解过程，或支持分步复盘最终结果。
* **数据驱动：** 结构化的数据管理，轻松导入新的谜题数据集或导出求解评估指标。
* **清晰的架构：** 代码结构整洁，将核心逻辑、数据处理与前端展示严格分离。

### 📂 目录结构

项目采用了清晰的职责分离架构，目录说明如下：

| 目录/文件 | 详细说明 |
| :--- | :--- |
| 📁 `algorithm/` | 核心算法库，包含拼图求解算法（如进化算法、搜索算法等）。 |
| 📁 `data/` | 数据文件夹，用于存放输入的谜题数据、配置文件及输出结果。 |
| 📁 `utils/` | 工具箱，存放项目中通用的辅助函数和全局常量。 |
| 📁 `visualization/` | 可视化模块，负责图形渲染和求解过程的动态展示。 |
| 📄 `run.py` | 项目主程序入口，用于执行完整的求解流程。 |
| 📄 `puzzle_viewer.py` | 独立的查看器脚本，用于直观地预览谜题和展示结果。 |

### 🚀 快速开始

**1. 克隆项目到本地：**

    git clone https://github.com/Jimmi1e/PuzzleEvo.git
    cd PuzzleEvo

**2. 运行主求解程序：**

    python run.py

**3. 启动谜题可视化查看器：**

    python puzzle_viewer.py

---
*Created with ❤️ by [Jimmi1e](https://github.com/Jimmi1e)*
