---
id: bagu-link-metrics-aggregator-1-map
node: links.metrics-aggregator
type: qa
step: 1
---
## Q
**指标聚合系统（计数指标 + 直方图仪表盘） · 会被追问哪些八股**｜必会

设计指标聚合系统（计数指标 + 直方图仪表盘）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 计数可加，所以尽早聚合。基础是：高频计数不抢同一变量、缓存行对齐、哈希表扩容抖动、分位数要合并直方图、聚合窗口不重不漏。

**下钻路线。**
- 高频计数怎么写 → 每线程累加自己的槽再汇总，上报时求和是近似，[[a.runtime.java-chm|ConcurrentHashMap 如何线程安全]]
- 槽位怎么摆才不互相拖慢 → 缓存行对齐，避免伪共享，[[b.net.cpu-cache-schedule|CPU 缓存、伪共享与进程调度]]
- 聚合窗口到点 flush → 哈希表扩容和搬迁会卡住，预估容量，[[a.runtime.java-hashmap-collections|Java HashMap 结构、扩容与常用集合]]
- 多机延迟分位数 → 不能平均 P99，要合并直方图桶或 t-digest，[[b.scenario.timeseries-cardinality|时序基数与降采样]]
- 窗口聚合不重不漏 → 消费幂等，晚到数据留宽限期，[[b.mq.no-duplicate|重复消费与恰好一次]]
- 按时间范围查明细很慢 → EXPLAIN 确认 (指标, 时间) 索引无 filesort，[[b.mysql.explain|EXPLAIN 执行计划怎么看]]

```mermaid
flowchart LR
    A["每线程计数槽"] --> B["缓存行对齐"]
    B --> C["窗口 flush<br/>哈希表预估容量"]
    C --> D["合并直方图<br/>算分位数"]
    D --> E["幂等写入<br/>晚到留宽限期"]
    E --> F["(指标, 时间) 索引查询"]
```

**业务场景。** 支付成功率与延迟按渠道、币种汇总：多台机器的渠道 P99 要合并桶，不能把各机 P99 求平均。
**系统设计。** [[links.metrics-monitoring-alerts|指标监控与告警平台]]：写入侧同源，但那里多了告警状态机；[[links.ad-click-aggregator|广告点击聚合]]：同样先聚合后写，但点击要去重，计数指标不用。
