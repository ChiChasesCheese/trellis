---
id: pl-conc-memmodel-mechanism
node: concurrency.atomics-memory-models
type: qa
step: 5
---
## Q
什么是原子操作（atomic operation）？CPU 的写缓冲怎样让两个线程同时读到 0？可以用什么实验观察到它？

## A
**原子操作**是对一个内存位置的读 / 改 / 写，要么整体完成、要么没发生，别的线程看不到中间状态。硬件提供了：
- 原子加载和存储（对齐的机器字）；
- 读-改-写指令，如 `fetch_add`、CAS（compare-and-swap，只有当前值等于期望值时才写入新值）；x86 用 `lock` 前缀，ARM 用 LL/SC 或原子指令。

原子操作还带有**顺序**要求：它前后的普通读写能不能被重排到它的另一侧。需要时编译器会插入内存屏障（memory barrier / fence）。

**写缓冲实验**（store-buffering 测试）：两个线程，初始 `X = Y = 0`：
- 线程 1：`X = 1; r1 = Y`
- 线程 2：`Y = 1; r2 = X`

顺序一致下，至少有一个线程能看到对方的写，所以不可能 `r1 == 0 && r2 == 0`。但真实 CPU 上，每个核把自己的 `X = 1` 先放进写缓冲，接着就去读 `Y`，此时对方的写还在对方的缓冲里，于是两边都读到 0。

用 Rust 在 Apple Silicon（12 核）上跑 100 万轮（每轮重置 `X`、`Y`，两个线程用屏障同时起跑；一次测量）：
```rust
X.store(1, st);                    // thread 1; st = Relaxed or SeqCst
R1.store(Y.load(ld), Relaxed);
Y.store(1, st);                    // thread 2
R2.store(X.load(ld), Relaxed);
```
结果：
- 用 `Ordering::Relaxed`：`r1 == 0 && r2 == 0` 出现了 10 次。
- 用 `Ordering::SeqCst`：出现 0 次。

`SeqCst` 会在存储和加载之间加屏障，把写缓冲排空，代价就是慢一点。这个实验说明：弱序不是理论问题，每一百万次里就会有几次「违反直觉」的结果，而且测试通常很难复现。
