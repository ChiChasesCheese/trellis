---
id: hft-research-infra-time-series-db-clickhouse
node: research-infra.time-series-db
type: qa
step: 3
---
## Q
ClickHouse 是什么？用它替代 kdb+ 存放行情历史，有哪些利弊？

## A
**ClickHouse** 是开源的列式分析数据库（OLAP，面向分析的查询），用标准的 SQL 查询，可以横向扩展到多台机器，扫描和聚合十亿行数据通常只需要秒级。它也支持 `ASOF JOIN`，能做类似 kdb+ 的“按时间对齐”的连接。

**相对 kdb+ 的优点**：
- 开源，没有昂贵的授权费；
- 用 SQL，学习门槛低，会写 SQL 的工程师和研究员都能用；
- 社区活跃，和 Python、Grafana、各类 BI 工具集成好；
- 分布式存储和副本机制成熟，容易扩展到很大的数据量。

**缺点或局限**：
- 在极低延迟的**实时流式**场景（内存内毫秒以下的处理、盘中滚动计算）通常不如 kdb+；
- 针对金融时间序列的内置函数没有 kdb+/q 那么丰富；
- 已经有大量 q 代码和人员积累的团队，迁移成本不小。

典型选择：新建的研究平台、对成本敏感的团队倾向 ClickHouse；已有 kdb+ 投入、需要实时分析的老牌机构继续用 kdb+。
