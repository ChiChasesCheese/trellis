---
id: clone-tasks-pipes-suspended
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
把生产数据库克隆一份做测试，为什么不必担心克隆里的任务（Task）立刻开始跑、或 Snowpipe 自动摄取重复加载文件？

## A
克隆出的任务默认处于挂起状态，需要逐个 `ALTER TASK … RESUME`；告警（alert）同样默认挂起。对管道（pipe）：`AUTO_INGEST = FALSE` 的克隆默认暂停，`AUTO_INGEST = TRUE` 的克隆处于 `STOPPED_CLONED` 状态，不积累新文件的事件通知，恢复后只处理新通知触发的文件。另外，引用内部暂存区（internal stage）的管道根本不会被克隆。
