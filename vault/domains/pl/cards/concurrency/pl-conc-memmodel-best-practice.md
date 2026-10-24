---
id: pl-conc-memmodel-best-practice
node: concurrency.atomics-memory-models
type: qa
step: 8
---
## Q
实际工程里，什么时候该用原子操作和 `volatile`，什么时候不该？选内存顺序的经验法则是什么？

## A
**默认顺序**：先用高层同步（锁、通道、线程安全容器、`Once`、`Future`），它们已经建立好了 happens-before。大多数程序不需要直接碰原子操作。

**适合用原子操作的场景**：
1. **独立的计数器和统计**（请求数、字节数）：`Relaxed` 的 `fetch_add` 就够。实测 4 线程 × 100 万次：Go 的 `atomic.Int64` 约 60 毫秒，`Mutex` 约 171 毫秒（一次测量）。
2. **单个标志位**（停止、就绪）：Java 的 `volatile boolean`，Go 的 `atomic.Bool`，Rust 的 `AtomicBool` 配 `Release`/`Acquire`。
3. **一次性发布不可变对象**：先把对象构造完整，再用一次 `volatile`/`Release` 写发布引用，读方看到引用就看到完整对象。

**不要用原子操作的场景**：
- 多个变量要同时保持一致（余额和流水）：原子操作只保护单个变量，需要锁。
- 看似简单的“无锁队列、无锁栈”：ABA 问题、内存回收、弱序，都是专家领域。优先用 JDK 的 `ConcurrentLinkedQueue`、Rust 的 crossbeam 等经过验证的库。

**选顺序**：
- 不确定就用最强的（Rust `SeqCst`，Java/Go 默认）；先正确，再用性能分析证明它是瓶颈，才降到 `Acquire`/`Release`/`Relaxed`，并在注释里写明配对关系。
- 每个 `Release` 都要有对应的 `Acquire`；只有一边写了，就等于没写。

**验证**：Go 的 `-race`；Java 的 jcstress；Rust 的 loom/Miri。弱序 bug 在 x86 上可能永远不出现，要在 ARM 上也测。在 Apple Silicon 上做 100 万轮写缓冲实验，`Relaxed` 出现了 10 次“两个都读到 0”，`SeqCst` 为 0（一次测量）。
