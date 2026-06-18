# NotebookLM Researcher / NotebookLM 深度研究

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于深度研究的技能，帮助用户在 5 大通用平台搜索有价值的信息源；遇到学术、科研或专业技术选题时，还会检索高相关、前沿与奠基性论文，自动汇入 [NotebookLM](https://notebooklm.google/) 项目，并生成报告、信息图表、思维导图和学习路径指导文档，最后将所有产出保存到本地 Obsidian Vault。

A deep-research skill that searches five general-purpose platforms for high-quality sources. For academic, scientific, or technical topics, it also identifies highly relevant, frontier, and foundational papers. It imports the selected sources into NotebookLM, generates a briefing report, infographic, mind map, and learning path guide, then saves everything to your local Obsidian Vault.

---

## 📸 效果预览 / Preview

完成一次研究后，你将获得：

- 📄 **简报 (Briefing Report)** — Markdown 格式，含所有信息源概述、核心观点和链接
- 🖼️ **信息图表 (Infographic)** — PNG 格式，可视化呈现选题核心概念
- 🧠 **思维导图 (Mind Map)** — JSON 格式，结构化展示知识体系
- 📚 **学习路径 (Learning Path)** — Markdown 格式，从入门到精通的递进学习指南

所有文件自动保存到 Obsidian Vault 的选题文件夹中，可直接在 Obsidian 中查看和编辑。

---

## 🔧 前置依赖 / Prerequisites

使用本技能前，请确保安装了以下工具：

| 工具 | 版本要求 | 用途 | 安装方式 |
|------|---------|------|---------|
| [opencli](https://github.com/nicepkg/opencli) | v1.8+ | 跨平台搜索（B站、YouTube、知乎、小红书） | `npm i -g opencli` |
| [notebooklm](https://github.com/nicepkg/notebooklm-cli) | v0.7+ | NotebookLM 完整操作 | `npm i -g notebooklm-cli` |
| [GitHub CLI (`gh`)](https://cli.github.com/) | latest | GitHub 仓库搜索（可选） | `winget install GitHub.cli` |
| [Obsidian](https://obsidian.md/) | latest | 知识库管理 | 官网下载 |

### 配置 opencli 浏览器

opencli 首次运行需要浏览器支持：

```bash
opencli doctor
```

根据提示完成浏览器配置（推荐 Chrome/Chromium）。

### 配置 GitHub CLI（可选）

如果需要在 GitHub 上搜索仓库：

```bash
gh auth login
```

如果不配置，GitHub 平台将被自动跳过，不影响其他平台的搜索。

---

## 📦 安装 / Installation

### 方法一：通过技能管理器安装（推荐）

在支持技能发现的环境中运行：

```
/find-skills notebooklm
```

选择 **notebooklm-research** 技能安装即可。

### 方法二：手动安装

1. 克隆本仓库：

```bash
git clone https://github.com/tangchengyu/notebooklm-researcher.git
```

2. 将 `SKILL.md` 复制到本地 skills 目录：

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills\notebooklm-research"
Copy-Item .\SKILL.md "$env:USERPROFILE\.codex\skills\notebooklm-research\SKILL.md"
```

**macOS / Linux:**
```bash
mkdir -p ~/.codex/skills/notebooklm-research
cp SKILL.md ~/.codex/skills/notebooklm-research/SKILL.md
```

3. 重启技能宿主，或在新对话中使用。

---

## 🚀 使用方式 / Usage

在支持该技能的对话中，使用以下任一方式触发：

### 中文（推荐）

```
研究一下 [选题名称]
帮我调研 [选题名称]
做一个关于 [选题名称] 的深度调研
用 NotebookLM 分析 [选题名称]
帮我收集 [选题名称] 的资料
```

### 英文

```
Research [topic] for me
Do a deep dive on [topic]
Collect multi-platform sources about [topic] for NotebookLM
```

### 示例 / Example

```
帮我调研一下 AI Agent 框架的最新进展
```

技能将按以下步骤执行：

1. ✅ 确认选题和搜索范围（可自定义搜索平台）
2. 📂 在 Obsidian Vault 中创建选题文件夹
3. 🔍 在 5 大通用平台搜索高质量信息源（B站、YouTube、知乎、小红书、GitHub）；学术类选题额外检索高相关、前沿与奠基性论文
4. 📥 创建 NotebookLM 项目并导入信息源
5. 🤖 生成 4 种产物（简报、信息图表、思维导图、学习路径）
6. 💾 下载所有产物到 Obsidian 文件夹
7. 📊 展示最终汇总

### 学术论文检索 / Academic Paper Research

对于学术、科研或专业技术选题，本技能会把论文作为独立证据通道，并分别覆盖：

- **高相关论文**：直接回答研究问题的综述、元分析和代表性研究
- **前沿论文**：最近 3 年的工作，并重点检查最近 12 个月的预印本与新发表成果
- **奠基性论文**：通过综述、共同引用和领域术语来源追溯的早期关键工作

主要检索和核验来源包括 arXiv、Crossref、OpenAlex、Semantic Scholar、PubMed/PMC、CORE、Unpaywall、出版社页面、作者主页和机构仓储。技能会记录 DOI、arXiv ID、版本、发表状态、同行评审状态、主要贡献和局限，并区分正式论文、预印本及“仅摘要”来源。

本技能不使用 Sci-Hub 或其他绕过付费墙、版权或访问控制的服务。遇到受限论文时，会优先寻找 arXiv、PubMed Central、机构仓储、作者主页或 Unpaywall 提供的合法开放版本；找不到全文时，仅使用合法获得的摘要与元数据，并明确标注。

For academic, scientific, or technical topics, the skill treats papers as a separate evidence stream and covers three categories:

- **Highly relevant papers:** reviews, meta-analyses, and representative studies that directly address the question
- **Frontier papers:** work from the last three years, with an additional check of preprints and publications from the last 12 months
- **Foundational papers:** early key work traced through reviews, co-citation patterns, and the origins of established terminology

Primary discovery and verification sources include arXiv, Crossref, OpenAlex, Semantic Scholar, PubMed/PMC, CORE, Unpaywall, publisher pages, author pages, and institutional repositories. The workflow records stable identifiers, versions, publication and peer-review status, contribution, and limitations, while distinguishing published papers, preprints, and abstract-only records.

The skill does not use Sci-Hub or other services that bypass paywalls, copyright, or access controls. For restricted papers, it searches for lawful open versions through arXiv, PubMed Central, institutional repositories, author pages, or Unpaywall. If no full text is legally available, it uses only accessible metadata and abstracts and labels that limitation explicitly.

### 自定义搜索平台

你也可以指定只在部分平台搜索：

```
帮我在 B站 和 知乎 搜索一下 [选题名称]
研究一下 [选题名称]，只看 YouTube 和小红书
```

---

## 📂 产出文件结构 / Output Structure

```
Obsidian Vault/
└── [选题名称]/
    ├── report-*.md              # 简报（Markdown）
    ├── infographic-*.png        # 信息图表（PNG）
    ├── mind-map-*.json          # 思维导图（JSON）
    └── 学习路径-*.md             # 学习路径指导文档（Markdown）
```

---

## ⚙️ 自定义配置 / Customization

### 修改默认搜索平台

编辑 `SKILL.md`，找到「第一步：确认选题和搜索范围」，修改默认平台列表。

### 修改 NotebookLM 产物类型

编辑 `SKILL.md` 中的「第五步：生成 NotebookMLM 产物」，添加或删除产物生成命令。

### 修改 Obsidian Vault 路径

编辑 `SKILL.md`，将所有 `G:\obsidian_vault\Obsidian Vault\` 替换为你的 Vault 路径。

> **建议**：安装后根据你的系统环境调整路径和默认平台配置。

---

## ❓ 常见问题 / FAQ

### 某个平台搜索无结果？

这是正常的——说明该平台没有与你选题相关的高质量内容。技能会跳过该平台并在汇总中说明。

### NotebookLM 生成超时怎么办？

默认超时为 600 秒（10 分钟）。如果信息源较多，可以在 `SKILL.md` 中将 `--timeout` 改为更大的值（如 1200）。

### GitHub 搜索报错？

运行 `gh auth login` 登录 GitHub 账号。如果不想登录，技能会自动跳过 GitHub 平台。

### opencli 浏览器报错？

运行 `opencli doctor` 诊断问题。通常是因为浏览器未正确配置或版本不兼容。

### 产物下载后文件名混乱？

使用 `notebooklm artifact list -n <notebook_id>` 查看所有产物 ID，再用 `--artifact` 参数精确下载指定产物。

---

## 🐛 反馈与贡献 / Feedback & Contributing

- 发现 Bug 或有新功能建议？欢迎提交 [Issue](https://github.com/tangchengyu/notebooklm-researcher/issues)
- 想贡献代码？欢迎提交 Pull Request
- 有使用问题？在 [Discussions](https://github.com/tangchengyu/notebooklm-researcher/discussions) 中提问

---

## 📄 许可证 / License

MIT © [tangchengyu](https://github.com/tangchengyu)

---

## 🙏 致谢 / Acknowledgements

- [NotebookLM](https://notebooklm.google/) — Google 出品的 AI 研究助手
- [opencli](https://github.com/nicepkg/opencli) — 跨平台搜索 CLI 工具
- [notebooklm-cli](https://github.com/nicepkg/notebooklm-cli) — NotebookLM 命令行工具
- [Obsidian](https://obsidian.md/) — 强大的知识库管理工具
