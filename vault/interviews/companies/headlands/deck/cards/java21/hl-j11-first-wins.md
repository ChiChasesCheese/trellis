---
id: hl-j11-first-wins
node: java21.j11-structured-concurrency
type: qa
step: 11
---
## Q
向 NYSE（300 ms）、NASDAQ（80 ms）、ARCA（500 ms）查同一个报价，谁先回用谁，用 `ShutdownOnSuccess` 怎么写？另外两个子任务会怎样？

## A
```java
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> query("NYSE", 300));
    scope.fork(() -> query("NASDAQ", 80));
    scope.fork(() -> query("ARCA", 500));
    String first = scope.join().result();
}
```
结果拿到 NASDAQ；ARCA 和 NYSE 被中断取消（`InterruptedException`）。重点：离开 `try` 块（`close()` 等待之后）三个子线程**确定**都已结束，无需自己 `awaitTermination`。
