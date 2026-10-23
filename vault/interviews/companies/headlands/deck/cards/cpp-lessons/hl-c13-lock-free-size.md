---
id: hl-c13-lock-free-size
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 5
---
## Q
`atomic<T>::is_lock_free()` 说明什么？`atomic<bool>`、`atomic<uint64_t>`、64 字节结构体的 `atomic` 实测结果是什么？

## A
- 小型整数/指针的 `atomic` 是真正的**无锁**（单条原子指令）；大结构会退化为**内部加锁**。
- 实测：`atomic<bool>` true，`atomic<uint64_t>` true，`atomic<64 字节结构体>` **false**（落回隐藏的锁）。
- `sizeof(atomic<long>)` = 8。
- 实验：多个线程共累加 400000 次，atomic 计数器与 mutex 计数器都精确得 400000；CAS 循环求最大值得 3999。
