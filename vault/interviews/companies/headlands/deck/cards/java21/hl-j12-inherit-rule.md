---
id: hl-j12-inherit-rule
node: java21.j12-scoped-values
type: qa
step: 11
---
## Q
哪些线程会继承 `ScopedValue` 的绑定，哪些不会？为什么只有结构化并发能继承？

## A
- 在 `StructuredTaskScope` 里 `fork` 的子线程，**自动继承**父线程 fork 时刻的所有 `ScopedValue` 绑定。
- 普通 `new Thread`、`Thread.ofVirtual().start`、`ExecutorService.submit` 的任务**不继承**（读不到）。

原因：只有结构化并发能保证「子线程一定在父绑定范围结束前结束」，继承才安全；否则子线程可能在父已解绑后还在读。线程池线程的生命周期不受提交者控制。

对策：用 `StructuredTaskScope`，或在任务里自己重新 `where(...)`。
