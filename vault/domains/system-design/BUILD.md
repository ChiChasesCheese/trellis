# BUILD — system-design：设计题库（`problems` 分支）

这份文件是这个专题的持久记录：调研了什么、为什么是这 49 道题、每一步做到哪、下一步做什么。
新会话从这里接手。所有数字由 `scripts/design_problem_survey.py` 和
`scripts/check_design_problems.py` 算出，不是手数的。

## 1. 调研（2026-09-19，GitHub 优先）

三个调研代理各自负责一组来源，原始记录逐行带 URL，未改写：

- [[sd-problems-survey-github]]：8 个 GitHub 仓库，逐个读了 LICENSE 原文
- [[sd-problems-survey-hellointerview-bytebytego]]：Hello Interview 题解索引、Alex Xu 两卷目录、ByteByteGo 其他课程
- [[sd-problems-survey-grokking-exponent-others]]：Grokking 三门课、Exponent、interviewing.io、systemdesign.one、Codemia 等

合计 **538 行、20 个来源、149 个去重后的题名**。
LeetCode Discuss 全部返回 403，未计入；两个疑似 AI 内容农场的榜单被排除。

### 入选线

**至少被 3 个独立来源当作一道题来教** → 49 道题，成为 `problems` 下的叶子。
别名折叠规则在 `scripts/design_problem_aliases.py`（例如 WhatsApp 并入 Chat，Robinhood 并入 Stock exchange）。

### 范围外（有记录，不建叶子）

- **ML 模型设计题**（推荐系统、视觉搜索、机器翻译、生成式图像等）：是另一类面试，来自 ByteByteGo 的 ML/GenAI 课程。
- **Case study 类**（Dynamo、Cassandra、GFS、BigTable、Kafka 等）：是读论文，不是设计题；对应内容在概念叶子和 cases 里。
- **面向对象 / 低层设计题**（停车场、自动售货机、ATM）：属于 `low-level-design` 域。
- **移动端客户端设计题**：另一类面试。
- 共 31 个题名。

### 观察名单（1–2 个来源，未入选）

Data infrastructure system（3）、Web analytics（2）、Tax-filing platform（2）、RAG (retrieval-augmented generation)（2）、Online presence indicator（2）、Music streaming (Spotify)（2）、Load balancer（2）、LLM customer support bot（2）、Google Street View（2）、Fitness tracking (Strava)（2）、CI/CD pipeline service（2）、Weather reporting system（1）、Voting system（1）、Virtualization system（1）、Video streaming (YouTube/Netflix) (mobile client)（1）、VR streaming service（1）、Text-to-video generation（1）、Text-to-image generation（1）、Task management application（1）、Tagging service（1）、Stock exchange (mobile client)（1）、Smart home system（1）、Serverless architecture framework（1）、Screenshot capture system（1） 等 69 个。
其中 RAG 已有概念叶子 `ai.rag`。下次刷新调研时，若某题升到 3 个来源就补进来。

## 2. 覆盖矩阵（按来源数排序）

| 来源数 | 免费完整题解数 | 叶子 | 题目 | 核心 |
|---|---|---|---|---|
| 16 | 16 | `problems.social.chat-messaging` | Chat & Messaging (WhatsApp) | ✓ |
| 15 | 14 | `problems.foundations.url-shortener` | URL Shortener | ✓ |
| 14 | 19 | `problems.social.news-feed` | News Feed & Timeline (Twitter/Facebook) | ✓ |
| 13 | 16 | `problems.media.video-streaming` | Video Streaming (YouTube/Netflix) | ✓ |
| 13 | 12 | `problems.search.web-crawler` | Web Crawler | ✓ |
| 12 | 9 | `problems.social.instagram` | Photo Sharing (Instagram) | ✓ |
| 12 | 12 | `problems.media.google-docs` | Collaborative Editing (Google Docs) | ✓ |
| 10 | 9 | `problems.media.file-sync` | File Sync (Dropbox/Google Drive) | ✓ |
| 10 | 8 | `problems.geo.proximity` | Proximity & Nearby Search (Yelp) | ✓ |
| 9 | 7 | `problems.foundations.rate-limiter` | Distributed Rate Limiter | ✓ |
| 9 | 7 | `problems.foundations.unique-id-generator` | Unique ID Generator |  |
| 9 | 9 | `problems.search.search-engine` | Search Engine & Post Search |  |
| 9 | 7 | `problems.geo.ride-hailing` | Ride Hailing (Uber) |  |
| 9 | 7 | `problems.commerce.payment-system` | Payment System | ✓ |
| 8 | 8 | `problems.foundations.key-value-store` | Distributed Key-Value Store |  |
| 8 | 9 | `problems.foundations.distributed-cache` | Distributed Cache |  |
| 8 | 5 | `problems.search.typeahead` | Typeahead & Autocomplete |  |
| 8 | 13 | `problems.search.top-k` | Top-K & Trending (Heavy Hitters) |  |
| 7 | 9 | `problems.foundations.cdn` | Content Delivery Network |  |
| 7 | 7 | `problems.search.metrics-monitoring` | Metrics, Monitoring & Alerting |  |
| 7 | 5 | `problems.geo.google-maps` | Maps & Navigation (Google Maps) |  |
| 7 | 6 | `problems.commerce.stock-exchange` | Stock Exchange & Trading (Robinhood) |  |
| 7 | 6 | `problems.commerce.ticket-booking` | Ticket Booking (Ticketmaster) |  |
| 6 | 8 | `problems.foundations.message-queue` | Distributed Message Queue |  |
| 6 | 5 | `problems.foundations.job-scheduler` | Distributed Job Scheduler |  |
| 6 | 6 | `problems.foundations.pastebin` | Pastebin |  |
| 6 | 3 | `problems.social.notification-system` | Notification System |  |
| 6 | 4 | `problems.realtime.online-judge` | Online Judge (LeetCode) |  |
| 6 | 5 | `problems.realtime.multiplayer-game` | Online Multiplayer Game (Chess) |  |
| 6 | 7 | `problems.realtime.llm-chat-service` | LLM Chat Service (ChatGPT) |  |
| 5 | 4 | `problems.social.reddit` | Forum & Threaded Comments (Reddit) |  |
| 5 | 3 | `problems.media.email-service` | Email Service (Gmail) |  |
| 5 | 6 | `problems.search.ad-click-aggregation` | Ad Click Aggregation |  |
| 5 | 5 | `problems.geo.food-delivery` | Food & Grocery Delivery (DoorDash/Gopuff) |  |
| 5 | 7 | `problems.realtime.calendar` | Calendar & Scheduling (Google Calendar) |  |
| 5 | 5 | `problems.commerce.hotel-reservation` | Hotel & Marketplace Reservation (Airbnb) |  |
| 4 | 3 | `problems.foundations.object-storage` | Object Storage (S3) |  |
| 4 | 4 | `problems.foundations.lock-service` | Distributed Lock & Coordination Service |  |
| 4 | 4 | `problems.foundations.auth-service` | Authentication & Identity Service |  |
| 4 | 5 | `problems.social.social-graph-search` | Social Graph & Friend Search |  |
| 4 | 3 | `problems.commerce.digital-wallet` | Digital Wallet |  |
| 3 | 4 | `problems.social.live-comments` | Live Comments |  |
| 3 | 3 | `problems.social.tinder` | Dating & Matching (Tinder) |  |
| 3 | 3 | `problems.media.video-conferencing` | Video Conferencing (Zoom) |  |
| 3 | 1 | `problems.search.news-aggregator` | News Aggregator (Google News) |  |
| 3 | 2 | `problems.realtime.leaderboard` | Real-Time Leaderboard |  |
| 3 | 2 | `problems.commerce.auction` | Online Auction (eBay) |  |
| 3 | 6 | `problems.commerce.e-commerce` | E-Commerce Platform (Amazon) |  |
| 3 | 1 | `problems.commerce.flash-sale` | Flash Sale & High-Contention Inventory |  |

标为核心（`core: true`）的 11 道是来源数最高的一档，会在 Anki 的第一遍里出现，连同它们依赖的概念叶子。

## 3. 每道题的交付物与验收

写法见 `proposals/design-problems/AGENT.md`，每题的任务简报在 `proposals/design-problems/tasks/<slug>.md`。

- `readings/problems/solution-<slug>.md`：自写题解（中文，11 个固定小节，≥ 9000 字，≥ 4 个深入探讨，mermaid 图，≥ 3 个来源链接）
- `readings/problems/src-<site>-<slug>.md`：来源条目；商业备考网站一律 `no-archive`，只留链接不入库（仓库是公开的）
- `cards/problems/…`：6–8 张自包含卡片（英文 + 中文翻译），经 `grow` 导入，带 `step`
- `drills/problems/design-<slug>.md`：题面、约束、评分点（链接到真实卡片）、题解链接

验收命令：`uv run python scripts/check_design_problems.py --all`

## 4. 台账

| 日期 | 步骤 | 结果 |
|---|---|---|
| 2026-09-19 | 调研 | 538 行 / 20 来源，三份原始记录入库 |
| 2026-09-19 | 骨架 | `problems` 分支：7 个家族、49 个叶子，`validate` 0 错误 |
| 2026-09-19 | 试点 3 题 | url-shortener、chat-messaging、ticket-booking 验收通过；主会话复算后改正 3 处数字（哈希碰撞概率差六个数量级、状态行 486→506GB、一个未核实的二手数字从卡片移除）；两条教训写入 AGENT.md |

## 5. 下一步

按家族分批写题（每批 3 个并行 sonnet 代理，每个代理拥有自己那几道题的文件）。
每批由主会话重跑验收脚本和 `validate`、抽读题解后提交。全部通过后：核对各代理报告的「最不确定的论断」，
对开放许可和一手工程来源跑 `trellis --domain system-design clip --node problems`，然后 sync、build、anki-push。

### 写题队列（每组一个 sonnet 代理，两道同家族的题；最多 3 组并行）

状态以 `uv run python scripts/check_design_problems.py --all` 为准，这张表只记顺序。
验收流程：代理回报 → 主会话跑 `scripts/review_design_problem.py <slug>…`，复算容量估算，核对代理自报的
「最不确定的三条论断」，抽读题解 → 改正 → 按题提交。

| # | 题目 | | # | 题目 |
|---|---|---|---|---|
| 1 | news-feed + instagram | | 13 | notification-system + live-comments |
| 2 | video-streaming + file-sync | | 14 | metrics-monitoring + news-aggregator |
| 3 | google-docs + web-crawler | | 15 | google-maps + food-delivery |
| 4 | proximity + ride-hailing | | 16 | online-judge + multiplayer-game |
| 5 | payment-system + digital-wallet | | 17 | llm-chat-service + leaderboard |
| 6 | rate-limiter + unique-id-generator | | 18 | pastebin + lock-service |
| 7 | key-value-store + distributed-cache | | 19 | hotel-reservation + flash-sale |
| 8 | search-engine + typeahead | | 20 | email-service + video-conferencing |
| 9 | top-k + ad-click-aggregation | | 21 | reddit + social-graph-search |
| 10 | cdn + object-storage | | 22 | tinder + calendar |
| 11 | message-queue + job-scheduler | | 23 | e-commerce + auth-service |
| 12 | stock-exchange + auction | | | |

每个代理的提示词是同一个模板：读 `proposals/design-problems/AGENT.md`，读两份
`proposals/design-problems/tasks/<slug>.md`，先完整做完第一题再做第二题，跑验收命令，按 AGENT.md 的格式回报。
代理自带续跑规则（验收已通过的题跳过），所以中断后原样重发即可。
