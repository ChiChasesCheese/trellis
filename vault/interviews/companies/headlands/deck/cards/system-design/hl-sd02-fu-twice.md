---
id: hl-sd02-fu-twice
node: system-design.sd02-job-scheduler
type: qa
step: 34
---
## Q
追问：会不会触发两次？怎么保证「恰好一次」？

## A
不承诺 exactly-once。at-least-once 的成因：交付成功与写 `Fired` 之间的崩溃窗口，恢复后会重发；反向顺序会丢触发（违反 I4），所以顺序固定。下游用 jobId 作幂等键去重；若下游是同一数据库，业务结果与「已处理 jobId」同事务提交才有效果上的 exactly-once。调度器自身保证同一任务在日志里只有一个活动状态。

可以说：「交付可以重复，效果靠幂等键去重。我宁可重复也不丢。」
