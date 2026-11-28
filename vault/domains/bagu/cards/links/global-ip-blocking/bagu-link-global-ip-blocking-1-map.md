---
id: bagu-link-global-ip-blocking-1-map
node: links.global-ip-blocking
type: qa
step: 1
---
## Q
**全球分布式封禁（黑名单）系统 · 会被追问哪些八股**｜必会

设计全球分布式封禁（黑名单）系统时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 把拿规则和拦请求分开：每个节点本地查快照。基础是：布隆过滤器与哈希表做本地查询、配置动态下发、多区域复制的最终一致、断线补齐、SYN 洪泛的队列。

**下钻路线。**
- 查不在名单的 IP 不每次查库 → 布隆过滤器放查询入口，[[b.cache.bloom-filter|布隆过滤器原理与误判]]
- 节点内存规则被高频查 → 防构造冲突 key，链表树化兜底，[[a.runtime.java-hashmap-collections|Java HashMap 结构、扩容与常用集合]]
- 规则怎么实时下发 → 配置中心推送快照，不是发版，[[b.distributed.microservice-governance|微服务拆分与治理]]
- 封禁怎么全球生效 → 多区域复制，一个区域挂了怎么办取决于 RPO，[[b.protect.ha-redundancy|高可用架构]]
- 某地区副本断线重连 → 偏移量在积压内增量补，超出全量，积压按最长断线估，[[b.redis.replication-sync|主从复制]]
- 控制平面不可用时 → 读取选可用，节点用最近一份快照，[[a.distributed.cap-base|CAP 与 BASE]]
- SYN 洪泛源地址伪造 → 封 IP 没用，要看半连接队列与 SYN cookie，[[b.net.tcp-queues-attacks|半连接/全连接队列、SYN 攻击与单机连接数上限]]

**业务场景。** 支付风控把盗刷用的 IP 和设备拉黑后，各区域边缘要几秒内生效；误封商户回调 IP 本身就是一次故障。
**系统设计。** [[links.distributed-rate-limiter|分布式限流器（Rate Limiter）]]：同样本地决策加中心下发，但限流有计数状态而名单只读；功能开关服务（Feature Flag Service）：同样的快照下发和客户端本地缓存。
