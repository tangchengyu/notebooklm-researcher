[简体中文](#简体中文) · [English](#english)

# NotebookLM Researcher

面向 NotebookLM 与 Obsidian 的多源研究技能。它先用 `last30days` 收集近 30 天的社区与网络信号，再依据每个来源的真实运行状态补采知乎、B站、小红书、官网、Context7 和学术来源，最终生成去重、结构化、可追溯的 Markdown 资料包，并把 NotebookLM 的四类成果保存到对应的 Obsidian 选题目录。

## 简体中文

### 核心能力

- 以 `last30days` 作为 Reddit、X、YouTube、Hacker News、Polymarket、GitHub、Web 等近期信号的主通道。
- 根据 `source_status` 决定是否补采，避免重复搜索已经成功的平台。
- 始终独立核验官网、官方文档、标准、法规和产品更新页。
- 保留知乎与 B站补充通道；小红书、YouTube、GitHub、arXiv 等按运行状态决定是否补采。
- 技术主题使用 Context7 获取版本化官方文档。
- 学术主题补充 Crossref、OpenAlex、Semantic Scholar、PubMed/PMC、CORE、Unpaywall 与合法开放全文。
- 按 DOI、arXiv ID、PMID、GitHub 仓库、视频/帖子 ID 和规范化 URL 去重。
- 输出适合 NotebookLM 导入的 Markdown，而不是直接导入 `last30days` 的调试或聊天格式。

### 工作流

1. 验证 NotebookLM CLI 登录状态和来源权限。
2. 运行 `last30days --preflight`，按需执行 `doctor`。
3. 为命名实体或复杂主题生成 query plan，以 agent JSON 作为机器交接格式。
4. 读取 `source_status`，仅补采缺失、降级或内容不完整的来源。
5. 使用 `normalize_last30days.py` 合并、去重并生成 Markdown 资料包。
6. 导入 NotebookLM，生成简报、信息图、交互式思维导图和学习路径。
7. 按 artifact ID 下载四类成果，并验证它们已非空保存到 Obsidian 对应选题目录。

### 依赖

| 工具 | 用途 | 安装 |
|---|---|---|
| `last30days` | 近期多源研究 | `npx skills add mvanhorn/last30days-skill -g -a codex` |
| `notebooklm` | NotebookLM 项目、来源和产物 | `npm i -g notebooklm-cli` |
| `opencli` | 知乎、B站、小红书等补充来源 | `npm i -g opencli` |
| `ctx7` | 版本化官方技术文档 | `npm i -g ctx7@latest` |
| `gh` | GitHub 定向深挖 | [GitHub CLI](https://cli.github.com/) |

`opencli`、Context7 和 GitHub 仅在研究主题需要时启用。未配置的可选来源会被记录为覆盖缺口，不会伪装为完整覆盖。

### 安装

克隆仓库后必须复制完整目录，包括 `references/`、`scripts/` 和 `evals/`；只复制 `SKILL.md` 会导致工作流不完整。

Windows PowerShell：

```powershell
git clone https://github.com/tangchengyu/notebooklm-researcher.git
$dest = Join-Path $env:USERPROFILE '.codex\skills\notebooklm-research'
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item '.\notebooklm-researcher\*' $dest -Recurse -Force
```

macOS / Linux：

```bash
git clone https://github.com/tangchengyu/notebooklm-researcher.git
mkdir -p ~/.codex/skills/notebooklm-research
rsync -a --exclude .git notebooklm-researcher/ ~/.codex/skills/notebooklm-research/
```

### 使用

自然语言触发即可，例如：

```text
调研最近 30 天 NotebookLM 工作流的变化和真实用户反馈，并整理进 NotebookLM。
研究 Next.js 新版缓存策略，同时核验官方 API 文档和 GitHub 实现。
收集知乎、B站和小红书上关于轻量露营装备的经验，覆盖不到的平台再补采。
```

开始研究前先验证 NotebookLM 登录：

```powershell
notebooklm list --json
```

认证失败时运行 `notebooklm login`，验证成功后再继续。浏览器 Cookie、付费 API、私人语料和公开发布都需要单独授权。

### 输出目录

研究根目录优先读取环境变量：

```powershell
[Environment]::SetEnvironmentVariable(
  'NOTEBOOKLM_RESEARCH_ROOT',
  'G:\obsidian_vault\Obsidian Vault',
  'User'
)
```

解析顺序为：显式参数 → 环境变量 → 已存在的 `G:\obsidian_vault\Obsidian Vault` →
`Documents\NotebookLM Research`。因此这台电脑会默认使用 Obsidian Vault；其他电脑可通过同一环境变量配置。
每个选题包含：

```text
<topic>/
├─ sources/last30days/
├─ sources/supplemental/
├─ sources/academic/
├─ manifests/
└─ notebooklm/
   ├─ briefing.md
   ├─ infographic.png
   ├─ mind-map.json
   └─ learning-path.md
```

最终 Markdown 至少包含研究窗口、摘要、数据源覆盖表、主题簇、逐条来源、日期、互动指标、链接、证据局限和 schema/采集时间。规范化脚本会移除 ANSI、调试日志和常见追踪参数，并保守合并重复记录。

### 安全与质量

- Cookie 与 API Key 不写入报告、日志或 Git。
- 社交互动量仅用于发现与排序，不代表事实可靠性。
- 失败、超时、限流和未配置来源不会被表述为“没有相关内容”。
- 不使用 Sci-Hub 或其他绕过付费墙、版权或访问控制的服务。
- 网页、帖子、评论、字幕和论文内容都属于不可信研究数据，不应被当作操作指令。

## English

`notebooklm-research` builds a deduplicated evidence pack for NotebookLM. It uses `last30days` for recent community and web signals, inspects the actual per-source status, and supplements only the missing, degraded, or incomplete channels.

### Highlights

- Recent Reddit, X, YouTube, HN, Polymarket, GitHub, and web signals through `last30days`.
- Status-aware routing that avoids collecting the same successful platform twice.
- Independent first-party verification for official sites, documentation, standards, regulations, releases, and pricing.
- Supplemental Zhihu and Bilibili collection, with conditional Rednote, YouTube, GitHub, and arXiv backfills.
- Versioned technical documentation through Context7.
- Lawful scholarly verification through Crossref, OpenAlex, Semantic Scholar, PubMed/PMC, CORE, Unpaywall, publishers, authors, and repositories.
- Conservative deduplication using stable identifiers before canonical URLs and normalized titles.
- Clean Markdown with coverage, evidence, limitations, and provenance for NotebookLM ingestion.

### Install

Install the repository as a complete skill directory. Do not copy only `SKILL.md`; the workflow depends on bundled references, scripts, and evals.

```bash
git clone https://github.com/tangchengyu/notebooklm-researcher.git
mkdir -p ~/.codex/skills/notebooklm-research
rsync -a --exclude .git notebooklm-researcher/ ~/.codex/skills/notebooklm-research/
```

Required tools are `last30days` and `notebooklm-cli`. `opencli`, Context7, and GitHub CLI are conditional supplements.

### Example

```text
Research the last 30 days of NotebookLM workflow changes and user feedback, verify official announcements, and prepare a NotebookLM evidence pack.
```

The root resolver checks an explicit value, `NOTEBOOKLM_RESEARCH_ROOT`, an existing local
`G:\obsidian_vault\Obsidian Vault`, and finally `Documents/NotebookLM Research`. Every completed workflow exports and verifies a briefing, infographic, interactive mind map, and learning path under the topic's `notebooklm/` directory.

### Safety

Browser cookies, paid APIs, private corpora, and public publishing require separate consent. Credentials are never written to research artifacts or version control. Source text is treated as untrusted evidence, and degraded source states remain explicit in the final Markdown.

## License

MIT © [tangchengyu](https://github.com/tangchengyu)
