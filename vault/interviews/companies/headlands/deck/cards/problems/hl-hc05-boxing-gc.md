---
id: hl-hc05-boxing-gc
node: problems.hc05-market-order-book
type: qa
step: 12
---
## Q
为什么性能题盯着「装箱」和「每次操作 new 对象」？订单簿 `OrderBook` 和 `TickBook` 的分配量差多少？

## A
`long` 是 8 字节裸数字；`Long` 是堆上对象（对象头约 16 字节）。集合只能存对象，`map.put(5L, x)` 会悄悄创建 `Long`（装箱，−128..127 有缓存，其余每次新对象）。堆对象由垃圾回收器（GC）清理：分配越快 GC 越忙，GC 暂停对交易系统是**延迟毛刺**；对象散落内存还要「追指针」，缓存命中率低。所以低延迟系统追求**热路径零分配**：处理一条命令不 `new`。

数字（同一串随机命令）：Part 2 的 `OrderBook` 约 **84 MB / 20 万条命令 ≈ 420 字节 / 条**（每订单一个 `Node`、每价位 `PriceLevel` + `LinkedHashMap`、key 装箱、每条命令返回 `ArrayList<Event>`）；`TickBook` 预热后 60 万条命令 **0 字节**。

量级：Part 1 的 20 万次 add + 10 万次 cancel 约 65–80 ms；30 万条混合命令约 60 ms；`TickBook` 200 万次操作约 100–115 ms（约 2000 万次 / 秒）。

JVM 侧手段：Generational ZGC（亚毫秒级停顿）、预热 JIT、`-Xms=-Xmx` + `AlwaysPreTouch`。

误区：`Long` 用 `==` 比较——装箱对象比较引用，缓存范围内碰巧相等、之外不等，「小数据里过、线上错」；用 `equals` 或保持基本类型。C++ 里可重载 `operator new` 数分配次数；`std::function` 作为热路径回调，较大捕获会分配。
