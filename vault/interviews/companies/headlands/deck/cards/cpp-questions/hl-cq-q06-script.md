---
id: hl-cq-q06-script
node: cpp-questions.a-why-fast
type: qa
step: 35
---
## Q
用英文 60 秒回答：Why can a `std::vector` scan beat a `std::list` scan by 20x even though both are O(n)? What is cache locality?

## A
结构：Big-O 不数内存访问 → 缓存行与预取、链表未命中约 100 ns（0.2 / 4 / 28 ms）→ SoA 对 AoS 同理 → 结论：默认连续容器。

- Big-O counts operations, not **memory accesses**. The CPU reads a whole **cache line** - 64 bytes - and the hardware **prefetches** sequential access, so a vector scan is nearly free per element.
- A linked list's nodes live all over the heap, so every step can be a **cache miss** costing around 100 nanoseconds. For four million ints: vector 0.2 ms, list 4 ms, and a list whose nodes were shuffled in memory about 28 ms.
- The same idea applies to layout: scanning one field of a **struct of arrays** was about ten times faster than an **array of structs**, because each cache line carries 16 useful values instead of one.
- So in latency-sensitive code I default to contiguous containers and keep hot data compact.
