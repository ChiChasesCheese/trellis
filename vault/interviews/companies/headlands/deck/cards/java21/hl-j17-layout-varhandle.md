---
id: hl-j17-layout-varhandle
node: java21.j17-ffm-api
type: qa
step: 10
---
## Q
`layout.varHandle(路径)` 给出什么？在 JDK 21 里怎么用它读写 100 万条记录里第 i 条的 `px`？

## A
给出一个 **`VarHandle`**（能对变量做各种强度原子读写的句柄，见并发原语），JIT 能把它内联成一条加载/存储指令。

JDK 21 里 `POOL.varHandle(sequenceElement(), groupElement("px"))` 得到的句柄：

```java
MemorySegment pool = arena.allocate(POOL);          // 24 000 000 字节
POOL_PX.set(pool, i, 18_950L + (i % 100));          // (segment, 元素下标, 值)
long px = (long) POOL_PX.get(pool, i);
```
和 `VarHandle` 一样，应声明为 `static final`。
