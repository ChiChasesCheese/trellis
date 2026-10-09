# 子代理指令 · Abnormal AI 尽调（`catalog/raw/`）

> 你是 `sonnet` 子代理，**不得再派生代理**。只写分配给你的 `catalog/raw/` 文件，不碰别的。
> 候选人 Chi：1.5 年后端（PayPal Braintree，Python/Kotlin/Snowflake/SQL），自建 66K 行 Python 量化研究平台。
> 职位：**Abnormal AI · Software Engineer II – Insider Risk**。已过 HR + HM。下一轮 = **AI Technical Screen**（官方候选人页，2026-10-06 读到）：
> 60 min，在一个**已有的 Python 代码库**里实时编码，浏览器 VS Code + **Claude Code 预装**，AI 是"必须用"；
> ~10 min 探索建心智模型 → ~35 min 一个**故意说不清楚的 feature**（怎么处理模糊性本身被评）→ 剩余 walkthrough + 反问。
> 评分：Judgment（评估方案、拆里程碑、是否契合现有系统）· Agency（陈述假设、自测、不等指令推进）· 交付契合系统的可用 v1。
> 视频：David Hagar（Sr Director of Engineering）讲 AI Technical Screen；Shrivu Shankar（VP of AI）讲 Claude Code 技巧。
> 之后几轮未知 —— 这正是你要查的。

## 恢复规则

开工先 `ls catalog/raw/`；你负责的文件若已存在，读它、只补缺，不重写已有条目。

## 硬规则

1. **每条事实带 URL + 访问日期（2026-10-06）+ 可信度**：[高] 一手/官方 · [中] 一手但只有摘要 / 标了日期轮次的聚合 · [低] SEO/无日期。原文尽量引英文原句（加引号），不改写数字。
2. **不采信**：lodely.com、vervecopilot.com（AI 题目农场）。CSDN 等混有 AI 农场的站逐条辨伪。
3. **一次抓取失败不判死刑**：记录哪个路径失败（HTTP 码），换路径再试。已知可达路径（本仓库实测）：
   - teamblind：**浏览器 UA**（`curl -sS -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"`），机器人 UA 403。
   - reddit：`https://www.reddit.com/r/<sub>/search.rss?q=<q>&restrict_sr=1&sort=new`、全站 `https://www.reddit.com/search.rss?q=...`（可能 0 条）、单帖 `/comments/<id>/.rss`（含评论全文）。试 r/cscareerquestions、r/csMajors、r/leetcode、r/ExperiencedDevs。
   - Hacker News：`https://hn.algolia.com/api/v1/search?query=abnormal%20security%20interview&tags=comment`（和 story）。
   - leetcode discuss：HTML 403；`POST https://leetcode.com/graphql`（discuss 搜索查询）可用。
   - 1point3acres：直连 Cloudflare 死锁；**用 Chi 的 Chrome（browser-use）可直接打开**（2026-10-09 实测；公司标签页 `bbs/tag-8728-1.html`，隐藏内容需积分 ≥ 188）；**Telegram 镜像** `https://t.me/s/usinterview?q=abnormal` 可读摘要（再试 `?q=Abnormal%20Security`）。1p3a 已知帖：thread 1072363（Tech Phone Screen · Image Deduplication）、1074077（Full process）。
   - GitHub：`api.github.com` 不可用；`git clone --depth 1` 公开仓库可用，`raw.githubusercontent.com` 可用；用 WebSearch `site:github.com` 找。
   - prachub / interviewdb / levels.fyi / nowcoder 直接抓。medium 403 → 用搜索摘要，标"摘要"。glassdoor：`curl -A <浏览器 UA> https://api.glassdoor.com/Interview/...htm` 返回 200，评论正文以转义 JSON 嵌在 HTML 里（2026-10-09 实测，全量 152 条）。
   - 用 `curl -sS -L --max-time 30` 走默认代理（不要关 TLS 校验、不要 unset HTTPS_PROXY）。
4. 中间产物放 `$CLAUDE_JOB_DIR/tmp/` 或 `/tmp/claude-0/.../scratchpad`，不要进仓库。
5. 文件用中文写说明、英文保留原句。不写过程话。
6. 最后回复里给：写了哪些文件、每个文件条目数、你认为最可疑的 3 条事实。

## 分工

### Agent A —— 面经与流程（写 `catalog/raw/process_and_rounds.md`、`catalog/raw/questions_reported.md`、`catalog/raw/github_repos.md`）

- **GitHub 先**：WebSearch `site:github.com "abnormal security"`、`"abnormal ai" interview`、company-wise leetcode 仓库里有没有 Abnormal（`liquidslr/leetcode-company-wise-problems` 已确认**没有** Abnormal 目录；查 `snehasishroy/leetcode-companywise-interview-questions`、`krishnadey30/LeetCode-Questions-CompanyWise` 等，clone 后 `ls | grep -i abnormal`）。`github_repos.md`：仓库 · stars（若可得）· 最近更新 · 可信度 · 用途；没找到也要写清查了什么。
- **流程**：每一轮（recruiter / HM / AI technical screen / OA / onsite 各轮：coding、code review、system design、ML design、behavioral/values、"Fourth Round Video"）——时长、形式、面谁、评什么、按日期排；特别区分 **2025 年中以后的 AI-assisted 新流程** 与旧流程（CodeSignal/LC 式）。新流程 onsite 是不是还有 AI-assisted coding、代码库是否同一个、是否 Django/Flask/FastAPI、是否涉及 email/安全领域、feature 是什么类型（报道里出现过的一律记下原话）。
- **题目**：每个被报道的题（coding / system design / code review / ML / behavioral）一行：原话、轮次、角色、日期、来源、可信度。已知线索：duplicate-file removal、photo/image dedup service、high-throughput event pipeline、scaling to 10x、Django take-home with Cursor + 录视频、"15 min LC-style"、code review + system design 一轮。
- 渠道：Blind（`teamblind.com/company/Abnormal-Security/posts/...`、搜 "abnormal interview"、"abnormal ai technical screen"）· reddit · HN · leetcode discuss · 1p3a 镜像 · prachub（`/companies/abnormal-security`、`/companies/abnormal-ai`、experience 页）· interviewquery · dataford（429 就记）· glassdoor 摘要 · 小红书（只能靠搜索摘要）· YouTube 视频标题/描述。

### Agent B —— 公司、团队、AI 面试官方口径（写 `catalog/raw/official.md`、`catalog/raw/ai_screen_format.md`）

- **官方**：abnormal.ai careers / "how we hire" / interview 指南页、engineering blog（`abnormal.ai/blog` 的 engineering 分类，旧域名 abnormalsecurity.com）、"AI-native engineering"/"how we use Claude Code" 类文章、技术栈（Python、Django?、Kafka、Spark、Redis、Postgres、AWS…，逐条给原文）、公司 values（官方原文）、规模/融资/ARR（标日期）。
- **Insider Risk 产品**：Abnormal 的 insider risk / "Data Protection" / "Account Takeover" / "AI Security Mailbox" 产品页原话：检测什么信号（行为基线、数据外泄、邮件外发到个人邮箱、离职员工…）、数据源（Microsoft 365 / Graph API、Google Workspace、Slack、Zoom、Okta…）。这会决定练习代码库的领域，越具体越好。
- **SWE II – Insider Risk JD**：找到职位原文（greenhouse / ashby / lever / jobright 镜像），整段引用 responsibilities / requirements / nice-to-have。
- **AI Technical Screen 官方口径**：David Hagar 视频（YouTube 标题、描述、任何文字稿/字幕：试 `https://www.youtube.com/watch?v=...` 页面里的 `"shortDescription"`）；Shrivu Shankar 的博客 `blog.sshh.io`（或 shrivu.com）—— 他写过 Claude Code / AI coding 的文章（"How I use every Claude Code feature"、关于 Abnormal 内部 AI 工程实践、面试改革的文章），逐篇列标题 + 日期 + 与面试相关的原句（CLAUDE.md、plan mode、subagents、hooks、"review at the right altitude" 之类）。也查 Abnormal 是否公开写过"我们为什么改成 AI 面试"。
- **同类面试的外部报道**（作为补充，标[中/低]）：其它公司 "AI-assisted coding interview in an existing codebase" 的形式与评分（Meta AI-enabled coding、Shopify、Rippling、Canva…），只取对 Abnormal 这种格式有迁移价值的要点（评分维度、常见挂法），每条带 URL。
