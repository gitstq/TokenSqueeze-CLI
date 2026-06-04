# TokenSqueeze-CLI

<p align="center">
  <b>Lightweight LLM Input Intelligent Compression Engine</b><br>
  <b>轻量级LLM输入智能压缩引擎</b><br>
  <b>輕量級LLM輸入智能壓縮引擎</b>
</p>

<p align="center">
  <a href="#-english">English</a> |
  <a href="#-简体中文">简体中文</a> |
  <a href="#-繁體中文">繁體中文</a>
</p>

---

## English

### Introduction

**TokenSqueeze-CLI** is a lightweight, zero-dependency command-line tool designed to intelligently compress text inputs before sending them to Large Language Models (LLMs). By reducing token usage by **50-90%** while preserving semantic meaning, TokenSqueeze helps you save API costs and stay within context window limits.

**Inspiration**: This project was inspired by the growing need to optimize LLM token usage. As AI models become more powerful, context windows expand, but token costs remain a significant concern. TokenSqueeze provides an elegant solution to maximize the value of every token.

**Differentiation**: Unlike other compression tools, TokenSqueeze is completely zero-dependency, supports multiple content-specific compression strategies, and provides both CLI and TUI interfaces for maximum flexibility.

### Core Features

- **Zero Dependencies** - Pure Python standard library, no external packages required
- **Multi-Strategy Compression** - 6 built-in strategies: Smart Truncate, Code, JSON, Log, Markdown, Semantic
- **Auto-Detection** - Automatically selects the best compression strategy based on content type
- **Token Counting** - Built-in token estimation without requiring tiktoken
- **TUI Interface** - Interactive terminal UI for easy exploration
- **Pipe Support** - Full Unix pipe compatibility for seamless integration
- **Compression Stats** - Real-time display of token savings and reduction percentage
- **Cross-Platform** - Works on Linux, macOS, and Windows

### Quick Start

#### Requirements
- Python 3.7+
- Zero external dependencies!

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/TokenSqueeze-CLI.git
cd TokenSqueeze-CLI

# Install in development mode
pip install -e .

# Or install directly
python setup.py install
```

#### Basic Usage

```bash
# Auto-detect and compress a file
tokensqueeze input.txt

# Use specific strategy
tokensqueeze input.py -s code

# Pipe input
echo "Your text here" | tokensqueeze

# Save output to file
tokensqueeze input.txt -o output.txt

# Adjust compression ratio (keep 30%)
tokensqueeze input.txt -r 0.3

# Quiet mode (output only)
tokensqueeze input.txt -q

# List all strategies
tokensqueeze --list-strategies

# Interactive TUI
tokensqueeze-tui
```

### Detailed Usage Guide

#### Compression Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `smart_truncate` | Keeps beginning and end, truncates middle | Long documents |
| `code` | Removes comments and extra whitespace | Source code |
| `json` | Minifies JSON by removing whitespace | JSON data |
| `log` | Removes timestamps and deduplicates | Log files |
| `markdown` | Simplifies formatting while keeping structure | Markdown docs |
| `semantic` | Extractive summarization keeping key sentences | Articles, reports |

#### Examples

**Compress Python Code:**
```bash
$ cat script.py | tokensqueeze -s code
# Removes comments and docstrings, reduces tokens by ~50%
```

**Compress JSON:**
```bash
$ echo '{"key": "value", "nested": {"a": 1}}' | tokensqueeze -s json
{"key":"value","nested":{"a":1}}
```

**Compress Logs:**
```bash
$ cat app.log | tokensqueeze -s log
# Removes timestamps, deduplicates similar entries
```

### Design Philosophy

TokenSqueeze follows the Unix philosophy: do one thing well. It focuses exclusively on text compression for LLM inputs, providing:

- **Simplicity**: No complex configuration, works out of the box
- **Efficiency**: Minimal overhead, maximum compression
- **Transparency**: Clear statistics on token savings
- **Extensibility**: Easy to add new compression strategies

#### Future Roadmap

- [ ] Add more compression strategies (XML, YAML, CSV)
- [ ] Support for custom compression plugins
- [ ] Batch processing for multiple files
- [ ] Integration with popular LLM frameworks
- [ ] Web UI for browser-based compression

### Packaging and Deployment

```bash
# Build distribution
make build

# Run tests
make test

# Run with coverage
make test-cov

# Clean build artifacts
make clean
```

### Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- All tests pass (`make test`)
- New features include tests
- Commit messages follow conventional commits

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 简体中文

### 项目介绍

**TokenSqueeze-CLI** 是一款轻量级、零依赖的命令行工具，专为在向大型语言模型（LLM）发送文本前进行智能压缩而设计。通过在保留语义的同时减少 **50-90%** 的token使用量，TokenSqueeze 帮助您节省 API 成本并保持在上下文窗口限制内。

**灵感来源**：本项目源于对优化 LLM token 使用量的日益增长的需求。随着 AI 模型变得越来越强大，上下文窗口不断扩大，但 token 成本仍然是一个重要问题。TokenSqueeze 为每一个 token 的最大化价值提供了优雅的解决方案。

**差异化亮点**：与其他压缩工具不同，TokenSqueeze 完全零依赖，支持多种内容特定的压缩策略，并提供 CLI 和 TUI 两种界面，灵活性极高。

### 核心特性

- **零依赖** - 纯 Python 标准库实现，无需任何外部包
- **多策略压缩** - 内置6种策略：智能截断、代码、JSON、日志、Markdown、语义
- **自动检测** - 根据内容类型自动选择最佳压缩策略
- **Token 计数** - 内置 token 估算，无需 tiktoken
- **TUI 界面** - 交互式终端界面，便于探索
- **管道支持** - 完整的 Unix 管道兼容性，无缝集成
- **压缩统计** - 实时显示 token 节省量和压缩率
- **跨平台** - 支持 Linux、macOS 和 Windows

### 快速开始

#### 环境要求
- Python 3.7+
- 零外部依赖！

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/TokenSqueeze-CLI.git
cd TokenSqueeze-CLI

# 开发模式安装
pip install -e .

# 或直接安装
python setup.py install
```

#### 基本用法

```bash
# 自动检测并压缩文件
tokensqueeze input.txt

# 使用特定策略
tokensqueeze input.py -s code

# 管道输入
echo "Your text here" | tokensqueeze

# 保存到文件
tokensqueeze input.txt -o output.txt

# 调整压缩比例（保留30%）
tokensqueeze input.txt -r 0.3

# 静默模式（仅输出）
tokensqueeze input.txt -q

# 列出所有策略
tokensqueeze --list-strategies

# 交互式 TUI
tokensqueeze-tui
```

### 详细使用指南

#### 压缩策略

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| `smart_truncate` | 保留开头和结尾，截断中间 | 长文档 |
| `code` | 移除注释和多余空白 | 源代码 |
| `json` | 移除空白字符压缩 JSON | JSON 数据 |
| `log` | 移除时间戳并去重 | 日志文件 |
| `markdown` | 简化格式但保留结构 | Markdown 文档 |
| `semantic` | 提取摘要保留关键句 | 文章、报告 |

#### 示例

**压缩 Python 代码：**
```bash
$ cat script.py | tokensqueeze -s code
# 移除注释和文档字符串，减少约50%的token
```

**压缩 JSON：**
```bash
$ echo '{"key": "value", "nested": {"a": 1}}' | tokensqueeze -s json
{"key":"value","nested":{"a":1}}
```

**压缩日志：**
```bash
$ cat app.log | tokensqueeze -s log
# 移除时间戳，去重相似条目
```

### 设计思路

TokenSqueeze 遵循 Unix 哲学：把一件事做好。它专注于 LLM 输入的文本压缩，提供：

- **简洁性**：无需复杂配置，开箱即用
- **高效性**：最小开销，最大压缩
- **透明性**：清晰的 token 节省统计
- **可扩展性**：易于添加新的压缩策略

#### 后续迭代计划

- [ ] 增加更多压缩策略（XML、YAML、CSV）
- [ ] 支持自定义压缩插件
- [ ] 多文件批处理
- [ ] 与主流 LLM 框架集成
- [ ] Web UI 浏览器压缩界面

### 打包与部署

```bash
# 构建分发包
make build

# 运行测试
make test

# 覆盖率测试
make test-cov

# 清理构建产物
make clean
```

### 贡献指南

欢迎贡献！请遵循以下规范：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

请确保：
- 代码遵循 PEP 8 风格指南
- 所有测试通过 (`make test`)
- 新功能包含测试
- 提交信息遵循 conventional commits 规范

### 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 項目介紹

**TokenSqueeze-CLI** 是一款輕量級、零依賴的命令列工具，專為在向大型語言模型（LLM）發送文本前進行智能壓縮而設計。透過在保留語義的同時減少 **50-90%** 的 token 使用量，TokenSqueeze 幫助您節省 API 成本並保持在上下文視窗限制內。

**靈感來源**：本項目源於對優化 LLM token 使用量的日益增長的需求。隨著 AI 模型變得越來越強大，上下文視窗不斷擴大，但 token 成本仍然是一個重要問題。TokenSqueeze 為每一個 token 的最大化價值提供了優雅的解決方案。

**差異化亮點**：與其他壓縮工具不同，TokenSqueeze 完全零依賴，支持多種內容特定的壓縮策略，並提供 CLI 和 TUI 兩種界面，靈活性極高。

### 核心特性

- **零依賴** - 純 Python 標準庫實現，無需任何外部包
- **多策略壓縮** - 內置6種策略：智能截斷、代碼、JSON、日誌、Markdown、語義
- **自動檢測** - 根據內容類型自動選擇最佳壓縮策略
- **Token 計數** - 內置 token 估算，無需 tiktoken
- **TUI 界面** - 交互式終端界面，便於探索
- **管道支持** - 完整的 Unix 管道兼容性，無縫集成
- **壓縮統計** - 實時顯示 token 節省量和壓縮率
- **跨平台** - 支持 Linux、macOS 和 Windows

### 快速開始

#### 環境要求
- Python 3.7+
- 零外部依賴！

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/TokenSqueeze-CLI.git
cd TokenSqueeze-CLI

# 開發模式安裝
pip install -e .

# 或直接安裝
python setup.py install
```

#### 基本用法

```bash
# 自動檢測並壓縮文件
tokensqueeze input.txt

# 使用特定策略
tokensqueeze input.py -s code

# 管道輸入
echo "Your text here" | tokensqueeze

# 保存到文件
tokensqueeze input.txt -o output.txt

# 調整壓縮比例（保留30%）
tokensqueeze input.txt -r 0.3

# 靜默模式（僅輸出）
tokensqueeze input.txt -q

# 列出所有策略
tokensqueeze --list-strategies

# 交互式 TUI
tokensqueeze-tui
```

### 詳細使用指南

#### 壓縮策略

| 策略 | 描述 | 適用場景 |
|------|------|----------|
| `smart_truncate` | 保留開頭和結尾，截斷中間 | 長文檔 |
| `code` | 移除註釋和多餘空白 | 源代碼 |
| `json` | 移除空白字符壓縮 JSON | JSON 資料 |
| `log` | 移除時間戳並去重 | 日誌文件 |
| `markdown` | 簡化格式但保留結構 | Markdown 文檔 |
| `semantic` | 提取摘要保留關鍵句 | 文章、報告 |

#### 示例

**壓縮 Python 代碼：**
```bash
$ cat script.py | tokensqueeze -s code
# 移除註釋和文檔字符串，減少約50%的token
```

**壓縮 JSON：**
```bash
$ echo '{"key": "value", "nested": {"a": 1}}' | tokensqueeze -s json
{"key":"value","nested":{"a":1}}
```

**壓縮日誌：**
```bash
$ cat app.log | tokensqueeze -s log
# 移除時間戳，去重相似條目
```

### 設計思路

TokenSqueeze 遵循 Unix 哲學：把一件事做好。它專注於 LLM 輸入的文本壓縮，提供：

- **簡潔性**：無需複雜配置，開箱即用
- **高效性**：最小開銷，最大壓縮
- **透明性**：清晰的 token 節省統計
- **可擴展性**：易於添加新的壓縮策略

#### 後續迭代計劃

- [ ] 增加更多壓縮策略（XML、YAML、CSV）
- [ ] 支持自定義壓縮外掛
- [ ] 多文件批處理
- [ ] 與主流 LLM 框架集成
- [ ] Web UI 瀏覽器壓縮界面

### 打包與部署

```bash
# 構建分發包
make build

# 運行測試
make test

# 覆蓋率測試
make test-cov

# 清理構建產物
make clean
```

### 貢獻指南

歡迎貢獻！請遵循以下規範：

1. Fork 本倉庫
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 發起 Pull Request

請確保：
- 代碼遵循 PEP 8 風格指南
- 所有測試通過 (`make test`)
- 新功能包含測試
- 提交信息遵循 conventional commits 規範

### 開源協議

本項目採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 文件。
