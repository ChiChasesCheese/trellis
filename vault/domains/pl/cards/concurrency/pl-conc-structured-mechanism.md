---
id: pl-conc-structured-mechanism
node: concurrency.structured-concurrency
type: qa
step: 6
---
## Q
一个结构化并发的作用域内，三个子任务 A、B、C，B 在 100 毫秒时失败，其余要 500 毫秒。Python、Java、Go 分别会发生什么？背后的机制是什么？

## A
实验：A、C 各需 500 毫秒，B 在 100 毫秒后失败。三门语言的结果几乎一致（真实输出）：

- Python `asyncio.TaskGroup`：
```
C cancelled
A cancelled
caught: ['B failed']
scope exited; no task outlives it
```
- Java 25 `StructuredTaskScope`（预览特性，需 `--enable-preview`）：
```
C cancelled
A cancelled
caught: ...StructuredTaskScope$FailedException: IllegalStateException: B failed
scope exited
```
- Go `errgroup.WithContext`（`golang.org/x/sync`）：
```
A cancelled
C cancelled
Wait returned: B failed
```

机制是同一套：
1. **作用域持有子任务的集合**，退出作用域（`async with` 结束、`try-with-resources` 的 `close`、`g.Wait()`）时必须等待全部完成。
2. **第一个失败触发取消**：作用域把取消信号发给仍在运行的兄弟。Python 向任务注入 `CancelledError`；Java 对线程发 `interrupt`；Go 取消共享的 `context.Context`，任务要在阻塞点监听 `ctx.Done()`。
3. **取消是协作式的**：任务只有在到达可取消点（`await`、`sleep`、`select`）时才响应。一个不让出的死循环取消不了。
4. **错误聚合**：Python 把多个并发错误包成 `ExceptionGroup`（用 `except*` 捕获）；Java 抛 `FailedException`；Go 的 `errgroup` 只返回第一个错误。

Rust 的 `thread::scope` 同样保证作用域结束前全部 join，但它不提供取消：线程要自己检查标志位。
