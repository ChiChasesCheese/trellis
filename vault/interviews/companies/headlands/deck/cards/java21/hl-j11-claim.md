---
id: hl-j11-claim
node: java21.j11-structured-concurrency
type: qa
step: 3
---
## Q
结构化并发（structured concurrency）的核心主张是什么？它要保证什么性质？

## A
主张：把「开一组子任务」也变成**有入口有出口的代码块**。

保证：**块结束时所有子任务一定已结束或被取消**，失败可统一处理，取消统一传播。子任务的生命周期被词法作用域（lexical scope）框住，不会泄漏。

对比 `ExecutorService`：任务只由池管理，与发起它的代码块无关，没有「块结束必须结束」的约束，取消和异常也不自动传播。
