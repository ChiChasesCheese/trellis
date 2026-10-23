---
id: hft-java-gc-choices-gen-zgc
node: java.gc-choices
type: qa
step: 5
---
## Q
在 JDK 21 上要启用分代 ZGC（Generational ZGC）应该写什么参数？分代为什么对 ZGC 有帮助？

## A
JDK 21 里要写两个参数：`-XX:+UseZGC -XX:+ZGenerational`。只写 `-XX:+UseZGC` 得到的是旧的非分代版本。JDK 23 起默认就是分代，JDK 24 起非分代模式被移除。

为什么分代有帮助：非分代 ZGC 每一轮都要标记**整个堆**，包括很久不变的长寿对象，而大部分垃圾其实是刚分配的短命对象。分代版本按分代假设，常回收便宜的年轻代、很少回收老年代，因此 GC 占的 CPU 更少、需要的堆余量更小、更不容易出现 allocation stall，而暂停仍在 1 ms 以内。

选型的粗略规则：离线批处理看吞吐，G1 或 Parallel 足够；在线低延迟服务选分代 ZGC。
