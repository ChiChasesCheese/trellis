---
id: hl-j12-submit-vs-fork
node: java21.j12-scoped-values
type: qa
step: 22
---
## Q
在 `ExecutorService.submit(() -> log("..."))` 里，任务能看到提交者的 `ScopedValue` 绑定吗？在 `StructuredTaskScope.fork` 里呢？为什么有区别？

## A
- `submit`：**不能**。任务在池线程上运行，线程池线程的生命周期不受提交者控制，可能在父已解绑后才运行，所以不继承。
- `fork`：**可以**。子线程一定在 scope 关闭前结束，继承父绑定安全。

要在池里用，就在任务里自己重新 `where(...)`，或改用 `StructuredTaskScope`。
