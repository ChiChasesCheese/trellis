---
id: problems-job-scheduler-cron-reuses-oneoff-discovery
node: problems.foundations.job-scheduler
type: qa
step: 5
tags: [grown]
---
## Q
In a distributed job scheduler, why does a recurring cron job not need its own separate discovery data structure alongside one-off jobs, even though a cron expression describes an infinite sequence of future trigger times?

## A
Instead of feeding the infinite cron sequence into the discovery mechanism, the scheduler precomputes only the single next due timestamp from the cron expression and stores it on the job as an ordinary due_ts field; the moment that trigger fires, the scheduler immediately recomputes and writes back the next due timestamp. This turns an infinite sequence into 'exactly one pending future timestamp at any given moment,' letting cron jobs reuse the exact same timing-wheel/time-bucket discovery path built for one-off jobs, with no separate structure needed for recurrence itself.

## Q zh
在一个分布式任务调度器里，即使一个 cron 表达式描述的是一个无限的未来触发时间序列，为什么周期性（cron）任务不需要在一次性任务之外单独维护一套发现数据结构？

## A zh
调度器不把整个无限的 cron 序列喂给发现机制，而是只从 cron 表达式预先算出下一次到期时间，把它作为一个普通的 due_ts 字段存在任务上；这次触发一旦发生，调度器立刻重新计算并写回下一次到期时间。这把一个无限序列变成了「任意时刻只有一个待定的未来时间点」，让 cron 任务可以直接复用为一次性任务搭建的同一套时间轮/时间分桶发现路径，不需要为周期性本身单独设计结构。
