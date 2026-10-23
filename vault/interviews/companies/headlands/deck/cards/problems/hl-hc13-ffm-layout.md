---
id: hl-hc13-ffm-layout
node: problems.hc13-fixed-memory-pool
type: qa
step: 7
---
## Q
`OffHeapOrderPool` 怎么用 FFM 的 `Arena` / `StructLayout` / `SequenceLayout` / `VarHandle` 布局堆外记录？为什么槽位是 32 字节、`VarHandle` 要 `static final`？

## A
FFM 外部内存 API（Java 21 预览，22 转正）：
- **`Arena.ofShared()`** 管一块内存的生命周期，`close()` 整块归还；`ofShared` 允许别的线程访问，`ofConfined` 只允许创建它的线程（JUnit 超时断言换线程会 `WrongThreadException`）；
- **`arena.allocate(bytes, 对齐)`** 分配并清零；
- **`MemoryLayout.structLayout(...)`** 像 C 的 struct；
- **`layout.varHandle(sequenceElement(), groupElement("px"))`** 得 `VarHandle`，`PX.get(segment, i)` / `PX.set(segment, i, v)` 读写第 i 个槽位的 px，偏移由 JDK 算。

```java
private static final StructLayout SLOT = MemoryLayout.structLayout(
    JAVA_INT.withName("gen"), JAVA_INT.withName("next"),
    JAVA_LONG.withName("id"), JAVA_LONG.withName("px"),
    JAVA_INT.withName("qty"), JAVA_INT.withName("side"));
private static final SequenceLayout SLOTS = MemoryLayout.sequenceLayout(MAX_CAPACITY, SLOT);
private static final VarHandle GEN = SLOTS.varHandle(sequenceElement(), groupElement("gen"));
this.seg = arena.allocate(SLOT.byteSize() * capacity, 64);
```
**32 字节槽位**：头 8（`gen:int` + `next:int`）+ 载荷 24（`id:long, px:long, qty:int, side:int`），4+4+8+8+4+4 无隐式填充。32 是 2 的幂，一条 64 字节缓存行正好 2 个槽位，不会有槽位横跨两行。空闲链表和版本号也放进槽位里，堆上没有 per-slot 对象。

`SLOTS` 只是描述，不分配内存；用它生成 **`static final`** 的 `VarHandle`，JIT 能把读写内联成一条加载 / 存储指令；若在构造器里按实际 capacity 生成（实例字段），JIT 不能当常量折叠，会慢。

**注意**：全零内存所以 `gen = 0`（空闲偶数）不用初始化，`next` 要显式写成 `i + 1`；`VarHandle.get` 返回 `Object`（签名多态）要 `(int)` 强转；下标一律转 `long`，传 `int` 会让调用点静态类型不匹配，运行时才 `WrongMethodTypeException`；`byteSize()` 是 `long` 可超 2 GiB（`ByteBuffer` 容量 `int` 做不到）。

对比 `ByteBuffer.allocateDirect`：容量 `int`、无确定性释放、偏移手算。代价：手动 `close`、固定容量、边界检查（JIT 能消掉大部分）、JDK 21 预览 API 名字会变（如 `allocateUtf8String`）。
