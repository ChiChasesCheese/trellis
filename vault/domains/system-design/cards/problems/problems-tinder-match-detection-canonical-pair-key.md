---
id: problems-tinder-match-detection-canonical-pair-key
node: problems.social.tinder
type: qa
step: 6
tags: [grown]
---
## Q
A dating app must detect a mutual match exactly once when two users right-swipe each other within milliseconds of each other. Compare three approaches — a relational transaction with row locking, an ordered log (e.g. Kafka) partitioned by a pair key with a downstream stream processor, and an atomic check-and-set on a canonical pair key in an in-memory store — and explain why the third is chosen when the product requires the user to see 'it's a match!' immediately after the deciding swipe.

## A
A relational transaction is correct but throughput-bound by the relational primary's assumed ceiling (a few thousand/sec), which the computed right-swipe peak (about 10,417 QPS) already exceeds by roughly 3.5x. An ordered log partitioned by pair key guarantees the same two swipes are processed in order by one consumer, avoiding the race, but introduces asynchronous processing latency between the swipe and the match confirmation — unacceptable when the product must show the match instantly on the deciding swipe. The atomic check-and-set on a canonical pair key (built by sorting the two user ids into a fixed order so both swipes land on the same key) resolves the race synchronously within the swipe's own request, and the computed safety margin (about 17.3x over a single Redis instance's benchmark) shows a single instance is sufficient at this scale — durable match records and notifications are then written asynchronously after the atomic gate has already decided.

## Q zh
约会应用必须在两个用户几毫秒内互相右滑时恰好一次检测到匹配。比较三种方案——带行锁的关系型事务、按 pair key 分区的有序日志（如 Kafka）加下游流处理器、以及在内存存储上对 canonical pair key 做原子 check-and-set——并解释为什么产品要求用户在划出决定性一次右滑后立刻看到「配对成功」时，第三种方案会被选中。

## A zh
关系型事务正确，但吞吐受限于关系型主库假设的上限（几千/秒），而算出的右滑峰值（约 10,417 QPS）已经超出这个上限约 3.5 倍。按 pair key 分区的有序日志能保证同一对用户的两次滑动被同一个消费者按顺序处理，避免竞态，但在滑动和匹配确认之间引入了异步处理延迟——当产品要求用户在决定性的一次滑动后立刻看到匹配时，这是不可接受的。在 canonical pair key（把两个用户 id 按固定规则排序拼接而成，保证两次滑动落在同一个 key 上）上做原子 check-and-set，能在滑动本身的请求里同步解决这场竞态，而算出的安全边际（相对单个 Redis 实例基准约 17.3 倍）说明这个规模下单实例就够用——持久化的匹配记录和通知则在原子网关已经做出判定之后异步写入。
