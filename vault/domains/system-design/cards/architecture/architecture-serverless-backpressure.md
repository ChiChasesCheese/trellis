---
id: architecture-serverless-backpressure
node: architecture.serverless
type: qa
---
## Q
A traffic spike makes your FaaS platform spawn 3,000 concurrent function instances, which flatten the database behind them. What is the structural mismatch, and the two standard fixes?

## A
FaaS **scales concurrency near-instantly and unboundedly**, while downstream stateful systems (relational DBs, third-party APIs) have hard concurrency/connection ceilings — serverless removed *your* bottleneck and turned it into a weapon against dependencies. Each instance also opens its own DB connections, multiplying the damage.

- **Cap and queue**: set reserved/max concurrency on the function, and put a **queue between trigger and function** (queue-based load leveling) so bursts buffer instead of amplify.
- **Connection proxying**: a pooler (e.g. RDS Proxy, pgbouncer) multiplexes thousands of function instances onto a bounded connection pool.

## Q zh
流量峰值使你的 FaaS 平台生成 3,000 个并发函数实例，它们压平后面的数据库。结构不匹配是什么，两个标准修复？

## A zh
FaaS**近乎瞬间和无界缩放并发**，而下游有状态系统（关系 DB、第三方 API）有硬并发/连接上限——serverless 移除*你的*瓶颈并将其转变为对依赖的武器。每个实例也打开它自己的 DB 连接，乘以伤害。

- **Cap 和 queue**：在函数上设置 reserved/max 并发，并在触发器和函数之间放置一个**queue**（queue 基础负载平衡）所以突发缓冲而不是放大。
- **连接代理**：一个 pooler（例如 RDS Proxy、pgbouncer）复用数千个函数实例到一个有界连接池。
