---
id: pl-cpp-concurrency-found-memory-order
node: cpp.concurrency
type: qa
step: 5
---
## Q
C++ 的六种 `memory_order` 是什么意思？acquire/release 怎样保证一个线程写的数据对另一个线程可见，默认的顺序一致（seq_cst）又贵在哪里？

## A
**为什么需要内存序**：编译器和 CPU 都会重排内存操作以求更快。单线程里重排不可见，多线程里另一个线程可能先看到"标志位已设置"、后看到"数据已写入"。内存序（memory order）规定一个原子操作对**周围的其他读写**施加什么顺序约束。

**六种**（`std::memory_order_*`）：
1. `relaxed`：只保证这个原子变量本身的操作不撕裂，**不约束周围读写**的顺序。适合独立计数器。
2. `acquire`（用于读）：这次读之后的读写**不能被移到它之前**。
3. `release`（用于写）：这次写之前的读写**不能被移到它之后**。
4. `acq_rel`：读改写操作同时具备 acquire 和 release。
5. `seq_cst`：在 acq_rel 之上，所有 `seq_cst` 操作有一个**全局唯一的总顺序**，所有线程看到一致。这是**默认值**。
6. `consume`：理论上比 acquire 弱，实际上没有编译器正确实现，标准实践中被当作 acquire，不要用。

**acquire/release 配对**：生产者把数据写好后用 `release` 设标志，消费者用 `acquire` 读到标志为真，那么消费者**一定看得到**生产者在设标志之前写的所有数据。

```cpp
// 生产者
data = 42; ready.store(true, std::memory_order_release);
// 消费者
while (!ready.load(std::memory_order_acquire)) {}   // 之后读 data 一定是 42
```

**在 ARM64 上的实际指令**（本机 `-O2` 汇编）：

| 操作 | 指令 |
|---|---|
| `load(relaxed)` | `ldr` |
| `load(acquire)` | `ldapr` |
| `load(seq_cst)` | `ldar` |
| `store(release)` / `store(seq_cst)` | `stlr` |
| `fetch_add(relaxed)` / `fetch_add(seq_cst)` | `ldadd` / `ldaddal` |

x86 的硬件内存模型本来就较强：acquire/release 几乎免费，只有 `seq_cst` 的 store 需要额外的屏障指令。

**seq_cst 贵在哪里**：要保证全局顺序，在弱内存序硬件（ARM、POWER）上需要更强的指令或屏障；在 x86 上写操作要带全屏障。成本通常是几个到十几个周期，只在极热的无锁代码里才有意义。

**要记住的一点**：先用默认的 `seq_cst`，只有测出瓶颈并且证明其他序正确时才降级；内存序是在牺牲可推理性换性能。
