---
id: hl-j19-q1-gc-pauses
node: java21.j19-runtime-zgc-jit
type: qa
step: 34
---
## Q
面试问：你怎么处理 Java 里的 GC 暂停？
How do you deal with GC pauses in Java?

## A
思路：先说暂停从哪来（搬对象、STW），再说**两个杠杆**，两条都要，先减少分配再选 GC。
1. **少产生垃圾**：热路径用基本类型数组代替装箱集合、预分配或池化对象、大表放堆外，垃圾少了就没什么可回收；
2. **选对收集器**：能并发移动对象的 JDK 21 分代 ZGC，暂停保持亚毫秒且不随堆大小增长；G1 落后时会 Full GC，可到几十到几百毫秒。
3. **测量**：用 JFR 和 GC 日志在自己的负载上测，不信默认值。

英文骨架：「Two levers: allocate less on the hot path, and pick a collector that moves objects concurrently — Generational ZGC on JDK 21. I'd measure with JFR and GC logs on our own workload.」
