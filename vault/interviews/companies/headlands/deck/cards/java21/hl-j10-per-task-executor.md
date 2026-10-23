---
id: hl-j10-per-task-executor
node: java21.j10-virtual-threads
type: qa
step: 8
---
## Q
`Executors.newVirtualThreadPerTaskExecutor()` 怎么写？它是线程池吗？离开 try-with-resources 时发生什么？

## A
```java
try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Quote> f = ex.submit(() -> fetch(sym));
    Quote q = f.get();
}   // close()：不再接新任务，并等所有已提交任务结束
```
- 它**不是线程池**：每次 `submit` 新建一个虚拟线程，任务结束线程消失，不复用，因为便宜到不需要复用。
- Java 19 起 `ExecutorService` 实现 `AutoCloseable`，块结束自动 `shutdown()` 再 `awaitTermination()`。老的 `ExecutorService` 忘了 `shutdown()` 会让 JVM 退不出去。
- 与固定池版本只差一行 `Executors.xxx`，并发度却能从 50 提到 10 000。
