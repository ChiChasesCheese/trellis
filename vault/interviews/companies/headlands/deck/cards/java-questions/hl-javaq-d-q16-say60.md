---
id: hl-javaq-d-q16-say60
node: java-questions.d-memory
type: qa
step: 33
---
## Q
用英文 60 秒回答：When and how would you use off-heap memory in Java? What are the risks?

## A
结构：堆外是什么（direct buffer、mmap、21 预览的 FFM）→ 用途（大数据、零拷贝、定长布局）→ 风险（生命周期、不可见）→ FFM 的 Arena 与边界检查如何改善。

> "Off-heap means memory the GC doesn't manage or scan: direct byte buffers, memory-mapped files, and in Java 21 the preview Foreign Function and Memory API with `Arena` and `MemorySegment`. I'd use it for very large, long-lived data like tick history so the heap stays small and collections stay short, for zero-copy I/O, and for fixed-layout records or sharing between processes. The risks are lifetime and visibility: a direct buffer is only freed when its owner object is collected, so you can hit the direct-memory limit - I reproduced that error with a 16 MB cap - and leaks don't show up in heap dumps. FFM improves that with deterministic `Arena` closing and bounds checks: using a segment after close throws instead of crashing."
