---
id: bagu-link-tt-realtime-auction-bidding-1-map
node: links.tt-realtime-auction-bidding
type: qa
step: 1
---
## Q
**实时竞价拍卖 · 会被追问哪些八股**｜必会

设计实时竞价拍卖时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 核心是同一场拍卖的出价必须有唯一顺序，且每次出价只生效一次。依赖的基础：条件更新做最终仲裁、Redis 异步复制不能当账本、租约加世代号防双主、幂等键、outbox 与有序事件、长连接推送。

**下钻路线。**
- 多人同时出价 → 带版本或价格条件的更新，影响行数为 0 就是被超越，[[b.mysql.lock-types|MySQL 锁分类]]
- 为什么不全放 Redis → 主从切换会丢最近写入，价格倒退，Redis 只做读缓存，[[a.redis.ha-overview|主从、哨兵与 Cluster 怎么保证高可用]]
- 旧拥有者网络分区后还在写 → 租约加世代号，数据库拒绝旧世代的写入，[[b.distributed.fencing-token|Fencing Token、租约与脑裂防护]]
- 手机超时重试同一次出价 → 幂等键唯一，重复请求原样返回第一次的结果，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 接受出价后事件一定要发出 → 同事务写 outbox，再投递到 Kafka，[[a.idem.outbox|本地消息表 / Outbox 与最大努力通知]]
- 事件顺序 → 分区键用 auction_id，同一场内有序，[[a.mq.ordering|消息顺序性怎么保证]]
- 五万观众怎么推 → 每个网关一份再本地分发，100 到 200 毫秒合并一次，[[a.net.websocket-push|消息推送]]
- 拍卖到点结束 → 延迟任务触发关闭，关闭与出价在同一串行点，[[b.mq.delay-message|延迟消息怎么实现]]

**业务场景。** 直播间拍卖最后几秒每秒上千次出价，赢家付款失败时订单按顺位转给第二高者，付款用拍卖号做幂等键，不会扣两次。
**系统设计。** [[links.online-auction|在线拍卖（eBay）]]：同样的出价排序，这个变体重点在推送合并和世代号；[[links.ticketmaster|票务预订（Ticketmaster）]]：同样是热点行的争用，但抢的是座位，不比较价格。
