<p align="center">
  <a href="#简体中文">简体中文</a> ·
  <a href="#繁體中文">繁體中文</a> ·
  <a href="#english">English</a>
</p>

---

<a id="简体中文"></a>
# 🔢 BaseForge · 零依赖 Base 编码工具箱

> 纯 Python 标准库实现的 Base 编码工具箱 —— **Base16 / Base32 / Base58 / Base62 / Base64 / Base85** 编码解码，外加密码学随机**短 ID 生成** —— **零依赖 · 离线优先 · 可测试**。

## 🎉 项目介绍

**BaseForge** 是一个面向开发者与后端工程师的轻量级编码工具库。它把常见的进制编码收敛到一个统一、可测、零依赖的接口里，并补齐了标准库缺失的 **Base58 / Base62** 与实用的 **短 ID 生成器**。

- **核心价值**：在任意 Python 脚本、短链系统、主键生成、令牌场景中，**无需引入重型依赖**即可完成 Base 体系编解码。
- **解决的痛点**：标准库没有 Base58 / Base62；自研易出错；短 ID 生成常依赖第三方；多算法散落各处难以统一。
- **自研差异化亮点**：Base58 / Base62 **从零实现**（大整数运算、前导零保真）；标准库仅作 Base16/32/64/85 的安全封装；`shortid()` 基于 `secrets` 密码学随机；统一的 `encode/decode(algo)` 接口与 CLI。
- **灵感来源**：Bitcoin Base58、URL-safe 短 ID、各类 Base 编码规范，结合"零依赖单仓可落地"的工程目标自研实现。

## ✨ 核心特性

- 🔡 **六算法支持**：Base16、Base32(RFC4648)、Base58(Bitcoin)、Base62、Base64(RFC4648)、Base85(RFC1924)。
- 🛠️ **自研 Base58 / Base62**：从零实现，正确处理**前导零字节**（`\x00` → `1` / `0`），与标准向量一致。
- 🆔 **短 ID 生成**：`shortid()` 基于 `secrets` 密码学随机，适合短链、主键代理、令牌（非安全密钥）。
- 🔌 **统一接口**：`encode(data, algo)` / `decode(text, algo)`，一处调用切换所有算法。
- 🖥️ **命令行 CLI**：`encode / decode / shortid / list` 四类子命令，零配置即用。
- 📦 **零依赖**：仅用 Python 3.8+ 标准库，**无第三方依赖**，可离线运行。
- 🧪 **测试完备**：含已知向量（Base64/32/58）与全算法随机往返测试。

## 🚀 快速开始

**环境要求**：Python **3.8 及以上**（仅标准库）。

**安装（可编辑模式）**：
```bash
git clone https://github.com/gitstq/BaseForge.git
cd BaseForge
python3 -m pip install -e .
```

**无需安装，直接运行**（仓库内）：
```bash
python3 -m baseforge encode --algo base58 --data "hello world"
```

**库用法最小示例**：
```python
from baseforge import encode, decode, shortid

# 编码
s = encode("hello world".encode(), "base58")   # -> 'StV1DL6CwTryKyV'
b = decode(s, "base58")                          # -> b'hello world'
# 短 ID
uid = shortid(12)                               # 例如 'aZ3kQ9xP2mB1'
```

## 📖 详细使用指南

### 库 API

```python
from baseforge import encode, decode, shortid, b58encode, b62encode, ALGOS

# 1) 统一编码/解码
encode(b"\x01\x02\xff", "base16")               # '0102FF'
decode("aGVsbG8=", "base64")                    # b'hello'
encode(b"hello", "base32")                      # 'NBSWY3DP'

# 2) 标准库缺失的算法（自研）
b58encode(b"hello world")                        # 'StV1DL6CwTryKyV'
b62encode(b"BaseForge")                          # 'NWxjrH4An0rt'

# 3) 短 ID（密码学随机）
shortid(16)                                     # 16 位 Base62 字符串

# 4) 支持的算法
print(ALGOS)                                    # ['base16','base32','base58','base62','base64','base85']
```

### 命令行 CLI

```bash
# 编码
python3 -m baseforge encode --algo base58 --data "hello world"
# 解码（可解码文本则输出原文，否则输出十六进制）
python3 -m baseforge decode --algo base58 --data "StV1DL6CwTryKyV"
# 生成随机短 ID
python3 -m baseforge shortid --len 16
# 列出算法
python3 -m baseforge list
```

> 📸 演示截图占位：建议补充 `encode` / `shortid` 子命令的终端录屏或动图，放在 `docs/` 下并在此处引用。

## 💡 设计思路与迭代规划

**设计理念**：把"进制编码"视为**纯函数变换**——同样的输入输出恒定，便于测试与嵌入；Base58/62 用大整数运算实现，前导零以填充字符保真。

**技术选型原因**：Base16/32/64/85 直接复用标准库（安全、经过审计），仅 Base58/62 需自研；`secrets` 提供密码学随机，避免 `random` 的可预测性。

**后续迭代计划**：
- 🔗 增加 **Base58Check**（带版本字节 + 双 SHA256 校验和），用于地址场景。
- 🔑 增加 **Base58/62 流式编解码**（大文件分块）。
- 🌐 补充 **Bech32**（BIP173）等现代编码。
- 🌏 补充日语、韩语、西班牙语文档。

**社区贡献方向**：欢迎提交新算法、已知测试向量、以及性能优化（如查表法）。

## 📦 打包与部署指南

BaseForge 属于**工具库类项目**，无需上传 GitHub Release 二进制；通过 PyPI / 源码即可集成。

- **打包（生成分发包）**：
  ```bash
  python3 -m pip install build
  python3 -m build            # 产出 dist/*.whl 与 dist/*.tar.gz
  ```
- **本地安装验证**：
  ```bash
  python3 -m pip install dist/*.whl
  baseforge list
  ```
- **兼容环境**：CPython 3.8–3.12；任何含标准库的平台（Linux / macOS / Windows）。
- **依赖**：无。`requirements.txt` 为空，仅标准库。

> ⚠️ **注意**：Base85 会去除尾部零字节（编码歧义），往返测试请使用无尾部零的数据。

## 🤝 贡献指南

- 提交遵循 [Conventional Commits](https://www.conventionalcommits.org/)：`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`。
- 新增算法须附带已知测试向量；保持零依赖（仅标准库）。
- 提交 Issue 请提供算法类型、输入、期望/实际输出、Python 版本。
- 详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📄 开源协议说明

本项目基于 **MIT License** 开源。可自由用于商业与非商业场景，请保留版权声明。详见 [LICENSE](./LICENSE)。

---

<a id="繁體中文"></a>
# 🔢 BaseForge · 零依賴 Base 編碼工具箱

> 純 Python 標準函式庫實作的 Base 編碼工具箱 —— **Base16 / Base32 / Base58 / Base62 / Base64 / Base85** 編碼解碼，外加密碼學隨機**短 ID 生成** —— **零依賴 · 離線優先 · 可測試**。

## 🎉 專案介紹

**BaseForge** 是一個面向開發者與後端工程師的輕量級編碼工具庫。它把常見的進位編碼收斂到一個統一、可測、零依賴的介面裡，並補齊了標準函式庫缺失的 **Base58 / Base62** 與實用的 **短 ID 生成器**。

- **核心價值**：在任意 Python 腳本、短鏈系統、主鍵生成、令牌場景中，**無須引入重型依賴**即可完成 Base 體系編解碼。
- **解決的痛點**：標準函式庫沒有 Base58 / Base62；自研易出錯；短 ID 生成常依賴第三方；多演算法散落各處難以統一。
- **自研差異化亮點**：Base58 / Base62 **從零實作**（大整數運算、前導零保真）；標準函式庫僅作 Base16/32/64/85 的安全封裝；`shortid()` 基於 `secrets` 密碼學隨機；統一的 `encode/decode(algo)` 介面與 CLI。
- **靈感來源**：Bitcoin Base58、URL-safe 短 ID、各類 Base 編碼規範，結合「零依賴單倉可落地」的工程目標自研實作。

## ✨ 核心特性

- 🔡 **六演算法支援**：Base16、Base32(RFC4648)、Base58(Bitcoin)、Base62、Base64(RFC4648)、Base85(RFC1924)。
- 🛠️ **自研 Base58 / Base62**：從零實作，正確處理**前導零位元組**（`\x00` → `1` / `0`），與標準向量一致。
- 🆔 **短 ID 生成**：`shortid()` 基於 `secrets` 密碼學隨機，適合短鏈、主鍵代理、令牌（非安全密鑰）。
- 🔌 **統一介面**：`encode(data, algo)` / `decode(text, algo)`，一處呼叫切換所有演算法。
- 🖥️ **命令列 CLI**：`encode / decode / shortid / list` 四類子指令，零設定即用。
- 📦 **零依賴**：僅用 Python 3.8+ 標準函式庫，**無第三方依賴**，可離線運行。
- 🧪 **測試完備**：含已知向量（Base64/32/58）與全演算法隨機往返測試。

## 🚀 快速開始

**環境要求**：Python **3.8 及以上**（僅標準函式庫）。

**安裝（可編輯模式）**：
```bash
git clone https://github.com/gitstq/BaseForge.git
cd BaseForge
python3 -m pip install -e .
```

**無須安裝，直接執行**（倉庫內）：
```bash
python3 -m baseforge encode --algo base58 --data "hello world"
```

**函式庫用法最小範例**：
```python
from baseforge import encode, decode, shortid

s = encode("hello world".encode(), "base58")   # -> 'StV1DL6CwTryKyV'
b = decode(s, "base58")                          # -> b'hello world'
uid = shortid(12)                               # 例如 'aZ3kQ9xP2mB1'
```

## 📖 詳細使用指南

### 函式庫 API

```python
from baseforge import encode, decode, shortid, b58encode, b62encode, ALGOS

encode(b"\x01\x02\xff", "base16")               # '0102FF'
decode("aGVsbG8=", "base64")                    # b'hello'
encode(b"hello", "base32")                      # 'NBSWY3DP'
b58encode(b"hello world")                        # 'StV1DL6CwTryKyV'
b62encode(b"BaseForge")                          # 'NWxjrH4An0rt'
shortid(16)                                     # 16 位 Base62 字串
print(ALGOS)
```

### 命令列 CLI

```bash
python3 -m baseforge encode --algo base58 --data "hello world"
python3 -m baseforge decode --algo base58 --data "StV1DL6CwTryKyV"
python3 -m baseforge shortid --len 16
python3 -m baseforge list
```

> 📸 示範截圖佔位：建議補充 `encode` / `shortid` 子指令的終端錄製或動圖，放在 `docs/` 下並於此處引用。

## 💡 設計思路與迭代規劃

**設計理念**：把「進位編碼」視為**純函式變換**——同樣的輸入輸出恆定，便於測試與嵌入；Base58/62 用大整數運算實作，前導零以填充字元保真。

**技術選型原因**：Base16/32/64/85 直接複用標準函式庫（安全、經過審計），僅 Base58/62 需自研；`secrets` 提供密碼學隨機，避免 `random` 的可預測性。

**後續迭代計畫**：
- 🔗 增加 **Base58Check**（帶版本位元組 + 雙 SHA256 校驗和），用於地址場景。
- 🔑 增加 **Base58/62 串流編解碼**（大檔案分塊）。
- 🌐 補充 **Bech32**（BIP173）等現代編碼。
- 🌏 補充日語、韓語、西班牙語文件。

**社群貢獻方向**：歡迎提交新演算法、已知測試向量、以及效能最佳化（如查表法）。

## 📦 打包與部署指南

BaseForge 屬於**工具庫類專案**，無須上傳 GitHub Release 二進位；透過 PyPI / 原始碼即可整合。

- **打包（產生分發包）**：
  ```bash
  python3 -m pip install build
  python3 -m build
  ```
- **本機安裝驗證**：
  ```bash
  python3 -m pip install dist/*.whl
  baseforge list
  ```
- **相容環境**：CPython 3.8–3.12；任何含標準函式庫的平台（Linux / macOS / Windows）。
- **依賴**：無。`requirements.txt` 為空，僅標準函式庫。

> ⚠️ **注意**：Base85 會去除尾部零位元組（編碼歧義），往返測試請使用無尾部零的資料。

## 🤝 貢獻指南

- 提交遵循 [Conventional Commits](https://www.conventionalcommits.org/)：`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`。
- 新增演算法須附帶已知測試向量；保持零依賴（僅標準函式庫）。
- 提交 Issue 請提供演算法類型、輸入、期望/實際輸出、Python 版本。
- 詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📄 開源協議說明

本專案基於 **MIT License** 開源。可自由用於商業與非商業場景，請保留版權聲明。詳見 [LICENSE](./LICENSE)。

---

<a id="english"></a>
# 🔢 BaseForge · Zero-Dependency Base Encoding Toolkit

> A pure-Python-standard-library base-encoding toolkit —— **Base16 / Base32 / Base58 / Base62 / Base64 / Base85** plus a cryptographically-random **short-id generator** —— **zero dependencies · offline-first · testable**.

## 🎉 Introduction

**BaseForge** is a lightweight encoding toolkit for developers and backend engineers. It consolidates common base encodings behind one unified, testable, zero-dependency interface, and fills the gap left by the standard library with **Base58 / Base62** plus a handy **short-id generator**.

- **Core value**: encode/decode across the Base family in any Python script, URL-shortener, primary-key or token scenario — **without pulling in a heavy dependency**.
- **Pain points solved**: the stdlib lacks Base58 / Base62; hand-rolling them is error-prone; short-id generation usually needs a third-party lib; algorithms are scattered.
- **Self-developed differentiators**: Base58 / Base62 **implemented from scratch** (big-integer math, faithful leading-zero handling); stdlib only wraps Base16/32/64/85 safely; `shortid()` uses `secrets` for cryptographic randomness; unified `encode/decode(algo)` API and CLI.
- **Inspiration**: Bitcoin Base58, URL-safe short ids, and the various Base encoding specs — reimplemented in-house for a zero-dependency, single-repo deliverable.

## ✨ Core Features

- 🔡 **Six algorithms**: Base16, Base32 (RFC4648), Base58 (Bitcoin), Base62, Base64 (RFC4648), Base85 (RFC1924).
- 🛠️ **From-scratch Base58 / Base62**: correct **leading-zero byte** handling (`\x00` → `1` / `0`), matching reference vectors.
- 🆔 **Short-id generation**: `shortid()` uses `secrets` (cryptographically random) — great for short links, primary-key surrogates, tokens (not security secrets).
- 🔌 **Unified API**: `encode(data, algo)` / `decode(text, algo)` switch every algorithm from one call.
- 🖥️ **CLI**: `encode / decode / shortid / list` subcommands, zero-config.
- 📦 **Zero dependencies**: Python 3.8+ standard library only — **no third-party deps**, runs fully offline.
- 🧪 **Well tested**: known vectors (Base64/32/58) plus randomized round-trip tests across all algorithms.

## 🚀 Quick Start

**Requirements**: Python **3.8+** (standard library only; nothing to `pip install`).

**Install (editable)**:
```bash
git clone https://github.com/gitstq/BaseForge.git
cd BaseForge
python3 -m pip install -e .
```

**Run directly (in-repo, no install)**:
```bash
python3 -m baseforge encode --algo base58 --data "hello world"
```

**Minimal library example**:
```python
from baseforge import encode, decode, shortid

s = encode("hello world".encode(), "base58")   # -> 'StV1DL6CwTryKyV'
b = decode(s, "base58")                          # -> b'hello world'
uid = shortid(12)                               # e.g. 'aZ3kQ9xP2mB1'
```

## 📖 Detailed Guide

### Library API

```python
from baseforge import encode, decode, shortid, b58encode, b62encode, ALGOS

encode(b"\x01\x02\xff", "base16")               # '0102FF'
decode("aGVsbG8=", "base64")                    # b'hello'
encode(b"hello", "base32")                      # 'NBSWY3DP'
b58encode(b"hello world")                        # 'StV1DL6CwTryKyV'
b62encode(b"BaseForge")                          # 'NWxjrH4An0rt'
shortid(16)                                     # 16-char Base62 string
print(ALGOS)
```

### Command-Line CLI

```bash
python3 -m baseforge encode --algo base58 --data "hello world"
python3 -m baseforge decode --algo base58 --data "StV1DL6CwTryKyV"
python3 -m baseforge shortid --len 16
python3 -m baseforge list
```

> 📸 Demo screenshot placeholder: consider adding a terminal recording / GIF of the `encode` / `shortid` subcommands under `docs/` and referencing it here.

## 💡 Design & Roadmap

**Design philosophy**: treat base encoding as a **pure function** — same input yields same output, trivial to test and embed; Base58/62 use big-integer math with padding characters preserving leading zeros.

**Why stdlib only**: Base16/32/64/85 reuse the audited standard library; only Base58/62 need custom code; `secrets` gives cryptographic randomness, avoiding `random`'s predictability.

**Roadmap**:
- 🔗 **Base58Check** (version byte + double SHA256 checksum) for address scenarios.
- 🔑 Streaming Base58/62 codec for large files.
- 🌐 **Bech32** (BIP173) and other modern encodings.
- 🌏 Japanese, Korean and Spanish documentation.

**Community direction**: new algorithms, known test vectors, and performance optimizations (e.g. lookup tables) are all welcome.

## 📦 Packaging & Deployment

BaseForge is a **tool/library project** — no GitHub Release binaries required; integrate via PyPI or source.

- **Build distributions**:
  ```bash
  python3 -m pip install build
  python3 -m build            # produces dist/*.whl and dist/*.tar.gz
  ```
- **Local install verification**:
  ```bash
  python3 -m pip install dist/*.whl
  baseforge list
  ```
- **Compatible environments**: CPython 3.8–3.12; any platform with the standard library (Linux / macOS / Windows).
- **Dependencies**: none. `requirements.txt` is empty (stdlib only).

> ⚠️ **Note**: Base85 strips trailing zero bytes (encoding ambiguity) — use non-trailing-zero data for round-trip tests.

## 🤝 Contributing

- Follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`.
- New algorithms must ship known test vectors; keep zero third-party dependencies (stdlib only).
- When filing an Issue, include the algorithm, input, expected/actual output, and Python version.
- See [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📄 License

Released under the **MIT License** — free for commercial and non-commercial use; please retain the copyright notice. See [LICENSE](./LICENSE).
