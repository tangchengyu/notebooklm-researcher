---
name: notebooklm-research
description: >
  当用户给出一个选题，帮助用户在多平台搜索有价值的信息源；遇到学术、科研选题时，
  额外检索高相关、前沿与奠基性论文；遇到软件开发、框架工具等技术性选题时，
  通过 Context7 查询相关技术的最新官方文档，并核验论文身份、版本和可获取性；再汇入 NotebookLM 项目，
  并生成报告（简报）、信息图表（Infographic）、思维导图（Mind Map）
  和学习路径指导文档，最后将所有产出保存到 Obsidian Vault 的选题文件夹中。
  触发场景：用户说"研究一下XX"、"帮我调研XX选题"、"用 NotebookLM 分析XX"、
  "做一个关于XX的深度调研"、"帮我收集XX的资料"等。即使用户没有明确提到 NotebookLM，
  但只要涉及"收集多平台资料 + 生成报告"的需求，就应该使用此技能。
---

# NotebookLM 深度研究技能

## 概述

此技能完成一个完整的「选题研究 → 多平台信息收集 → NotebookLM 分析 → 产出保存」工作流。

## 核心工具链

- **opencli**（v1.8+）：跨平台搜索 CLI，支持 B站、YouTube、知乎、小红书等站点适配器
- **notebooklm** CLI（v0.7+）：NotebookLM 完整操作（创建项目、添加来源、生成产物、下载）
- **gh** CLI：GitHub 仓库搜索（opencli github 适配器仅支持登录操作）
- **ctx7** CLI：Context7 文档查询，为技术性选题获取最新官方文档（框架 API、库用法、签名示例等）
- **学术检索入口**：arXiv，以及 Crossref、OpenAlex、Semantic Scholar、PubMed/PMC、CORE、Unpaywall、出版社或作者/机构仓储等合法来源（按学科选择）

## 工作流

### 第一步：确认选题和搜索范围

当用户给出选题后：

1. **确定选题名称**：用作文件夹名和 NotebookLM 项目名
2. **确认搜索平台**：如果用户没有指定平台，默认搜索全部 5 个通用平台：
   - B站（bilibili）
   - YouTube
   - 知乎（zhihu）
   - 小红书（rednote）
   - GitHub

   判断选题类型：
   - 若属于学术、科研问题 → 默认启用“学术论文检索”
   - 若属于软件开发、框架工具等技术性问题 → 默认启用“Context7 技术文档查询”
   - 若同时是学术研究型技术问题（如“深度学习在图像分割中的新进展”）→ 两项都启用
   - 若只是生活消费、娱乐或一般经验类选题 → 均不启用

   询问用户：「我将在这 5 个平台为你搜索相关资料，是否需要调整？」

   如果用户指定了部分平台，只搜索指定的平台。

### 第二步：创建选题文件夹

在 `G:\obsidian_vault\Obsidian Vault\` 下创建以选题名称命名的文件夹：

```powershell
New-Item -ItemType Directory -Force -Path "G:\obsidian_vault\Obsidian Vault\<选题名>"
```

### 第三步：多平台搜索

对每个目标平台执行搜索。所有 opencli 命令使用 `--window background` 以在后台运行浏览器，使用 `-f json` 获取结构化输出。

#### B站搜索

```bash
opencli bilibili search "<选题关键词>" --limit 20 -f json --window background
```

返回字段：`rank, title, author, score, url`
按 `score`（综合评分）排序，选取 score 最高的 3-5 个结果。

#### YouTube 搜索

```bash
opencli youtube search "<选题关键词>" --limit 20 --sort views -f json --window background
```

返回字段：`rank, title, channel, views, duration, published, url`
按 `views`（播放量）排序，选取播放量最高的 3-5 个结果。

#### 知乎搜索

```bash
opencli zhihu search "<选题关键词>" --limit 20 --type all -f json --window background
```

返回字段：`rank, title, type, author, votes, url`
按 `votes`（赞同数）排序，选取赞同数最高的 3-5 个结果。

#### 小红书搜索

```bash
opencli rednote search "<选题关键词>" --limit 20 -f json --window background
```

返回字段：`rank, title, author, likes, published_at, url, author_url`
按 `likes`（点赞数）排序，选取点赞数最高的 3-5 个结果。

#### GitHub 搜索

```bash
gh search repos "<选题关键词>" --sort stars --limit 20 --json name,owner,url,stargazersCount,description
```

按 `stargazersCount`（Star 数）排序，选取 Star 数最高的 3-5 个结果。

#### Context7 技术文档查询（软件开发、框架工具等技术性选题默认执行）

当选题属于技术性问题（如编程语言特性、框架/库用法、工具链配置、API 调用等），通过 [Context7](https://context7.com) 查询相关技术的官方文档作为信息源。Context7 维护与官方文档同步的最新 API 签名、用法示例和变更记录，能覆盖训练数据截止后的最新变化。

执行步骤：

1. **分析技术栈**：根据选题关键词判断涉及的核心技术栈（库名、框架名、工具名、编程语言等），确定需要查询的库和具体问题
2. **对每个目标库执行查询**：

```bash
# 第一步：解析库 ID
ctx7 library "<库名>" "<查询上下文>"

# 第二步：获取文档内容
ctx7 docs <libraryId> "<具体问题>"
```

3. **记录文档内容**作为信息源，包含：
   - 库名 / 框架名及版本
   - API 签名、关键参数说明
   - 用法示例代码
   - 版本变更或弃用说明（如有）
   - 查询时间
4. **将文档内容以文本形式**添加到 NotebookLM 项目（使用 `--type text`）

#### 信息源去重与整合

对于同时启动学术论文检索和 Context7 技术文档查询的选题，注意区分两类信息源的定位：学术论文提供理论背景和前沿研究进展，Context7 文档提供工程实践中的 API 用法和实现参考。两者互补而非重复。

#### 学术论文检索（学术、科研或专业技术选题默认执行）

把论文检索作为独立证据通道，不用社交平台热度代替学术质量。先用中英文关键词、常用缩写、同义词和核心作者扩展查询，再按以下三类分别寻找候选论文：

1. **高相关论文**：与研究问题、方法或对象直接匹配，优先系统综述、元分析、权威综述和代表性实证研究。
2. **前沿论文**：优先最近 3 年，另外单独检查最近 12 个月的预印本、顶级会议/期刊论文与重要研究团队的新工作。前沿性不能只按发布日期判断，还要看其是否提出新方法、新数据、新基准或改变当前讨论。
3. **奠基性论文**：通过综述的参考文献、后续论文的共同引用、领域公认术语来源和高被引早期工作进行追溯。高引用量只是线索，不是唯一标准。

优先检索与交叉核验这些来源：

- **arXiv**：搜索预印本与最新版本，记录 arXiv ID、版本号和提交日期；明确标注“预印本/尚未确认同行评审”，并检查是否已有正式发表版本。
- **Crossref / OpenAlex / Semantic Scholar**：核验标题、作者、年份、DOI、引用关系及相近工作。
- **PubMed / PubMed Central**：医学、生命科学和健康主题优先使用；区分摘要记录与可公开访问全文。
- **CORE、Unpaywall、出版社页面、作者主页、大学或机构仓储**：寻找合法开放获取全文或作者接受稿。

不要使用 Sci-Hub 或其他绕过付费墙、版权或访问控制的服务。若正式版本受限，保留 DOI/出版社页面作为书目信息来源，并通过 arXiv、PubMed Central、机构仓储、作者主页或 Unpaywall 查找合法版本；仍无全文时，只导入已合法获得的摘要与元数据，不声称读过全文。

对每篇入选论文至少记录：

- 标题、作者、年份、论文类型（期刊/会议/预印本/综述等）
- DOI、arXiv ID、PMID 等稳定标识符（如有）
- 正式发表状态与同行评审状态
- 入选类别：高相关 / 前沿 / 奠基性（可多选）
- 与选题的具体关联、主要贡献、关键局限
- 合法全文 URL；若只有摘要，明确标注“仅摘要”

默认每类保留 3-5 篇高质量论文；去除重复版本时，优先保留正式发表页，同时附上合法开放版本。若某一类别证据不足，不要凑数，在汇总中说明检索范围与缺口。

#### 信息源筛选原则

- 优先选择高赞、高播放量、高收藏/Star 数的内容
- 每个平台选取 **3-5 个**最有价值的信息源
- 跳过明显低质量或无关内容
- 记录每个信息源的：标题、作者/频道、链接、互动数据（播放量/赞同数/Star数等）
- 学术论文不得按点赞、播放量或 Star 数筛选；应综合主题相关性、发表/评审状态、方法质量、引用关系、版本新旧与来源可靠性
- 对关键结论尽量使用正式论文或权威数据库交叉验证；不要把预印本结论表述为已经确立的学术共识

### 第四步：创建 NotebookLM 项目并添加来源

#### 创建项目

```bash
notebooklm create "<选题名称>"
```

记录返回的 Notebook ID。

#### 添加来源

将所有筛选出的信息源 URL 逐个添加到项目中：

```bash
notebooklm source add "<URL>" -n <notebook_id>
```

如果你收集到的信息源是文本描述（如某个帖子的核心观点），也可以用文本方式添加：

```bash
notebooklm source add "<核心内容文本>" --type text --title "<标题>" -n <notebook_id>
```

等所有来源添加完毕后，用以下命令确认来源处理完成：

```bash
notebooklm source wait -n <notebook_id>
```

### 第五步：生成 NotebookLM 产物

依次生成以下四种产物。每种产物生成后等待完成再继续下一个。

#### 1. 生成报告（简报）

```bash
notebooklm generate report --format briefing-doc -n <notebook_id> --wait --timeout 600
```

报告会包含：
- 对所有收集信息源的概述
- 每个信息源的核心内容和优势特点
- 对应链接

#### 2. 生成信息图表（Infographic）

```bash
notebooklm generate infographic -n <notebook_id> --wait --timeout 600
```

信息图表以可视化方式呈现选题的核心概念、数据或流程。

#### 3. 生成思维导图（Mind Map）

```bash
notebooklm generate mind-map -n <notebook_id> --wait --timeout 600
```

思维导图以结构化方式展示选题的知识体系和各概念之间的关联。

#### 4. 生成学习路径指导文档

```bash
notebooklm generate report --format custom -n <notebook_id> --wait --timeout 600 "请基于本项目中收集的所有信息源，生成一份学习路径指导文档。要求：
1. 按照从入门到精通的递进顺序，将学习内容分为 3-4 个阶段（如：入门基础、进阶深入、实战应用、前沿拓展）
2. 每个阶段列出推荐的学习资源（从已收集的信息源中选取），说明每个资源适合的学习阶段和原因
3. 给出各阶段的学习目标、预计耗时和关键里程碑
4. 标注资源之间的前置依赖关系（哪些需要先学再看哪些）
5. 最后给出一个建议的总体学习时间线和学习策略建议
请用中文输出，格式清晰，使用 Markdown 标题层级组织内容。"
```

### 第六步：下载产物到选题文件夹

将生成的所有文件下载到第二步创建的选题文件夹中：

```bash
# 报告（简报）
notebooklm download report --all --force "G:\obsidian_vault\Obsidian Vault\<选题名>\" -n <notebook_id>

# 信息图表
notebooklm download infographic --all --force "G:\obsidian_vault\Obsidian Vault\<选题名>\" -n <notebook_id>

# 思维导图（JSON 格式）
notebooklm download mind-map --all --force "G:\obsidian_vault\Obsidian Vault\<选题名>\" -n <notebook_id>

# 学习路径指导文档（报告类的自定义产物，用 report 下载第二个）
notebooklm download report --all --force --name "学习路径" "G:\obsidian_vault\Obsidian Vault\<选题名>\" -n <notebook_id>
```

> **注意**：学习路径指导文档也是报告类型产物，下载时需要区分它与简报。简报通常先生成，学习路径后生成。可以用 `--name` 参数按标题模糊匹配来分别下载，或者用 `--artifact` 指定具体 artifact ID。先用 `notebooklm artifact list -n <notebook_id>` 查看所有产物的 ID 和标题，然后逐个指定下载。

### 第七步：汇总报告

完成所有步骤后，向用户展示一个汇总：

```
📁 选题文件夹：G:\obsidian_vault\Obsidian Vault\<选题名>\
📋 NotebookLM 项目：<选题名称>（ID: xxx）
📊 收集信息源：X 个（B站 X个、YouTube X个、知乎 X个、小红书 X个、GitHub X个；学术论文 X篇：高相关 X篇、前沿 X篇、奠基 X篇；技术文档 X 项
📄 已生成文件：
  - report-*.md（简报）
  - infographic-*.png（信息图表）
  - mind-map-*.json（思维导图）
  - 学习路径指导文档-*.md（学习路径）
```

## 常见问题处理

### 搜索无结果

如果某个平台搜索返回空结果，跳过该平台并在汇总中说明「XX 平台未找到相关内容」。

### NotebookLM 生成超时

如果 `--timeout 600` 不够，可以增大超时时间到 1200 秒。如果仍然超时，使用 `notebooklm artifact list -n <notebook_id>` 检查产物状态，然后单独下载。

### GitHub gh CLI 未登录

如果 `gh search repos` 报错，提示用户运行 `gh auth login` 登录。如果用户不想登录 GitHub，跳过 GitHub 平台。

### ctx7 命令未找到

如果 `ctx7` 命令不可用，尝试：

```bash
npx ctx7@latest library "<库名>" "<查询上下文>"
```

或全局安装：

```bash
npm install -g ctx7
```

### Context7 查询无结果

如果 `ctx7 library` 返回的库名与预期不符，尝试不同的关键词组合（如全称、缩写、npm 包名、GitHub 组织名等）。如果仍无结果，跳过 Context7 并在汇总中说明「未找到相关技术文档」。

### opencli 浏览器问题

如果 opencli 报浏览器相关错误，尝试：
```bash
opencli doctor
```
根据诊断结果修复，或使用 `--window foreground` 查看具体问题。
