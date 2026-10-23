---
id: hl-sd03-decode-book
node: system-design.sd03-low-latency-trading
type: qa
step: 14
---
## Q
零分配的解码和订单簿数据结构怎么设计？价格、品种用什么类型？

## A
- **解码**：flyweight，一个预分配的「视图」对象指向缓冲区偏移量，字段读取 `buffer.getLong(offset + FIELD_OFFSET)`，不拷贝、不创建对象；缓冲区是堆外 / 直接内存（`MemorySegment` 或 `ByteBuffer.allocateDirect`）；二进制协议用固定布局（SBE 一类的模板化编码思想）；
- **订单簿**：价位用围绕当前价的**连续数组**，下标 = (价格 − 基准价) / tick，数量用 `long[]`，最优价用游标维护（只在最优档清空时向外扫），O(1) 更新、顺序访问、缓存友好，比 `TreeMap` 少对象指针追逐和全部分配；订单 ID → 位置用开放寻址的 `long → int` 哈希表；价位的订单队列用预分配数组 + 整数链表（free list），不用 `LinkedList<Order>`；
- **价格**是 `long` 定点（如 1e-4 为单位），**禁止 `double`**（相等比较、累加误差、重放时机器差异）；品种用 `int` 稠密 id，风控与状态按数组下标查，不哈希字符串。
