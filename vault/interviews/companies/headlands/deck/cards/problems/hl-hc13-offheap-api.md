---
id: hl-hc13-offheap-api
node: problems.hc13-fixed-memory-pool
type: qa
step: 8
---
## Q
`OffHeapOrderPool` 的 `allocate`、`put`、`close` 有哪些语义要求？为什么要多提供 `put(h, id, px, qty, side)` 这种重载？

## A
```java
public long allocate() {
    int index = head;
    if (index == END) return NONE;
    head = (int) NEXT.get(seg, (long) index);
    int g = (int) GEN.get(seg, (long) index) + 1;
    GEN.set(seg, (long) index, g);
    ID.set(seg, (long) index, 0L);  PX.set(seg, (long) index, 0L);    // 清零载荷
    QTY.set(seg, (long) index, 0);  SIDE.set(seg, (long) index, 0);
    available--;
    return GenPool.handle(index, g);
}
public void put(long handle, Order order) {
    switch (order) {
        case Order(long id, long px, int qty, int side) -> put(handle, id, px, qty, side);
    }
}
public void close() { if (arena.scope().isAlive()) arena.close(); }
```
- **`allocate` 必须清零载荷**：`Arena.allocate` 只在第一次分配时清零，复用的槽位没人帮你清；否则上一个主人的数据泄漏给下一个（bug 来源也是信息泄漏）。
- `put/get/px/qty` 遇到非当前有效的 handle 抛 `IllegalStateException`（陈旧、越界、`NONE` 都算）；`put(h, null)` 抛 `NullPointerException`（record 模式 switch 对 null 抛 NPE）。
- `close()` 幂等（重复 `Arena.close()` 会抛，所以先判 `arena.scope().isAlive()`）；`close()` 之后任何访问抛 `IllegalStateException("Already closed")`，由 FFM 运行时保证，不要自己拦，不崩进程。
- handle 规则、`free` 判定与 `GenPool` 相同，可复用 `GenPool.handle/indexOf/generationOf`。

**为什么多一个看起来多余的重载**：只提供 `put(h, Order)` / `Order get(h)` 会强迫调用方每次 `new Order`，把省下的分配补回去。所以另给 `put(h, id, px, qty, side)` 和 `px(h)` / `qty(h)` 零分配读；`get(h)` 会 `new`，文档写明不在热路径用。**API 设计和内存管理是一回事**：API 的形状决定调用方能否写出零分配代码。

校验：极值 `Long.MIN_VALUE` / `Integer.MIN_VALUE` 往返；相邻记录互不覆盖；复用记录是零；`close` 后访问；重复 `close`；100 万记录的堆外池 < 2 s（约 62 ms）。

为什么堆外而不是 `Order[]` 预分配：`Order[]` 里的 `Order` 是堆对象，会晋升老年代，写引用要写屏障，GC 完整回收要遍历；堆外纯数值记录 GC 看不见。
