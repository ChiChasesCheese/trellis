---
id: pl-trends-conc-intro-structured
node: trends.concurrency-evolution
type: qa
step: 5
---
## Q
结构化并发（structured concurrency）是什么？它解决“野生任务”的什么问题，`TaskGroup` 与 `StructuredTaskScope` 的行为是什么样？

## A
**问题**：传统的“启动一个后台任务”（`go f()`、`executor.submit`、`asyncio.create_task`）有点像 `goto`：任务可以比启动它的函数活得久，没人负责等它、取消它或接住它的异常。后果：任务泄漏、错误被吞掉、请求取消后后台工作继续跑。

**结构化并发的原则**：子任务的生命周期必须**嵌套**在父作用域里。离开作用域时，所有子任务都已经结束；任何子任务失败，同伴被取消，错误向上传播。就像普通函数调用，调用者等被调者返回。

**Python 3.11 的 `TaskGroup`**：

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(ok())      # sleeps 1s
    tg.create_task(bad())     # raises RuntimeError("boom")
```

真实输出：捕获到异常组 `['boom']`，整个块的耗时约 0 秒，说明睡眠的 `ok()` 被**取消**了，没有等它一秒。

**Java 的 `StructuredTaskScope`**（Java 25 仍是预览特性，需 `--enable-preview`）：

```java
try (var scope = StructuredTaskScope.open()) {
    var x = scope.fork(() -> { Thread.sleep(50); return 1; });
    var y = scope.fork(() -> { throw new IllegalStateException("boom"); });
    scope.join();            // throws: a subtask failed
}
```

真实输出：`StructuredTaskScope$FailedException: java.lang.IllegalStateException: boom`，另一个子任务被取消。

**Go 的对应物**：`errgroup`（标准扩展库）+ `context`：`g.Go(f)` 启动，`g.Wait()` 等全部，第一个错误取消共享的 `context`。是库约定，而不是语言强制。Kotlin 协程、Swift 的任务组也是同一思想。

**要记住的一点**：结构化并发不改变任务怎样被调度，它只规定任务的**所有权**与**作用域**。
