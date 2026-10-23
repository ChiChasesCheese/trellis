---
id: hl-j11-join-forgotten
node: java21.j11-structured-concurrency
type: qa
step: 19
---
## Q
下面代码错在哪？应该怎么改？
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var a = scope.fork(() -> compute());
    System.out.println(a.get());
    scope.join();
}
```

## A
`join()` 之前调用了 `a.get()`，抛 `IllegalStateException`。应先 `scope.join()`（通常带 `.throwIfFailed()`），再 `a.get()`。

相关的忘记 `join()` 后果：
- fork 后直接 `get()` → `IllegalStateException`；
- fork 后不 `join` 就退出块 → `StructureViolationException`。
