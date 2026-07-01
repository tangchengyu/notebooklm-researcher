# NotebookLM Researcher / NotebookLM 深度研究

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于深度研究的技能，帮助用户在 5 大通用平台搜索有价值的信息源；遇到学术、科研选题时，还会检索高相关、前沿与奠基性论文；遇到软件开发、框架工具等技术性选题时，通过 Context7 查询最新官方文档，自动汇入 [NotebookLM](https://notebooklm.google/) 项目，并生成报告、信息图表、思维导图和学习路径指导文档，最后将所有产出保存到本地 Obsidian Vault。

A deep-research skill that searches five general-purpose platforms for high-quality sources. For academic or scientific topics, it also identifies highly relevant, frontier, and foundational papers; for technical topics (frameworks, libraries, dev tools), it queries Context7 for up-to-date official documentation. It imports the selected sources into NotebookLM, generates a briefing report, infographic, mind map, and learning path guide, then saves everything to your local Obsidian Vault.

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
| SubBatch - B站字幕批量下载工具 | latest | B站视频无字幕或 opencli 无法提取时的字幕生成/导出兜底（可选） | Chrome 扩展商店安装 |
| 社媒助手 | latest | 小红书被登录墙或 opencli 无法稳定提取时，导出笔记、搜索结果和评论数据（可选） | Chrome 扩展商店安装 |

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

0. 🔐 先检查 NotebookLM CLI 和目标平台登录状态；如果登录过期，停止并提醒登录
1. ✅ 确认选题和搜索范围（可自定义搜索平台）
2. 📂 在 Obsidian Vault 中创建选题文件夹
3. 🔍 在 5 大通用平台搜索高质量信息源（B站、YouTube、知乎、小红书、GitHub）；学术类选题额外检索高相关、前沿与奠基性论文；技术类选题查询 Context7 官方文档
4. 📥 创建 NotebookLM 项目并导入信息源
5. 🤖 生成 4 种产物（简报、信息图表、思维导图、学习路径）
6. 💾 下载所有产物到 Obsidian 文件夹
7. 📊 展示最终汇总

### 登录状态预检 / Login Preflight

NotebookLM 网页登录和 `notebooklm` CLI 登录不是完全等价的。即使你能打开 <https://notebooklm.google.com/?pli=1>，CLI 本地 profile 也可能已经过期。因此本技能在开始调研前必须先运行：

```bash
notebooklm list --json
```

如果返回 notebook 列表或 `count` 字段，才继续调研。如果返回 `Authentication expired or invalid`、跳转到 `accounts.google.com`、超时或任何认证错误，技能会停止，不会开始搜索或创建项目。此时先运行：

```bash
notebooklm login
notebooklm list --json
```

For NotebookLM, browser login and CLI login are not always the same session. Even if <https://notebooklm.google.com/?pli=1> opens normally, the local CLI profile may still be expired. This skill must run `notebooklm list --json` before research starts. If authentication fails, it stops and asks you to run `notebooklm login`, then verifies again with `notebooklm list --json`.

对小红书等平台，也需要在采集前检查登录状态：

```bash
opencli rednote whoami -f json --site-session persistent --window background
```

如果返回 `AUTH_REQUIRED` 或 anonymous，先登录小红书；如果必须使用该平台，技能会等待登录，不会直接跳过或开始调研。

### 学术论文检索 / Academic Paper Research

对于学术、科研选题，本技能会把论文作为独立证据通道，并分别覆盖：

- **高相关论文**：直接回答研究问题的综述、元分析和代表性研究
- **前沿论文**：最近 3 年的工作，并重点检查最近 12 个月的预印本与新发表成果
- **奠基性论文**：通过综述、共同引用和领域术语来源追溯的早期关键工作

主要检索和核验来源包括 arXiv、Crossref、OpenAlex、Semantic Scholar、PubMed/PMC、CORE、Unpaywall、出版社页面、作者主页和机构仓储。技能会记录 DOI、arXiv ID、版本、发表状态、同行评审状态、主要贡献和局限，并区分正式论文、预印本及“仅摘要”来源。



### Context7 技术文档查询 / Technical Documentation via Context7

对于软件开发、框架工具等技术性选题，本技能通过 [Context7](https://context7.com) 查询相关技术的官方文档，获取最新的 API 签名、用法示例和版本变更记录，作为独立信息源汇入 NotebookLM。

用法：

```bash
# 解析库 ID
ctx7 library "<库名>" "<查询上下文>"

# 获取文档
ctx7 docs <libraryId> "<具体问题>"
```

For software development, framework, and tooling topics, the skill queries official documentation via [Context7](https://context7.com) to obtain the latest API signatures, usage examples, and changelog entries as a separate source stream into NotebookLM.

Usage:

```bash
# Resolve library ID
ctx7 library "<library-name>" "<query-context>"

# Fetch docs
ctx7 docs <libraryId> "<specific-question>"
```
本技能不使用 Sci-Hub 或其他绕过付费墙、版权或访问控制的服务。遇到受限论文时，会优先寻找 arXiv、PubMed Central、机构仓储、作者主页或 Unpaywall 提供的合法开放版本；找不到全文时，仅使用合法获得的摘要与元数据，并明确标注。

For academic or scientific topics, the skill treats papers as a separate evidence stream and covers three categories:

- **Highly relevant papers:** reviews, meta-analyses, and representative studies that directly address the question
- **Frontier papers:** work from the last three years, with an additional check of preprints and publications from the last 12 months
- **Foundational papers:** early key work traced through reviews, co-citation patterns, and the origins of established terminology

Primary discovery and verification sources include arXiv, Crossref, OpenAlex, Semantic Scholar, PubMed/PMC, CORE, Unpaywall, publisher pages, author pages, and institutional repositories. The workflow records stable identifiers, versions, publication and peer-review status, contribution, and limitations, while distinguishing published papers, preprints, and abstract-only records.

The skill does not use Sci-Hub or other services that bypass paywalls, copyright, or access controls. For restricted papers, it searches for lawful open versions through arXiv, PubMed Central, institutional repositories, author pages, or Unpaywall. If no full text is legally available, it uses only accessible metadata and abstracts and labels that limitation explicitly.

### B站字幕来源 / Bilibili Subtitle Sources

对 B站入选视频，技能优先用 `opencli bilibili video/subtitle/summary` 获取元数据、字幕和官方 AI 总结。不要只把 B站 URL 作为唯一来源；更稳的做法是把字幕、总结和元数据整理成 Markdown，再作为 NotebookLM 文本或文件来源导入。

如果 `opencli bilibili subtitle` 和 `opencli bilibili summary` 都返回空结果，可以用 SubBatch Chrome 扩展作为兜底：打开对应 B站视频或列表，在 SubBatch 侧边栏中生成/获取字幕，导出格式选择 `MD`，将 `.md` 文件保存到选题文件夹的 `sources/bilibili/` 下，再通过 `notebooklm source add "<path>.md" --type file` 导入。若文件导入受限，则读取 Markdown 内容后用 `--type text --title "<视频标题>"` 导入。

For selected Bilibili videos, the skill first tries `opencli bilibili video/subtitle/summary` to collect metadata, subtitles, and the official AI summary. Do not rely on the Bilibili URL alone; the more reliable path is to turn subtitles, summaries, and metadata into Markdown and import that into NotebookLM as a text or file source.

If both `opencli bilibili subtitle` and `opencli bilibili summary` return empty results, use the SubBatch Chrome extension as a fallback. Open the target Bilibili video or list, generate or fetch subtitles from the SubBatch side panel, export `MD`, save the `.md` file under `sources/bilibili/` in the topic folder, then import it with `notebooklm source add "<path>.md" --type file`. If file import is blocked, read the Markdown content and add it with `--type text --title "<video title>"`.

### 小红书来源 / Rednote Sources

对小红书入选笔记，技能优先用 `opencli rednote search/note/comments` 获取搜索结果、笔记正文和评论。如果 opencli 被登录墙拦截或无法稳定提取，可以用社媒助手 Chrome 扩展作为兜底：在 Chrome 中登录小红书并搜索关键词，使用社媒助手导出搜索结果、笔记数据和评论数据。

推荐筛选方式：每个关键词保留 2-3 条点赞数、收藏数和主题相关性最高的笔记；每条笔记保留 2-3 条点赞数最高且有实质信息量的评论。将导出的 Excel/CSV/JSON 整理成 Markdown，保存到 `sources/rednote/`，再通过 `notebooklm source add "<path>.md" --type file` 导入。若文件导入受限，则读取 Markdown 内容后用 `--type text --title "<Rednote title>"` 导入。

For selected Rednote/Xiaohongshu notes, the skill first tries `opencli rednote search/note/comments` to collect search results, note body, and comments. If opencli is blocked by the login wall or cannot extract reliably, use the Social Media Copilot browser extension as a fallback: log into Xiaohongshu in Chrome, search the target keywords, and export search results, note data, and comments.

Recommended filtering: keep 2-3 notes per keyword with the strongest combination of likes, saves, and topic relevance; for each note, keep 2-3 high-like comments that add real substance. Convert the exported Excel/CSV/JSON into Markdown, save it under `sources/rednote/`, then import it with `notebooklm source add "<path>.md" --type file`. If file import is blocked, read the Markdown content and add it with `--type text --title "<Rednote title>"`.

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
- [Context7](https://context7.com) — 最新技术文档查询服务
