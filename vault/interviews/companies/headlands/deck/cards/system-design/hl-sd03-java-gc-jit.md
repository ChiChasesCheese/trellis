---
id: hl-sd03-java-gc-jit
node: system-design.sd03-low-latency-trading
type: qa
step: 27
---
## Q
落到本系统，Java 的 GC、JIT、safepoint 纪律分别怎么做、怎么验证？

## A
- **GC**：稳态零分配：消息用预分配环 / 缓冲，事件用可复用 flyweight，意图 / 订单用对象池或结构体数组，集合用原语版本（`long → int` 哈希表、`int[]` 链表）。验证：开 `-Xlog:gc` / JFR，**交易时段内 GC 次数应为 0**。备选 ZGC（亚毫秒停顿，但有读屏障与并发线程开销，对 µs 级预算仍可能过大），或「一天分配一次的大堆 + 夜里重启」；
- **JIT**：开盘前用合成 / 回放流量预热到编译稳定（C2 编译完成）；热路径调用点保持**单态**（同一接口调用点不要见到多种实现类，否则内联失效）；避免热方法里抛异常、方法过大（> 8000 字节码不被 JIT 编译，`-XX:-DontCompileHugeMethods`）；用 `-XX:+PrintCompilation` / JFR 监控 deopt；
- **safepoint**：任何需要 safepoint 的操作会停住所有线程；避免热路径里没有 safepoint 轮询的超长计数循环、避免触发 safepoint 的诊断 / JMX / JFR 重配置；用 `-Xlog:safepoint` 检查。
