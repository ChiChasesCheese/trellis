---
id: hft-java-off-heap-ffm-arena
node: java.off-heap
type: qa
step: 4
---
## Q
FFM API 的 `Arena` 和 `MemorySegment` 怎样给堆外内存提供“安全网”？三种常用的 Arena 有什么区别？

## A
`Arena` 管内存的生命周期，`MemorySegment` 是带边界的一段内存。三道安全网：新分配的内存自动清零；越界访问抛 `IndexOutOfBoundsException`；Arena 关闭后再访问抛 `IllegalStateException`，而不是像 C 那样 use-after-free 直接崩进程。大小用 `long`，可以超过 2 GB。

三种 Arena：
- `ofConfined()`：只有创建它的线程能访问，最快，默认选择；
- `ofShared()`：任何线程能访问，关闭时要与其他线程同步，较慢，别在热路径反复开关；
- `ofAuto()`：由 GC 回收，不能手动关闭。

代价：每次访问仍有检查，JIT 内联后能消掉大部分，但不是零成本。
