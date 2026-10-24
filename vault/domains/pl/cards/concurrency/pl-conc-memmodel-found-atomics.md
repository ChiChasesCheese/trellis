---
id: pl-conc-memmodel-found-atomics
node: concurrency.atomics-memory-models
type: qa
step: 3
---
## Q
原子变量（Java `AtomicInteger`、Go `atomic.Int64`）和 CAS（compare-and-swap）是什么？为什么它们能不加锁地更新计数器？

## A
**原子操作**：对一个变量的“读-改-写”作为不可分割的一步执行，别的线程看不到中间状态，不需要锁。硬件直接提供指令支持。

**CAS**（compare-and-swap，比较并交换）是最基础的原子原语：`CAS(变量, 期望值, 新值)` ——只有变量当前值等于期望值时才写入新值并返回成功，否则什么都不改、返回失败。
用 CAS 实现无锁累加的思路：循环 `读出旧值 → 算出新值 → CAS(旧值, 新值)`；如果别的线程在中间改过，CAS 失败，重新读再试。`AtomicInteger.incrementAndGet()` 在底层就是这样（或直接用硬件的原子加指令）。

```java
AtomicInteger c = new AtomicInteger();
// 4 threads, each: for (...1_000_000) c.incrementAndGet();
```
输出：`AtomicInteger: 4000000`。

```go
var n atomic.Int64
// 4 goroutines, each: for j < 1_000_000 { n.Add(1) }
var v atomic.Int64
fmt.Println(v.CompareAndSwap(0, 5), v.CompareAndSwap(0, 7), v.Load())
```
输出：`atomic.Int64: 4000000 60ms`（一次测量），CAS 行是 `true false 5`：第一次期望 0 成功写入 5，第二次期望 0 但当前是 5，失败。同样的 4 线程累加，用 `sync.Mutex` 是 171 毫秒，原子操作约快 3 倍，因为竞争时不需要把线程挂起再唤醒。

适用范围：原子操作只保护**单个变量**的单次更新。要让多个变量一起保持一致（扣款并记流水），需要锁。Python 标准库没有原子整数；Rust 有 `AtomicU64` 等。

两个重要概念：
1. **无锁（lock-free）**不等于更快：高竞争时大量 CAS 失败重试会空转；
2. **ABA 问题**：值从 A 变 B 又变回 A，CAS 看不出中间变过，在无锁数据结构里需要版本号等手段处理。
