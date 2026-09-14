---
id: storage-connection-pooling
node: storage.relational.operations
type: qa
---
## Q
Why does a fleet of 200 app instances talking straight to Postgres fall over even at modest QPS, and what is the standard fix?

## A
Each Postgres connection is a **forked OS process** with its own memory (~5–10MB) and scheduling cost; a few thousand connections exhausts memory and burns CPU on context switching even if most connections are idle. 200 instances × 20-connection app pools = 4,000 connections.

Fix: an external pooler (**PgBouncer**, RDS Proxy) in transaction mode, multiplexing thousands of client connections onto tens–hundreds of server connections. Caveat: transaction pooling breaks session state (prepared statements, `SET`, advisory locks held across transactions).

## Q zh
为什么一队 200 个应用实例直接连到 Postgres 即使在适度的 QPS 也会倒下，标准修复是什么？

## A zh
每个 Postgres 连接是一个**分叉的 OS 进程**，有自己的内存（~5–10MB）和调度成本；几千个连接会耗尽内存，即使大多数连接空闲也会在上下文切换上烧 CPU。200 实例 × 20 连接应用池 = 4,000 个连接。

修复：一个外部池化器（**PgBouncer**、RDS Proxy）以 transaction 模式，复用数千个客户端连接到几十到几百个服务器连接。注意：transaction 池化会破坏会话状态（prepared statement、`SET`、跨事务持有的 advisory lock）。
