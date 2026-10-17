# 系统设计题单（System Design Questions）

这里每一篇都是一道完整的系统设计题：先用大白话讲清这个系统是什么、难在哪里，再按面试的顺序走一遍——澄清问题、
需求、容量估算、核心实体与 API、架构图、三到四个深挖、staff 层面的权衡与故障、面试官会追问什么、60 分钟怎么分配、
自测。标准按 senior / staff 写：每个选择都说清楚「是什么逼出了它」和「它换来了什么、代价是什么」。

和具体题目无关的通用知识（复制、分区、缓存、一致性……）在 [[System Design MOC|系统设计域]]，这里只放面试里真实出过的题。

## 题单（按学习顺序）

先做前两道：它们是 Amazon 系统设计轮里长期出现最多的两道题，而且一道考「读多写少的全局服务」，一道考「库存预留与
状态流转」，覆盖了后面几道的大部分基本功。

| # | 题 | 考什么 | 题解 | 先读的通用题解 |
|---|---|---|---|---|
| SD01 | 短链接服务（URL Shortener） | 编号怎么生成才永不碰撞；怎样把 99% 的读挡在数据库之外；单个爆款链接的热点 | [[sd01-url-shortener]] | [[solution-url-shortener]] |
| SD02 | Amazon Lockers 投递系统 | 结账时预留柜格而不超卖；柜机断网时怎么取件；投递与退货的状态流转 | [[sd02-amazon-lockers]] | [[solution-amazon-locker]] |
| SD03 | 配送中心库存状态服务 | 海量库存事件的幂等摄入；账本与当前状态分开存；最后一件库存的争抢 | [[sd03-dc-stock-state]] | [[solution-e-commerce]]、[[solution-flash-sale]] |
| SD04 | 文件系统跨区域复制 | 只传变化的部分；文件内容与元数据的先后顺序；对端宕机后怎么追平 | [[sd04-fs-replication]] | [[solution-file-sync]]、[[solution-object-storage]] |
| SD05 | 疫苗资格与预约 | 资格规则可配置且可追溯；时段与剂量两种库存同时约束；开放日的瞬时洪峰 | [[sd05-vaccine-booking]] | [[solution-ticket-booking]]、[[solution-hotel-reservation]] |
| SD06 | AI Agent 安全事件平台（1 TB/天） | 每天 1 TB 事件的流式摄入；实时规则与离线检测两条路；多租户隔离与敏感数据脱敏 | [[sd06-agent-security]] | [[solution-ad-click-aggregation]]、[[solution-metrics-monitoring]] |
| SD07 | 大文件外部排序（200 GB 数据 / 8 GB 内存） | 内存放不下时怎么排序：分段排序再多路归并；多台机器怎么分工 | [[sd07-external-sort]] | — |

## 怎么用

1. 先读表里「先读的通用题解」，再读这里的题解：这里假设你已经知道通用版本，重点讲每道题自己特有的难点和 senior 深挖。
2. 读完一篇，合上它，照着末尾的「60 分钟怎么分配」计时口述一遍，再做「自测」（答案在折叠块里）。
3. 维护者验收：`python3 vault/interviews/core/system-design/check_sd.py`（结构、图的尺寸、写作规则）。

## 来源

- 题目来自 2026-09-16..10-16 一亩三分地与 Hello Interview 上 Amazon 候选人的报告（不含 OA）；逐条记录见
  `interviews/companies/amazon/catalog/raw/1p3a_2026-10-16.md` 与 `hellointerview_2026-10-16.md`。每篇题解的最后一节写明该题
  的具体出处、日期、级别、置信度，以及题面里哪些是根据有限信息补全的。
- 学习顺序依据：Hello Interview 上 Amazon Lockers 累计 14 条报告、URL Shortener 累计 12 条，是 Amazon 系统设计题里最常见的两道；
  SD01 另有一亩三分地 2026-10-02 现场轮的报告。
- 30 天窗口外但长期高频的 Amazon 系统设计题（本批未写，可先读通用题解）：实时协作文档 14 条（[[solution-google-docs]]）、
  停车场管理 11 条、网约车 9 条（[[solution-ride-hailing]]）、大规模通知系统 7 条（[[solution-notification-system]]）。
- 另有两条系统设计轮的报告内容被隐藏、看不到题目；一亩三分地的一篇整理帖提到 SDE-2 的 OA 里有 15–20 分钟的系统设计，属于 OA，不在这份题单里。
- 与 Hello Interview 题解重合的题，沿用了它的分析骨架和关键取舍并在每篇末尾注明；它是付费内容，仓库公开，所以只链接、不摘录。
