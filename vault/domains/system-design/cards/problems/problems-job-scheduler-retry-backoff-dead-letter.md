---
id: problems-job-scheduler-retry-backoff-dead-letter
node: problems.foundations.job-scheduler
type: qa
step: 7
tags: [grown]
---
## Q
In a distributed job scheduler, why does retrying a failed job with fixed-interval, unlimited retries cause worse problems than exponential backoff with a retry cap and dead-letter queue, specifically for a job that fails permanently (e.g. malformed payload) rather than transiently?

## A
A permanently failing job retried at a fixed interval forever keeps consuming queue and worker capacity indefinitely without ever succeeding, and gives operators no signal that something needs human attention -- it just silently loops. Exponential backoff with a retry cap (e.g. delays of 1s, 2s, 4s, 8s, 16s across 5 attempts, 31 seconds of cumulative backoff) bounds how much capacity a single failing job can consume before the system gives up automatically; once the cap is hit, the job moves to a dead-letter queue that halts automatic retries, preserves full failure context (error, last lease token, execution history), and surfaces the job for manual inspection instead of retrying it forever.

## Q zh
在一个分布式任务调度器里，对于一个永久性失败（比如 payload 格式错误）而非瞬时故障的任务，为什么固定间隔、无限次数的重试比指数退避加重试上限加死信队列会造成更坏的问题？

## A zh
一个永久性失败的任务如果按固定间隔无限重试，会一直无休止地占用队列和 worker 容量却永远不会成功，也不给运维任何「这里需要人介入」的信号——它只是悄悄地无限循环。指数退避加重试上限（比如 5 次尝试分别延迟 1s、2s、4s、8s、16s，累计退避 31 秒）限定了单个失败任务在系统自动放弃之前最多能消耗多少容量；一旦达到上限，任务进入死信队列（dead-letter queue），停止自动重试、保留完整的失败上下文（错误信息、最后一次 lease token、执行历史），把这个任务暴露出来等待人工排查，而不是无限重试下去。
