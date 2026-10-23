---
id: hl-hc13-what-asked
node: problems.hc13-fixed-memory-pool
type: qa
step: 1
---
## Q
定长内存池（Fixed-Size Memory Pool）题是什么？四个 Part 和共同约定是什么？

## A
低延迟系统（行情网关、撮合引擎）不希望热路径上 `new`：启动时一次性准备好 `capacity` 个等大的块，运行时只「借」（`allocate`）和「还」（`free`）。

- **Part 1 `IndexPool`**：块 = `int` 编号，`allocate/free` O(1)，重复归还与非法编号检测；
- **Part 2 `GenPool`**：handle = `long`（高 32 位版本号 + 低 32 位槽位），检测 use-after-free 与 ABA；
- **Part 3 `OffHeapOrderPool`**：一块 FFM `MemorySegment`（`Arena`），32 字节定长记录，`ValueLayout` / `MemoryLayout` 读写；
- **Part 4 `ConcurrentPool`**：线程安全，无锁 Treiber 栈 + 带 tag 的 head（`VarHandle` CAS）。

**共同约定**：
- 池满**不是错误**：`allocate()` 返回 `NONE`（`IndexPool.NONE = -1`，handle 池 `NONE = -1L`），不抛异常；
- 归还返回 `FreeResult { FREED, DOUBLE_FREE, INVALID }`：`FREED` 成功；`DOUBLE_FREE` 这块当前不在使用中（已还过，或 handle 已陈旧）；`INVALID` 根本不是这个池发出的编号（越界、`NONE`、全零 handle、从没发过的版本号）；
- 容量必须在 `[1, 1 << 28]`，否则构造器抛 `IllegalArgumentException`；
- **分配顺序**：初始依次 0,1,2…；归还的块插在链头，**最后归还的最先被再分配（LIFO）**，对缓存友好且测试可确定地断言。

考点：把借 / 还的所有失败模式想全（池满、重复归还、归还别人的块、编号被复用、并发下两个人拿到同一块）；解释为什么要池（GC 压力）；池自己引入的新问题（use-after-free 变成逻辑错误而不是崩溃、ABA、数据泄漏、碎片）。
