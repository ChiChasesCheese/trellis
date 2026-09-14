---
id: runtime-polyglot-error-vocabulary
node: runtimes.polyglot
type: qa
---
## Q
One service returns `timeout`, another `UPSTREAM_5XX`, and Lua turns every failure into `500`. What should the cross-runtime error contract preserve?

## A
Preserve a stable machine code, retryability, HTTP mapping, blame boundary, and optional bounded details. Separate timeout, cancellation, overload, invalid input, not found, and dependency failure; do not leak language exception strings as protocol. Each hop may wrap context for logs, but must not erase the original category. Clients need the category to choose retry, stale serving, bypass, or immediate failure safely.

## Q zh
一个服务返回 `timeout`，另一个返回 `UPSTREAM_5XX`，Lua 又把所有失败变成 `500`。跨 runtime error contract 应保留什么？

## A zh
保留稳定 machine code、retryability、HTTP mapping、blame boundary，以及可选且有界的 details。区分 timeout、cancellation、overload、invalid input、not found 和 dependency failure；不要把语言 exception string 暴露成 protocol。每一 hop 可为 log 包装 context，但不能抹掉原始 category。client 需要该类别，才能安全选择 retry、serve stale、bypass 或立即失败。
