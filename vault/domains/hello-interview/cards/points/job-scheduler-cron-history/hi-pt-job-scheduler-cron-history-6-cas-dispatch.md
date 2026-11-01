---
id: hi-pt-job-scheduler-cron-history-6-cas-dispatch
node: qb.sd.job-scheduler-cron-history.points
type: qa
step: 6
---
## Q
**分布式任务调度器 · CAS 保证只分发一次**｜出自：分布式任务调度器 › 整体设计

调度器分片属主切换时可能出现两个调度器同时处理同一行。怎样保证同一次触发只分发一次？

## A
**要点。** 触发时执行 `UPDATE run SET state='QUEUED', version=version+1 WHERE run_id=? AND state='SCHEDULED'`，影响行数为 1 才投队列。
**为什么。** CAS 是不重复分发的真正防线，选主只是为了减少无谓竞争。
**高可用。** 分片属主靠租约或协调服务（etcd、ZooKeeper）选出，宕机后另一节点在租约过期后接管；短暂重叠也不会双发。
