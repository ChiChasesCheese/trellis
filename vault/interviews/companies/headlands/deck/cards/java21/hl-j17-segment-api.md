---
id: hl-j17-segment-api
node: java21.j17-ffm-api
type: qa
step: 7
---
## Q
`MemorySegment` 怎么按字节偏移或元素下标读写？每次访问做哪些检查，分别抛什么？

## A
```java
seg.set(ValueLayout.JAVA_LONG, 0, 18_950L);      // 偏移（字节）0 处写 long
seg.get(ValueLayout.JAVA_INT, 8);                // 偏移 8 处读 int
seg.setAtIndex(ValueLayout.JAVA_LONG, 2, 7L);    // 按元素下标（偏移 = 2 * 8）
seg.byteSize();                                  // long，可超过 2GB
```
每次访问都检查**边界**和**生命周期**（所属 `Arena` 是否还活着）：
- 越界 → `IndexOutOfBoundsException`；
- 关闭后访问 → `IllegalStateException`（`Already closed`）；
- `ofConfined` 的 segment 被别的线程访问 → `WrongThreadException`。

这是三张「安全网」：新内存清零、越界抛异常、关闭后抛异常（而不是 use-after-free）。
