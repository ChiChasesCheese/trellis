---
id: hl-j11-misuse-exceptions
node: java21.j11-structured-concurrency
type: qa
step: 9
---
## Q
使用 `StructuredTaskScope` 违反规则时会抛哪些异常？分别对应什么违规？

## A
- `WrongThreadException`：不是创建作用域的线程（owner）去 `fork`/`join`/`close`。
- `IllegalStateException`：在 `join()` **之前**调用 `subtask.get()`。
- `StructureViolationException`：fork 后**不 `join` 就退出块**，或作用域嵌套时**不按顺序关闭**。

另外：`ShutdownOnFailure.throwIfFailed()` 把第一个失败子任务的异常包成 `ExecutionException` 抛出，`throwIfFailed(Function)` 可映射成自己的异常类型；`ShutdownOnSuccess.result()` 返回第一个成功的结果，全部失败则抛 `ExecutionException`。
