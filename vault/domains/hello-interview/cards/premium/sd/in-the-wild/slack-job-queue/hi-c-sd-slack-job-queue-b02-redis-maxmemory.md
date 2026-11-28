---
id: hi-c-sd-slack-job-queue-b02-redis-maxmemory
node: sd.in-the-wild.slack-job-queue.beyond
type: qa
step: 2
---
## Q
**Slack 作业队列 · Redis 内存满了到底会怎样**｜拓展 · 加分

Redis 达到 `maxmemory` 后会发生什么？为什么淘汰策略不能拿来救队列？

## A
- **默认行为：** 内存策略为 `noeviction` 时，会拒绝会增加内存的写命令（入队失败），读命令仍可用。这正是"队列满了入队全失败"的表现。
- **淘汰策略不适用：** `allkeys-lru` 等策略会把键淘汰掉；对缓存很好，对队列则是悄悄丢作业——比报错更糟。作业数据不能让 Redis 自作主张地删。
- **容量规划的要点：** Redis 用作队列时，要为最坏积压留内存，或者像 Slack 那样让积压别进 Redis。同时要预留 fork 持久化时的写时复制内存余量。
- **面试用法：** 说到用 Redis 当队列，主动提"满了会怎样"。
