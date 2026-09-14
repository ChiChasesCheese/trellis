---
id: distributed-xa-in-practice
node: distributed.transactions.distributed
type: qa
---
## Q
What is XA, and what specifically goes wrong when a team adopts it to keep a database and a message broker in sync?

## A
XA is the standard C API/protocol for 2PC across heterogeneous resource managers (a DB, a JMS broker, another DB), driven by a transaction manager that usually runs **in the application process** (JTA in a Java app server, `@Transactional` spanning two `XADataSource`s).

Where it goes wrong:

- **The transaction manager becomes stateful and critical.** Its log holds the commit decisions, so it must be durable and highly available — but it lives in an application server people treat as stateless and redeploy freely. Lose that log, keep in-doubt transactions forever.
- **In-doubt transactions require a DBA.** Recovery means listing prepared transactions (`XA RECOVER`, Postgres `pg_prepared_xacts`) and manually committing/rolling back. Meanwhile the locks are still held, and Postgres won't advance its snapshot horizon, so vacuum stalls and bloat grows.
- **Locks are held across network calls**, so throughput collapses (commonly cited as an order of magnitude) and one slow participant stalls the rest.
- **Coverage is thin in modern stacks**: HTTP/gRPC services, most cloud-managed datastores, and Kafka do not implement XA at all — so the pattern doesn't even apply to the microservice case people reach for it in.

Modern default: outbox + idempotent consumers for DB↔broker, sagas for cross-service workflows.

## Q zh
XA 是什么？当一个团队用它来保持数据库和消息代理同步时，具体会出什么问题？

## A zh
XA 是跨异构资源管理器（一个数据库、一个 JMS broker、另一个数据库）做 2PC 的标准 C API/协议，由一个事务管理器驱动，而这个管理器通常运行**在应用进程里**（Java 应用服务器里的 JTA，`@Transactional` 横跨两个 `XADataSource`）。

出问题的地方：

- **事务管理器变成了有状态且关键的组件。** 它的日志保存着提交决定，所以必须持久且高可用——但它偏偏活在一个被当作无状态、可以随意重新部署的应用服务器里。丢了这份日志，悬而未决的事务就永远悬着。
- **悬而未决的事务需要 DBA 介入。** 恢复意味着列出已 prepare 的事务（`XA RECOVER`，Postgres 的 `pg_prepared_xacts`），然后手动提交/回滚。与此同时锁还在被持有，Postgres 也没法推进它的快照 horizon，于是 vacuum 停滞、bloat 增长。
- **锁被跨网络调用一直持有**，所以吞吐量会崩掉（常被引用为下降一个数量级），而且一个慢参与者会拖住所有其他人。
- **在现代技术栈里覆盖面很窄**：HTTP/gRPC 服务、大多数云托管数据存储、Kafka 都完全没有实现 XA——所以这个模式甚至不适用于人们最想用它的微服务场景。

现代默认做法：DB↔broker 之间用 outbox + 幂等消费者，跨服务的工作流用 saga。
