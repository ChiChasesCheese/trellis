---
id: hl-hc05-followups-engine
node: problems.hc05-market-order-book
type: qa
step: 19
---
## Q
追问：订单簿多线程怎么办？怎么加 IOC / FOK / 冰山单 / 止损单 / self-trade？「怎么让它更快」怎么开场？

## A
- **多线程**：撮合有严格顺序依赖，锁粒度难细分。常见做法：**单线程撮合引擎**（一个品种一个线程，单写者），命令经队列（如 LMAX Disruptor 的 ring buffer）串行进入——无锁、可重放、延迟稳定；扩展靠按品种分片；线程间用 SPSC 环形队列传命令和事件。不要给每个方法加 `synchronized`：撮合仍须整体串行，锁只增开销，且 Java 21 里 `synchronized` 会钉住虚拟线程。
- **新订单类型**：sealed `Command` 加一个子类，编译器会指出所有要改的 switch；**IOC** 就是 Market 的限价版（吃不完的作废）；**FOK** 要先 dry-run 数一下对面总量够不够再下手；冰山单、止损单、self-trade 同理。
- **「怎么让它更快」开场**：先 profile 看是 CPU 还是 GC。这里是对象多（装箱 key、Node、entry、Event 列表），把「对象图」变「数组」。口述：「热路径零分配，内存启动时一次分配；价格是有界整数，所以树换成数组；代价是价格带和容量固定，边界上拒绝并返回错误码。」
- **价格范围很大**：数组放不下；只对靠近中间价的一段（±几千 tick）用数组，远处放 `TreeMap`；或有序数组 + 二分（缓存友好）。
- 其他追问：撤单怎么做到 O(1) 或 O(log L)；同价位怎么保证先来先成交；为什么用 `long` 不用 `double`；市价单没有价格怎么放进结构（限价无穷大 / 0，同一个循环）。
