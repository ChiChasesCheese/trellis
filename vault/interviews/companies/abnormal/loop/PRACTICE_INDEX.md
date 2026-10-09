# 练习总表 · 按可信度排序

> 排序只看一件事：**这道题和真实面试一致的把握有多大**。同档内按"离下一轮（AI Technical Screen）多近"排。
> 证据编号：`Q-n` = `catalog/raw/questions_reported.md` · `GD-<id>` = `catalog/raw/glassdoor_2026-10-09.md` 的 review id · `S-n` = `catalog/raw/ai_round_sweep_2026-10-07.md` · `LC #` = LeetCode Discuss 帖号。
> 入口：AI screen 题 `python3 loop/ai_screen.py start <cb> <t>`；其他轮 `python3 loop/mock.py start <id>`（都在 kit 根目录跑）。每道 AI screen 题的逐场脚本在 `loop/rounds/01_ai_screen/<cb>/walkthrough.md`。

## A · 一手原题 / 原代码库形态（HIGH）

| # | 练什么 | 依据 | 入口 | 时长 |
|---|---|---|---|---|
| A1 | **cb01 real**：富化层写死 → 插件机制（面试官口述版） | LC #8335187 原文（2026-06-15）· PracHub 同题标题（S-7） | `start cb01 real` | 60 |
| A2 | **cb01 t1**：用户自定义规则抑制（含 geo-ip 这类复杂条件） | LC #8335187 题①原文 · **GD-104787687 "was given Sentinal code base - asked to implement a rule engine"**（2026-07-15） | `start cb01 t1` | 60 |
| A3 | **cb05 t1**：客户自写检测规则的表达式语言（tokenizer + 递归下降 + 求值） | 同 GD-104787687 的 "rule engine"；题面是本 kit 构造，**概念 HIGH、具体形态 MED** | `start cb05 t1` | 60 |
| A4 | **cb01 t3**：告警去重 | LC #8335187 的代码库形态 + PracHub 题标题（reconstructed，第三张票没有原文） | `start cb01 t3` | 45 |

A 档每题至少做两遍，第二遍换一种设计（例如 A1：目录发现 vs 配置写模块路径）。

## B · 一手报告过的轮次与题型，具体题目未披露（MED）

| # | 练什么 | 依据 | 入口 | 时长 |
|---|---|---|---|---|
| B1 | **cb06 t1–t3**：File Vault（去重 + 并发 · 搜索过滤 · 配额 / 统计 / 限流）+ 5 分钟"我怎么用 AI"录屏 | GitHub 模板与 40 个仓库（S-1）· GD-104243539（2026-06，"24h File Vault"）· PracHub 报告题 "secure file storage vault … how you prompted your AI tool"（S-7） | `start cb06 t1` … `t3` | 各 45–60 |
| B2 | **限流中间件 + 用 AI 写并发与令牌桶耗尽的单测** | PracHub 报告题（S-7） | `cb06 t3` 的限流部分；再加练：给 `TokenBucket` 写并发测试 | 30 |
| B3 | **cb02 t1–t3**：陌生代码库 + 未披露 feature + 测试 + 扩展讨论（格式本身） | LC #8496901 · LC #8387564 · GD-104679337（"prompting claude code"）· GD-105890472（2026-10-08）· GD-102948019（Cursor） | `start cb02 t1` … `t3` | 各 60 |
| B4 | **cr01 / cr02**：小仓库 code review，P0/P1 排序，再讨论扩展到大规模的行为 | LC #8496901 第 4 轮（Q12、Q13）· Glassdoor 多条 "code review" | `mock.py start cr01_alert_fanout` / `cr02_risk_api` | 60 |
| B5 | **sd02**：worker / 队列扩容、并发、吞吐与失败场景 | LC #8496901 第 4 轮下半（Q13） | `mock.py start sd02_worker_queue_scaling` | 45 |
| B6 | **ic01 / ic02**：AWS 环境里排查 incident（根因 · 信号 · 止血 · 长期修复） | LC #8496901 第 3 轮（Q8）· LC #8387564（Q9）· GD-103339969 / 104329591（"simulation of an on call scenario"） | `mock.py start ic01_ingest_lag` / `ic02_api_5xx` | 45 |
| B7 | **sd01**：给一个已有系统，讲读扩展、写扩展、瓶颈 | LC #8496901 第 3 轮下半（Q10）· LC #8387564（Q11） | `mock.py start sd01_scale_event_pipeline` | 45 |
| B8 | **pc01**：图片 / 文件去重（内存受限、哈希、碰撞） | Q16（一亩三分地 4 帖，2024–2025 旧流程电面）· GD-103260492（2026-02 London，"A question on finding duplicates"） | `mock.py start pc01_image_dedup` | 45 |
| B9 | **Technical deep dive**：讲清楚你做过的技术决定与取舍 | LC #8496901 第 6 轮（因 "judgment" 被 hold）· GD-105890472（AI 轮之后是 technical deep dive） | `../../core/stories/` 里挑 2 个项目，按"决定 → 备选 → 为什么 → 结果 → 现在会怎么改"各讲 5 分钟 | 30 |
| B10 | **3 道概念题**：GIL · JSON 解析内存泄漏 · Spark 数据倾斜 | PracHub 报告题（S-7，无日期） | `study/20-cards/python_runtime_data.md` | 20 |

## C · 题型推断 / 类比（LOW–MED）

| # | 练什么 | 依据 | 入口 |
|---|---|---|---|
| C1 | **cb04 t1–t3**：修埋好的 bug → 推到生产可用 → 突发流量 | HI 开放式最常见题型；Abnormal 无报道 | `start cb04 t1` … `t3` |
| C2 | **cb05 t2 / t3**：检测器依赖的拓扑排序 · 被盗账号影响面的 BFS | HI Patterns；印度路径 OA 有图论题（S-2，单一来源） | `start cb05 t2` / `t3` |
| C3 | **cb03 t1–t3**：候选人身份欺诈（Chi 要进的团队的产品领域） | 0 份面经；领域来自 JD 与产品页 | `start cb03 t1` … `t3` |
| C4 | **HI 开放式 8 题**（Schedulr · LinkLock · Transcribe · Fileshare · Gridbot · LRU · Collaborative Editor · Text Render） | 同类公司的 AI 面试；提交后有 hire 评级 | `loop/rounds/01_ai_screen/hi_practice.md` |
| C5 | **HI 结构化 13 题**（浏览器里的 CoderPad 式：Maze Solver、Task Scheduler、Kitchen Orders …） | Meta / LinkedIn 风格，算法 + 限制版 AI | hellointerview.com/practice/ai-coding（Structured） |

## D · 长期编码能力（无面试证据，按 kit 题型配对）

每道都对应上面某个题型。用 T7 的方式做（先写测试，再让 AI 实现，你审），练的是同一套方法。

| 题型（对应） | LeetCode | 练到什么程度算过 |
|---|---|---|
| 去重 / 内容寻址（B1 B8） | 609 Find Duplicate File in System · 1166 Design File System · 588 Design In-Memory File System | 能讲清哈希碰撞与大文件分块哈希 |
| 限流 / 计数窗口（B2） | 359 Logger Rate Limiter · 362 Design Hit Counter | 写出令牌桶与滑动窗口两种，并说清各自的取舍 |
| 时间范围查询（B1 t2） | 981 Time Based Key-Value Store · 635 Design Log Storage System | 二分 + 边界含不含说得清 |
| 表达式解析（A3） | 150 Evaluate Reverse Polish Notation → 227 Basic Calculator II → 224 Basic Calculator → 394 Decode String | 不看题解写出递归下降，优先级与括号一次写对 |
| 拓扑排序（C2） | 207 Course Schedule → 210 Course Schedule II → 269 Alien Dictionary | Kahn 算法 + 环检测并报出环上的节点 |
| 图 / BFS（C2 · S-2 的 OA） | 200 Number of Islands → 994 Rotting Oranges（按时间层推进）→ 127 Word Ladder | 入队即标记；层数截断写对 |
| 关联 / 合并身份（C3 t1） | 721 Accounts Merge（并查集） | 能说出"两类标识重合才合并"如何改写 |
| 告警窗口合并（A4） | 56 Merge Intervals · 253 Meeting Rooms II | 半开 / 闭区间的选择说得清 |
| 缓存（C4 LRU） | 146 LRU Cache · 460 LFU Cache | O(1)，并发时加锁的位置说得清 |
| 并发与队列（B5） | 1188 Design Bounded Blocking Queue · 1242 Web Crawler Multithreaded · 1114 Print in Order | 能讲清锁、条件变量、背压 |
| 会话统计（SRE 报道 Q28，低相关） | 1396 Design Underground System | — |

## 怎么用

- 下周一之前：A1–A3 各两遍 + B1 t1 + B3 t1（这 6 场覆盖了把握最大的部分），其余按 `loop/rounds/01_ai_screen/WEEK_PLAN.md`。
- 面试之后：按 B → C → D 的顺序继续。D 档每周 4–6 题，配合当周的 kit 题型，一个月后再回头重做 A 档，用计时来对比。
