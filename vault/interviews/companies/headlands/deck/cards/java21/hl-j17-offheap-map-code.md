---
id: hl-j17-offheap-map-code
node: java21.j17-ffm-api
type: qa
step: 21
---
## Q
堆外定长哈希表（`OffHeapTickerMap`，槽位 `[key:8][value:8]` 共 16 字节）用 FFM 怎么分配、读 key 和 value、关闭？

## A
```java
private static final long SLOT_BYTES = 16;
this.arena = Arena.ofShared();
this.seg = arena.allocate(capacity * SLOT_BYTES, 64);   // 保证已清零，key == 0 就是空格
private long keyAt(int slot)   { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES); }
private long valueAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES + 8); }
public void close() { if (arena.scope().isAlive()) arena.close(); }
```
- `ofShared`：允许别的线程使用（JUnit 的超时断言会换线程）；`ofConfined` 略快。
- `allocate(size, 64)` 的第二个参数是**对齐**，64 = 一条缓存行，4 个 16 字节槽位正好一行，一次探测落在同一缓存行内。
- 「全零 = 空槽」省掉初始化，`checkKey` 要求 key > 0。
- 手算偏移 `slot * SLOT_BYTES`，因为只有两个字段；字段多了就该用 `MemoryLayout`。
