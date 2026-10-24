# Chinese aggregators and GitHub mirrors — TikTok / ByteDance

Collected 2026-10-24. Window 2025-10 to 2026-10-24. CodeTop frequencies are not collected here (orchestrator already merged them into `index.json`).

## 0. GitHub search log (step 0 of the method)

`gh api -X GET search/repositories` queries and what was kept. Searches run: "tiktok interview", "bytedance interview", "字节 面经", "字节跳动 面经", "tiktok oa", "tiktok system design", "company wise leetcode", "job-compass"; `search/code`: "tiktok phone screen", "字节跳动 面经 后端", "bytedance interview onsite", "TikTok USDS interview".

| Repo | Pushed | Verdict |
|---|---|---|
| atomeocean/job-compass | 2026-10-23 | KEPT: 12 ByteDance/TikTok reports (section 1) |
| wearzdk/interview-experience | 2026-10-24 | KEPT: auto-mirror of Nowcoder / Maimai, 3544 reports, 289 mention ByteDance/TikTok/抖音/飞书 (section 2; detail in `forums_cn.md`) |
| emmazhang-ai-sde/shuyangzhang-leetcode-notes (`docs/tiktok-interviews`, `docs/tiktok-leo-10-20`) | 2026-10-23 | KEPT: 126-record structured TikTok 面经 compilation (107 in window) and a 30+20 question TikTok docx (sections 3, 4). Found by code search "TikTok USDS interview" |
| DerekLin924/interview-experience-collection | 2026-10-22 | index only: links to Nowcoder 专栏 zhuanlanId=04ypb2 "字节面经-字节跳动后端开发岗面经-01..19" (+ Agent 01..., 测开 01..15); the 19 backend pieces are mirrored in section 2. No text. |
| Imironman123/llm-interview-notes | 2026-10-21 | seen: ByteDance LLM-algorithm 复盘 (`10_字节跳动大模型面试...md`, `11_字节跳动大模型面试复习手册 2025至2026.md`), algorithm / MLE oriented, not opened for backend. low relevance |
| kevin-2023-code/Tech-Interview-Questions `companies/bytedance/*` | - | seen: generic process pages (English), SEO-style; not used |
| jugaldb/faang-interview-prep `docs/companies/tiktok.md` | - | seen: English company page, left to the EN kit |
| lmiztbrv/tiktok-interview-patterns, AlexiosNine/tiktok-algorithm-prep, uniyalVJ/TikTok, cantaible/tiktok-interview, Thea-xuyang/tiktok-interview, basav16/tiktok-interview-prep | 2025-2026 | seen: English SEO article, a quiz site, or unrelated course work (Thea-xuyang = SQL homework "submitted to ByteDance"). Not used. Do not cite lmiztbrv (reads as an SEO farm). |
| resumejob/interview-questions, 0voice/*, aylei/interview, colourful987/bytedance-alibaba-interview, rhwayfun/interview, lwlpyl/ByteDance | 2019-2025 | pre-window (2019-2024 校招/社招 notes); background only, not recorded |
| yugef3h/interview-yuge, CocaineCong/Golang-Interview | 2022-2026 | generic Q&A, not dated reports |
| afatcoder/LeetcodeTop | - | CodeTop-style frequency list; skipped by instruction |

Reachability notes: GitHub API fine; `git clone --depth 1` fine. Nowcoder pages (`nowcoder.com/discuss/<id>`, `/feed/main/detail/<uuid>`) fetch directly with a browser UA (200) and carry the body inside `window.__INITIAL_STATE__`; the search API `POST https://gw-c.nowcoder.com/api/sparta/pc/search` (body `{"type":"all","query":"...","page":1,"order":"create","tag":[],"companyTag":[]}`) works without login. WebSearch for 知乎 / 掘金 / CSDN returned nothing usable for 2026 (results were 1point3acres tag pages and old jiangren.com.au process pages).

## 1. atomeocean/job-compass (`docs/zhHans/interview-experience/{tiktok,bytedance}`; pages created 2025-12 .. 2026-10-23; site https://jobcompass.atomeocean.com)

Source repo https://github.com/atomeocean/job-compass. The page text is a hand-edited re-write of community posts; file path given as the URL tail.

- tiktok/bozm71 | page 2026-10-17 | TikTok MLE, E-commerce, San Jose or Bellevue onsite | recruiter written screen (timeline, work authorization, relocation), two technical rounds booked together, round 2 cancelled if round 1 fails. Round 1: project discussion (model choice, data, evaluation) + ML basics (self-attention formula, Q K V dimensions, why divide by sqrt(d_k), multi-head, complexity vs length, class imbalance and precision / recall / AUC) + coding "LeetCode medium" at the level of LC 347 Top K Frequent Elements + CS basics + work history / some system design. Result: fail, rejection 2 days later. conf medium (MLE).
- tiktok/o8aelo | source date 2025-03 (page 2026-10-01) | TikTok MLE new grad (CV/NLP/multimodal/LLM), Lark video, 45-60 min | project discussion + coding at level of LC 200 Number of Islands + CS basics; round 2 deeper: attention formula / dimensions, normalization layer, regularization, skip connections. "TikTok wants the result to run, must pass." Result: rejected. conf medium (pre-window event; process facts only).
- tiktok/tiktok-sde-intern-1 | event 2025-03-14 (pre-window) | backend intern (payment), referral, Chinese interviewer | OS memory management, HashMap + collision, rotate-print a matrix, finance-theory BQ. Fail after 4 days. conf medium. Process background only.
- tiktok/tiktok-sde-intern-2 | event 2025-04-21 (pre-window) | backend intern | microservices / Java / multithreading probing, Oracle vs MySQL, coding: binary search for the smallest value greater than the target in a sorted array + boundary follow-up. Fail. Background only.
- tiktok/xmc27l | 2025-11-01 (source: Xiaohongshu note "TIKTOK 10.31 NG SDE面试" by 湾区发型师, https://www.xiaohongshu.com/explore/6906628c00000000070084a6) | TikTok SDE new grad | round 1: resume (AI projects), linked-list kinds, de-duplicate a singly linked list and a doubly linked list, then "where does TikTok business need list de-dup"; round 2 HM from an unrelated team, 45 min mostly about AI. Result: Offer. conf medium (in window).
- tiktok/k9f2q7 | page 2025-12 | TikTok PM (5 rounds) | product, content-governance: complaints vs growth trade-off, complaint-rate reduction plan, metrics, cross-team conflict, failed-decision reflection. conf low (PM, not backend).
- bytedance/bytedance-sde-ng-1 | 2025-08-26 (just before window) | ByteDance North America new-grad backend (e-commerce), first technical round | resume / microservice / sharding questions, networking (3xx codes, TCP vs UDP, DNS), OS (virtual memory, process, coroutine, producer-consumer), algorithm **LC 43 Multiply Strings**. Fail. conf medium.
- bytedance/bytedance-sde-ng-2 | 2025-09-26 | NG backend data platform | Hive layering, partitioning, TCP retransmission, 4-way close, kernel mode; algorithms **LC 162 Find Peak Element** then "find a target in a mountain-shaped array" (peak then two binary searches); BQ. Fail. conf medium.
- bytedance/bytedance-sde-ng-3 | 2025-10-17 | NG backend, automated-testing org | 25 min left for **count inverse pairs in O(n log n)** (剑指 Offer 51 / merge sort); resume-only first part (service architecture, QPS, data quality checks, DevOps stages, abnormal-data triage, sharding / master-slave). Status waiting. conf medium.
- bytedance/v2na3e | source post 2026-05-25 (1P3A thread 1177932) | Senior SRE | R1 project + easy system design + easy LeetCode (15 test cases run), R2 Linux theory + shell script + medium LeetCode; thank-you letter the next day. conf medium.
- Also in repo but different company: rednote/rednote-ny (mentions TikTok comparison), interview-prepare/8-bit-career.

## 2. wearzdk/interview-experience (面灵面经 mirror, https://mj.mianlingai.com)

3544 Markdown reports; 289 with a ByteDance / TikTok / 抖音 / 飞书 / 懂车帝 company field or tag, all `date` between 2026-01 and 2026-10 (month only; counts: 2026-10 83, 2026-09 78, 2026-08 31, 2026-07 34, 2026-06 11, 2026-05 11, 2026-04 24, 2026-03 16, 2026-01 1). Every report names source 牛客网; about half have a Nowcoder URL (`sourceUrl`). The "参考解析" blocks are AI-written; only the problem lists come from the poster. The per-report catalogue (213 backend / full-stack / agent-dev reports; 171 with a named algorithm or design prompt) is in `forums_cn.md` section 3, with the mirror URL pattern `https://mj.mianlingai.com/interview/<file-name-without-.md>`.

TikTok-labelled backend items in the mirror: `bytedance-ai-backend-first-round-2830567` (2026-04, TikTok AI backend R1: **LC 224 Basic Calculator**, 10k producers / 50k consumers concurrency design, RAG, MySQL vs Redis), `bytedance-backend-first-round-2925500` (2026-10, TikTok international live base business, intern R1: "design a TikTok live-room like system", flash-sale, LC 152, LC 200), `bytedance-backend-interview-1-2833873` (2026-04, international payment R1, DDD, distributed transactions, **LC 567**), `bytedance-tiktok-backend-intern-second-round-2929684` (2026-10, TikTok backend intern R2, "design a high-concurrency live-room comment system", **LRU**), `tiktok-ai-backend-second-round-2825446` (2026-04: Newton sqrt, count ways 10 shots sum to 80), `tiktok-backend-2901760` / `tiktok-backend-2905920` (2026-09, TikTok backend R1/R2: invoice-rule engine with QLExpress, "design a highly available distributed file storage so files are never lost", agent loop with checkpoint / resume, permutations), `bytedance-global-ads-backend-intern-933056720308305920` (2026-09, international ads, K-group reverse variant, hex big-number multiply), `bytedance-international-ad-crm-2903637` (2026-09), `bytedance-java-2910816` (2026-09, international ads R2: best time to buy and sell stock once).

Senior-flavoured items (社招) in the mirror: `bytedance-interview-920379874269794304` (2026-08, "3年经验 ... 四面终于OC": distributed cache with range queries, Redis-based distributed rate limiter with sliding window and token bucket, **IM for 10M DAU**, spike of 10x QPS), `bytedance-interview-921465359255752704` (2026-08: local cache with expiry, distributed rate limiting, **IM 10M DAU**, **flash sale**), `bytedance-java-backend-931517876673007616` (2026-09: ConcurrentHashMap, ThreadLocal in pools, full GC, MVCC + gap locks, MQ no-loss; R2 **e-commerce big-promotion system for 100M traffic** + TCC / SAGA / eventual consistency incl. empty rollback and suspension; R3 cross interview **full-link load-test platform**), `bytedance-java-backend-934417678071058432` (2026-09, 5 years: virtual threads, GraalVM; R2 **serverless function platform with millions concurrency**; R3 P0 incident), `bytedance-ai-platform-924248590447280128` (2026-06, AI platform 4 years: dynamic-batching request queue, multi-model hybrid inference platform, AIGC content moderation), `bytedance-backend-2929706` (2026-10, 社招 R3: kth node from the end of a linked list). The first five use a template with emoji numbering and "思路参考" blocks, so treat them as conf low (possible content-farm rewrite).

## 3. emmazhang-ai-sde/shuyangzhang-leetcode-notes — "tiktok-jiajun-08/26" (TikTok 面经 PDF, 18 pages, anonymous compilation)

Repo https://github.com/emmazhang-ai-sde/shuyangzhang-leetcode-notes, path `docs/tiktok-interviews/interviews.json` + `source-pages.md`. 126 dated records 2025-01-27 .. 2026-08-12 plus 65 undated high-frequency references; 107 records fall inside the window and are listed below (newest first). Dates are the PDF's own markers, not verified as interview dates. LC numbers: explicit in the PDF, or "candidate" matches by the repo's maintainer (marked in the JSON; treat as medium). Role is mostly SWE (several USDS, Growth); level seldom given. Confidence: medium (summary of an unnamed compilation that names the problem). Likely duplicates of 1P3A threads are cross-referenced in section 5.

- TT-001 | 2026-08-12 |  | 
  - raw: bq techinical challenge 项目 Coding:course schedule
  - coding: Course Schedule [LC207]
  - BQ: technical challenge
- TT-002 | 2026-08-11 |  | 
  - raw: 前面深挖简历，问了一些项目设计和衍生的八股，后面才开始编码。 编码题不难，两个带正负号的字符存 储相加，注意负号
  - coding: 两个含正负号的字符串表示的数相加
  - tech: 基于项目的八股
- TT-003 | 2026-08-09 |  | 
  - raw: 简历深挖，问了很多细节比如数据模式，为什么要这么设计等等 然后围绕项目八股 CAP、索引、并发 然后 LC lru
  - coding: LRU Cache [LC146]
  - tech: CAP; 索引; 并发
- TT-004 | 2026-08-09 |  | 
  - raw: 变种的 695
  - coding: 岛屿最大面积变种 [LC695]
- TT-005 | 2026-08-07 |  | 
  - raw: 大概 60 分钟，前面 45 分钟挖简历上的项目，会问的很深，甚至会问到对整个 infra 的了解， 以及为什么 组织级别上为什么这么设计。10 分钟刷题。 一个漫长的回文字符子串。
  - coding: 回文子串题，原文“一个漫长的回文字符子串” [LC5]
- TT-006 | 2026-08-07 |  | 
  - raw: 面试询问简历里的项目。 然后进行二进制搜索。
  - coding: 二分搜索题，具体题意未给
- TT-007 | 2026-07-30 |  | 
  - raw: 拷打简历 40 分钟，挖的比较深，会考到你用的技术细节，留了不到 20 分钟做题。 LC 题目不长。给一个数字 N，和 1 个数组 A，里面有 0-9，可以用无限次数组内的数字， 来组成一个小 于 N 的最大数。 比如，N=23415，A={2, 4, 9}, 输出 22999 idea 应该是从左往右 greedy+backtracking。
  - coding: 使用给定数字集合无限次，组成严格小于 N 的最大数
- TT-008 | 2026-07-29 |  | 电话面试
  - raw: 45 分钟电话屏幕，先简历聊然后正常做题，两个题，子排列和为 k 的个数，以及最后无重 复子字符串长 度。总共做题也 10 分钟，剩下都是简历和反向 BQ
  - coding: 和为 k 的子数组个数 [LC560] ; 最长无重复字符子串长度 [LC3]
- TT-009 | 2026-07-24 |  | 第一轮,第二轮,第三轮
  - raw: 第一轮面试 55 分钟，挖了下简历，问了一下对 LLM 应用的看法，给了一道 LC239 原题。 第二轮面试 45 分钟挖简历，问了一下如何在他们现有的系统上运用 LLM。问完给了一道 LC424 题 第三轮面试 聊了 45 分钟的八股文。最后给了两道题: 第一道只问的思路(答了最优解用 QuickSelect);第二道 LC33，写了逻辑正确的代码
  - coding: 滑动窗口最大值 [LC239] ; 最长重复字符替换 [LC424] ; 未具名的 QuickSelect 题 ; 搜索旋转排序数组 [LC33]
  - tech: 第三轮约45分钟八股，细目未给
- TT-010 | 2026-07-24 |  | 
  - raw: 上来先问问简历，然后开始 coding 问了一些工作中遇到了什么样的 technical challenge, 直接给了 25 分钟左右的时间 coding 题目 merge interval
  - coding: 合并区间 [LC56]
  - BQ: 工作中遇到的 technical challenge
- TT-011 | 2026-07-19 | team=USDS | 
  - raw: USDS 组 coding meeting room II 和 III design 设计聊天室弹幕
  - coding: Meeting Rooms II [LC253] ; Meeting Rooms III [LC2402]
  - SD: 聊天室弹幕系统
- TT-012 | 2026-07-18 | team=USDS | 第一轮：经理面,第二轮：IC
  - raw: USDS 组 第一轮是经理面，面的题是实现一个 In-memory KV Store 并且支持 snapshot 和 restore。具体 难点应该是 怎么写 seder  第二轮是一个 IC，面了两题，第一题是 LC430 变种，主要是 nested node 那个节点数值为空， 所以要排除 在外。第二题是 LC124，dfs+dp
  - coding: 实现内存KV存储，支持snapshot与restore ; 扁平化多级链表变种，nested空值节点需排除 [LC430] ; 二叉树最大路径和 [LC124]
- TT-013 | 2026-07-15 | team=USDS | 第一轮
  - raw: USDS 组 第一轮面试 首先问了下 BQ，最喜欢的 project，技术难点在哪。 Coding2 题 1. warm up Input integer array, return most frequent element, if tie, return the smaller number 扫一遍，frequency 写入 map, 同时更新最大 freq 的 k, v, 如果 v 和最大的相等，记录小的 key.  2. Tree, (not binary), each node has a value, 
  - coding: 整数数组最高频元素；并列时返回较小值 ; N叉树只允许节点值加1，使所有根到叶路径和相等的最少操作 [LC2673]
  - BQ: 最喜欢的project及技术难点
- TT-014 | 2026-07-14 |  | 
  - raw: 先问了简历+衍生的八股 coding 考的是 lc316
  - coding: 去除重复字母 [LC316]
  - tech: 基于简历的八股，细目未给
- TT-015 | 2026-07-08 |  | 
  - raw: 自我介绍+聊简历 Coding 经典岛屿题，followup 让算边界
  - coding: 经典岛屿题，具体基础题意未详述 [LC200] FU: 计算边界（原文未明确是边界单元还是周长）
- TT-016 | 2026-07-07 |  | 
  - raw: coding 题是岛屿数量问题，follow up distinct islands 的数量，LC694 问了复杂度。最后 15mins 问问题。
  - coding: 岛屿数量 [LC200] FU: 统计不同形状的岛屿数量，原文明示LC694 ; 不同岛屿数量（follow-up） [LC694]
- TT-017 | 2026-07-06 |  | 
  - raw: 自我介绍，然后聊了一下项目，之后就是 coding 环节，题目就是类似 LC 的 622，写了一下 代码，边写边 解释了思路
  - coding: 循环队列相关题 [LC622]
- TT-018 | 2026-07-06 | team=USDS | 第一轮coding,第二轮八股,第三轮HM
  - raw: USDS 组 第一轮 coding，两道 easy 到 medium 的算法题，要求跑通所有 test case。不是 leetcode 原题， 但是不 难，会最基本的 binary search 和 dp 就没问题。 第二轮八股，Linux 操作系统，network 系统，docker，K8s 等 第三轮 HM，简历和 BQ，主要考察背景是否 match
  - coding: 两道非LeetCode原题，easy至medium
  - BQ: HM背景匹配 | tech: Linux操作系统; 网络系统; Docker; Kubernetes
- TT-019 | 2026-07-03 |  | 第一轮
  - raw: 第一轮总共一个小时的 video 面 半个小时问了简历，先是简单的自我介绍，然后问做过的 project，project 里的难点还有具 体细节是怎么 实现的，还问了如果从头来的话，这个 project 有没有需要改的地方 15 到 20 分钟写了一题 LC98，要自己写 test case 自己跑
  - coding: 验证二叉搜索树 [LC98]
- TT-020 | 2026-07-02 | team=USDS | 第一轮,第二轮
  - raw: usds 组 第一轮: most common suffix，类似 3093，思路就是建 trie  第二轮:lc 原题岛屿面积，紧接着是要求写地图太大，岛放不进 memory 怎么办。应该是把 地图分块，然 后用 union find 找相邻的地图有没有相邻的岛
  - coding: Most common suffix [LC3093] ; 岛屿面积 [LC695] FU: 地图大到放不进内存；原文建议分块后用并查集合并相邻块中的岛屿
- TT-021 | 2026-06-30 | team=Growth | 第一轮,第二轮
  - raw: Growth 组 一面问了大概 15 分钟简历，coding 题 grid 里找最短路径，follow up 问了如果最多能消除 k obstable 怎么 改  二面问了 30 分钟简历，然后一道 recommendation engine design 题
  - coding: 网格最短路径 FU: 最多能消除k个障碍；候选LC1293 ; 网格最短路径，允许消除k个障碍（follow-up） [LC1293]
  - SD: 二面：recommendation engine design
- TT-022 | 2026-06-27 |  | 第一轮
  - raw: 第一轮 约 60 min，开头简单自我介绍，聊了一些过往项目，主要是后端系统、稳定性、线上问题 处理、 ownership 这类。  Coding 一题，带 follow-up 给一个 sorted array，array length >= 3，找出所有出现频率大于 array length 的 1/3 的数字 例子: [1,2,3] -> [] [1,1,2,3,4] -> [1] [1,1,2,4,4] -> [1,4] [1,2,3,4,5,6,7] -> [] Follow-up: 要求 time com
  - coding: 有序数组中找所有出现频次大于n/3的数 FU: 要求时间复杂度小于O(n)，利用有序条件
- TT-023 | 2026-06-26 |  | 
  - raw: 前 30 分钟过了一遍 resume，讲了一些 project 和项目。BQ 很常见的之前最困难的项目是什 么，过了一 些 resume 之前的东西。 Coding LC1248 brute froce
  - coding: 统计优美子数组 [LC1248]
  - BQ: 之前最困难的项目
- TT-024 | 2026-06-25 |  | 一面
  - raw: 一面 总共一小时，前一半介绍项目问了一些 DB、REDIS 和 Kafka 的概念。后半小时出了一 道题 Given a string s, remove duplicate letters so that every letter appears once and only once. You must make sure your result is the smallest in lexicographical order among all possible results. Example 1:  Inp
  - coding: 去除重复字母，保持每种字母一次且字典序最小 [LC316]
  - tech: 数据库; Redis; Kafka
- TT-025 | 2026-06-04 |  | 
  - raw: 面试 1 个小时 前半小时 八股拷问 各种问题 后半小时 LC linkedlist k 个翻转  怎么做 RAG 怎么用的 langraph lanchain Agent 里的 tool 和 MCP 问题 Kafka 的 Rebalance 问题 Kafka 里有 topics 有 partition 有 consumer group - 消费组，消费组消费的是一样的信息吗 Network 的 layer 并发和并行的区别 线程的渐进式加载 Python 的 GIL 锁 Mysql 和 redis 可以互用吗 R
  - coding: 链表每k个一组翻转 [LC25]
  - tech: RAG设计; LangGraph / LangChain（原文拼写langraph/lanchain）; Agent tools及MCP; Kafka rebalance、topic、partition、consumer group; 网络分层; 并发与并行; 线程的渐进式加载（原文措辞）; Python GIL; MySQL与Redis能否互用; Redis持久化; Agent memory及记忆架构; LLM上下文超245k如何处理
- TT-026 | 2026-06-04 |  | 电面,第一次onsite
  - raw: 电面，简历 deep dive，问了真实系统中一些异常场景怎么处理。 LC:875。先暴力，再优化，需要每一行 分析时间复杂度，不用跑 case。 1st onsite 照旧简历 deep dive。LC43，需要自己写一些 case 跑
  - coding: 爱吃香蕉的珂珂 [LC875] ; 字符串乘法 [LC43]
- TT-027 | 2026-05-30 |  | 
  - raw: 挖了 20 分钟简历。主要问题是 hardest project，遇到什么 edge case，深挖这个项目的详细 细节 之后做了一道 lc437 变种， tree 从 binary 变成了 N ary Tree。
  - coding: 路径总和III的N叉树变种 [LC437]
- TT-028 | 2026-05-16 |  | 第一轮,第二轮,第三轮：中文面
  - raw: 第一轮:一道包含连续 1 的最长 subbarray 的题 sliding window 就能秒 follow-up 是 2D array 第二轮:简历+ 题目是 LRU 第三轮:中文面 45 分钟的流程如下: 疯狂拷打简历 抓着工作经历疯狂挖 甚至挖一些当时并没用过但是觉得'why not use that'的 技术栈  问了一堆八股 涉及的话题什么都有 甚至是大学课本和考试上的填空题这种东西 口头抛给一道类似 SD 的 题 只有两句话描述 没有任何其他提示 但是这是一道 topK 的变种 也算答出来了整体框架 
  - coding: 连续1最长子数组 FU: 扩展到二维数组 ; LRU Cache [LC146] ; 口头Top-K变种，描述未给 ; 口头脑筋急转弯，描述未给
  - SD: 第三轮仅两句话描述的类系统设计题，实为Top-K变种，题意不足 | tech: 八股范围广，原文未列细目
- TT-029 | 2026-05-13 |  | 
  - raw: 上来先自我介绍， 问一下工作经历 15 分钟， 紧接着 n 皇后，两个 test case 跑通，时间复 杂度分析做完 之后还剩 15 分钟问八股。最后拖延了 5 分钟问问题。
  - coding: N皇后 [LC51]
  - tech: 约15分钟八股，细目未给
- TT-030 | 2026-05-13 |  | 
  - raw: 问了大约 20 分钟左右的项目。然后就开始做题，LC2673
  - coding: 使二叉树根到叶路径代价相等 [LC2673]
- TT-031 | 2026-05-12 |  | 
  - raw: 类似于 LC 904 的变种。a straight line of 糖果 只能拿两种糖果，选一种糖果后必须还要选糖果 next to 这个 的。遇到第三种糖果后就 stop。 问能拿到的最多的糖果的数量。
  - coding: 直线上只拿连续两类糖果，遇第三类停止，求最多数量 [LC904]
- TT-032 | 2026-05-11 |  | 
  - raw: 上来先是面试官自我介绍，然后要求自我介绍 然后面试官提问:为什么选择 Tiktok 下面进入 coding 环节，LC 156 变种，但是加了附加的要求，要求支持 TTL，具体细节就是， TTL 作为附加 参数在调用的时候传进去，然后需要额外考虑 TTL expire 的情况 大概讲了下解题思路，就是用双链表，不 同的地方就是需要加入处理 TTL 过期的情况，如果 过期了，需要删掉，这样就相当于这个值不存在，然后 再操作 之后开始码代码。题目本身已经是 hard 难度，又要处理 TTL， 所以整个代码量还是比较大，
  - coding: 带TTL过期管理的缓存；原文写LC156 [LC156,146] FU: 每次调用传入TTL；先处理过期删除，再做后续操作；目标O(1)
  - BQ: 为什么选择TikTok
- TT-033 | 2026-05-08 |  | 
  - raw: 题目本身其实是很常规的 bfs 就是 leetcode 365 以及 followup，能不能找到并且找到最短路径 2 cups，size x, y, unlimited water, 3 operations, 1. fill one cup, 2. empty one coup, 3. pour one to the other. ask if we can get size z by operation chains. need to confirm with interviewer whether we n
  - coding: 水壶问题及最短操作路径 [LC365] FU: 不仅判是否可达，还要找最短路径
- TT-034 | 2026-04-25 |  | 
  - raw: 自我介绍 +behavior 最自豪的项目 lc236 变形 q 不在 tree 情况下 如何处理
  - coding: 最低公共祖先，q可能不在树中 [LC236]
  - BQ: 最自豪的项目
- TT-035 | 2026-04-14 |  | 
  - raw: 面试过程: 询问基本情况 Coding:LeetCode151 写出第一版解法后，面试官让多写几个测试用例，然后让保留空格数 不变修改第一版 代码，并问了算法复杂度让优化。 最后问项目、未来职业规划等等
  - coding: 反转字符串中的单词 [LC151] FU: 保留空格数量不变；多写测试并优化复杂度
  - BQ: 未来职业规划
- TT-036 | 2026-04-12 |  | 
  - raw: 第一题 类似于 course schedule， 第二题，类似于 word ladder，在第一题的基础上加难度，输出最短路径
  - coding: 类似Course Schedule [LC207] ; 类似Word Ladder并要求输出最短路径 [LC127,126]
- TT-037 | 2026-04-09 |  | 
  - raw: 先来 5 分钟自我介绍 然后 HackerRank 共享视频做题 第 1 题:sliding window, easy 秒 Longest Substring with at most K Distinct Characters Description: Given a string s and an integer k return the length of the longest substring of s that contains at most k distinct characters. Input
  - coding: 至多K种不同字符的最长子串 [LC340] ; 带代价、障碍和燃料补充的网格最小代价路径 [LC1293] FU: K很大时，O(mnK)状态过多如何优化
- TT-038 | 2026-04-02 |  | 
  - raw: 先是介绍一个项目然后 dive 进去了，然后问有没有过设计过于复杂的时候，问做过什么事 情对用户体验 提升很大的 题目是 LC 228 的变种，[3,5,10] -> 得出 [[0,2],[4],[6,9]]但是有 lower 和 upper bound
  - coding: 有上下界的缺失区间 [LC228,163]
- TT-039 | 2026-04-01 |  | 
  - raw: 一道 grid 題+ gpt 类似 LC 778 大意是在最少 T 内从左上到右下路径，给了 priority queue 做法和 binary search 思路
  - coding: 网格从左上到右下，最小化可通过时间T [LC778]
- TT-040 | 2026-03-27 |  | 第一轮VO,第二轮Linux+Cloud
  - raw: 第一轮 VO: 1-n 选 k 个数字排列组合不能重复  第二轮考 linux+cloud，以下每个问题都深挖了 5-6 个 follow up Disk full 怎么 troubleshoot。followup(例如到某一步用了某个 command 之后，what would you look for next?)(What if the disk is full but you cannot find large files?)(How would you identify which process is 
  - coding: 从1到n中选k个数，不重复 [LC77]
  - tech: Linux应用部署方式; Linux / cloud深入follow-up
- TT-041 | 2026-03-25 |  | 
  - raw: coding 类似二合 后面就是常规 bq，tell me about a complex problem you solved
  - coding: 原文“coding 类似二合”，题意不足
  - BQ: Tell me about a complex problem you solved
- TT-042 | 2026-03-25 |  | 
  - raw: 给一个 String，先 validate if it's a valid math expression，然后计算。 evaluate expression 类似 LC227
  - coding: 校验数学表达式有效性，再计算 [LC227] FU: 不仅求值，还需validate expression
- TT-043 | 2026-03-25 |  | 
  - raw: 给一个 fixed size 的 array，然后实现 api 有 pushhead pophead pushtail poptail 还有 search 都在 O(1)时间完成
  - coding: 固定大小数组实现双端操作及search均O(1)
- TT-044 | 2026-03-10 |  | 
  - raw: 前 15 分钟问简历然后做题 LC323 变形 isSimilar[j] == 1 代表 photo i 和 photo j 是 directly similar，isSimilar[j] == 0 代表不是 directly similar。如果 A~B&&B~C⇒A~C 问一共有多少 photogroups
  - coding: 相似照片关系的传递闭包，统计photo groups [LC323]
- TT-045 | 2026-03-01 |  | 
  - raw: Valid Parenthesis
  - coding: Valid Parenthesis [LC20]
- TT-046 | 2026-02-27 |  | 
  - raw: 正常流程:先问 project，大概 20~25 分钟，然后一道算法题，最后是 Q&A。 TT 问 project 比较详细，问在做 project 之前有没有考虑过其它比较成熟的 infra，为什么 确定是这个 option;为什么要做这个 project，解决了什么问题;然后 metrics 怎么设置的。 Coding 是给一个 ArrayList 样 式的 String，ArrayList 可能是嵌套的，需要把它转化成 ArrayList，类似于 LC 339;用 stack 即可。 最后还问了一个平时工作怎
  - coding: 解析可能嵌套的ArrayList字符串为ArrayList [LC339,385]
  - BQ: 平时工作如何使用AI
- TT-047 | 2026-02-26 |  | 
  - raw: LC 49 测试定义 node
  - coding: 原文“LC49 测试定义node” [LC49]
- TT-048 | 2026-02-24 |  | 第一轮,第二轮
  - raw: 第一轮:LC827  第二轮:图的拓扑排序
  - coding: 最大人工岛 [LC827] ; 图的拓扑排序，具体题意未给
- TT-051 | 2026-02-24 |  | 
  - raw: 上来做了自我介绍 聊了一下简历上的 project 追问了实习经历 问了什么时候 disagree with manager or teammate coding: 给一串数据流 带时间 日期 和用户名 要求输出一个 list 表示每个用户每天 log in 多少次 按用户名排列 同时要检查错误的日期和时间
  - coding: 统计日志流中每用户每天登录次数，按用户名排序 FU: 校验错误日期与时间
  - BQ: 何时与manager或teammate意见不一致
- TT-049 | 2026-02-21 |  | 第一轮coding,第二轮coding
  - raw: 第一轮 coding 一个小时面试。前五分钟双方简单自我介绍，然后 45 分钟 coding，最后 10 分钟反向 bq。 LC 151 变形。口头跑 test case 都过。follow up 问如何 in place 解，讨论了一下，给了最 优解。  第二轮 coding 一个小时面试，前十到十五分钟 bq，最具挑战的项目，过程中会追问细节。 又问了一下有 没有自己 lead 的 project。 第一题 LC78 第二题 LC90  第三题，LC 1360
  - coding: 反转字符串单词变种 [LC151] FU: 如何原地处理；口头跑测试 ; 子集 [LC78] ; 子集II [LC90] ; 第三题，题意未给 [LC1360]
  - BQ: 挑战最大的项目; 自己lead的project
- TT-050 | 2026-02-18 |  | 一面,二面,三面
  - raw: 一面:Validate parenthesis (含*)， follow up 输出所有可能的 string(dfs)，自己写 test case 跑通。BQ/简历  二面:Smallest index to insert a value in array. Regular expression match. 自己写 test case 跑通。 BQ/简历  三面:八股(Java 有没有用过 linkedhashmap, concurrenthashmap, 有没有 concurrent 编程经 验)。简历深 挖。
  - coding: 含*的有效括号 [LC678] FU: DFS输出所有可能的string；自写测试 ; 数组中插入一个值的最小索引 [LC35] ; Regular Expression Matching [LC10] ; 设计list：rpush/rpop/lpush/lpop/index均O(1) ; 二叉树最大路径和，不要求经过根或叶 [LC124] FU: 打印路径 ; LRU设计 [LC146] ; LFU设计 [LC460]
  - tech: Java LinkedHashMap; ConcurrentHashMap; 并发编程经验
- TT-052 | 2026-02-11 |  | 
  - raw: 简单聊了想项目 问技术上最难的是什么部分 第一题 类似 LC215 第二题 类似 LC15
  - coding: 类似第K大元素 [LC215] ; 类似3Sum [LC15]
- TT-053 | 2026-02-01 |  | 
  - raw: 一题 leetcode49 二叉树右视图
  - coding: 二叉树右视图；原文写leetcode49 [LC49,199]
- TT-054 | 2026-01-29 |  | 
  - raw: LC2385，但必须用最优解
  - coding: 感染二叉树需要的总时间 [LC2385]
- TT-055 | 2026-01-29 |  | 
  - raw: 首先介绍了简历上的相关项目并相应提问细节 两道简单题介绍思路写代码不要求编译通过和运行 删除链表的倒数第几个节点 二叉树删除节点后重新连接
  - coding: 删除链表倒数第N个节点 [LC19] ; 删除二叉树节点并重连，题意不足
- TT-056 | 2026-01-28 |  | 第一轮technical coding,第二轮technical coding,第三轮HM behavioral
  - raw: 总共三轮，2 technical coding(each 60 min)+ HM behavioral(45 min) 第一轮 coding:一开始 5-10 分钟问简历，主要聊之前的 internship / project，在做什么， 用什么 tech stack，然后直接开始 coding。第一题是 LeetCode Longest Substring Without Repeating Characters，用的 sliding window + hashmap，写完之后让 analyze time com
  - coding: 最长无重复子串 [LC3] ; 柱状图最大矩形面积 [LC84] ; 数组步长1或2，从index0走到最后一个index的最小总代价 [LC746] ; 最长回文子串 [LC5]
  - BQ: Challenging project; Conflict with teammate; Handle ambiguity; A time you failed; Prioritize tasks
- TT-057 | 2026-01-22 |  | 
  - raw: 先拷打了一下简历，问得还挺细，基本都是围绕写过的项目展开，确认是不是自己真的做过。 JavaScript 部分  What is the rest parameter 基础题，考察对 ES6 的了解 Coding 岛屿数量 (DFS+BFS)
  - coding: 岛屿数量 [LC200]
  - tech: JavaScript rest parameter; ES6基础
- TT-058 | 2026-01-18 |  | 
  - raw: 基本前 20min 八股+后 40min LC210
  - coding: Course Schedule II [LC210]
  - tech: 前20分钟八股，细目未给
- TT-059 | 2026-01-16 |  | 
  - raw: 一共 1 小时，30min pride project + 30min coding (Leetcode 694)
  - coding: 不同岛屿数量 [LC694]
- TT-060 | 2026-01-16 |  | 
  - raw: coding 1 hrs coding 一题 binary search 变形题 most channelling work how kafka work design a distributed kv
  - coding: 二分搜索变种，具体题意未给
  - SD: 分布式KV | BQ: most challenging work（原文channelling） | tech: Kafka如何工作
- TT-061 | 2026-01-09 |  | 
  - raw: 一上来先问了 bq，问得很深但并没有问八股 之后 20 分钟做题，一个很经典的 lc medium sliding window，然后会问一些简单的 follow up.
  - coding: 经典medium滑动窗口题，具体题意未给 FU: 简单follow-up，未给细节
  - BQ: 深挖BQ，具体问题未给
- TT-062 | 2026-01-08 |  | 
  - raw: 面试 官先简单介绍了岗位方向，问岗位相关的八股(八股考得挺深的，大概需要研究过这个 技术/做过相关的工 作)，简单介绍自己做的项目 lc 1918
  - coding: 未具名题目 [LC1918]
  - tech: 与岗位方向相关的深入技术问答
- TT-063 | 2026-01-06 |  | 第一轮,第二轮,第三轮
  - raw: 第一轮 longest increasing subsequence/ kth largest element in two sorted array  第二轮 connect each level of a binary tree，也就是 lc 116  第三轮 number of islands
  - coding: Longest Increasing Subsequence [LC300] ; 两个有序数组中的第K大元素 ; 连接二叉树每一层的节点 [LC116] ; Number of Islands [LC200]
- TT-064 | 2026-01-03 |  | 一面,二面
  - raw: 一面 bfs 走迷宫  二面题目打家劫舍 3
  - coding: BFS走迷宫，题意未详述 ; 打家劫舍III [LC337]
- TT-065 | 2025-12-24 |  | 
  - raw: 
  - coding: -
- TT-066 | 2025-12-23 |  | 
  - raw: leetcode 原题, 2074, 链表分组翻转,先简单实现个链表翻转
  - coding: 反转偶数长度链表组 [LC2074] FU: 先实现一个简单的链表翻转
- TT-067 | 2025-12-13 |  | 
  - raw: 主要是 coding 面，简单过了一下简历 考得是 LC 1048，需要写 test case
  - coding: 最长字符串链 [LC1048]
- TT-068 | 2025-12-13 |  | 
  - raw: 20 分钟简历八股+40 分钟两个 lc 问了一个和 JD 相关的建立项目，常见 Python 八股，mysql lc2300, 721 做完之后还问了未来职业规划/怎样参加团队合作
  - coding: 咒语和药水的成功对数 [LC2300] ; 账户合并 [LC721]
  - BQ: 未来职业规划; 怎样参与团队合作 | tech: 常见Python八股; MySQL
- TT-069 | 2025-12-12 |  | 
  - raw: LC34 + 聊简历
  - coding: 查找排序数组中元素的首尾位置 [LC34]
- TT-070 | 2025-12-10 |  | 第一轮
  - raw: 第一轮 1 小时，自我介绍 5 分钟然后 2 道 leetcode,最后五分钟反向 bq 第一题岛屿 BFS，找到每一行能从 高到低流到边界的点 第二题原题 LC 210
  - coding: 水流网格题：找可从高到低流到边界的点 ; Course Schedule II [LC210]
- TT-071 | 2025-12-10 |  | 
  - raw: 自我介绍。接着开始逐条问简历的内容。 一道 leetcode209
  - coding: 长度最小的子数组 [LC209]
- TT-072 | 2025-11-27 |  | 
  - raw: 考了 lc 原题 124 有解出来 (optimal) 之后 roastresume, 蛮细节的问了跟组有关的 recommender 经验
  - coding: 二叉树最大路径和 [LC124]
- TT-073 | 2025-11-26 |  | 
  - raw: 面试官先是问了一些关于过去项目的问题，并做了一些深入的探讨。然后具体问了一些关于 Java concurrent Hashmap 和队列是怎么实现的。之后给了 15 分钟做题 (LeetCode 124) maximum path sum of a binary tree
  - coding: 二叉树最大路径和 [LC124]
  - tech: Java ConcurrentHashMap实现; 队列实现
- TT-074 | 2025-11-26 |  | 
  - raw: 自我介绍  Code: Title Contigous SubArray Question description Question: Given an array of n positive integers, find a contiguous subarray (containing more than one number) with the largest min + max. Return the sum Example [5, 12, 9, 6, 4] 12 + 9 = 21
  - coding: 正整数数组中长度至少2的连续子数组，最大化min+max并返回和
- TT-075 | 2025-11-21 |  | 
  - raw: 前半段基本在做 简历 deep dive，问得很细:项目职责、技术选型原因、遇到的瓶颈、优化 方式、架构的 trade-off 等等。 后半段开始做题: Merge k sorted lists 用的 min-heap 解法，思路比较标准，复杂度 O(N log k)。过程中面试官会深入追问: heap 是怎么比较 / 排 序的? 用哪个字段作为 key? 如果链表非常大，该怎么优化内存?
  - coding: 合并K个有序链表 [LC23] FU: heap比较/排序方式; 哪个字段作key; 链表非常大时如何优化内存
- TT-076 | 2025-11-20 |  | 
  - raw: 店面是 30 分钟 dive deep 简历+八股;另外 30 分钟做题。 Coding:简易计算器(+-*/)不含括号
  - coding: 无括号、含+-*/的简易计算器 [LC227]
  - tech: 八股细目未给
- TT-077 | 2025-11-20 |  | 第一轮
  - raw: 第一轮。简单自我介绍以后开始做题，第一道 LC 1247，第二道 LC 4293(岛屿题目 + follow up 的形式)。 最后反向 BQ
  - coding: 第一题，原文LC1247，题意未给 [LC1247] ; 岛屿题及follow-up；原文LC4293 [LC4293]
- TT-078 | 2025-11-19 |  | 
  - raw: 题目是 gird 里找一样的岛屿 用了 dfs followup 是如果把旋转翻转的也算一样
  - coding: 找相同形状的岛屿 [LC694] FU: 旋转或翻转后相同也算同类，候选LC711 ; 允许旋转/翻转的不同岛屿数量（follow-up） [LC711]
- TT-079 | 2025-11-15 |  | Technical,HM
  - raw: Technical 面:问了很多 project 相关信息。最后十分钟看了一个 coding: LRU cache with time limit 讨论了一下 思路。类似一个 system design 的问题。 HM 面:问了很多 project 相关信息。需要当场 implement 一段和工作内容相关的伪代码。
  - coding: 带时间限制的LRU [LC146] ; 当场实现与工作相关的伪代码，题意未给
- TT-080 | 2025-11-15 |  | 
  - raw: 互相自我介绍 问简历项目问题 Coding LC 679
  - coding: 24点游戏 [LC679]
- TT-081 | 2025-11-12 |  | 
  - raw: LC 43
  - coding: 字符串乘法 [LC43]
- TT-082 | 2025-11-12 |  | 
  - raw: 一道 LRU 用的是 hackerRank 并没有 test case, 自己写 test case 跑
  - coding: LRU Cache [LC146]
- TT-083 | 2025-11-11 |  | 
  - raw: coding 结果是实现一个 min heap, 要求利用数组实现, 提示是 i 位节点的子节点是 2n+1 和 2n+2. 要求基本 思想还是维护一个完整二叉树, 强调 push 和 pop 操作里要知道如何 swap 不 同的元素来维持 heap.
  - coding: 用数组实现最小堆
- TT-084 | 2025-11-05 |  | 第一轮,第二轮
  - raw: 第一轮, 先问简历项目半小时，问了几个关于 javaspring 的八股，比如@autowaved 还有 bean 生命周期的问 题，问了 HTTP get post 区别回答上来了，最后剩了 20 多分钟写一道题  第二轮，先给了一道 easy 题秒了，然后面 system design，要求设置一个 500 人群聊的消息 通知系统，最 近 30-40 条要求快速加载
  - coding: 第一轮未具名coding题 ; 第二轮easy题，题意未给
  - SD: 500人群聊消息通知系统，最近30至40条消息需快速加载 | tech: Java Spring注入（原文@autowaved，疑似@Autowired）; Bean生命周期; HTTP GET/POST区别
- TT-085 | 2025-10-31 |  | 一面,二面,三面,四面
  - raw: 一面 lc 140 + 一道 medium 题 前缀和+二分  二面 字符串题 标准 medium + bq 和简历 deep dive 三面 简单 bq 无八股无 sd 考了一道很偏的 coding 要求是写二叉树中序遍历 但是用 iterator  二叉树每个节点包含一个字符串 要求 iterator 按照中序遍历每次 next 一个字符出来  四面 简单 bq 无八股无 sd 上来直接 leetcode 588
  - coding: Word Break II [LC140] ; medium题，前缀和+二分，题意未给 ; 字符串medium，题意未给 ; 二叉树每节点存字符串，实现中序迭代器，每次next返回一个字符 ; 内存文件系统 [LC588]
  - BQ: 二三四面简单BQ，细目未给
- TT-086 | 2025-10-30 | level=NG | 
  - raw: NG  Hot 100 的题目: Jump Game 和 Jump Game 2  Transformer 的 k 能不能替换成 q，attention 分数改成 q 乘以 qT，说出数学原理的原因 想几个优化 attention 复杂度的方法出来，给的例子比如说就看最近三个 token
  - coding: Jump Game [LC55] ; Jump Game II [LC45]
  - tech: Transformer中K能否替为Q; 将attention改为Q×Qᵀ的数学原因; 降低attention复杂度，例如仅看最近3个token
- TT-087 | 2025-10-28 | level=Intern | 
  - raw: Intern 一小时面试，问了很多八股(包括数据库以及网络)-半小时  一道 leetcode hard tag 题-半小时
  - coding: 一道hard tag题，题意未给
  - tech: 数据库; 网络
- TT-088 | 2025-10-27 | level=Intern | 
  - raw: Intern LC:365(加强版，hard 难度)
  - coding: 水壶问题加强版 [LC365]
- TT-089 | 2025-10-21 |  | 
  - raw: 设计一个类 PercentileFinder，实时维护一组数字，并能随时返回当前数据的第 p 百分位值; 写两个 function addnums 还有 find Percentile，用 bisect;follow up 问还可以用什么数据结构 优化。
  - coding: PercentileFinder：实时addnums和find Percentile FU: 除bisect外还能用什么数据结构优化
- TT-090 | 2025-10-21 |  | 
  - raw: 考察题目:get massage function called get_chat_messages (), you pass in e chat message ID, and it returns 5 messages above and below the given chat ID. The 5 messages above and below a single are inclusive of the given chat ID. Merge the responses from the get_chat
  - coding: 合并多次get_chat_messages结果，去重并有序返回
- TT-091 | 2025-10-20 |  | 
  - raw: 1. 说一个 collaboration project : work with different roles, resolve conficts etc. 2. tree column traversal + sorting SD: Design Task System - Product Manager Need to define Task - QPS low - Select Creator based on their Profile - Creator Need to see task in Tikt
  - coding: 二叉树按列遍历并排序
  - SD: Task System：PM定义任务（低QPS）；按profile选择creator；creator在TikTok App查看任务（约10k QPS）；完成任务领奖（约1k） | BQ: 跨角色合作、处理冲突的project
- TT-092 | 2025-10-17 |  | 
  - raw: 大概 15 分钟 behavioral questions，然后做题。 leetcode 297。我是用 BFS 写的，test cases 也都跑出来了。 最后面试官想提高 space complexity。我是在 serialized 的时候把所有 null node 都用#表示出 来了，这部分 可以提高。
  - coding: 二叉树序列化与反序列化 [LC297] FU: 优化空间：原实现用#存储所有null节点
  - BQ: 前15分钟behavioral，细目未给
- TT-093 | 2025-10-17 | level=NG | 第一轮
  - raw: NG 第一轮，共一小时:自我介绍，project experience + impact，LC 39，最后 5 分钟随意问问题。
  - coding: 组合总和 [LC39]
- TT-094 | 2025-10-16 |  | 第一轮,第二轮
  - raw: 第一轮 coding 是写一个类 sampler (给 n 个数, a 按权重比例采样，写 rand()); 后续问了动态修改怎么办之类的(线 段树，树状数组，平衡树...) 第二轮 介绍 vllm，kvcache。 code 题给 n 哥 a/b=一个数，q 组询问问 x/y 是什么。 分析神秘并查集路径压缩复杂度。
  - coding: 按权重采样的sampler [LC528] FU: 支持动态修改权重，讨论线段树/树状数组/平衡树 ; 给定a/b比值，回答x/y查询 [LC399] FU: 并查集路径压缩的复杂度
  - tech: vLLM; KV cache
- TT-095 | 2025-10-15 | level=NG | 
  - raw: NG 前 30 分钟拷打简历项目，问到面试官熟悉的的技术栈会展开的比较深 (比如用过某一个轮 子，面试官就 会问这个轮子内部的构造是啥样的)。 后 30 分钟做题，是一个循序渐进的 binary search 系列题，一共 3 道(35/153/154)。
  - coding: 搜索插入位置 [LC35] ; 旋转有序数组最小值 [LC153] ; 含重复元素的旋转有序数组最小值 [LC154]
- TT-096 | 2025-10-14 |  | 
  - raw: 考察题目:题目是给定 ip 地址区间，输出 CIDR 表示的恰好包含此区间的列表，要求列表 最短。例子 "127.0.0.7" - "127.0.0.16" -> ['127.0.0.7/32', '127.0.0.8/29', '127.0.0.16/32']。
  - coding: 将给定IP起止区间精确覆盖为数量最少的CIDR列表 [LC751]
- TT-097 | 2025-10-12 |  | 
  - raw: 考查内容:coding + project 深挖+八股 LC1209:Remove All Adjacent Duplicates in String II 八股: 1. hashtable implementation (如何处理 collision) 2. load balancing (DBMS)  3. how DNS works
  - coding: 删除字符串中的所有相邻重复项II [LC1209]
  - tech: 哈希表实现及collision处理; load balancing（原文括注DBMS）; DNS工作原理
- TT-098 | 2025-10-11 |  | 第一轮,第二轮HM
  - raw: first was 2 LCs (easier medium + easy) and second was LC (easier medium) + behavioral with Hiring Manager + some general qs. 考察题目:LC medium hashmap question + LC medium string question
  - coding: 第一轮两道easy/easier medium，题意未详述 ; 第二轮一道easier medium，题意未详述
  - BQ: HM behavioral及general questions
- TT-099 | 2025-10-10 |  | 第一轮,第二轮
  - raw: 第一轮:design hash map 按照指示从简单到难，中间穿插一些技术问题，如 concurrency 怎 么解决; 第二轮:一个常见的写代码 OOD 题目
  - coding: 逐步实现HashMap，并讨论并发 ; 常见OOD编程题，具体题意未给
  - tech: HashMap concurrency
- TT-100 | 2025-10-10 |  | first round
  - raw: first round 考查内容:coding + project 深挖+八股 LC1209. Remove All Adjacent Duplicates in String II Project:简单描述了在 Amazon 实习做的项目 八股: hashtable implementation (如何处理 collision) load balancing (DBMS) how DNS works
  - coding: 删除字符串中的所有相邻重复项II [LC1209]
  - tech: 哈希表实现及collision处理; load balancing（原文括注DBMS）; DNS工作原理
- TT-101 | 2025-10-09 | level=NG | 第一轮coding,第二轮Systems / Troubleshooting / Problem Solving
  - raw: NG 1st Round Interview - coding 一小时 1 给一个 API，它的 parameters 是 city 和 page,作用是返回这个 city 的 array of food(返回的信 息中也包括 total page 是多少). 要求找到这个 city 下所有 food 中用户评论最高的 food 的名 字 2 给一个 array，每个元素都是一个 24bit 的 string，代表一个 color，这个 string 可以转化为 RGB 值(R、 G、B 依次序各占 8bit， 然
  - coding: 分页API：找到指定城市评论分数最高的food名称 ; 24bit颜色转RGB，为每色寻找5个pure color中距离最近者
  - tech: Grafana dashboard与metrics; 访问www.titok.com后的全过程（域名拼写按原文）; HTTP连接; Linux命令含义；原命令完整保留在raw_text
- TT-102 | 2025-10-09 |  | 
  - raw: 第一轮 VO 一个滑动窗口的 Medium 一个二叉树放摄像头的树形 dp hard，follow up 了另外 一个二叉树 hard follow up 的这个不用写 code 只说怎么做，并且每个都要说时间复杂度和空 间复杂度
  - coding: medium滑动窗口题，题意未给 ; 二叉树放摄像头 [LC968] ; 另一道二叉树hard follow-up，题意未给
- TT-103 | 2025-10-05 |  | 第一轮,第二轮
  - raw: 第一轮 第一道题目和 leetcode 的 valid parentheses 差不多，但是除了 '(' 和 ')' ，还可以有'*'， 星号可以当 (、)、或者空格;第二道题目大概是给一个 map，需要从一个点到另外一个点， 输出最短的路径，就是最 基本的 bfs+backtrace 那样子 第二轮问的也是个 leetcode 的题目，就是给你一串单词 和 每行的 max length，要让 empty space 均匀分布 那个。
  - coding: 含*有效括号，*可作(、)或空串 [LC678] ; 地图两点之间的最短路径并输出路径 ; 单词按最大行宽排版，均匀分配空格 [LC68]
- TT-104 | 2025-10-04 |  | 
  - raw: 第一问 unique path 原题 写完自己 print 了自己给的测试例子 follow up:在第一问的基础上 加上限制条件所有路径必须经过一个给定的点 (x, y) 问 unique paths 的个数 call 两次第一问的 function 乘一下结果就行
  - coding: Unique Paths [LC62] FU: 所有路径必须经过指定点(x,y)；原文建议起点到指定点和指定点到终点的路径数相乘
- TT-105 | 2025-10-03 |  | 
  - raw: Leetcode 是一道 backtrack
  - coding: 一道LeetCode回溯题，题意未给
- TT-106 | 2025-10-01 |  | 
  - raw: 题目是 LC399，写完之后问了时间空间复杂度，并且给了 hint 让做了一个小改动
  - coding: 除法求值 [LC399] FU: 在hint下做小改动，细节未给
- TT-107 | 2025-10-01 |  | 
  - raw: 先自我介绍 然后出来一道 k most frequent element 先用 hashmap+sort 写出来 然后打算用 quickselect 优化 被打断说 quickselect 不会优化 time complexity, 我依 稀记得 leetcodeeditorial 说 quickselect 可以 averageO(n)所以解释了一下 面 试官坚持要求想别的方法 这个 时候我被打断好几次已经懵了 提醒下用了 heap 开始手忙 脚乱改了两次才过 test case  然后开始拷打简历
  - coding: Top K Frequent Elements [LC347]

## 4. Undated and unsorted: the PDF's "65 undated high-frequency references" and the "tiktok-leo-10/20" docx

Undated list from the PDF (repeats kept as in source): Course Schedule (x2), Course Schedule II (x2), Tic Tac Toe (version unclear, LC 348 / 1275), iterative Binary Tree Pre / In / Postorder traversals, LRU Cache, Find First and Last Position (34), Daily Temperatures (739), All Nodes Distance K in Binary Tree (863), Minimum Distance Between BST Nodes (783), LC 1740, 3Sum (15), LC 347, Make Costs of Paths Equal in a Binary Tree (2673), Text Justification (68, x2), Valid Parenthesis String (678), LC 1091, Word Search (79), Word Search II (212), LC 694, LC 711, Word Break II (140), Subarray Sum Equals K (560), Maximum Width of Binary Tree (662), Remove Boxes (546), Remove All Adjacent Duplicates in String (1047), The Skyline Problem (218), Rotate String (796), Check Completeness of a Binary Tree (958), Minimum Path Sum (64), Path With Minimum Effort with union-find (1631), Sqrt(x) with a tweaked binary search (69), Find Peak Element (162), Maximal Rectangle (85), Maximal Square (221), LC 359, Random Pick with Weight (528), Reverse Linked List (206), Permutations (46) / II (47), Number of Atoms (726), Is Graph Bipartite (785), Minimum Window Substring (76), Construct Binary Tree from Preorder and Inorder (105), Design Task Manager (3408, x2), Regions Cut by Slashes (959), Coin Change (322), Subtree of Another Tree (572), Find the Duplicate Number (287), Maximum Subarray (53), Min Stack (155), Decode String (394), Kth Largest Element (215), Longest Consecutive Sequence (128), Basic Calculator II (227), Minimum Remove to Make Valid Parentheses (1249), LC 1361, LCA of a BST (235), LC 1647, Escape the Spreading Fire (2258). conf low (undated, anonymous).

"tiktok-leo-10/20" (docx, undated, 30 coding + 20 BQ; intern 45 min / NG 60 min). Many prompts are re-written with a TikTok theme ("TikTok Collectibles", "financial analytics"), which looks like an OA-style or AI-reworded bank, so conf low. Distinct prompts: (1) count values of a sorted array in [start, end), follow-up with duplicates; (2) equal packs from card categories (OA-flavoured); (3) longest subarray with every element greater than a limit-derived bound; (4) is `b` a subsequence of `a`; (5) replace `*` in "A*B" with A or B and list all strings; (6) minimum alternating +1 / +2 operations to equalise an array; (7) detect a loop of 1s enclosing 0s in a 2D image; (8) fill rooms with distance to nearest exit (LC 286, Walls and Gates); (9) longest palindromic substring, follow-up subsequence; (10) stack with `increment(k, val)` (LC 1381); (11) stars between bars for queries (LC 2055); (12) tile a 2xN board with dominoes; (13) longest consecutive watch-history IDs (LC 128); (14) Daily Temperatures; (15) build a tree from inorder and postorder (LC 106); (16) insert an array into a BST and return the in-order traversal; (17) a modified Gas Station problem; (18) **graph fault detection** with error codes E1 cycle, E2 node with in-degree > 1 and out-degree > 1, E3 disconnected components, return the combined code; (19) Minimum Window Substring; (20) Trapping Rain Water; (21) Intersection of Two Linked Lists; (22) Kth Largest Element; (23) minimum time for cats to catch fish (binary search on the answer); (24) battery charging schedule across k stations; (25) maximum GCD of any pair; (26) Move Zeroes; (27) Group Anagrams; (28) iterative merge sort; (29) Dijkstra on a social graph; (30) LRU cache O(1). BQs: tell me about yourself, why TikTok / ByteDance, most recent internship, tight deadline, challenging project, stress, disagreement with a teammate, learn something fast, debug a difficult problem, prioritise, failure, parallel programming / multithreading, what do you know about TikTok's products and culture, project ownership, feedback, questions for me.

## 5. Duplicate map (same event seen on several platforms; count once)

- PDF TT-056 (2026-01-28) = 1P3A thread 1162894 (TikTok NG SWE 3 rounds).
- PDF TT-050 (2026-02-18) = 1P3A thread 1165436 (Tiktok 26NG).
- PDF TT-037 (2026-04-09) = 1P3A thread 1172146 (TT SDE 电面 1轮).
- PDF TT-028 (2026-05-16) = 1P3A thread 1176917 (tt 三轮).
- PDF TT-009 (2026-07-24) = 1P3A thread 1183948 (Bytedance SDE 三轮).
- PDF TT-012 (2026-07-18) = 1P3A thread 1183355 (USDS two-round coding).
- PDF TT-053 (2026-02-01) = 1P3A thread 1163442 (right side view).
- PDF TT-019 (2026-07-03) = 1P3A thread 1181934.
- PDF TT-021 (2026-06-30) = 1P3A thread 1181618 (Growth, grid shortest path + recommendation design).
- job-compass v2na3e = 1P3A 1177932; xmc27l = Xiaohongshu note 2025-11-01.
- Nowcoder direct posts = wearzdk mirror rows (same posts) — do not count twice.

## 6. Frequency read (counts are sightings in this file's sources, not independent interviews)

PDF compilation, in-window 107 records, coding problems by LeetCode number: LC 146 LRU (6 records: TT-003, 028, 032 with TTL, 050, 079 with time limit, 082), LC 124 Binary Tree Maximum Path Sum (4: 012, 050, 072, 073), LC 200 Number of Islands (4: 015, 016, 057, 063) plus island family LC 694 (3), 695 (2), 711, 827 (so about 10 island-type sightings), LC 207/210 Course Schedule family (6), LC 3 longest substring (2) with sliding-window siblings 239, 340, 424, 209, 567 (5+), LC 2673 (2), LC 316 (2), LC 1293 (2), LC 43 Multiply Strings (2), LC 365 Water Jug (2), LC 151 (2), LC 227 / 224 calculator (2), LC 678 Valid Parenthesis String (2), LC 35/153/154 binary-search ladder (TT-095), LC 399 (2). Counted from the 1P3A bank (independent threads): number-of-islands-family n=10, lru-cache-with-ttl n=9, course-schedule-topo-sort n=8, reverse-nodes-in-k-group n=7, binary-tree-max-path-sum n=5, merge-intervals n=5, basic-calculator n=5.

TikTok-specific variants of a LeetCode problem (appear in more than one source): LRU with TTL (TT-032, 1P3A lru-cache-with-ttl); LRU "with time limit" (TT-079); Valid Parenthesis String with `*` plus "print all valid strings" (TT-050, 1165436); Course Schedule plus "output the shortest path / learning path" (TT-036, 1172524, mirror file `bytedance-backend-922660519729696768` (面经-01) item "课程表进阶题，输出可行学习路径"); distinct islands (LC 694) and rotation / flip islands (LC 711) (TT-016, 059, 078); islands too big for memory -> partition + union-find (TT-020); grid shortest path with k obstacle eliminations (LC 1293) and fuel / recharge cells (TT-021, 037); percentile finder (`PercentileFinder.addnums / findPercentile` with `bisect`, TT-089); `get_chat_messages` merge of overlapping message windows (TT-090); in-memory KV store with snapshot / restore (TT-012, 1P3A 1193703); seller task scheduler (1P3A 1188260 / bank seller-task-scheduler); IP range to minimal CIDR list (TT-096, LC 751); largest number below N from a digit set (TT-007, Chinese mirror "数组中的数能构成的比 n 小的最大数" x3).
