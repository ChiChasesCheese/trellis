---
id: pl-cpp-concurrency-found-atomics-race
node: cpp.concurrency
type: qa
step: 4
---
## Q
数据竞争（data race）具体会造成什么？`std::atomic` 解决了什么，没有解决什么？

## A
**数据竞争**：两个线程访问同一个内存位置，至少一个是写，并且没有同步。结果是**未定义行为**。最常见的可观察后果之一是**丢失更新**：`++counter` 实际是"读、加一、写"三步，两个线程交错执行，其中一次加法被覆盖。

**本机实测**（4 个线程，各对三个计数器加 20 万次，期望 800000）：

```
expected 800000  plain 798547  atomic 800000  mutex 800000
expected 800000  plain 798723  atomic 800000  mutex 800000
```

普通 `int` 丢了一千多次，每次运行结果都不同；`std::atomic<int>` 和加互斥锁的版本都正确。

**`std::atomic<T>`**：保证对该变量的读、写、`fetch_add`、`compare_exchange` 这些操作**不可分割**：别的线程要么看到操作前，要么看到操作后，看不到中间状态。在 ARM64 上 `fetch_add` 编译成一条原子指令（`ldadd`），不需要锁。

**TSan 能把竞争变成明确报错**：用 `-fsanitize=thread` 编译同一个程序，输出：

```
WARNING: ThreadSanitizer: data race (pid=59421)
  Write of size 4 at 0x00010289c040 by thread T2: ...
  Previous write of size 4 at 0x00010289c040 by thread T1: ...
```

并指出两个冲突访问的位置。

**atomic 没有解决的**：
1. **多个变量之间的一致性**：两个独立的原子变量，各自操作都不可分割，但"同时更新两个"不是原子的；要么用锁，要么设计成一个原子变量。
2. **操作之间的顺序**：原子只保证单个变量上的操作不被撕裂，**其他普通变量的可见性**取决于内存序（`memory_order`）。
3. **复合逻辑**：先读后写的检查（check-then-act）如 `if (x == 0) x = 1;`，需要 `compare_exchange`，否则两步之间可能被插入。

**对比**：Java 的 `volatile` 与 `AtomicInteger`、Go 的 `sync/atomic`、Rust 的 `AtomicUsize` 概念相同；Rust 的编译器会阻止你无同步地共享可变变量，C++ 不会。

**要记住的一点**：计数器、标志位用 `std::atomic`；一组需要一致更新的状态用锁；验证用 TSan。
