---
id: hl-javaq-a-q03-say60
node: java-questions.a-speed
type: qa
step: 21
---
## Q
用英文 60 秒回答：Where can Java approach C++ latency, and where can't it? How would you build a low-latency Java system?

## A
结构：稳态可接近 → 差距在尾部（预热与去优化、GC 与 safepoint、内存布局）→ GC 实测数字 → 做法清单 → 诚实承认内核旁路选 C++。

> "In steady state, hot loops can get close to C++. The gap is in the tail. First, warm-up and deoptimization - the first requests run in the interpreter, and a changed type profile can throw compiled code away. Second, GC and safepoints - I measured the same allocation-heavy workload with a jitter probe: Parallel GC had a max stall around 22 ms, G1 about 8 ms, generational ZGC about 0.14 ms. Third, memory layout: no value types, so objects carry headers and sit behind pointers. The way I'd build a latency-critical Java path is: keep the hot path allocation-free, use primitive arrays or off-heap buffers, pre-warm, use ZGC, pin threads, and verify with JFR and allocation counters rather than trust intuition. For things like kernel-bypass networking, I would honestly still expect C++."
