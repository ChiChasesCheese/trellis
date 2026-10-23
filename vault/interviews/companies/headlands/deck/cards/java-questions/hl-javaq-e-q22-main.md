---
id: hl-javaq-e-q22-main
node: java-questions.e-jit-gc
type: qa
step: 15
---
## Q
垃圾回收（GC）是怎么工作的？讲分代、根（roots），以及 Parallel、G1、ZGC 的区别。
How does garbage collection work? Explain generations, roots, and the differences among Parallel, G1 and ZGC.

## A
一句话：GC 从**根**（线程栈局部变量、static 字段、JNI 引用）沿引用标记存活对象，其余回收；回收方式有复制、清除、整理。

- **分代假说**：大部分对象朝生夕死，所以年轻代（Eden + 两个 Survivor）频繁小回收，存活多次的晋升老年代，老年代少回收。
- 年轻代 GC 的代价**正比于存活对象数**，而不是堆大小——分配很多短命垃圾本身不贵。
- **Parallel**：全停顿、吞吐高。
- **G1**：分 Region，按预期暂停时间增量回收（默认）。
- **ZGC**：并发标记 + 并发整理，暂停亚毫秒、与堆大小基本无关，代价是吞吐 / 内存开销。
