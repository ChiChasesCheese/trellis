---
id: bagu-link-camelcamelcamel-1-map
node: links.camelcamelcamel
type: qa
step: 1
---
## Q
**价格追踪（CamelCamelCamel） · 会被追问哪些八股**｜必会

设计价格追踪（CamelCamelCamel）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 难在数据从哪来，以及降价后一小时内通知。基础是：对源站限速、时序数据的存储和索引、事件驱动通知与削峰、幂等去重、乱序处理。

**下钻路线。**
- 5 亿商品爬不完 → 令牌桶按站点限速，按兴趣分层爬取，[[a.protect.rate-limit-algorithms|限流算法]]
- 价格只追加，长到数十亿行 → LSM 或时序库优于 B+ 树，[[b.search.lsm-vs-btree|LSM-Tree 与 B+ Tree 的本质区别]]
- 按商品和时间范围查历史 → (商品, 时间) 联合索引，图表另做预聚合，[[a.mysql.leftmost-index-failure|联合索引、最左前缀与索引失效]]
- 降价一小时内通知 → 价格变化事件驱动，不要定时扫全表，[[b.mq.why-mq|为什么用消息队列]]
- 热门商品降价通知几十万订阅者 → 积压扩容，分区并行，[[a.mq.backlog|消息积压怎么办]]
- 同一次降价不重复通知 → 通知去重键，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 扩展上报的价格乱序 → 带时间戳或版本，旧的丢弃，[[a.mq.ordering|消息顺序性怎么保证]]
- 到期扫描订阅 → 按到期时间排序的定时任务，[[b.scenario.delayed-task|定时调度与订单超时自动取消]]

**业务场景。** 抖音商城商品降价提醒：用户订阅价格阈值，降价事件触发通知，同一次降价只能提醒一次。
**系统设计。** [[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：降价通知就是它的一个场景，群发重点在渠道隔离；网络爬虫（Web Crawler）：同样对源站限速，这里的数据主要靠用户众包上报。
