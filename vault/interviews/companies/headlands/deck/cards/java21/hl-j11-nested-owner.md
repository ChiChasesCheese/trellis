---
id: hl-j11-nested-owner
node: java21.j11-structured-concurrency
type: qa
step: 20
---
## Q
子任务里想再并行做几件事时，能不能用外层的 `StructuredTaskScope`？该怎么做？

## A
不能。**只有创建作用域的线程（owner）才能 `fork`**，把 `scope` 传给别的线程用会抛 `WrongThreadException`。

正确做法：在子任务里**开自己的新作用域**（嵌套）。嵌套的作用域必须按顺序关闭（先开的后关），否则抛 `StructureViolationException`，这是 JVM 强制执行「结构化」的方式。
