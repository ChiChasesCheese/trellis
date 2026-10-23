---
id: hl-sd03-fu-gc
node: system-design.sd03-low-latency-trading
type: qa
step: 34
---
## Q
追问：用 Java 写，GC 停顿怎么办？

## A
思路：先算分配率和停顿代价（1 ms ⟹ 1,000 条消息），再说「根治是不分配」，最后才谈收集器。

要点：稳态零分配（预分配环、flyweight 解码、对象池 / 结构体数组、原语集合、不用 `String` / 装箱 / 流 / 捕获 lambda）；验证：交易时段 GC 次数 = 0（`-Xlog:gc`、JFR）；预热阶段完成所有类加载与分配；`-Xms=-Xmx` + `AlwaysPreTouch` 避免运行时扩堆和缺页；ZGC 把停顿压到亚毫秒但有读屏障与并发线程开销，不解决 µs 预算；「一天分配一次的大堆 + 夜里重启」是务实选项；堆外 / `MemorySegment` 绕开 GC。

可以说：「100 MB/s 的分配率意味着每 10 秒一次 minor GC，停顿几 ms，比预算大三个数量级。所以我不调 GC，我让热路径不分配。」
