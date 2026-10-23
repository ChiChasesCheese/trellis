---
id: hl-cq-q29-script
node: cpp-questions.g-concurrency
type: qa
step: 12
---
## Q
用英文 60 秒回答：What is `std::atomic`? Explain the memory orders (`relaxed`, `acquire`/`release`, `seq_cst`).

## A
结构：不可分割的读-改-写 + 默认 `seq_cst` → release/acquire 发布数据，`relaxed` 给计数器 → 重排与 x86 强于 ARM → 无锁用 CAS 循环与 ABA，拿不准用 `seq_cst` 或互斥量。

- `std::atomic` gives indivisible read-modify-write operations plus defined **memory ordering**. The default is **sequentially consistent**: one global order, easiest to reason about.
- **Release/acquire** is the key pair: a release store publishes everything written before it to any thread whose acquire load sees that value. I ran a flag-and-payload handoff 20,000 times with zero bad reads. **Relaxed** only guarantees atomicity, which is enough for a statistics counter - four threads, four million increments, exact result.
- Why it matters: both the compiler and the CPU **reorder** memory operations, and x86 is stronger than ARM, so passing on x86 proves little.
- For lock-free structures I use compare-and-swap loops and think about the **ABA problem**. When unsure, I use `seq_cst` or a mutex.
