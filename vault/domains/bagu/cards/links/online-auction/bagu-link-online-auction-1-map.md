---
id: bagu-link-online-auction-1-map
node: links.online-auction
type: qa
step: 1
---
## Q
**在线拍卖（eBay） · 会被追问哪些八股**｜必会

设计在线拍卖（eBay）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 同一件拍品的出价必须串行且只有更高价生效。基础是：乐观更新与行锁、多实例下 JVM 锁无效、Redis 锁串行、MVCC 版本链、延迟任务触发结束、幂等去重。

**下钻路线。**
- 多人同时出价 → `WHERE price < ?` 乐观更新，或锁拍品行，[[b.mysql.lock-types|MySQL 锁分类]]
- 为什么 JVM 锁在集群不管用 → 多实例要用数据库乐观锁（版本号），[[b.runtime.java-sync-lock|synchronized、ReentrantLock 与锁升级]]
- 要不要上分布式锁 → 优先对最高价做条件更新；真要串行再用 Redis 锁，释放校验持有者，[[b.distributed.lock-choice|Redis 锁、ZooKeeper 锁、数据库锁怎么选]]
- 同一行频繁更新，旧版本放哪 → 隐藏列加 undo 链，长事务让链变长，[[a.mysql.mvcc|MVCC]]
- 出价表索引列顺序 → 等值在前、范围在后、排序最后，[[a.mysql.leftmost-index-failure|联合索引、最左前缀与索引失效]]
- 拍卖到点怎么结束 → 延迟消息或时间轮，最后一秒延长则旧消息作废，[[b.mq.delay-message|延迟消息怎么实现]]
- 结算只能执行一次且耗时不定 → 看门狗续期的锁，崩溃后才让别人接手，[[a.distributed.lock-watchdog|锁过期了业务没完]]
- 同一个出价被改价重发 → 请求指纹不同，返回 422，[[a.idem.payment-idempotency|支付与扣款接口的幂等设计]]

**业务场景。** 直播间拍卖最后一秒出价密集，出价预授权冻结保证金，赢家付款失败时才转给第二高者。
**系统设计。** [[links.tt-realtime-auction-bidding|实时竞价拍卖]]：同样的出价排序，重点在推送合并和世代号；[[links.ticketmaster|票务预订（Ticketmaster）]]：同样争用热点行，但抢的是座位，不比较价格。
