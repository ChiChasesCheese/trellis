---
id: hi-c-sd-metrics-monitoring-n04-entities
node: sd.problem-breakdowns.metrics-monitoring.notes
type: qa
step: 4
---
## Q
**指标监控平台 · 核心实体：指标、标签与序列**｜摘要 · 必会

指标（metric）、标签（label）、序列（series）是什么关系？为什么说序列数是整个系统的核心扩展难题？

## A
- **指标：** 有名字的度量，带标签和某时刻的值，如 `cpu_usage{host="server-1", region="us-east"} = 0.75`。
- **标签：** 附在指标上的键值对，用来标明来源、供切片过滤，如 `host`、`region`。
- **序列：** 一个指标名加一组特定标签的唯一组合，随时间的 (时间戳, 值) 序列。`cpu_usage{host="server-1"}` 是一条序列，`server-2` 是另一条。
- **数量怎么算：** 50 万台服务器各报 `cpu_usage`，就有 50 万条序列；再加 `core` 标签就是几百万条。新增标签不一定增加序列：加 `region` 标签，如果每台服务器只在一个区域，序列数不变，因为只算实际出现的唯一组合。
- **为什么是核心难题：** 序列数的无控制增长（基数爆炸，cardinality explosion）会拖垮写入和查询，大多数系统都专门限制它。
- **其他实体：** 告警规则（指标查询加阈值加持续时间，如"us-east 平均 CPU 高于 90% 持续 5 分钟"）；仪表盘（一组面板，每个面板是一条查询结果的图或表）。仪表盘不细讲，但它决定读查询量。
