---
id: reliability-load-fault-success
node: reliability.load-testing
type: qa
---
## Q
During a fault test, the team injects 2 seconds of origin latency and sees no process crash. Is that a pass?

## A
Not by itself. Define pass criteria in user and protection terms: bounded p99, acceptable stale or error policy, no retry amplification, bounded queues and goroutines, origin concurrency below limit, and recovery within a stated time after fault removal. "Did not crash" can still mean zero useful goodput and an unrecoverable backlog.

## Q zh
fault test 中，团队注入了 2-second origin latency，process 没有 crash。这算通过吗？

## A zh
不能仅凭这一点判断。pass criteria 应以 user outcome 和 protection 定义：bounded p99、可接受的 stale 或 error policy、没有 retry amplification、bounded queue 与 goroutine、origin concurrency 低于 limit，并且 fault 移除后在规定时间内恢复。“没有 crash”仍可能意味着 useful goodput 为零，且 backlog 无法恢复。
