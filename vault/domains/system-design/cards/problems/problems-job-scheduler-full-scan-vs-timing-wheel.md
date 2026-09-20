---
id: problems-job-scheduler-full-scan-vs-timing-wheel
node: problems.foundations.job-scheduler
type: qa
step: 1
tags: [grown]
---
## Q
In a distributed job scheduler holding 3x10^8 outstanding scheduled jobs, why does a naive full-table scan for due jobs (WHERE due_ts <= now(), even with an index touching every not-yet-due row) fail to meet a P95 < 1 second trigger-latency target, and what does this force the design toward?

## A
At a conservative 1 microsecond per row, scanning 3x10^8 outstanding rows once takes about 300 seconds -- three hundred times slower than the 1-second P95 target, and that cost only grows as more jobs get scheduled, regardless of how many are actually due right now. This forces the design toward a discovery mechanism whose cost scales with how many jobs are due, not with how many are outstanding: a hierarchical timing wheel (cascading circular buffers of increasing time granularity, each giving O(1) insert/expire) for the near-term window, backed by a time-bucketed persistent store for everything further out.

## Q zh
在一个持有 3×10^8 个待定任务的分布式任务调度器里，为什么朴素的全表扫描找到期任务（WHERE due_ts <= now()，即使有索引也要触达每一行未到期的记录）满足不了 P95 < 1 秒的触发延迟目标？这个结论把设计逼向了什么方向？

## A zh
按保守的每行 1 微秒计算，扫描 3×10^8 行待定记录一次大约要 300 秒——比 1 秒的 P95 目标慢 300 倍，而且这个成本只会随着待定任务越来越多而持续增长，跟当下实际到期的任务数量无关。这把设计逼向一种成本只跟「当前有多少到期」成正比、而不是跟「总共有多少待定」成正比的发现机制：用分层时间轮（hierarchical timing wheel，级联多层不同时间粒度的循环缓冲区，每层都能做到 O(1) 的插入/到期检查）处理近期窗口，更远期的任务留在按时间分桶的持久化存储里。
