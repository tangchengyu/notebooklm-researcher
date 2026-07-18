# last30days 集成协议

## 目的

把 `last30days` 当作“近 30 天多源采集引擎”，而不是 NotebookLM 最终文档生成器。引擎输出必须保留完整运行状态，并转换成适合 NotebookLM 的结构化 Markdown。

## 安装路径解析

优先使用当前已加载的 `last30days` skill 目录。若宿主没有提供路径，在 Windows PowerShell 中按顺序检查：

```powershell
$candidates = @(
  "$env:USERPROFILE\.agents\skills\last30days",
  "$env:USERPROFILE\.codex\skills\last30days"
)
$last30daysDir = $candidates |
  Where-Object { Test-Path -LiteralPath (Join-Path $_ 'scripts\last30days.py') } |
  Select-Object -First 1
if (-not $last30daysDir) { throw 'last30days 未安装或脚本缺失' }
```

不要自行遍历整个用户目录寻找脚本，也不要从 Claude marketplace 的已知陈旧 clone 运行。

## 安全预检

在首次配置、版本更新或来源异常时运行：

```powershell
python3 "$last30daysDir\scripts\last30days.py" --preflight
python3 "$last30daysDir\scripts\last30days.py" doctor
```

`--preflight` 不应读取 Cookie、写配置或执行研究。检查结果中如出现自定义 `LAST30DAYS_API_BASE`、项目级配置或计划读取浏览器 Cookie，先向用户说明并取得同意。

默认安全策略：

- 每次研究命令带 `--no-browser-cookies`，除非用户本轮或持久配置中已经明确同意。
- 不设置 `LAST30DAYS_API_BASE` / `LAST30DAYS_API_KEY`。
- 不传 `--corpus`，除非用户明确选择本地私有资料。
- 不传 `--publish-html` / `--publish`。
- 输出只写到当前选题目录。
- 对下游自动化建议设置 `LAST30DAYS_STRICT_EXIT=1`，但仍读取已生成报告；退出码 3 表示“完成但覆盖降级”。

## 配置与用户同意

这些操作需要用户明确同意：

1. 读取浏览器 Cookie 以启用 X/Twitter 或其他登录态来源。
2. 安装外部 CLI 或 npm/Python 包。
3. 使用付费 API、远程深度研究或 ScrapeCreators。
4. 读取私人本地语料。
5. 公开发布 HTML 或研究库。

Cookie 同意与 API Key 不要混为一谈。允许安装免费 CLI 不代表允许读取 Cookie；允许 X Cookie 不代表允许上传私人文件。

## 运行前诊断

运行：

```powershell
python3 "$last30daysDir\scripts\last30days.py" --diagnose --no-browser-cookies
```

使用诊断结果中的真实 `available_sources`，不要只看环境变量名。对 NotebookLM 工作流重点记录：

- 当前版本；
- 可用源；
- 缺失源；
- Cookie 模式；
- Web 后端；
- GitHub、YouTube、arXiv、小红书等是否可用。

### Windows 下 Firefox 已登录但 X/Bird 超时

若 `setup --allow-browser-cookies` 已报告 `X cookies found in firefox`，但真实研究的
`source_status.x` 仍为 `timeout`，不要要求用户重复登录或改用付费 xAI API。先区分认证与网络：

1. `--diagnose` 只确认计划读取 Firefox，不会验证真实请求；必须以一次小规模真实 X 检索为准。
2. 若错误为 `Bird: Search timed out after 30s`，并且浏览器能访问 X，而 Node.js `fetch`
   出现 `UND_ERR_CONNECT_TIMEOUT`，通常是 Firefox 使用了本机代理，但 Node.js 没有继承 Windows
   代理设置。
3. 经用户同意后，只为 Bird 配置本地代理，不修改 Windows 全局代理。先检查安装的
   `last30days` 是否明确支持 `BIRD_PROXY_URL`；不要向不支持该变量的上游版本写入无效配置：

```dotenv
BIRD_PROXY_URL=http://127.0.0.1:<本机代理端口>
```

本机兼容构建可使用 `undici.ProxyAgent`，只把 Bird/X 的 Node 请求送入该代理。其他环境应使用
其安装版本正式支持的 Node/代理配置，不要自动修改第三方代码。代理地址不得写入公开报告；
若代理 URL 含账号或密码，不要在聊天、命令日志或 NotebookLM 来源中显示。

配置后按顺序验证：Node 经代理访问 `https://x.com`、一次 `--search x --quick` 真实检索、
`doctor --postmortem` 显示 `Succeeded: x`。上游 `last30days` 更新可能改变代理行为；每次更新后
必须重跑这三项检查，失败时报告网络缺口，不得仅凭 Cookie 检测结果宣称 X 可用。

## Query Plan

命名实体、产品、组织、人物、具体项目或复杂主题必须由宿主模型生成 plan，并作为文件传入 `--plan`。不要把包含撇号的 JSON 直接内联到命令行。

最小结构：

```json
{
  "intent": "concept",
  "freshness_mode": "balanced_recent",
  "cluster_mode": "none",
  "subqueries": [
    {
      "label": "primary",
      "search_query": "精炼的关键词",
      "ranking_query": "自然语言研究问题",
      "sources": ["reddit", "x", "youtube", "tiktok", "instagram", "hackernews", "polymarket", "github", "grounding"],
      "weight": 1.0
    }
  ]
}
```

规则：

- 1-4 个子查询；复杂主题使用 3-4 个互补角度。
- `search_query` 不写“最近 30 天”、月份、年份或“新闻/更新”等元词。
- 对易混淆名称加入公司、产品类别、作者或组织锚点。
- how-to 优先 YouTube/Reddit；预测加入 Polymarket；软件项目加入 GitHub/HN；官方信息加入 grounding，但后续仍做官网核验。
- 只把实际可用或希望显式记录为缺口的源放入 secondary 查询；primary 可保留广泛源以获得完整状态。

PowerShell 中用临时或选题目录文件保存 plan：

```powershell
$planPath = Join-Path $topicDir 'manifests\last30days-plan.json'
# 使用 apply_patch 或安全的结构化文件写入方式创建；不要在日志中写入密钥。
```

## 标准研究命令

以 agent JSON 作为机器交接格式：

```powershell
$env:LAST30DAYS_MEMORY_DIR = Join-Path $topicDir 'sources\last30days'
$env:LAST30DAYS_STRICT_EXIT = '1'

python3 "$last30daysDir\scripts\last30days.py" "<topic>" `
  --days 30 `
  --deep `
  --emit json `
  --json-profile agent `
  --plan "$planPath" `
  --no-browser-cookies `
  --output "$topicDir\sources\last30days\last30days-agent.json"
```

用户已明确同意 Cookie 时，才移除 `--no-browser-cookies`，并按上游配置启用浏览器来源。若无宿主 Web 搜索能力，可用 `--auto-resolve`，但仍应记录这是一条较弱路径。

研究可能需要数分钟。使用 5-10 分钟超时；不要在无输出时重复启动第二个实例。

## 输出契约

agent JSON 至少应包含：

- `schema_version`
- `query`
- `generated_at`
- `window_days`
- `source_status`
- `clusters`
- `results`

如果输出缺失 `source_status`、无法解析为 JSON、包含调试前缀或 schema 不兼容，停止规范化并报告具体错误。不要从聊天文本猜测运行状态。

## Source Status 语义

- `ok`：成功且有结果。
- `no-results`：成功但没有匹配。
- `partial`：只得到部分结果。
- `rate-limited`：受限流影响。
- `auth-failed`：认证失败。
- `unreachable` / `timeout`：网络或时限失败。
- `schema-drift`：上游页面/API 结构变化。
- `skipped-unconfigured`：未配置而跳过。
- `error`：其他错误。

只有 `ok` 与 `no-results` 能证明该源完成了本轮查询。其他状态都必须在最终 Markdown 的“证据质量与局限”中出现。

## NotebookLM 规范化

运行基础 skill 的脚本：

```powershell
python "$skillDir\scripts\normalize_last30days.py" `
  --input "$topicDir\sources\last30days\last30days-agent.json" `
  --supplement "$topicDir\manifests\supplemental-sources.json" `
  --output "$topicDir\notebooklm\<topic>-NotebookLM资料包.md"
```

不要把 `last30days --emit=compact` 的聊天回复或 `--emit=md` 的内部合成提示直接导入 NotebookLM。前者为宿主渲染优化，后者可能包含调试/合成边界；agent JSON 才是稳定交接层。

## 更新策略

上游更新后先重新运行：

1. `--preflight`
2. `--help`
3. `--mock --emit json --json-profile agent`
4. 本地规范化脚本测试

若 schema 版本变化，先适配规范化脚本，再用于真实研究。
