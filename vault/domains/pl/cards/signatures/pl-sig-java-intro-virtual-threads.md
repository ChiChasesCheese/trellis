---
id: pl-sig-java-intro-virtual-threads
node: signatures.java
type: qa
step: 4
---
## Q
Java 21 的虚拟线程（virtual thread）是什么？它怎样让“一个请求一个线程”的传统风格重新支持百万级并发，一个实测说明什么？

## A
**是什么**：虚拟线程是由 JVM 而不是操作系统调度的轻量线程。创建它的 API 与普通线程相同（`Thread.ofVirtual().start(...)`、`Executors.newVirtualThreadPerTaskExecutor()`），代码仍是同步阻塞风格。

**怎样做到**：虚拟线程的栈保存在堆上，只在运行时才“挂”到一个载体线程（carrier thread，真正的系统线程）上。当它执行阻塞操作（睡眠、网络 I/O、锁等待），JVM 把它的栈卸下，载体线程去运行别的虚拟线程；阻塞操作完成后再装回来。

**实测（本机）**：

```java
try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++)
        ex.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return 1; });
}
```

十万个各自睡眠 1 秒的任务，约 1.5 秒全部完成。同样的事情用 5000 个平台线程的缓存线程池，本机直接失败：`OutOfMemoryError: unable to create native thread`（系统线程数上限）。

**与其他语言的对应**：Go 的 goroutine（更早、语言内建）；Python/Rust 用 async/await（有函数染色）。虚拟线程的特点是**不改变编程模型**，现有的同步代码、库、调试器、线程转储都继续有效。

**使用要点**：
1. **不要池化**虚拟线程，每个任务一个新的，它们廉价。
2. **限制对下游的并发**用 `Semaphore`，而不是靠线程池大小。
3. **避免在 `synchronized` 内做阻塞 I/O**：JDK 21 里会钉住（pin）载体线程，吞吐退化；用 `ReentrantLock`。（新版本的 JDK 在改进这点。）
4. 线程局部变量（`ThreadLocal`）要少用，因为数量巨大。

**要记住的一点**：虚拟线程是 Java “保持编程模型，替换底层实现”哲学的代表，也是它在云时代保持竞争力的关键一步。
