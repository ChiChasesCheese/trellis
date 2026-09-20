---
nodes: [problems.foundations.lock-service]
url: https://etcd.io/docs/v3.6/learning/api/
tags: [reference]
---
# etcd 文档 — Learning: API

值得读：一手产品文档，本题解"读默认线性一致、可选可串行化"这条设计直接对应 etcd `Range`
API 的 `serializable` 选项；`keepAlive`/lease 续约机制的命名也参考了 etcd 的 Lease API。
和本题解的分歧在于：etcd 文档没有给出 TTL 的默认值（TTL 由调用方在建租约时协商），本题解
的 15 秒 TTL、5 秒续约间隔是按自己的容量估算和故障判定权衡独立选定的，不是抄自 etcd 的
默认值。
