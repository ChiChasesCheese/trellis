---
id: hi-c-sd-multi-step-processes-b03-activity-timeouts
node: sd.patterns.multi-step-processes.beyond
type: qa
step: 3
---
## Q
**多步流程 · Activity 的超时与心跳**｜拓展 · 加分

Temporal 的 Activity 怎么发现 worker 死了，长任务怎么避免被误判超时？

## A
- **超时是引擎判断失败的唯一依据：** 引擎无法知道 worker 是慢还是死了，只能靠超时。常用的有启动到结束的超时（单次尝试的最长时间）和整个调度到结束的超时（含所有重试的总时限）。
- **心跳（heartbeat）：** 长时间运行的 Activity 定期上报心跳，引擎设置心跳超时；worker 死了心跳停止，引擎很快就能重新调度，而不必等到很长的总超时。心跳里还可以带进度，重试时从进度继续。
- **重试策略：** 初始间隔、退避系数、最大次数；明确哪些错误不可重试（业务拒绝），避免对必然失败的调用无限重试。
- **配套：** 超时重试意味着可能重复执行，所以 Activity 要幂等。
