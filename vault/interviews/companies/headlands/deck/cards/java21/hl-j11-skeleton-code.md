---
id: hl-j11-skeleton-code
node: java21.j11-structured-concurrency
type: qa
step: 5
---
## Q
写出 JDK 21 `StructuredTaskScope.ShutdownOnFailure` 并行取行情和额度、全部成功才使用结果的完整骨架。

## A
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String>  quote = scope.fork(() -> fetchQuote());
    Subtask<Integer> limit = scope.fork(() -> fetchLimit());
    scope.join()              // 等所有子任务结束
         .throwIfFailed();    // 有失败就抛
    use(quote.get(), limit.get());   // join 之后才能 get
}   // close()：保证所有子线程已结束
```
顺序：开作用域 → `fork` 每个子任务（默认一个虚拟线程）→ `join()` → 按策略检查（`throwIfFailed`）→ `get()` → 退出块时 `close()`。这是预览 API，JDK 25 写法完全不同。
