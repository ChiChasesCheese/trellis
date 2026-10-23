---
id: hl-hc03-structured-scope-sum
node: problems.hc03-recursive-sum
type: qa
step: 16
---
## Q
`sumVirtual` 用 `StructuredTaskScope` 怎么写？它比手写线程或 `ExecutorService` 好在哪，有什么使用限制？

## A
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var parts = IntStream.range(0, chunks)
        .mapToObj(i -> scope.fork(() -> sumChunk(...)))
        .toList();
    scope.join().throwIfFailed();
    ...
}
```
- 一组子任务绑在一个作用域里，`try` 块退出前必须全部结束；一个失败其余被取消；`scope.fork` 默认每个子任务一个虚拟线程。
- 旧写法（`new Thread` + `join`，或 `ExecutorService` + `Future.get`）要自己保证异常时关闭、取消其余。
- `chunks < 1` 抛 `IllegalArgumentException`；不要吞掉 `InterruptedException`。
- 它在 Java 21 是**预览**特性，编译运行都要 `--enable-preview`。

**不该用虚拟线程**的场景：CPU 密集计算；长时间持有 `synchronized`（Java 21 会钉住载体线程）。

C++ 对应：没有现成的结构化并发，用 `std::async` / `std::thread` 手写；`std::async` 的 future 析构会**阻塞**，返回值被丢弃的 `std::async(...)` 会立刻同步执行完，看起来并行其实串行；固定数量工作线程 + 原子计数器分发块号时，`memory_order_relaxed` 够用（计数器只分发块号，数据可见性由 `join()` 保证）。
