# 补充采集协议

只读取并执行与当前任务相关的章节。

## B站

搜索：

```powershell
opencli bilibili search "<关键词>" --limit 20 -f json --window background
```

入选 2-5 个高相关结果后，按顺序获取正文：

```powershell
opencli bilibili video <BV_ID> -f md
opencli bilibili subtitle <BV_ID> -f md
opencli bilibili summary <BV_ID> -f md
```

优先合并元数据与字幕。无字幕但有官方总结时标注“未取得完整字幕”。都失败时可在 Chrome 使用 SubBatch 导出 MD，保存到 `sources\supplemental\bilibili`。只有标题/简介/互动量时标低信息量，不作为关键证据。

## 知乎

```powershell
opencli zhihu search "<关键词>" --limit 20 --type all -f json --window background
```

按主题相关性、作者专业性、论证完整度、引用质量和赞同数筛选 2-5 条。赞同数只是发现信号。尽量获取回答/文章正文，而不是只保留搜索结果标题和 URL。

对医疗、法律、财务、科学事实等高风险结论，知乎只能作为观点或解释线索，必须回到权威来源核验。

## 小红书

先看 `last30days` 的 `xiaohongshu`/`xhs` 状态与内容完整性。只有通道未成功或正文/评论不足时补采：

```powershell
opencli rednote search "<关键词>" --limit 20 -f json --window background
opencli rednote note "<包含 xsec_token 的完整URL>" -f md --window background
opencli rednote comments "<完整URL>" -f json --window background
```

选择 2-3 条高相关笔记，每条保留 2-3 条有实质信息的高赞评论。登录墙或反爬阻挡时，在 Chrome 登录后使用社媒助手导出 Excel/CSV/JSON，再转为 Markdown。删除广告、纯表情、重复和跑题评论。

每条至少记录：标题、作者、时间、URL、点赞/收藏/评论/分享、正文摘要、高价值评论、采集方式和限制。

## YouTube 补全

若 `last30days` 为 `ok` 且结果已有字幕/摘要，不再重复发现。若只有元数据或失败，可用：

```powershell
opencli youtube search "<关键词>" --limit 20 --sort views -f json --window background
```

再用可用工具获取字幕。合并到同一视频 ID，不把元数据和字幕作为两个 NotebookLM 来源。

## GitHub 深挖

`source_status.github == ok` 时默认不再运行仓库发现。以下情况才补充：

- 用户要求全历史或超出 30 天的成熟项目比较；
- 需要 README、Release、Issue、Discussion、PR 或 commit 级证据；
- `no-results` 但已知存在相关仓库；
- 运行状态失败或未配置。

仓库发现命令：

```powershell
gh search repos "<关键词>" --sort stars --limit 20 --json name,owner,url,stargazersCount,description
```

Star 只作为发现信号。根据活跃度、维护状态、Release、文档质量、许可证、Issue 响应和主题相关性筛选。

## 官网与权威一手来源

无论 Web 通道是否成功，只要主题涉及公司、产品、法规、标准、技术规范、价格、发布日期或政策，都单独核验官网：

- 官方产品/文档/博客/Release notes；
- 标准组织、政府或监管机构；
- 公司投资者关系、公告、招聘页；
- 原始数据集或项目主页。

记录页面标题、机构、发布日期/更新时间、版本、稳定 URL、查询时间和它支持的具体事实。官网营销主张仍需独立证据验证。

## Context7

软件、框架、API 或工具链主题启用：

```powershell
ctx7 library "<库名>" "<查询上下文>"
ctx7 docs <libraryId> "<具体问题>"
```

若 `ctx7` 不存在，先尝试：

```powershell
npx ctx7@latest library "<库名>" "<查询上下文>"
```

安装或运行外部包前遵守用户授权。记录库 ID、版本、API 签名、参数、示例、弃用/变更信息和查询时间。

## 学术通道

学术、科研、医学、工程和专业技术主题启用。`last30days` 的 arXiv 只负责近期信号；系统检索仍需：

1. 高相关论文：系统综述、元分析、代表性实证研究；
2. 前沿论文：最近 3 年，并检查最近 12 个月；
3. 奠基论文：通过综述、共同引用和术语来源追溯。

arXiv 必须用 bundled CLI：

```powershell
python "$skillDir\scripts\arxiv_cli.py" search "<英文查询>" `
  --max-results 10 --download 3 --output "<选题目录>\sources\academic\arxiv"
```

再用 Crossref/OpenAlex/Semantic Scholar 核验 DOI、作者、年份、引用与正式发表关系；医学/生命科学使用 PubMed/PMC；合法全文可来自 CORE、Unpaywall、出版社、作者主页或机构仓储。

每篇记录：标题、作者、年份、类型、DOI/arXiv/PMID、同行评审/发表状态、入选类别、贡献、局限、合法全文 URL。只有摘要时标注“仅摘要”。不使用 Sci-Hub。
