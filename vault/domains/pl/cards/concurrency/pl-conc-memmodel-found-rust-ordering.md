---
id: pl-conc-memmodel-found-rust-ordering
node: concurrency.atomics-memory-models
type: qa
step: 4
---
## Q
Rust 的原子类型和 `Ordering` 五个档位是什么，分别保证什么？

## A
`Ordering` 是每次原子操作都要传的参数，从弱到强：
1. `Relaxed`：只保证这一个变量上的操作是原子的，且它自己的修改历史有一致的顺序；对其他内存不建立任何顺序。适合计数器、统计。
2. `Release`（用于存储）：本线程在它**之前**的所有读写，不会被重排到它之后。
3. `Acquire`（用于加载）：本线程在它**之后**的所有读写，不会被重排到它之前。一个读到 `Release` 写入值的 `Acquire`，与它建立 happens-before。
4. `AcqRel`：读-改-写操作同时具备二者（如 `fetch_add`、CAS 在锁实现里）。
5. `SeqCst`：在 `AcqRel` 之上，再保证所有 `SeqCst` 操作有一个全局统一的顺序。在「两个线程各写自己的变量再读对方的变量」的写缓冲测试里，`Relaxed` 跑 100 万轮出现了 10 次两个都读到 0，`SeqCst` 一次也没有（一次测量）。

一个小场景（标志位发布数据）：
```rust
// reader thread:
while !READY.load(Acquire) { std::hint::spin_loop(); }
println!("data = {}", DATA.load(Relaxed));
// writer thread:
DATA.store(42, Relaxed);
READY.store(true, Release);   // everything before this is visible to an Acquire reader
```
输出：`data = 42`。`Release` 存储与读到它的 `Acquire` 加载配对，建立了 happens-before；`DATA` 自己只需 `Relaxed`，因为顺序由 `READY` 保证。

在 x86 上，`Acquire`/`Release` 的加载和存储本来就是硬件默认行为，几乎不花代价；在 ARM（含 Apple Silicon）上要用专门的指令（如 `ldar`、`stlr`），`SeqCst` 则可能多加屏障。所以档位选得弱，性能更好，但需要证明正确性。

Rust 的原子类型（`AtomicU64`、`AtomicBool` 等）是安全 API：档位选错会造成逻辑错误（读到旧值），但不会产生未定义行为的数据竞争。经验：不确定就用 `SeqCst`，用 profile 证明它是瓶颈再降档。
