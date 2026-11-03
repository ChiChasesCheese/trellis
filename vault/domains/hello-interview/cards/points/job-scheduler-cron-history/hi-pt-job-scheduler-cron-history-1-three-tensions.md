---
id: hi-pt-job-scheduler-cron-history-1-three-tensions
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 1
---
## Q
**分布式任务调度器 · 三件互相拉扯的事**｜必会 · 出自：分布式任务调度器 › 需求

设计峰值每秒 1 万个任务执行、含 cron 和一年执行历史的分布式任务调度器。难点为什么不是"存一张任务表再定时查"？

## A
**要点。** 三件事互相拉扯：在亿级待定任务里亚秒级找出现在到期的一小撮；worker 随时会死，仍要保证每次触发至少执行一次且不会同时执行两次；一年的执行历史与热的调度状态分开存，让两边不互相拖垮。
