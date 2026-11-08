---
id: hi-sd-tinder-7-redis-atomic
node: sd.problem-breakdowns.tinder.exam
type: qa
step: 7
---
## Q
**Tinder：用 Redis 做原子匹配检测**｜系统设计 · 问题拆解

为什么 Tinder 的实时匹配检测更适合放在 Redis，而不是 Cassandra？怎样保证原子，Redis 数据丢了怎么办？

## A
**思路。** Cassandra 擅长耐久和海量存储，但不擅长实时匹配需要的原子操作。把原子操作交给 Redis，Cassandra 继续做持久存储。

**做法。** 键仍然是排好序的用户对，如 `swipes:123:456`，值是哈希（hash），含两个字段：每人一个。用 Lua 脚本一次执行：先 HSET 写入自己的滑动，再 HGET 读对方的滑动。脚本在 Redis 里原子执行，若双方都是 right 就创建匹配。Redis Cluster 按键的哈希槽（hash slot，共 16384 个）分片，同一对用户的键完全相同，必然在同一节点。

**取舍。** 延迟低（内存），可水平扩展；代价是要管理 Redis 集群的节点故障和重新平衡。

**丢数据怎么办。** Redis 只留最近的滑动，定期刷到 Cassandra，可以激进地过期。节点丢失时最多漏掉很近的几次滑动的匹配检测，用户可以重新滑，历史记录仍在 Cassandra 里，影响可控。
