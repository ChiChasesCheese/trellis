---
id: hi-sd-dynamodb-4-consistency
node: sd.deep-dives.dynamodb
type: qa
step: 4
---
## Q
**DynamoDB：一致性模型与底层实现**｜系统设计 · 深入技术

DynamoDB 的一致性怎么选？最终一致读和强一致读各自的代价和底层路径是什么？

## A
**逐请求选择。** 不是表级配置，而是在每次 GetItem / Query / Scan 上用 ConsistentRead=true 指定。默认最终一致，整体上偏 AP 并具备 BASE 特性，但仍可在需要时（如预订系统）要强一致。

**最终一致读（默认）。** 三个副本里任何一个都能服务；leader 在多数确认后异步复制给 follower，所以 follower 可能还没有最新写入。更省容量（每 4KB 0.5 RCU），延迟更低。

**强一致读。** 路由到该分区的 leader，因为所有写入先经过它，数据最新。每 4KB 1 RCU，是最终一致读的两倍，延迟可能略高。

**限制。** GSI 不支持强一致读，只有主表和 LSI 支持，设计需要强一致的访问模式时要注意。

**事务。** 支持 ACID 事务（TransactWriteItems / TransactGetItems），可跨表最多 100 个条目、可串行化隔离，因此「NoSQL 没有事务」的老批评已经不成立。
