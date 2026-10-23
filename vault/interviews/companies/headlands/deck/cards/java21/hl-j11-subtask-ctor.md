---
id: hl-j11-subtask-ctor
node: java21.j11-structured-concurrency
type: qa
step: 8
---
## Q
`Subtask` 提供哪些方法和状态？`ShutdownOnFailure` 的构造器有哪两种形式，`name` 有什么用？

## A
`Subtask.get()` 取结果、`.exception()` 取异常、`.state()` 取状态，状态有三个：`UNAVAILABLE`、`SUCCESS`、`FAILED`。

构造器：
- `new StructuredTaskScope.ShutdownOnFailure()`：默认虚拟线程；
- `new ...ShutdownOnFailure(String name, ThreadFactory factory)`：起名并指定线程工厂，例如 `Thread.ofVirtual().factory()`。`name` 会出现在线程 dump 里，用来把线程对回作用域。

换成平台线程工厂就回到线程成本问题。
