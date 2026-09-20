---
id: problems-job-scheduler-fencing-token-lease
node: problems.foundations.job-scheduler
type: qa
step: 4
tags: [grown]
---
## Q
In a distributed job scheduler, why is a lease timeout ALONE insufficient to guarantee a job never runs concurrently on two workers, and what does adding a monotonically increasing fencing token fix?

## A
A lease timeout only controls how long the system waits before allowing a second worker to take over -- it cannot stop the first worker from resuming after a pause (GC stall, network partition) still believing it holds the lease, and writing its result anyway even though a second worker has since been granted the same job. A monotonically increasing fencing token fixes this by making the resource being written to -- not the worker -- the enforcer: every lease grant carries a token strictly greater than the last one issued for that job, and the store rejects any write carrying a token older than the latest one it has already accepted, so the resumed first worker's stale-token write is rejected outright regardless of whether that worker believes its execution succeeded.

## Q zh
在一个分布式任务调度器里，为什么单靠租约超时不足以保证一个任务不会被两个 worker 并发执行？加上一个单调递增的 fencing token 修复了什么？

## A zh
租约超时只能控制系统等多久之后才允许第二个 worker 接管——它阻止不了第一个 worker 在暂停（GC 停顿、网络分区）后恢复时仍然认为自己持有租约、继续写入结果，哪怕这期间第二个 worker 已经拿到了同一个任务。单调递增的 fencing token 通过让被写入的资源本身（而不是 worker）来做执行者，修复了这个问题：每次发放租约都携带一个严格大于该任务上一次 token 的新 token，存储层拒绝任何携带比自己已接受过的最新 token 更旧的写入——这样即使已恢复的第一个 worker 自认为执行成功，它带着过期 token 的写入也会被直接拒绝。
