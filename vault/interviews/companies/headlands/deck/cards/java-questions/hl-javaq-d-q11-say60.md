---
id: hl-javaq-d-q11-say60
node: java-questions.d-memory
type: qa
step: 28
---
## Q
用英文 60 秒回答：What happens on `new Foo()` in Java? Compare with `malloc` / `new` in C++. How fast is Java allocation, and what does it cost later?

## A
结构：先答 C++（malloc 与 new）→ Java 的 TLAB 指针碰撞 → 为什么能这么快（复制式 GC）→ 代价后移到 GC 频率、JIT 可消除 → 对象大小数字。

> "In C++, `malloc` just gives you raw uninitialised bytes from the allocator, and `new` is `malloc` plus running the constructor, and you must free it yourself. In Java, `new` is much cheaper at the allocation step: each thread has a TLAB in the young generation, so allocation is bumping a pointer - a handful of instructions, no lock - and the memory is already zeroed. That's possible because the collector copies live objects out and reclaims the whole region, so there's no free list or fragmentation. The cost moves to GC frequency - allocation rate is what drives young collections - and the JIT can eliminate allocations that don't escape. I measured a plain object at 16 bytes and a two-int record at 24 bytes."
