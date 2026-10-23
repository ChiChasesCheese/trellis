---
id: hl-javaq-a-q03-checklist
node: java-questions.a-speed
type: qa
step: 12
---
## Q
写一份低延迟 Java 热路径的 checklist（按顺序），并说明如何向面试官口述这个回答。

## A
热路径 checklist：
1. **单线程事件循环**，避免锁。
2. **预分配环形缓冲 / 对象复用**。
3. **原始类型**，避免装箱。
4. 不用 `String` 拼接和日志格式化。
5. 线程间用**无锁队列**（SPSC，单生产者单消费者）。
6. **预热**。
7. 用 **ZGC**，或足够大的堆加调好的 G1。
8. 线程**绑核**。
9. 用 JFR / 分配 profiler 验证"热路径真的不分配"（`ThreadMXBean.getThreadAllocatedBytes` 前后差）。

口述结构（60 秒）：先说稳态可接近，再按"预热与去优化 / GC 与 safepoint / 内存布局"三条讲差距，附 Parallel 约 22 ms、G1 约 8 ms、分代 ZGC 约 0.14 ms 的实测，最后给上述做法，并承认内核旁路场景仍选 C++。
