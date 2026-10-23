---
id: hl-j11-api-methods
node: java21.j11-structured-concurrency
type: qa
step: 7
---
## Q
`StructuredTaskScope` 的 `fork`、`join`、`joinUntil`、`shutdown`、`close` 各做什么？

## A
- `fork(Callable)`：在作用域里启动一个子任务，返回 `Subtask<U>`（**不是 `Future`**）；每个子任务默认一个虚拟线程。
- `join()`：阻塞，等所有子任务完成（或被 shutdown）；可被中断；**必须在 `get` 前调用**。
- `joinUntil(Instant deadline)`：带截止时间的 `join`，超时抛 `TimeoutException` 并 shutdown。
- `shutdown()`：主动取消，中断所有还没结束的子线程；策略内部在需要时自动调用。
- `close()`：由 try-with-resources 调用，`shutdown`（如果还没）并**等待所有子线程结束**。
