---
id: hft-java-at-hft-java-vs-cpp-extra-work
node: java-at-hft.java-vs-cpp
type: qa
step: 4
---
## Q
同一个订单簿，为了让 Java 版本接近 C++ 版本的速度，Java 需要额外做哪些工作？

## A
Java 需要把 C++ 默认就有的东西一项一项补回来：
- 用原始类型数组代替对象集合，避免指针跳转和装箱；
- 预分配加对象池，保证稳态零分配；
- 大块数据放堆外，避开 GC；
- 预热，保证 JIT 已经编译完；
- 线程绑核、隔离，避免调度抖动；
- 选 ZGC、固定堆、`AlwaysPreTouch`、大页。

例：把订单簿的价位按价格 tick 换算成下标，存进 `long[]` 数组，而不是 `TreeMap<Long, List<Order>>`。

结果是：热路径的 Java 写得“像 C”，比普通 Java 难写难读，生产力优势就不明显了。所以公司把极致热路径留给 C++，而这套技巧用在中等延迟（几十微秒）的系统上，性价比更高。
