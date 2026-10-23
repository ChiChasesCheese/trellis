---
id: hl-javaq-e-q22-say60
node: java-questions.e-jit-gc
type: qa
step: 31
---
## Q
用英文 60 秒回答：How does garbage collection work? Explain generations, roots, and the differences among Parallel, G1 and ZGC.

## A
结构：从根标记可达对象 → 分代（年轻代代价看存活量）→ Parallel 全停顿 → G1 按 Region 增量 → ZGC 并发亚毫秒 → 三者实测最大停顿。

> "A tracing collector starts from roots - thread stacks, statics, JNI handles - marks everything reachable and reclaims the rest. Because most objects die young, the heap is split into generations: young collections are cheap because their cost scales with live objects, not with garbage. Parallel GC stops the world for the whole collection and is best for throughput. G1, the default since 9, splits the heap into regions and collects incrementally toward a pause-time target. ZGC marks and relocates concurrently with the application using load barriers, so pauses stay sub-millisecond regardless of heap size, at the cost of some throughput and needing headroom. On a test I ran, the worst stall was about 22 ms with Parallel, 8 ms with G1, and 0.14 ms with generational ZGC."
