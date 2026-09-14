---
id: architecture-serverless-constraints
node: architecture.serverless
type: qa
---
## Q
Name the FaaS execution-model constraints that break naive designs — and the classic database mistake.

## A
- **Ephemeral, stateless instances**: no local state between invocations (disk/memory may or may not survive); anything durable goes to external stores.
- **Execution time caps** (e.g. Lambda 15 min) and no long-lived connections — websockets/streaming need a managed gateway pattern, not a function holding a socket.
- **Scale-out is the failure mode for downstreams**: 1000 concurrent invocations = 1000 clients hammering whatever's behind them.

Classic mistake: each instance opening its own **RDBMS connection** — a traffic spike exhausts the database's connection limit. Fix: a connection proxy/pooler (RDS Proxy, PgBouncer) or an HTTP-native serverless database.

## Q zh
命名打破朴素设计的 FaaS 执行模型约束——经典数据库错误。

## A zh
- **临时、无状态实例**：调用之间没有本地状态（磁盘/内存可能也可能不会生存）；任何持久东西去外部存储。
- **执行时间上限**（例如 Lambda 15 分钟）和没有长期连接——websocket/流需要托管网关模式，不是函数持有套接字。
- **横向扩展是下游的故障模式**：1000 个并发调用 = 1000 个客户端锤击它们后面的任何东西。

经典错误：每个实例打开自己的**RDBMS 连接** ——流量峰值耗尽数据库的连接限制。修复：连接代理/pooler（RDS Proxy、PgBouncer）或 HTTP 原生 serverless 数据库。
