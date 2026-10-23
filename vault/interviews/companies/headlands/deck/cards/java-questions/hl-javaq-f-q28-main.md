---
id: hl-javaq-f-q28-main
node: java-questions.f-concurrency
type: qa
step: 10
---
## Q
什么是 CAS？原子类（atomics）怎么工作？无锁一定比加锁快吗？`LongAdder` 是什么？
What is CAS? How do atomics work? Is lock-free always faster than locking? What is `LongAdder`?

## A
一句话：CAS（compare-and-swap）是一条**原子指令**——"如果内存值 == 期望值就写入新值，否则失败"；`AtomicLong` 在循环里重试它：`do { old = get(); new = old + 1 } while (!CAS(addr, old, new))`。x86 上是 `lock cmpxchg / lock xadd`，ARM64 上是 LL/SC 或 LSE 的 CAS 指令。

- **无锁 ≠ 更快**：高竞争下 CAS 重试风暴比锁还慢。
- **`LongAdder`** 把热点计数器拆成多个 `Cell`（分段），读时求和，写扩展性极好。
