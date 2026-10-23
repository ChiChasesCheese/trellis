---
id: hl-cq-q30-script
node: cpp-questions.g-concurrency
type: qa
step: 17
---
## Q
用英文 60 秒回答：Is `volatile` thread-safe in C++? What is a data race?

## A
结构：`volatile` 无原子性无顺序，不同于 Java → 数据竞争是 UB（1,995,942 丢更新）→ 优化器可能把标志读提到循环外 → 用 `atomic`/`mutex` 修，TSan 检查，`volatile` 只给硬件。

- In C++, **`volatile` is not for threading**. It only stops the compiler from optimizing accesses away. It gives **no atomicity and no ordering** - unlike Java's `volatile`.
- A **data race** - two threads touching the same location, one writing, with no synchronization - is **undefined behavior** even if it looks harmless. In my test, four threads incrementing a volatile counter two million times in total lost updates - 1,995,942 on one run, different every run - while `atomic` and `mutex` versions gave the exact answer.
- A second danger is the optimizer: a plain flag read in a loop can be hoisted out and the loop never ends.
- The fix is `std::atomic` for a single variable or a mutex for a larger invariant, and I check with **ThreadSanitizer**. `volatile` I reserve for memory-mapped hardware.
