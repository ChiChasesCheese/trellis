---
id: pl-conc-structured-best-practice
node: concurrency.structured-concurrency
type: qa
step: 9
---
## Q
日常写并发代码时，怎样落实结构化并发的原则？每种语言里的具体做法和何时可以例外？

## A
**总原则**：谁启动，谁等待，谁负责收尾。函数返回时，它启动的任务都应已结束或明确移交给一个有主人的长期组件。

做法：
1. **把并行分支放进作用域**：Python `async with TaskGroup()`，Java `try (var scope = StructuredTaskScope.open())`，Go `errgroup`，Rust `thread::scope`。避免裸 `create_task`、裸 `go`、裸 `new Thread`。
2. **把取消和超时放在最外层**：给整个作用域设一个截止时间，而不是每个子任务各设一个。Go 把 `context.WithTimeout` 传下去；Python `async with asyncio.timeout(...)`。
3. **子任务要响应取消**：在循环和阻塞点检查 `ctx.Done()` / `await` / `isInterrupted`；长计算每隔一段就检查。能被取消才谈得上结构化。
4. **清理放在 `finally` / `defer` / `Drop`**：取消随时可能在任何可取消点发生，持有的锁、连接、临时文件要靠清理块释放。
5. **控制扇出**：作用域里启动 10 万个子任务，用信号量或 `errgroup.SetLimit(n)` 限制同时运行数。
6. **只暴露同步接口**：并发是内部实现细节，函数对调用者表现为“调用，返回结果”，这也使测试更容易。

**例外**：需要长期存活、独立于请求的后台任务（连接池维护、指标上报），把它们挂到应用级的根作用域（服务启动时创建、关闭时统一取消），而不是挂在某个请求上。那是另一个有主人的作用域，而不是孤儿。

判断标准：读到一个 `go`、`create_task`、`start` 时问两句：它的结果谁取？它失败谁知道？答不上来就是缺陷。
