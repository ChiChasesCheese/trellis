# AI 编码轮补扫（2026-10-07）

访问日期 2026-10-07。可信度：[高] 一手/官方 · [中] 一手但只有摘要 / 候选人自建仓库 / 带日期聚合 · [低] SEO/无日期。条目编号 `S-n`。
只记**新增**事实（不在 `questions_reported.md` / `process_and_rounds.md` / `ai_screen_format.md` / `github_repos.md` / `CATALOG.md` 里的，或日期更新的）。

## 0. 渠道结果一览（含无结果，防止重复劳动）

| 渠道 | 路径 | 结果 |
|---|---|---|
| GitHub | `gh api -X GET search/repositories`（**本机 `gh` 可用**，与 `github_repos.md` 的"api.github.com 不可用"不同；`search/code` 503/422 不可用） | **有新发现**：Abnormal take-home 模板仓库被大量候选人克隆，见 S-1 |
| LeetCode Discuss | `POST https://leetcode.com/graphql` · `ugcArticleDiscussionArticles(keywords:["abnormal"])` 共 30 条，正文用 `ugcArticleDiscussionArticle(topicId:String!)` | 新帖 1 条有内容（S-2）；4 条无内容（S-3）；其余已在 kit 里或与 Abnormal 无关 |
| Telegram 镜像 | `t.me/s/usinterview?q=abnormal`（+ `abnormal ai` / `abnormal security` / `abnormal screen` / `%23Abnormal` / `abnormal claude` / `abnormal onsite`） | 去重后 **8 帖，全是已知**（1059585 · 1072363 · 1074077 · 1137132 · 1146766 · 1148780 · 1149759 · 1181621）。无新帖 |
| Reddit RSS | `r/cscareerquestions/search.rss?q=abnormal+ai+interview`（25 条）· csMajors / leetcode / ExperiencedDevs / developersIndia 0 条 · 全站 0 条 | 25 条无一条正文含 "abnormal"。**0 条 Abnormal 相关** |
| Hacker News | `hn.algolia.com/api/v1/search_by_date?query=abnormal security interview` | 4 条命中全是 "abnormal" 普通词，**0 条相关** |
| Blind | 浏览器 UA 可达 `teamblind.com/company/Abnormal-Security/posts`（200）；`/company/Abnormal-AI/posts` 404 | 列表有 ~30 个 Abnormal 帖。抽 9 个面试帖查 `datePublished`：2021-10-27 · 2022-10-26 · 2023-07-26 · 2023-12-30 · 2024-01-13 · 2024-08-31 · 2024-11-20 · 2025-01-09 · 2025-03-10，**全部早于 AI 流程**，页面内无 `__NEXT_DATA__`，正文未解析（只有 title/日期）。**无 2026 帖** |
| PracHub | `prachub.com/companies/abnormal-ai`、`/abnormal-security` 200 | 仍只有已知 3 篇（874b1387d9 · 6e26945209 · a2857641b5）。`/ai-assisted`、`/positions/software-engineer/ai-assisted` 200 但 0 条 Abnormal。**PracHub 自己的研究文**（`prachub.com/resources/*` 泛指南）不当作 Abnormal 证据 |
| Glassdoor / Indeed / InterviewQuery / dataford | 直连 403 / 403 / 429 / 429 | WebSearch 摘要只回显已知内容（"how you prompt AI to tackle the problem" 即 Q23）。**无新事实** |
| YouTube | 页面 `ytInitialPlayerResponse`（`shortDescription` / `publishDate`） | S-5。David Hagar 的 AI Technical Screen 视频仍无公开页（O-19 不变） |

## 1. 新来源条目

### S-1 · Abnormal "File Vault" take-home 模板（GitHub，>10 个候选人克隆）· [中]

- 模板 README 标题 "Abnormal File Vault"：Django 4.x + DRF + SQLite + Gunicorn + WhiteNoise + Docker（部分 fork 加 React 18/TypeScript/TanStack Query/Tailwind）；端点 `GET/POST /api/files/`、`GET/DELETE /api/files/<id>/`。**一个预置好的、可跑的小 Django 代码库，让候选人在上面加 feature。**
- 模板 README 里的提交要求（逐字，取自 DKunch30 的 README 第 251–259 行，同样文字在 preeti13456 / Aryank47 / dameon62 / zubiee 也出现）：
  > "**Video Guidance** - Record a screen share demonstrating: - How you leveraged Gen AI to help build the features … - Your prompting techniques and strategies … - Your thought process in using AI effectively"
  > "**IMPORTANT**: Please do not provide a demo of the application functionality. Focus only on your Gen AI usage and approach."
  > "Make sure to test the zip file and video before submitting"（提交为 zip + 视频 + Google Form）。
- 候选人自述的任务内容（仓库描述原话）：
  - https://github.com/Dhanush1357/abnormal-security-file-vault（2025-04-17）："Take-home project for Abnormal Security – Contributed to an existing codebase with a pre-configured setup. Focused solely on implementing file deduplication to optimize storage, along with search and filtering functionality based on filename, file type, size, and upload date. Also added metrics to monitor deduplication efficiency."
  - https://github.com/SlaveToJavascript/dplat-file-vault-coding-challenge（2026-03-09）："Abnormal AI, SWE 2 (Backend) take-home assignment (attempted for fun)"
  - https://github.com/dameon62/abnormal-security-assessment（2026-03-02）："Abnormal AI SDE II Assessment - Abnormal Vault for File handling with Deduplication"
  - https://github.com/Arindaam/FileVault（2026-01-26）："Abnormal Filevault Challenge- Full Stack File Deduplication Application with Advanced searching and sorting with cacheing"
  - https://github.com/DKunch30/dplat-file-vault-coding-challenge（2025-10-20）：README 功能表 "Deduplication by SHA-256: Files with identical hashes are stored once; re-uploads create reference records."、"Quota enforcement: Each user has a configurable 10 MB storage quota (dedup-aware)."、"Storage statistics endpoint: Shows original usage, deduplicated usage, and storage savings."（这是候选人的实现，不是题面）
  - 其它同模板：`Aryank47/…`（2025-06-07 创建）· `preeti13456/…`（2025-08-06）· `rohanyh101/…`（2025-10-25）· `galaxyte/Abnormal-File-Vault` · `hritik2899/abnormal-file-vault`（2026-05）· `abovEO/abnormal_ai_file_vault`（2026-05）· `zubiee/abnormal-file-vault`（2026-04）· `vaishnavi-vaishnav/abnormal-file-vault-task`（2026-06）· `mayankjn99/abnormal-file-hub`（2026-01）· `tarun2000/abnormal-file-vault`（2026-01）
- 轮次/级别：take-home（带 Gen-AI 屏幕录像），SDE II / SWE 2 Backend（印度/通用）。时间：模板最早 fork 2025-06-07，最新 2026-07-31（galaxyte 推送）。
- 意义：(1) 这是**第二种已被公开材料印证的 AI 题型：预置代码库上的 greenfield-ish feature**（dedup + 搜索过滤 + 配额 + 统计/metrics），且与旧流程电面 pc01（图片去重）同一主题；(2) 题面不在仓库里（在邮件里），仓库只给出候选人实现，所以 feature 清单是**候选人转述**，不是官方；(3) 评分对象是"如何用 AI"的录像，而不是 demo。`github_repos.md` 的"没找到 take-home 的公开 GitHub 仓库"结论**作废**。
- 另外旧 take-home 两份（日期早，非 AI 时代，仅作形态参考）：https://github.com/ramakeerthi/secure-file-share（2024-12-24，"File sharing application developed as part of Abnormal Security Interview process."，Docker，RBAC：首位注册者为 ADMIN，加密上传，分享权限 View/Download）；https://github.com/hr23232323/as-tech-interview（2021-10-14，"Given a large file, implement a data stream-based word counter."）。[中]

### S-2 · LeetCode Discuss #8538902 · [中]

- URL https://leetcode.com/discuss/post/8538902 · 发布 2026-09-25 · 作者 5+ YOE、FAANG、印度，标题 "My Ongoing Interview Experience for last 2 months"（多公司拒信清单）。
- Abnormal 段原话（全文）：
  > "# Abnormal Ai / R1 recruiter phone screen / Forward / R1 : OA / Graph based question to be attempted only in java"
- 轮次：OA（recruiter screen 之后）；级别：未说（5+ YOE，印度）。
- 意义：**2026-09 仍有区域性的 DSA 式 OA**（图题，限定 Java），与官方 "not leetcode" 相左；可能是印度 SDE-1/SSE 的另一条路径（见 S-3：6 月已有 "Upcoming DSA round for SDE-1"）。单一来源，无题面。

### S-3 · LeetCode Discuss 无正文的两帖 · [低]

- https://leetcode.com/discuss/post/8326147 · 2026-06-10 · "Upcoming DSA round for SDE-1 at Abnormal AI"：只有提问，"I have an upcoming DSA interview for an SDE-1 role at Abnormal Security (Abnormal AI)."——**SDE-1 有 DSA 轮**（旁证 S-2）。
- https://leetcode.com/discuss/post/8314495 · 2026-06-05 · "Upcoming Interview At Abnormal AI"：只有提问（SWE II）。
- 另有 2025 年的提问/薪资帖（7259463 · 7176383 · 7051638 · 7043211 · 6767374 · 6647083）：无题目内容；只有 7043211（2025-08-04）"It's going to be a live coding round for SSE position… The role is in India." 说明 2025-08 印度 SSE 仍是 live coding。

### S-4 · Abnormal 官方：Claude Code for On-Call Ops · [高]（类比 incident 轮，不是面试说明）

- URL https://abnormal.ai/transform/product-development/claude-code-for-on-call-ops （页面无日期；2026-10-07 抓取）
- 原话："Shrivu Shankar developed Claude Code for On-Call Ops, a tool that automatically connects to CloudWatch and Prometheus, executes the correct queries, and generates a clear diagnostic report."；"Fetching and parsing CloudWatch logs by service identity / Querying Prometheus counters in their native syntax / Detecting recurring errors and tallying frequency / Summarizing the impact and root cause for engineers / Suggesting fixes or even drafting PRs to resolve issues"；"I don't even tell it where to look."
- 意义：公司内部**用 Claude Code 做 incident 排障**是常态 → ic01/ic02（AWS 环境排障）可能允许/期待用 AI 查日志；`ic*` 的"信号 → 假设 → 验证"套路应加"让 AI 聚合，人判断"。轮次：incident（Q8/Q9 的类比）。

### S-5 · YouTube "Meet Shrivu Shankar, VP of AI Strategy: Learn Why He Says No One Is Using AI like Abnormal" · [高]

- URL https://www.youtube.com/watch?v=Vj5xjic6Bvw · 发布 2025-09-22
- 描述原话："He discusses the crossing point where he ships code without writing it and why Abnormal integrates AI more than any other company."
- 意义：官方招聘视频；确认 Shrivu 的头衔（"VP of AI Strategy"，与 O-n 里 "VP of AI" 的差异记一笔）与"ship code without writing it"的文化——面试里**让 AI 写**不会被扣分，**不理解**才会（与 F-1 "judging the tool by the final PR" 同向）。

### S-6 · 同类 AI 编码面试的 2026-10 动向（类比，[低]）

- LeetCode Discuss #8552696（2026-10-02）Amazon SDE 1 OA："1 DSA question + 1 AI-Assisted Coding Repo Question. The coding repo questions was very easy"；#8560273（2026-10-07）"In the new Amazon OA, along with traditional DSA problem, they've started AI coding assistant coding question"；#8559885（2026-10-06）JioHotstar "AI-assisted coding round (first round)"；#8556531（2026-10-05）Atlassian "DSA and AI enabled coding round"。均无题面。
- Reddit r/cscareerquestions https://www.reddit.com/r/cscareerquestions/comments/1wvr0da/ （2026-10-02）标题 "Got rejected in a final round because of how I answered "how do you use AI?""——**非 Abnormal**，只作 Q19（HM 问 "how I used AI in everyday work"）的类比：该问题可以单独致拒。[低，未读正文]
- 意义：AI 辅助代码库题已扩散到 Amazon / Atlassian / JioHotstar，"repo question 很简单、考的是流程与验证"是共同口径。

### S-7 · PracHub 指南 "Abnormal AI Software Engineer Interview Guide"（Updated 2026-09-24，2026-10-09 编排者用浏览器读全文）· [低]（编辑撰写）+ 题库 [中]
URL：https://prachub.com/interview-guide/abnormal-ai-software-engineer-interview-questions-guide-2026
- 页面自述："The stages below are what candidates describe, not a published process."；4 轮 Recruiter / HM / Technical Assessments / Interactive Pair-Programming；各轮正文是通用写法（换公司名即可复用），**不采信为 Abnormal 事实**。`#plan` 是 7 天通用系统设计清单（Numbers before diagrams … Defend it while being interrupted），面向资深候选人，与 AI screen 无关。
- 页面计数："1 Company bank questions · 3 Candidate experiences · 15 Practice prompts · 3 With worked solutions"。3 篇面经 = 已收的 874b1387d9 · 6e26945209 · "Screening Round Built on a Live Security Events Codebase"（付费，2026-10-09 仍未读到正文；页面显示 "Curated and edited by PracHub"，配套题 "Extensible Security-Event Pipeline: Rule Suppression and Plugin-Based Enrichment" = cb01 形态，疑与 LC #8335187 同源）。
- 题目锚点区分 `question-reported-*`（报告过）与 `question-drill-*`（站方自出）。**reported 的 8 题**（逐字标题）：
  - coding："Build a secure file storage vault application with backend and frontend components. Explain how you prompted your AI tool to generate the boilerplate and handle file encryption." → 与 S-1 File Vault take-home 互证；练习 `cb06_filevault`。
  - coding："Implement a rate-limiting middleware for an API endpoint. Show how you use an AI assistant to write unit tests that cover edge cases like concurrent requests and token bucket exhaustion." → `cb06` t3（`TokenBucket` 挂载 + 429/`Retry-After`）部分覆盖。
  - system design："How would you architect a system to detect and mitigate hash collisions in a high-volume photography and metadata storage service?" → 已有 sd03 / pc01。
  - system design："Describe how you would design an end-to-end incident management system that automatically triggers alerts and orchestrates response workflows when a security anomaly is detected." → 已有 ic01 / ic02（形态不同：设计 vs 排查）。
  - system design："Explain how you would structure a distributed data processing job in Apache Spark to analyze historical communication patterns. How do you identify and resolve bottlenecks like data skew?" → **新**。
  - other："Debug a complex Python script that is experiencing memory leaks during large-scale JSON parsing." → **新**。
  - other："How does Python's Global Interpreter Lock (GIL) impact the performance of multi-threaded data ingestion scripts, and how do you bypass these limitations?" → **新**。
  - behavioral：锚点 `question-reported-behavioral-6`，未在技术题分类中展示。
- drill 题（站方自出，不计入报道）：SQL 并发配额（write skew）、按小时汇总去重、webhook 多签名校验、限流响应语义、网关 p99 五分钟尖峰（cache stampede）。
- 独立性：reported 题没有日期与来源，可能来自同一批面经的改写；#refs 不另计，只作题型佐证。

## 2. 本次新增 3 条最重要事实（摘要）

1. 公开可见的 take-home 模板仓库 "Abnormal File Vault"（Django/DRF）+ Gen-AI 屏幕录像要求（S-1）。
2. 2026-09 仍有印度区域的 DSA/图 OA，限定 Java（S-2/S-3）——与"全是 AI 题"不一致。
3. 公司内部已把 Claude Code 用在 CloudWatch/Prometheus 排障（S-4）。

## 3. 数量

| 可信度 | 条数 |
|---|---:|
| 高 | 2（S-4, S-5） |
| 中 | 2（S-1，含 ~15 个仓库；S-2） |
| 低 | 2（S-3, S-6） |
| Telegram / Reddit / HN / Blind 新帖 | 0 |

## 题型地图

> 证据列：**Q/F/O** = 本 kit 已有 Abnormal 来源编号；**S** = 本文件；**类比** = 其它公司 AI 轮（`ai_screen_format.md` §C：Meta AI-enabled coding F-15/F-16、Pocus AI-native screen F-18、alexcloudstar F-17；以及本文件 S-6），**不是 Abnormal 的报道**。
> 已有练习：cb01 t1 规则抑制 · t2 enrichment 插件 · t3 告警去重（sentinel）；cb02 t1 离职外泄检测 · t2 alert cases · t3 GDrive 连接器（insiderwatch）；cb03 t1 协同申请人图 · t2 Workday 数据源 · t3 审核反馈（vetting）；cb04_quarantine = 埋雷 bug + 生产化加固 + burst 规模；cb05_rulelang = 表达式解析器 + detector 拓扑排序 + blast-radius BFS。`cr01` / `ic01` / `sd01` 是别的轮次的练习。

| # | 题型 | Abnormal 风味的具体例子 | 证据 | 已覆盖于 | 缺口 |
|---|---|---|---|---|---|
| 1 | 在已有代码库上做 feature 扩展（含故意含糊） | "让客户抑制规则（含 geo-ip 等复杂条件）"；"给 insider-risk 管线加离职前外泄检测" | Q1 · Q5 · Q6 · Q7 · F-12/F-13/F-14（Abnormal，直接）· 官方 "intentionally underspecified feature" | cb01 t1/t3 · cb02 t1/t2 · cb03 t1/t3 | 否 |
| 2 | 插件 / 可扩展性（把硬编码改成可配置） | "enrichment 层硬编码 geo-ip/history，客户要不改平台代码就能加" | Q2 · Q3（Abnormal，直接） | cb01 t2 | 否（只有一份领域；cb02/03 无插件票，但 cb01 t2 已练到机制） |
| 3 | 修埋雷 bug | 管线里 off-by-one 的时间窗、时区、重复计数；"Meta 式 bug 不是算法题" | 类比：F-16（"a type cast that breaks an assumption elsewhere, an off-by-one, a wrong conditional, a missing visited-set"）· F-18（Pocus 三个递增 bug）；Abnormal 侧无报道 | cb04_quarantine（planted bugs） | 否（Abnormal 侧证据弱，已按类比覆盖） |
| 4 | 生产化加固（幂等、重试、校验、可观测） | 摄取端 malformed event 隔离到 quarantine、重试+死信、指标 | 类比：F-3（"Make Every PR Prove Itself"，官方文化）· 官方 "ship a working v1 that fits the system"；Abnormal 面经无直接报道 | cb04_quarantine（production hardening） | 否 |
| 5 | 规模 / 性能（burst、吞吐、内存受限） | "事件突发 10x，如何不丢不重"；"内存有限时找重复文件" | Q13（扩容后续讨论，Abnormal）· Q16/S-1（dedup + 内存受限，Abnormal 旧流程与 take-home）· Q10 | cb04_quarantine（burst scale）· pc01（旧流程去重）· sd01 | 否 |
| 6 | 数据源集成 | "新增 Google Drive/Workday 数据源，字段映射、分页、增量游标" | O-1/O-4（官方产品页：M365/Google/Slack 等）· JD；Abnormal 面经无直接报道 | cb02 t3 · cb03 t2 | 否 |
| 7 | 算法核心（图 / 拓扑 / 解析 / DP / 回溯 / 数据结构设计） | "按依赖顺序跑 detector（拓扑）"；"规则表达式解析器"；"爆炸半径 BFS"；"每用户平均 session 时长" | Q28（Abnormal SRE CodeSignal，设计类）· S-2/S-3（印度 OA "graph based question … only in java"，**直接**）· Q25（JSON Schema parsing，旧 OA）· Q16 | cb05_rulelang（解析 + 拓扑 + BFS）· cb03 t1（图关联） | **部分：DP / 回溯 / 通用数据结构设计（LRU、限流器、Underground System 类）无练习；若 Chi 的通路含 DSA OA（印度路径）则需补；SWE II-Insider Risk 美国路径无此报道** |
| 8 | 从 README 起步的 greenfield / 预置脚手架 + 要求补全 | "File Vault"：去重存储 + 搜索过滤 + 配额 + 存储统计 + metrics（Django/DRF） | S-1（Abnormal take-home，**直接**，2025-06 → 2026-07）· Q23/Q24（Glassdoor SG 2026 "develop an application … how you prompt AI"）· Q26 | **无**（cb01–05 都是"已有管线"，没有"薄脚手架 + 写一个小产品"的 Django 题；`pc01` 只是旧流程去重算法） | **是**（take-home / 区域路径；也可作为 AI screen 前 10 分钟 "从 README 读起" 的形态） |
| 9 | 用 AI 做 code review（PR / 小仓库，P0/P1 排序） | "给一个小仓库做 review，按 P0/P1 排序、给修法" | Q12 · Q14 · Glassdoor 2026-04（"Code review & fix implementation with AI"）· F-13（Abnormal，直接）· F-3 | cr01（03_code_review，**别的轮次**） | 否（但 cb 系列没有"AI screen 内的 review"；cr01 已覆盖） |
| 10 | 调试失败的测试套件 / 回归 | "CI 红：3 个 pytest 失败，其中一个是 flaky"；让 AI 排查 | 类比：F-18（Pocus：不许直接让模型找 bug）· F-16 · S-4（内部用 Claude Code 排障）；Abnormal 面经无直接报道 | cb04_quarantine（planted bugs 含失败测试时）· ic01/ic02（线上而非测试） | 否 |
| 11 | 并发 / 竞态 | "两个 worker 同时处理同一用户 → 重复告警 / 配额超卖；check-then-act；幂等键" | Q13（"Concurrency / Parallelism / Worker scaling / Message queue scaling … Failure scenarios"，Abnormal，**直接**，但是讨论题）· S-1（quota 强制，dedup 引用计数天然有竞态） | cb04_quarantine（burst 只测吞吐，**未测竞态正确性**）· sd02 讨论 | **是**（缺"写代码证明竞态并修"的练习） |
| 12 | API 设计（REST/契约、分页、错误码、向后兼容） | "给 alert case 暴露 API：创建/分配/关闭、乐观并发、分页、幂等 POST" | Q1/Q2 原文含 "created apis on top of it"；S-1 端点；官方 "think about the user, not just the code" | cb02 t2（alert cases）· cb01（API 层只是附带） | **部分**（无以"先定契约再实现"为核心的票；若面试官只给一句话需求要求设计 API，则需补） |
| 13 | 产品内的 LLM / prompt 功能 | "为 alert 生成一句人话摘要 / 让 LLM 给检测结果分类，要处理幻觉、成本、评估" | O-n（Abnormal 官方：AI Security Mailbox、AI Phishing Coach 等）· 类比：任务书 "Abnormal 把 AI 做进产品"；**无任何面经报道此题型** | **无** | **是**（证据弱：仅类比；优先级低于 8/11） |
| 14 | 代码库阅读 / walkthrough + 扩展讨论 | "解释这个代码库怎么工作，再讨论可能的扩展" | Q5 · F-12/F-14 · 官方 ~10 min 探索 | 每个 cb0x 的 walkthrough.md / REPORT | 否 |
| 15 | 面试官改题 / 模糊澄清（过程型，不是题型） | "sorry I gave the wrong question and it was still a vague question" | Q1（#8335187） | `ai_screen.py` real 模式 · REAL_QUESTION.md | 否 |
| 16 | 事故排障（AWS，日志/指标）——**后续轮**，但可用 AI | "AWS 环境里排查一个 incident" | Q8 · Q9 · S-4（官方 on-call + Claude Code） | ic01 · ic02 | 否 |

**缺口行（gap = 是 / 部分）**：#8 greenfield/脚手架 take-home（File Vault，有直接证据 S-1）· #11 并发/竞态（有 Q13 直接证据，但现有练习只测吞吐）· #12 API 设计（部分）· #7 DP/回溯/通用数据结构（部分，仅印度 OA 路径证据 S-2/S-3）· #13 产品内 LLM/prompt 功能（仅类比，优先级低）。
