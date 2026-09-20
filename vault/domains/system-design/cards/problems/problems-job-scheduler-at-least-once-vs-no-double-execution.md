---
id: problems-job-scheduler-at-least-once-vs-no-double-execution
node: problems.foundations.job-scheduler
type: qa
step: 3
tags: [grown]
---
## Q
In a distributed job scheduler, why are 'the job executes at least once' and 'the job never executes concurrently on two workers at the same time' two completely independent guarantees that both need their own mechanism, rather than one implying the other?

## A
At-least-once is about not silently dropping a job -- it is satisfied even if the same job runs sequentially multiple times across separate, non-overlapping attempts, and is achieved by having the scheduler err on the side of redelivering whenever it is uncertain a dispatch succeeded, combined with idempotent workers absorbing any resulting duplicate execution. Preventing concurrent double execution is about mutual exclusion at a single point in time -- a worker that only paused (rather than truly died) resuming and writing results after a second worker has already taken over the same job -- and needs its own mechanism (a lease with a fencing token) because idempotency alone does nothing to stop two workers from running simultaneously and racing on side effects before either one's write is even attempted.

## Q zh
在一个分布式任务调度器里，为什么「任务至少被执行一次」和「任务不会被两个 worker 同时并发执行」是两个完全独立、各自需要不同机制的保证，而不是满足其中一个就自动满足另一个？

## A zh
至少一次执行关心的是「不会悄悄丢任务」——即使同一个任务在若干次互不重叠的尝试里被顺序执行了多次，这条保证依然成立，实现方式是调度器在不确定上一次分发是否成功时宁可重新投递，再配合幂等的 worker 吸收由此产生的重复执行。防止并发重复执行关心的是某一时刻的互斥性——一个只是暂停（而非真正死亡）的 worker 恢复后，在第二个 worker 已经接管同一任务的情况下仍然写入结果——这需要自己的机制（带 fencing token 的租约），因为幂等性本身完全阻止不了两个 worker 同时运行、在任何一方真正写入之前就已经产生副作用层面的竞争。
