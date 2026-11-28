---
id: hi-pt-github-cicd-workflow-10-thread-pool-vs-runner
node: qb.sd.github-cicd-workflow.points
type: qa
step: 10
---
## Q
**CI/CD 平台 · 线程池与执行机的对应**｜追问 · 出自：CI/CD 平台 › 取舍与追问

单进程的线程池里 worker 从队列取任务，分布式 CI 平台的执行机也从队列取任务。两者在失败模型上的关键差别是什么，因此哪个机制要变？还有哪些单机机制对应变形？

## A
**差别。** 线程池的 worker 崩了整个进程一起崩，任务归属不会悬空；执行机会无声消失。

**变形。** 锁变成租约加围栏号；按拓扑序执行依赖图，变成依赖表加完成事件触发后继就绪；进程标准输出管道，变成带序号的分块日志。
