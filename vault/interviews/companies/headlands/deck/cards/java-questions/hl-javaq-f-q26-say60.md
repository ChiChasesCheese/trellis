---
id: hl-javaq-f-q26-say60
node: java-questions.f-concurrency
type: qa
step: 31
---
## Q
用英文 60 秒回答：What does `volatile` guarantee and what doesn't it? Is `volatile int count; count++` thread-safe?

## A
结构：volatile 保证可见性与有序性 → 不保证复合操作原子 → `count++` 是三步 → 实测 68.5 万对 400 万 → 标志位与发布用 volatile，计数器用原子类。

> "`volatile` gives you visibility and ordering: a write is seen by subsequent reads in other threads, and the compiler and CPU won't reorder around it in a way that breaks that. It does not make compound operations atomic - `count++` on a volatile is a read, an add and a write, and two threads can interleave. I tested it: four threads each doing a million increments ended at 685,000 on one run and 2.1 million on another instead of four million, while `synchronized` and `AtomicInteger` were exact. I use volatile for status flags and for publishing immutable state; for counters I use atomics or `LongAdder`."
