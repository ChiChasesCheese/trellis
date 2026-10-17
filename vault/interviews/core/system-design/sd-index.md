# 系统设计面经题单（Reported System Design Questions）

面试中真实报告过的系统设计（System Design）题，一题一篇中文题解，按 senior / staff 标准写：需求量化、容量估算、
mermaid 架构图、三到四个深挖、权衡与故障模式、面试官追问。和公司无关的通用知识在
[[System Design MOC|system-design 域]]，这里只放「被真实问过的题」以及它在那家公司的问法。

- 第一批：Amazon，2026-09-16..10-16 一亩三分地（1point3acres）与 Hello Interview 的报告（**不含 OA**）。
  原始记录：`interviews/companies/amazon/catalog/raw/1p3a_2026-10-16.md`、`hellointerview_2026-10-16.md`。
- 与 Hello Interview 重合的题：沿用它的分析骨架与取舍要点，链接原页，正文用自己的话写，并写出我们和它不同的地方
  （它是付费内容，仓库是公开的，所以不摘录原文）。
- 置信度：**高** = 候选人原帖里看得到题目原文；**中** = 聚合站摘要或题库条目点名了题目；**低** = 只有片段。
  看不到的部分一律标 **（重建）**。

## 题单（按学习顺序）

| # | 题 | 报告 | 级别 | 置信度 | 与 Hello Interview 重合 | 本库已有 | 题解 |
|---|---|---|---|---|---|---|---|
| SD01 | 短链接服务（URL Shortener） | 1p3a 1193105 onsite 2026-10-02；Hello Interview 累计 12 条（最近 2026-09） | SDE II | 高（题名） | Bitly | [[solution-url-shortener]] | [[sd01-url-shortener]] |
| SD02 | Amazon Lockers 投递系统（Amazon Lockers Delivery） | Hello Interview 累计 14 条（最近 2026-09-10，senior） | senior | 中 | Ticketmaster、Notification、Multi-step | [[solution-amazon-locker]]（LLD） | [[sd02-amazon-lockers]] |
| SD03 | 配送中心库存状态服务（Distribution Center Stock State） | 1p3a 题库，onsite 2026-09-18 | — | 中 | GoPuff、Flash Sale | [[solution-e-commerce]]、[[solution-flash-sale]] | [[sd03-dc-stock-state]] |
| SD04 | 文件系统跨区域数据复制（File System Replication） | Hello Interview，2026-10-01 | mid | 中 | Dropbox、Large Blobs、CDC | [[solution-file-sync]]、[[solution-object-storage]] | [[sd04-fs-replication]] |
| SD05 | 疫苗资格与预约（Vaccine Eligibility & Booking） | Hello Interview，2026-09-10 | senior | 中 | Ticketmaster、Dealing with Contention | [[solution-ticket-booking]]、[[solution-hotel-reservation]] | [[sd05-vaccine-booking]] |
| SD06 | Agentic AI 安全事件平台，1 TB/天（AI Agent Security Telemetry） | 1p3a 1192714，L5 店面 2026-10-11 | L5 | 中 | Ad Click Aggregator、Metrics Monitoring | [[solution-ad-click-aggregation]]、[[solution-metrics-monitoring]] | [[sd06-agent-security]] |
| SD07 | 大文件外部排序，200 GB / 8 GB 内存（External Sort） | Hello Interview，2026-09-10 | mid | 中 | 无 | — | [[sd07-external-sort]] |

30 天窗口外、但在 Hello Interview 上长期高频的 Amazon SD 题（本批不写，先看本库通用题解）：实时协作文档 14 条（最近 2026-06，
[[solution-google-docs]]）、停车场管理 11 条（2026-06）、网约车 9 条（2025-12，[[solution-ride-hailing]]）、
大规模通知系统 7 条（2026-08，[[solution-notification-system]]）。

另有两条 SD 轮内容被隐藏、看不到题目：1p3a 1190132（onsite 四轮，2026-09-19）、1189932（SDE2 VO 挂经，2026-09-17）。
1p3a 1191766（2026-10-02 整理帖）说 SDE-2 的 OA 里有独立的 15–20 分钟系统设计，那属于 OA，不在本题单。

## 怎么用

1. 先读题单里「本库已有」的通用题解，再读本目录的题解——这里的每篇都假设你知道通用版本，专讲 Amazon 的问法和 senior 深挖。
2. 每篇末尾的「60 分钟怎么分配」照着计时口述一遍；「自测」的答案在折叠块里。
3. 验收（维护者用）：`python3 vault/interviews/core/system-design/check_sd.py`。
